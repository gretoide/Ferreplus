from django.shortcuts import render
import os
from pathlib import Path
from ferreplus.modulos.modulos_inicio_sesion import staff_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from vista_usuario.models import Intercambio
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

@never_cache
@login_required
@staff_required
def pagina_empleado(request):
    return render(request,os.path.join(TEMPLATE_DIR,'vista_empleado','inicio_empleado.html')) 

def listar_intercambios_pendientes(request):
    usuario = request.user
    sucursal = usuario.sucursal  # Asumiendo que el modelo User tiene una relación con Sucursal
    intercambios = Intercambio.objects.filter(sucursal=sucursal, estado=Intercambio.PENDIENTE)
    return render(request, os.path.join(TEMPLATE_DIR,'vista_empleado','ver_intercambios.html'), {'intercambios': intercambios})