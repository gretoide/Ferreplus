from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from pathlib import Path
from vista_administrador.models import Sucursal
from .models import User, Publicacion, Imagen
from ferreplus.modulos import modulos_registro
from .modulos import modulos_publicacion
from .forms import PublicacionForm
from django.contrib.auth.decorators import login_required
from ferreplus.modulos.modulos_inicio_sesion import normal_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.csrf import csrf_protect
from django.core.signing import Signer
signer = Signer()

import os
import secrets



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

    # Obtener todas las publicaciones excepto las del usuario actual
    publicaciones = Publicacion.objects.exclude(autor=usuario_actual)

    # Crear un diccionario para almacenar las imágenes asociadas a cada publicación
    imagenes_por_publicacion = {}

    # Iterar sobre todas las publicaciones
    for publicacion in publicaciones:
        # Obtener todas las imágenes relacionadas con la publicación actual
        imagenes_publicacion = publicacion.imagenes.all()
        
        # Almacenar las imágenes en el diccionario con la clave como la publicación misma
        imagenes_por_publicacion[publicacion] = imagenes_publicacion

    # Renderizar la plantilla con las publicaciones y las imágenes asociadas
    print('-'*100,imagenes_por_publicacion)
    return render(request, 'vista_usuario/vista_principal.html', {'publicaciones': publicaciones, 'imagenes_por_publicacion': imagenes_por_publicacion})


    
@login_required
@normal_required
def subir_publicacion(request):
    
    if request.method == "POST":
        # Obtener datos de la publicación y las imágenes del formulario
        datos_publicacion = request.POST.dict()
        usuario = request.user

        # Verificar campos y obtener las imágenes
        imagenes = request.FILES.getlist('imagen')
        if len(imagenes) > 5 or len(imagenes) <= 0:
            return render(request, 'vista_usuario/subir_publicacion.html', {'error': 'El máximo de imágenes es 5 y el mínimo 1.'})
        
        # Verificar campos
        exito, mensaje_error = modulos_publicacion.verificar_campos(datos_publicacion)
        if len(imagenes) > 5 or len(imagenes) <= 0:
            return render(request, 'vista_usuario/subir_publicacion.html', {'error': 'El máximo de imágenes es 5 y el mínimo 1.'})
        if not exito:
            return render(request, 'vista_usuario/subir_publicacion.html', {'error': mensaje_error})
        else:
            # Crear publicación
            modulos_publicacion.crear_publicacion(datos_publicacion,usuario,imagenes)
            
            # Mostrar mensaje de éxito
            return render(request, 'vista_usuario/subir_publicacion.html', {'aviso': "La publicación se ha creado con éxito."})
    else:
        # Si es una solicitud GET, simplemente renderizar la página principal
        return render(request, 'vista_usuario/subir_publicacion.html',{"sucursales": Sucursal.objects.all()})

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

def detalle_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    imagenes = publicacion.imagenes.all()

    contexto = {
        'publicacion': publicacion,
        'imagenes': imagenes,
    }

    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','detalle_publicacion.html'), contexto)


@login_required
@normal_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)

    if request.method == 'POST':
        form_publicacion = PublicacionForm(request.POST, instance=publicacion)

        if form_publicacion.is_valid():
            try:
                # Manejar la eliminación de imágenes
                imagenes_a_eliminar = request.POST.getlist('eliminar_imagenes')
                nuevas_imagenes = request.FILES.getlist('nuevas_imagenes')
                
                # Número total de imágenes después de las eliminaciones y adiciones
                imagenes_actuales = publicacion.imagenes.count()
                nuevas_imagenes_count = len(nuevas_imagenes)
                imagenes_a_eliminar_count = len(imagenes_a_eliminar)
                imagenes_finales_count = imagenes_actuales - imagenes_a_eliminar_count + nuevas_imagenes_count
                
                if imagenes_finales_count < 1:
                    error = 'Debe haber al menos una imagen asociada a la publicación.'
                    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'editar_publicacion.html'), {
                        'form_publicacion': form_publicacion,
                        'publicacion': publicacion,
                        'sucursales': Sucursal.objects.all(),
                        'error': error
                    })
                
                if imagenes_finales_count > 5:
                    error = 'Solo se permiten hasta 5 imágenes.'
                    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'editar_publicacion.html'), {
                        'form_publicacion': form_publicacion,
                        'publicacion': publicacion,
                        'sucursales': Sucursal.objects.all(),
                        'error': error
                    })
                
                # Guardar la publicación
                publicacion = form_publicacion.save()

                # Eliminar las imágenes especificadas
                for imagen_id in imagenes_a_eliminar:
                    imagen = publicacion.imagenes.get(pk=imagen_id)
                    imagen.delete()

                # Agregar las nuevas imágenes
                for imagen in nuevas_imagenes:
                    publicacion.imagenes.add(Imagen.objects.create(imagen=imagen))

                return redirect('mis_publicaciones')
            except ValidationError as e:
                error = '; '.join(str(v[0]) for v in e.message_dict.values())
                return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'editar_publicacion.html'), {
                    'form_publicacion': form_publicacion,
                    'publicacion': publicacion,
                    'sucursales': Sucursal.objects.all(),
                    'error': error
                })
    else:
        form_publicacion = PublicacionForm(instance=publicacion)

    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'editar_publicacion.html'), {
        'form_publicacion': form_publicacion,
        'publicacion': publicacion,
        'sucursales': Sucursal.objects.all()
    })
    
@login_required
@normal_required
def crear_oferta(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','crear_oferta.html'))




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
