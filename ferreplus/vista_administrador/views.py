from django.shortcuts import render
import os
from pathlib import Path
from ferreplus.modulos.modulos_inicio_sesion import admin_required
from django.contrib.auth.decorators import login_required

BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
# Create your views here.

@login_required
@admin_required
def pagina_administrador(request):
    return render(request,os.path.join(TEMPLATE_DIR,'vista_administrador','inicio_administrador.html'))
