from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import views as auth_views
from pathlib import Path
from .models import Usuario, Publicacion, Imagen
from ferreplus.modulos import modulos_sesion
from .modulos import modulos_publicacion
import os
import secrets



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

def subir_publicacion(request):
    if request.method == "POST":
        # Obtener datos de la publicación y las imágenes del formulario
        datos_publicacion = request.POST.dict()
        imagenes = request.FILES.getlist('imagen')  # Obtener lista de imágenes

        # Verificar y crear la publicación utilizando la función modularizada
        exito, mensaje = modulos_publicacion.verificar_y_crear_publicacion(datos_publicacion, imagenes)
        
        if exito:
            # Redirigir a la misma página o a otra de tu elección
            return render(request, 'vista_usuario/vista_principal.html', {'aviso': mensaje})
        else:
            # Mostrar mensaje de error
            return render(request, 'vista_usuario/vista_principal.html', {'error': mensaje})
    else:
        # Si es una solicitud GET, simplemente renderizar la página principal
        return render(request, 'vista_usuario/vista_principal.html')


def crear_oferta(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','crear_oferta.html'))

def registro(request):
    if request.method == "POST":
        #Obtengo usuario si el metodo fue un post
        usuario = request.POST.dict()
        condicion,motivo = modulos_sesion.verificar(usuario)
        if condicion: 
            Usuario(usuario["nombre_completo"],usuario["dni"],usuario["contraseña"],usuario["correo_electronico"],usuario["fecha_nacimiento"]).save()
            return render(request,os.path.join(TEMPLATE_DIR,'pagina_inicio.html'),{"aviso": "Cuenta creada con exito"})
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','registro_usuario.html'),{'error' : motivo})
    else:
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','registro_usuario.html'),{})

def restablecerContraseña(request):
    if request.method == "GET":
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','reestablecer_contraseña.html'), {
                "error": ""
            })
    else:
        if Usuario.objects.filter(email=request.POST["email"]).exists():
            return redirect("ingresar_codigo", email=request.POST["email"])
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','reestablecer_contraseña.html'), {
                "error": "El correo electronico ingresado no esta registrado."
            })
        
def ingresarCodigo(request, email, codigo=[""]):
    user = get_object_or_404(Usuario, email=email)
    if request.method == "GET":
        codigo[0] = secrets.token_urlsafe(6)
        send_mail("Cambiar contraseña", f"El codigo para cambiar su contraseña es {codigo[0]}", settings.EMAIL_HOST_USER,[email])
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','ingresar_codigo.html'), {
            "codigo": codigo[0],
            "error": ""
        })
    else:
        if request.POST["codigo"] == codigo[0]:
            print("hola")
            return redirect("cambiar_contraseña", email=email, contraseña=user.contrasenia)
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','ingresar_codigo.html'), {
            "codigo": codigo[0],
            "error": "El codigo ingresado no coincide con el enviado al correo electronico."
        })

def cambiarContraseña(request, email, contraseña):
    user = get_object_or_404(Usuario, email=email)
    if request.method == "GET":
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña.html'), {
            "error": ""
        })
    else:
        if request.POST["contraseña1"] == request.POST["contraseña2"]:
            user.contrasenia = request.POST["contraseña1"]
            user.save()
            return redirect("cambiar_contraseña_exito") 
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña.html'), {
                "error": "Las contraseñas no coinciden."
            })
        
def cambiarContraseñaExito(request):
    return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña_exito.html'))
