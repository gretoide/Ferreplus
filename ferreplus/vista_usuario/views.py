from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from django.shortcuts import render, redirect

from django.core.mail import send_mail
from django.conf import settings

from pathlib import Path
from .models import User, Publicacion, Imagen
from ferreplus.modulos import modulos_registro
from .modulos import modulos_publicacion
from django.contrib.auth.decorators import login_required
from ferreplus.modulos.modulos_inicio_sesion import normal_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseForbidden

import os
import secrets



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

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
        imagenes = request.FILES.getlist('imagen')
        usuario = request.user
        
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
        return render(request, 'vista_usuario/subir_publicacion.html')

# Apartado de 'Mis publicaciones'
@login_required
@normal_required
def mis_publicaciones(request):
    if request.method == 'POST':
        publicacion_id = request.POST.get('publicacion_id')
        publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
        
        if request.user == publicacion.autor:
            publicacion.delete()
            messages.success(request, "Publicación eliminada con éxito.")
            return redirect('mis_publicaciones')
        else:
            messages.error(request, "No tienes permiso para eliminar esta publicación.")
            return redirect('mis_publicaciones')

    publicaciones = Publicacion.objects.filter(autor=request.user)
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','mis_publicaciones.html'), {'publicaciones': publicaciones})

@login_required
@normal_required
def editar_publicacion(request, publicacion_id):
    # Obtiene la instancia de la publicación
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    
    if request.method == 'POST':
        # Obtener datos del formulario y las nuevas imágenes
        datos_publicacion = request.POST.dict()
        nuevas_imagenes = request.FILES.getlist('imagen')

        # Verificar campos
        exito, mensaje_error = modulos_publicacion.verificar_campos(datos_publicacion)
        if not exito:
            return render(request, 'vista_usuario/editar_publicacion.html', {'publicacion': publicacion, 'error': mensaje_error})
        else:
                exito, mensaje = modulos_publicacion.editar_publicacion(publicacion, datos_publicacion, nuevas_imagenes)
                if exito:
                    return render(request, 'vista_usuario/editar_publicacion.html', {'publicacion': publicacion, 'aviso': mensaje})
                else:
                    return render(request, 'vista_usuario/editar_publicacion.html', {'publicacion': publicacion, 'error': mensaje})       
    else:
        # Renderizar el formulario de edición con los datos actuales de la publicación
        return render(request, 'vista_usuario/editar_publicacion.html', {'publicacion': publicacion})

    
@login_required
@normal_required
def eliminar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    
    if request.method == 'POST':
        # Verifica si el usuario tiene permiso para eliminar la publicación
        if request.user == publicacion.autor:  # Asume que la publicación tiene un campo 'autor' que indica quién la creó
            # Si el usuario tiene permiso, elimina la publicación
            publicacion.delete()
            return HttpResponseForbidden("Publicación eliminada con éxito.")
        else:
            # Si el usuario no tiene permiso, devuelve un error de prohibido
            return HttpResponseForbidden("No tienes permiso para eliminar esta publicación.")
        
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
            return redirect("ingresar_codigo", email=request.POST["email"])
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','reestablecer_contraseña.html'), {
                "error": "El correo electronico ingresado no esta registrado."
            })
        
def ingresarCodigo(request, email, codigo=[""]):
    user = get_object_or_404(User, email=email)
    if request.method == "GET":
        codigo[0] = secrets.token_urlsafe(6)
        send_mail("Cambiar contraseña", f"El codigo para cambiar su contraseña es {codigo[0]}", settings.EMAIL_HOST_USER,[email])
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','ingresar_codigo.html'), {
            "codigo": codigo[0],
            "error": ""
        })
    else:
        if request.POST["codigo"] == codigo[0]:
            return redirect("cambiar_contraseña", email=email, contraseña=user.password)
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','ingresar_codigo.html'), {
            "codigo": codigo[0],
            "error": "El codigo ingresado no coincide con el enviado al correo electronico."
        })

def cambiarContraseña(request, email, contraseña):
    user = get_object_or_404(User, email=email)
    if user.password != contraseña:
        raise Http404
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
                return redirect("cambiar_contraseña_exito") 
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