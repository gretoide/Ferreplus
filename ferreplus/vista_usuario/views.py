from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from pathlib import Path
from ferreplus.modulos import modulos_sesion
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

def  principal(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario', 'vista_principal.html'))

def crear_oferta(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_usuario','crear_oferta.html'))

def registro(request):
    if request.method == "POST":
        #Obtengo usuario si el metodo fue un post
        usuario = request.POST.dict()
        condicion,motivo = modulos_sesion.verificar_fecha(usuario["fecha_nacimiento"])
        if condicion: 
            return redirect("inicio")
        return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','registro_usuario.html'),{'error' : motivo})
    return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','registro_usuario.html'))
    