from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.core.signing import Signer
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from pathlib import Path
import os
import secrets
from vista_administrador.models import Sucursal
from .models import User, Publicacion, Oferta, Intercambio
from ferreplus.modulos import modulos_registro
from .modulos import modulos_publicacion, modulos_oferta, modulos_intercambio
from .forms import PublicacionForm
from ferreplus.modulos.modulos_inicio_sesion import normal_required

signer = Signer()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

@csrf_protect
@login_required
@normal_required
@never_cache
def pagina_principal(request):
    # Obtener el usuario actual
    usuario_actual = request.user

    # Sucursales para filtrar
    sucursales = Sucursal.objects.all()

    # Chequeamos que tiene solicitudes pendientes para la notificacion
    solicitudes_pendientes = Oferta.objects.filter(usuario_recibe_id=usuario_actual).count()

    # Obtener todas las publicaciones excepto las del usuario actual o las que son privadas
    publicaciones = Publicacion.objects.exclude(es_privada=True).exclude(parte_oferta=True).exclude(autor=usuario_actual)
    

    # Crear un diccionario para almacenar las imágenes asociadas a cada publicación
    imagenes_por_publicacion = {}

    # Iterar sobre todas las publicaciones
    for publicacion in publicaciones:
        # Obtener todas las imágenes relacionadas con la publicación actual
        imagenes_publicacion = publicacion.imagenes.all()
        
        # Almacenar las imágenes en el diccionario con la clave como la publicación misma
        imagenes_por_publicacion[publicacion] = imagenes_publicacion
    return render(request, 'vista_usuario/vista_principal.html', {
        'publicaciones': publicaciones,
        'imagenes_por_publicacion': imagenes_por_publicacion,
        'tiene_solicitudes_pendientes': solicitudes_pendientes > 0,
        'sucursales': sucursales
        })

@login_required
@normal_required
def subir_publicacion(request):
    
    sucursales = Sucursal.objects.all()

    if request.method == "POST":
        
        # Obtener datos de la publicación y las imágenes del formulario
        datos_publicacion = request.POST.dict()
        usuario = request.user

        # Verificar campos y obtener las imágenes
        imagenes = request.FILES.getlist('imagen')
        if len(imagenes) > 5 or len(imagenes) <= 0:
            return render(request, 'vista_usuario/subir_publicacion.html', {'error': 'El máximo de imágenes es 5 y el mínimo 1.', "sucursales": Sucursal.objects.all()})
        
        # Verificar campos
        exito, mensaje_error = modulos_publicacion.verificar_campos(datos_publicacion)
        if len(imagenes) > 5 or len(imagenes) <= 0:
            return render(request, 'vista_usuario/subir_publicacion.html', {'error': 'El máximo de imágenes es 5 y el mínimo 1.', "sucursales": Sucursal.objects.all()})
        if not exito:
            return render(request, 'vista_usuario/subir_publicacion.html', {'error': mensaje_error, "sucursales": sucursales})
        else:
            # Crear publicación
            modulos_publicacion.crear_publicacion(datos_publicacion,usuario,imagenes)
            
            # Mostrar mensaje de éxito
            return render(request, 'vista_usuario/subir_publicacion.html', {'aviso': "La publicación se ha creado con éxito.", "sucursales": Sucursal.objects.all()})
    else:
        # Si es una solicitud GET, simplemente renderizar la página principal
        return render(request, 'vista_usuario/subir_publicacion.html',{"sucursales": sucursales})
    
@login_required
@normal_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)

    if request.method == 'POST':
        form_publicacion = PublicacionForm(request.POST, instance=publicacion)
        if form_publicacion.is_valid():
            imagenes_a_eliminar = request.POST.getlist('eliminar_imagenes')
            nuevas_imagenes = request.FILES.getlist('nuevas_imagenes')

            if not modulos_publicacion.validar_cantidad_imagenes(publicacion, nuevas_imagenes, imagenes_a_eliminar):
                return modulos_publicacion.render_con_error(request, form_publicacion, publicacion, 'Debe haber entre 1 y 5 imágenes asociadas a la publicación.')

            publicacion = modulos_publicacion.guardar_publicacion(form_publicacion, imagenes_a_eliminar, nuevas_imagenes)
            return redirect('mis_publicaciones')
    else:
        form_publicacion = PublicacionForm(instance=publicacion)

    return modulos_publicacion.render_editar_publicacion(request, form_publicacion, publicacion)

