from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib import messages
from pathlib import Path
from .models import Sucursal
from .forms import formularioSucursal as nue_sucur
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
import os
import secrets


# Create your views here.


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


def inicio_admin(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_administrador', 'pagina_principal_admin.html'))


def agregar_sucursal(request):
    if request.method == "POST":

        form_sucursal = nue_sucur(request.POST)

        if form_sucursal.is_valid():
            datos = form_sucursal.cleaned_data

            sucursal_nueva = Sucursal.objects.create(
                nombre=datos['nombre'],
                direccion=datos['direccion']
            )
            sucursal_nueva.save()
    else:
        form_sucursal = nue_sucur()
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_administrador', 'nueva_sucursal.html'),{"form":form_sucursal})

# def nueva_sucursal(request):

# def crear_sucursal():
