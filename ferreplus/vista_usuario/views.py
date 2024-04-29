from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.template import loader
from pathlib import Path
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
    return render(request, os.path.join(TEMPLATE_DIR,'vista_usuario','registro_usuario.html'))
    