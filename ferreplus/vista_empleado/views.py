from django.shortcuts import render, redirect
from django.urls import reverse
import os
from pathlib import Path
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from ferreplus.modulos.modulos_inicio_sesion import staff_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils import timezone
from vista_usuario.models import Intercambio, User
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

def aceptarIntercambio(request,intercambio_id):
    try:
        intercambio = Intercambio.objects.get(id=intercambio_id)
    except Intercambio.DoesNotExist:
        messages.error(request, "El intercambio no existe")
        return redirect(listar_intercambios_pendientes)
    intercambio.estado = Intercambio.REALIZADO
    intercambio.save()
    messages.success(
        request, "El intercambio ha sido marcado como exitoso.")
    return redirect(listar_intercambios_pendientes)

def cancelarIntercambio(request,intercambio_id):
    try:
        intercambio = Intercambio.objects.get(id=intercambio_id)
    except Intercambio.DoesNotExist:
        messages.error(request, "El intercambio no existe")
        return redirect(listar_intercambios_pendientes)
    intercambio.estado = Intercambio.CANCELADO
    intercambio.save()
    messages.success(
        request, "El intercambio ha sido marcado como cancelado.")
    return redirect(listar_intercambios_pendientes)
    
    

def intercambio_ausente(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    usuario_uno = intercambio.base.autor
    usuario_dos = intercambio.ofer.autor
    usuarios = [usuario_uno,usuario_dos]

    context = {
        'usuarios': usuarios,
        'intercambio': intercambio
    }
    return render(request, 'vista_empleado/marcar_ausente.html', context)

    """if request.method == 'POST':
        usuario_ausente_id = request.POST.get('usuario_ausente')
        usuario_ausente = get_object_or_404(User, id=usuario_ausente_id)
        intercambio.estado = Intercambio.CANCELADO_AUSENTE
        intercambio.usuario_ausente = usuario_ausente
        intercambio.save()
        return redirect(listar_intercambios_pendientes)  # Update this to your actual main view name
    """

def marcado_ausente(request,intercambio_id,usuario_id):
    
    usuario_ausente = get_object_or_404(User, id=usuario_id)
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)

    intercambio.estado = Intercambio.CANCELADO_AUSENTE
    intercambio.usuario_ausente = usuario_ausente
    intercambio.save()
    return redirect(listar_intercambios_pendientes)  
