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

from django.core.exceptions import ValidationError
import os
import secrets

from django.shortcuts import render
import os
from pathlib import Path
from ferreplus.modulos.modulos_inicio_sesion import admin_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from vista_usuario.models import User
from ferreplus.modulos import modulos_carga_empleado

BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
# Create your views here.


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates', 'vista_administrador')

@login_required
@admin_required
def inicio_admin(request):
    return render(request,os.path.join(TEMPLATE_DIR,'pagina_principal_admin.html'))


@login_required
@admin_required
def agregar_sucursal(request):
    if request.method == "POST":

        form_sucursal = nue_sucur(request.POST)

        if form_sucursal.is_valid():
            datos = form_sucursal.cleaned_data

            if Sucursal.objects.filter(nombre=datos['nombre']).exists():
               error = 'Ya existe una sucursal con ese nombre'
               return render(request,  os.path.join(TEMPLATE_DIR, 'nueva_sucursal.html'), {"form": form_sucursal, 'error': error})

            exito = 'Sucursal creada con exito'
            sucursal_nueva = Sucursal.objects.create(
                nombre=datos['nombre'],
                direccion=datos['direccion']
            )
            sucursal_nueva.save()
            return render(request,  os.path.join(TEMPLATE_DIR, 'nueva_sucursal.html'), {"form": form_sucursal, 'exito': exito})

    else:
        form_sucursal = nue_sucur()
    return render(request, os.path.join(TEMPLATE_DIR, 'nueva_sucursal.html'), {"form": form_sucursal})

@login_required
@admin_required
def ver_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, os.path.join(TEMPLATE_DIR, 'ver_sucursales.html'), {'sucursales': sucursales})

@login_required
@admin_required
def detalle_sucursal(request, sucursal_id):
    a_ver = Sucursal.objects.get(id=sucursal_id)
    return render(request, os.path.join(TEMPLATE_DIR, 'detalle_sucursal.html'), {'sucursal': a_ver})