# Apartado de 'Mis publicaciones'
@login_required
@normal_required
def mis_publicaciones(request):
    if request.method == 'POST':
        publicacion_id = request.POST.get('publicacion_id')
        publicacion = get_object_or_404(Publicacion, pk=publicacion_id)

        if request.user == publicacion.autor:
            publicacion.delete()
            return redirect('mis_publicaciones')
        else:
            return redirect('mis_publicaciones')

    publicaciones = Publicacion.objects.filter(autor=request.user)
    if len(publicaciones) == 0:
        error = 'No hay publicaciones cargadas.'
        return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','mis_publicaciones.html'), {'publicaciones': publicaciones, 'error' : error})
    else:
        return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','mis_publicaciones.html'), {'publicaciones': publicaciones})

@login_required
@normal_required
def detalle_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    imagenes = publicacion.imagenes.all()

    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','detalle_publicacion.html'), {'publicacion': publicacion, 'imagenes': imagenes})
    
@login_required
@normal_required
def crear_oferta(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','crear_oferta.html'))


# APARTADO DE OFERTAS E INTERCAMBIOS
@login_required
@normal_required
def publicacion_existente(request, publicacion_id):
    publicacion_base = get_object_or_404(Publicacion, id=publicacion_id)
    publicaciones_usuario = Publicacion.objects.filter(autor=request.user)

    mensaje = ''

    if request.method == "POST":
        publicacion_id = request.POST.get('publicacion')
        fecha_encuentro = request.POST.get('fecha_encuentro')
        hora_encuentro = request.POST.get('hora_encuentro')

        mensaje, success = modulos_oferta.procesar_oferta(publicacion_base, request.user, publicacion_id, fecha_encuentro, hora_encuentro)
        
        if success:
            mensaje = 'Oferta creada con éxito.'
    
    contexto = {
        'aviso': mensaje,
        'publicacion_a_ofertar': publicacion_base,
        'publicaciones_usuario': publicaciones_usuario
    }
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'publicacion_existente.html'), contexto)

@login_required
@normal_required
def publicacion_privada(request, publicacion_id):

    publicacion_oferta = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == "POST":
        
        # Obtener datos de la publicación y las imágenes del formulario
        datos_publicacion = request.POST.dict()
        usuario = request.user

        # Verificar campos y obtener las imágenes
        imagenes = request.FILES.getlist('imagen')
        if len(imagenes) > 5 or len(imagenes) <= 0:
            return render(request, 'vista_usuario/publicacion_privada.html', {'publicacion_a_ofertar': publicacion_oferta,'error': 'El máximo de imágenes es 5 y el mínimo 1.'})
        
        # Verificar campos
        exito, mensaje_error = modulos_publicacion.verificar_campos_privada(datos_publicacion)
        if len(imagenes) > 5 or len(imagenes) <= 0:
            return render(request, 'vista_usuario/publicacion_privada.html', {'publicacion_a_ofertar': publicacion_oferta,'error': 'El máximo de imágenes es 5 y el mínimo 1.'})
        if not exito:
            return render(request, 'vista_usuario/publicacion_privada.html', {'publicacion_a_ofertar': publicacion_oferta,'error': mensaje_error})
        else:
            # Crear publicación (el 1 al final es para privada)
            nueva_publicacion = modulos_publicacion.crear_publicacion_privada(datos_publicacion,usuario,imagenes,publicacion_oferta.sucursal.id)
        
            # Mostrar mensaje de éxito
            return redirect('oferta_privada', publicacion_id=publicacion_oferta.id, publicacion_nueva_id=nueva_publicacion.id)
    else:
        # Si es una solicitud GET, simplemente renderizar la página principal
        return render(request, 'vista_usuario/publicacion_privada.html', {'publicacion_a_ofertar': publicacion_oferta})

