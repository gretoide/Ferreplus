from django.shortcuts import render, redirect
import os
from pathlib import Path
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
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

def obtener_usuarios(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    publicacion_base = intercambio.publicacion_base
    publicacion_oferta = intercambio.publicacion_oferta
    
    usuarios = [
        {'id': publicacion_base.usuario.id, 'nombre': publicacion_base.usuario.nombre},
        {'id': publicacion_oferta.usuario.id, 'nombre': publicacion_oferta.usuario.nombre}
    ]
    
    return JsonResponse({'usuarios': usuarios})

def intercambio_ausente(request, intercambio_id):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        intercambio = get_object_or_404(Intercambio, id=intercambio_id)
        intercambio.estado = 'Ausente'
        intercambio.usuario_ausente = usuario_id
        intercambio.save()
        return redirect(listar_intercambios_pendientes)  # Cambia esto al nombre de tu vista principal
