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
from django.db.models import Q
from datetime import datetime
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent

# Define the template directory path using os.path.join
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


@never_cache
@login_required
@staff_required
def pagina_empleado(request):
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_empleado', 'inicio_empleado.html'))


@never_cache
@login_required
@staff_required
def listar_intercambios_pendientes(request):
    usuario = request.user
    # Asumiendo que el modelo User tiene una relación con Sucursal
    sucursal = usuario.sucursal
    intercambios = Intercambio.objects.filter(
        sucursal=sucursal, estado=Intercambio.PENDIENTE)

    if request.method == "POST":
        busqueda = request.POST.dict()
        if busqueda["buscador"] != "":
            a_buscar = busqueda["buscador"]
            intercambios_dni = intercambios.filter(Q(base__autor__dni__icontains=a_buscar) | Q(ofer__autor__dni__icontains=a_buscar))
            intercambios_nombre = intercambios.filter(Q(base__autor__first_name__icontains=a_buscar) | Q(base__autor__last_name__icontains=a_buscar) | Q(
                    ofer__autor__first_name__icontains=a_buscar) | Q(ofer__autor__last_name__icontains=a_buscar))
            intercambios_producto = intercambios.filter(Q(base__titulo__icontains=a_buscar) | Q(ofer__titulo__icontains=a_buscar))
            if a_buscar.isdigit():
                intercambios = list(intercambios_dni.distinct()) + list(intercambios_producto.distinct()) + list(intercambios_nombre.distinct())
            else:
                intercambios = list(intercambios_nombre.distinct()) + list(intercambios_producto.distinct()) + list(intercambios_dni.distinct())
        if busqueda["fecha"] != "":
            busqueda_fecha = datetime.strptime(busqueda["fecha"], '%Y-%m-%d').date()
            intercambios = filter(lambda i: i.fecha_intercambio == busqueda_fecha,intercambios)
        
    orden = request.GET.get('orden')
    if orden == "descendente":
        intercambios = sorted(intercambios,key=lambda x: (x.fecha_intercambio, x.hora),reverse=True)
    else:
        intercambios = sorted(intercambios,key=lambda x:(x.fecha_intercambio,x.hora))
    return render(request, os.path.join(TEMPLATE_DIR, 'vista_empleado', 'ver_intercambios.html'), {'intercambios': intercambios})

@never_cache
@login_required
@staff_required
def aceptarIntercambio(request, intercambio_id):
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


@never_cache
@login_required
@staff_required
def cancelarIntercambio(request, intercambio_id):
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


@never_cache
@login_required
@staff_required
def intercambio_ausente(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    usuario_uno = intercambio.base.autor
    usuario_dos = intercambio.ofer.autor
    usuarios = [usuario_uno, usuario_dos]

    context = {
        'usuarios': usuarios,
        'intercambio': intercambio
    }
    return render(request, 'vista_empleado/marcar_ausente.html', context)


@never_cache
@login_required
@staff_required
def marcado_ausente(request, intercambio_id, usuario_id):

    usuario_ausente = get_object_or_404(User, id=usuario_id)
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)

    intercambio.estado = Intercambio.CANCELADO_AUSENTE
    intercambio.usuario_ausente = usuario_ausente
    intercambio.save()
    return redirect(listar_intercambios_pendientes)