@login_required
@normal_required
def mis_ofertas(request):
    if request.method == 'POST':
        oferta_id = request.POST.get('oferta_id')
        oferta = get_object_or_404(Oferta, pk=oferta_id)

        if request.user == oferta.usuario_recibe:
            mensaje, exito = modulos_intercambio.procesar_intercambio(oferta)
            if exito:
                return redirect('mis_ofertas')  # Redirecciona para actualizar la página
            else:
                return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'mis_ofertas.html'), {'aviso': mensaje})
        else:
            return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'mis_ofertas.html'), {'aviso': 'No tienes permisos para realizar esta acción.'})

    else:
        ofertas = Oferta.objects.filter(usuario_recibe=request.user)

        if len(ofertas) == 0:
            error = 'Usted no ha recibido nuevas solicitudes de intercambio.'
            return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'mis_ofertas.html'), {'ofertas': ofertas, 'aviso': error})
        else:
            return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'mis_ofertas.html'), {'ofertas': ofertas})

@login_required
@normal_required
def oferta_privada(request, publicacion_id, publicacion_nueva_id):
    publicacion_original = get_object_or_404(Publicacion, id=publicacion_id)
    publicacion_nueva = get_object_or_404(Publicacion, id=publicacion_nueva_id)

    if request.method == 'POST':
        # Obtener datos del formulario (fecha, hora, etc.)
        fecha_encuentro = request.POST.get('fecha_encuentro')
        hora_encuentro = request.POST.get('hora_encuentro')

        # Validar y crear la oferta privada
        mensaje, exito = modulos_oferta.procesar_oferta_privada(publicacion_original, publicacion_nueva, fecha_encuentro, hora_encuentro)

        if exito:
            # Mostrar mensaje de éxito
            return render(request, 'vista_usuario/oferta_privada.html', {'exito': "La oferta se ha creado con éxito."})
        else:
            # Mostrar mensaje de error
            return render(request, 'vista_usuario/oferta_privada.html', {'aviso': mensaje})

    # Renderizar el template 'oferta_privada.html' y pasar los datos necesarios
    return render(request, 'vista_usuario/oferta_privada.html', {
        'publicacion_original': publicacion_original,
        'publicacion_nueva': publicacion_nueva,
        'form_action': request.build_absolute_uri()
    })


@login_required
@normal_required
def mis_intercambios(request):
    user = request.user

    intercambios_base = Intercambio.objects.filter(base__autor=user)
    intercambios_oferta = Intercambio.objects.filter(ofer__autor=user)

    intercambios = intercambios_base | intercambios_oferta

    if not intercambios.exists():
        error = 'Usted no posee nuevos intercambios.'
        return render(request, 'vista_usuario/mis_intercambios.html', {'intercambios': intercambios, 'aviso': error})
    else:
        return render(request, 'vista_usuario/mis_intercambios.html', {'intercambios': intercambios})

# APARTADO DE USUARIO

def registro(request):
    
    if request.method == "POST":
        usuario = request.POST.dict()
        
        condicion_validacion, motivo_validacion = modulos_registro.verificar(usuario)

        if condicion_validacion:
                usuario_creado = User.objects.create(
                    username=usuario["correo_electronico"],
                    email=usuario["correo_electronico"],
                    first_name=usuario["nombre"],
                    last_name=usuario["apellido"],
                    dni=usuario["dni"],
                    fecha_nacimiento=usuario["fecha_nacimiento"]
                )
                usuario_creado.set_password(usuario["contraseña"])
                usuario_creado.save()

                
                mensaje_exito = "Usuario creado correctamente. Inicia sesión para continuar." #ACA SI LLEGA, PODRA PASAR ALGO EN EL MEDIO?
                return render(request,"pagina_inicio.html",{"aviso": mensaje_exito}) #NUNCA LLEGA ACA AUNQUE 


            
        else:
            return render(request, "vista_usuario/registro_usuario.html", {"error": motivo_validacion})

    else:
        return render(request, "vista_usuario/registro_usuario.html")
       
def restablecerContraseña(request):
    if request.method == "GET":
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','reestablecer_contraseña.html'), {
                "error": ""
            })
    else:
        if User.objects.filter(email=request.POST["email"]).exists():
            response = redirect("ingresar_codigo")
            response.set_cookie("email", request.POST["email"], httponly=True, secure=True)
            return response
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','reestablecer_contraseña.html'), {
                "error": "El correo electrónico ingresado no está registrado."
            })
        
