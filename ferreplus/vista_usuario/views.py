from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
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

def pagina_principal(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','vista_principal.html'))

def subir_publicacion(request):
    if request.method == "POST":
        # Obtener datos de la publicación y las imágenes del formulario
        datos_publicacion = request.POST.dict()
        imagenes = request.FILES.getlist('imagen')  
        
        # Verificar campos
        exito, mensaje_error = modulos_publicacion.verificar_campos(datos_publicacion)
        if len(imagenes) > 5:
            return render(request, 'vista_usuario/subir_publicacion.html', {'error': 'El máximo de imágenes permitidas es 5.'})
        if not exito:
            return render(request, 'vista_usuario/subir_publicacion.html', {'error': mensaje_error})
        else:
            # Crear publicación
            modulos_publicacion.crear_publicacion(datos_publicacion, imagenes)
            
            # Mostrar mensaje de éxito
            return render(request, 'vista_usuario/subir_publicacion.html', {'aviso': "La publicación se ha creado con éxito."})
    else:
        # Si es una solicitud GET, simplemente renderizar la página principal
        return render(request, 'vista_usuario/subir_publicacion.html')


def crear_oferta(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','crear_oferta.html'))

def registro(request):
    if request.method == "POST":
        #Obtengo usuario si el metodo fue un post
        usuario = request.POST.dict()
        condicion,motivo = modulos_sesion.verificar(usuario)
        if condicion: 
            Usuario(usuario["nombre"],usuario["apellido"],usuario["dni"],usuario["contraseña"],usuario["correo_electronico"],usuario["fecha_nacimiento"]).save()
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
            return redirect("cambiar_contraseña", email=email, contraseña=user.contrasenia)
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','ingresar_codigo.html'), {
            "codigo": codigo[0],
            "error": "El codigo ingresado no coincide con el enviado al correo electronico."
        })

def cambiarContraseña(request, email, contraseña):
    user = get_object_or_404(Usuario, email=email)
    if user.contrasenia != contraseña:
        raise Http404
    if request.method == "GET":
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','cambiar_contraseña.html'), {
            "error": ""
        })
    else:
        if request.POST["contraseña1"] == request.POST["contraseña2"]:
            resultado = modulos_sesion.validar_contraseña(request.POST["contraseña1"])
            if resultado[0]:
                user.contrasenia = request.POST["contraseña1"]
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