def ingresarCodigo(request, codigo=[""]):
    if not "email" in request.COOKIES:
        raise Http404

    email = request.COOKIES["email"]
    user = get_object_or_404(User, email=email)
    if request.method == "GET":
        codigo[0] = secrets.token_urlsafe(6)
        send_mail("Cambiar contraseña", f"El código para cambiar su contraseña es '{codigo[0]}'.", settings.EMAIL_HOST_USER,[email])
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','ingresar_codigo.html'), {
            "codigo": codigo[0],
            "error": ""
        })
    else:
        if request.POST["codigo"] == codigo[0]:
            response = redirect("cambiar_contraseña")
            response.set_cookie("valid", True, httponly=True, secure=True)
            response.set_cookie("email", signer.sign(value=email), httponly=True, secure=True)
            return response
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','ingresar_codigo.html'), {
            "codigo": codigo[0],
            "error": "El código ingresado no coincide con el enviado al correo electrónico."
        })

def cambiarContraseña(request):
    if "valid" not in request.COOKIES:
        raise Http404
    try:    
        email = signer.unsign(request.COOKIES["email"])
    except:
        raise Http404
    
    user = get_object_or_404(User, email=email)
    if request.method == "GET":
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña.html'), {
            "error": ""
        })
    else:
        if request.POST["contraseña1"] == request.POST["contraseña2"]:
            resultado = modulos_registro.validar_contraseña(request.POST["contraseña1"])
            if resultado[0]:
                user.set_password(request.POST["contraseña1"])
                user.save()
                response = redirect("cambiar_contraseña_exito")
                response.delete_cookie("email")
                response.delete_cookie("valid")
                return response
            else:
                return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña.html'), {
                    "error": resultado[1]
                })
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña.html'), {
                "error": "Las contraseñas no coinciden."
            })
        
def cambiarContraseñaExito(request):
    return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña_exito.html'))

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")

@login_required
@normal_required
def mostrarPerfilCliente(request):
    user = get_object_or_404(User, email=request.user)
    if request.method == "GET":
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','mi_cuenta.html'),{
            "nombre": user.first_name,
            "apellido": user.last_name,
            "email": user.email,
            "dni": user.dni,
            "fecha_nacimiento": user.fecha_nacimiento
        })
    else:
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','mi_cuenta.html'))

@login_required
@normal_required
def editarPerfilCliente(request):
    user = get_object_or_404(User, email=request.user)
    if request.method == "GET":
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','editar_perfil_cliente.html'), {
            "nombre": user.first_name,
            "apellido": user.last_name,
            "exito": "",
            "error": ""
        })
    else:
        resultado_nombre = modulos_registro.validar_nombre(request.POST["nombre"])
        resultado_apellido =  modulos_registro.validar_nombre(request.POST["apellido"])
        if not resultado_nombre[0] or not resultado_apellido[0]:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','editar_perfil_cliente.html'), {
                "nombre": user.first_name,
                "apellido": user.last_name,
                "exito": "",
                "error": "Formato inválido para nombre/apellido."
            })
        else:
            user.first_name = request.POST["nombre"]
            user.last_name = request.POST["apellido"]
            user.save()
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','editar_perfil_cliente.html'), {
                "nombre": user.first_name,
                "apellido": user.last_name,
                "exito": "Cambios guardados correctamente.",
                "error": ""
            })
    
@login_required
@normal_required
def cambiarContraseñaCliente(request):
    user = get_object_or_404(User, email=request.user)
    if request.method == "GET":
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña_cliente.html'), {
            "exito": "",
            "error": ""
        })
    else:
        if user.check_password(request.POST["contraseña"]):
            if request.POST["contraseña1"] == request.POST["contraseña2"]:
                resultado = modulos_registro.validar_contraseña(request.POST["contraseña1"])
                if resultado[0]:
                    user.set_password(request.POST["contraseña1"])
                    user.save()
                    return render(request, os.path.join(TEMPLATE_DIR,'pagina_inicio.html'), {
                        "aviso": "Contraseña cambiada exitosamente.\nDebe iniciar sesión nuevamente.",
                    })
                else:
                    return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña_cliente.html'), {
                        "exito": "",
                        "error": resultado[1]
                    })
            else:
                return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña_cliente.html'), {
                        "exito": "",
                        "error": "Las contraseñas no coinciden."
                    })
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña_cliente.html'), {
                        "exito": "",
                        "error": "La contraseña es incorrecta."
                    })
