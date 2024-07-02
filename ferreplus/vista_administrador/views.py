from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
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

import requests

from django.shortcuts import render
import os
from pathlib import Path
from ferreplus.modulos.modulos_inicio_sesion import admin_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from vista_usuario.models import User
from ferreplus.modulos import modulos_carga_empleado
import subprocess
import os

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
    return render(request, os.path.join(TEMPLATE_DIR, 'pagina_principal_admin.html'))

def ejecutar_estadisticas(request):
    # Ruta del archivo de Streamlit
    ruta_estadisticas = os.path.join(settings.BASE_DIR, 'vista_administrador', 'ejecutar_streamlit.py')

    # Verificar si Streamlit ya está ejecutándose
    try:
        respuesta = requests.get("http://localhost:8501")
        if respuesta.status_code == 200:
            # Streamlit ya está ejecutándose, redirigir directamente
            return redirect("http://localhost:8501")
    except requests.exceptions.ConnectionError:
        # Streamlit no está ejecutándose, iniciar
        subprocess.Popen(["streamlit", "run", ruta_estadisticas])

    return render(request, os.path.join(TEMPLATE_DIR, 'pagina_principal_admin.html'))

@login_required
@admin_required
def agregar_sucursal(request):
    if request.method == "POST":

        form_sucursal = nue_sucur(request.POST)

        if form_sucursal.is_valid():
            datos = form_sucursal.cleaned_data

            if Sucursal.objects.filter(nombre=datos['nombre']).exists():
                messages.success(
                    request, "Ya existe una sucursal con ese nombre.")
                return render(request,  os.path.join(TEMPLATE_DIR, 'nueva_sucursal.html'), {"form": form_sucursal})
            sucursal_nueva = Sucursal.objects.create(
                nombre=datos['nombre'],
                direccion=datos['direccion']
            )
            sucursal_nueva.save()
            messages.success(
                request, f"La sucursal '{sucursal_nueva.nombre}' se creó con éxito.")
            return render(request,  os.path.join(TEMPLATE_DIR, 'nueva_sucursal.html'), {"form": form_sucursal})

    else:
        form_sucursal = nue_sucur()
    return render(request, os.path.join(TEMPLATE_DIR, 'nueva_sucursal.html'), {"form": form_sucursal})

@login_required
@admin_required
def ver_sucursales(request):
    sucursales = Sucursal.objects.all()
    if len(sucursales) == 0:
        messages.error(request, "No hay sucursales disponibles para mostrar.")
    return render(request, os.path.join(TEMPLATE_DIR, 'ver_sucursales.html'), {'sucursales': sucursales})

@login_required
@admin_required
def eliminar_sucursal(request, sucursal_id):
    try:
        a_eliminar = Sucursal.objects.get(id=sucursal_id)
    except Sucursal.DoesNotExist:
        messages.error(request, "La sucursal no existe.")
        return redirect(ver_sucursales)
    a_eliminar.delete()
    messages.success(
        request, f"La sucursal '{a_eliminar.nombre}' se eliminó con éxito.")
    return redirect(ver_sucursales)


@login_required
@admin_required
def detalle_sucursal(request, sucursal_id):
    a_ver = Sucursal.objects.get(id=sucursal_id)
    empleados_de_sucursal = User.objects.filter(
        is_staff=1, is_active=1).filter(sucursal_id=sucursal_id)
    return render(request, os.path.join(TEMPLATE_DIR, 'detalle_sucursal.html'), {'sucursal': a_ver, 'empleados': empleados_de_sucursal})

def detalle_empleado(request,empleado_id):
    a_ver = User.objects.get(id=empleado_id)
    return render(request,os.path.join(TEMPLATE_DIR,'detalle_empleado.html'),{'empleado' : a_ver})

@login_required
@admin_required
def cargar_empleado(request):
    if request.method == "POST":
        usuario = request.POST.dict()

        condicion_validacion, motivo_validacion = modulos_carga_empleado.verificar(
            usuario)

        if condicion_validacion:
                sucursal = Sucursal.objects.get(id=usuario["sucursal"])
                
                usuario_creado = User.objects.create(
                    username=usuario["correo_electronico"],
                    first_name=usuario["nombre"],
                    last_name=usuario["apellido"],
                    dni=usuario["dni"],
                    cuil=usuario["cuil"],
                    fecha_nacimiento=usuario["fecha_nacimiento"],
                    sucursal=sucursal
    
                )
                if usuario["correo_personal"]:
                     usuario_creado.email = usuario["correo_personal"]
                else:
                    usuario_creado.email = usuario["correo_electronico"]
                
                usuario_creado.is_staff = True
                password = get_random_string(length=12).upper()
                usuario_creado.set_password(password)
                #usuario_creado.set_sucursal_id(usuario["sucursal"]) 
                usuario_creado.save()
                subject = 'Bienvenido a la empresa'
                message = f'Hola {usuario["nombre"]},\n\nTu cuenta ha sido creada exitosamente. Tu contraseña es: {password}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [usuario_creado.email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    

                mensaje_exito = "Empleado cargado correctamente."
                return render(request, os.path.join(TEMPLATE_DIR, 'registro_empleado.html'), {"aviso": mensaje_exito, "sucursales": Sucursal.objects.all()})

        else:
            return render(request, os.path.join(TEMPLATE_DIR, 'registro_empleado.html'), {"error": motivo_validacion, "sucursales": Sucursal.objects.all()})

    else:
        return render(request, os.path.join(TEMPLATE_DIR, 'registro_empleado.html'), {"sucursales": Sucursal.objects.all()})


@login_required
@admin_required
def ver_empleados(request):
    empleados = User.objects.filter(is_staff=1,is_active=True)
    exempleados = User.objects.filter(is_staff=1,is_active=False)
    if len(empleados) == 0:
        messages.error(request, "No hay empleados para mostrar.")
    return render(request, os.path.join(TEMPLATE_DIR, 'ver_empleados.html'), {'empleados': empleados,"exempleados":exempleados})

@login_required
@admin_required
def eliminar_empleado(request, empleado_id):
    try:
        a_eliminar = User.objects.get(id=empleado_id)
    except User.DoesNotExist:
        messages.error(request, "El empleado no existe")
        return redirect(ver_empleados)
    a_eliminar.is_active = False
    nuevo_user="###"+a_eliminar.username
    a_eliminar.username = str(nuevo_user)
    eliminado=False
    while not eliminado:
        try:
            a_eliminar.save()
            eliminado = True
        except:
            nuevo_user+="#"
            a_eliminar.username=nuevo_user
    messages.success(
        request, f"El empleado con CUIL '{a_eliminar.cuil}' se eliminó con éxito.")
    return redirect(ver_empleados)

@login_required
@admin_required
def editar_sucursal(request, sucursal_id):
    aEditar = get_object_or_404(Sucursal, id=sucursal_id)
    if request.method == "POST":
        datos = request.POST.dict()
        
        try:
            repetido = Sucursal.objects.get(nombre=datos["nombre"])
            if repetido.id == aEditar.id:
                aEditar.nombre = datos["nombre"]
                aEditar.direccion = datos["direccion"]
                aEditar.save()
            else:
                messages.error(request,"El nombre que se quiere ingresar ya se encuentra registrado.")
                return render(request, os.path.join(TEMPLATE_DIR, 'editar_sucursal.html'), {'sucursal': aEditar})
        except Sucursal.DoesNotExist:
            aEditar.nombre = datos["nombre"]
            aEditar.direccion = datos["direccion"]
            aEditar.save()
        messages.success(request,"La sucursal se modificó con éxito.")
        return redirect(detalle_sucursal,aEditar.id)
    return render(request, os.path.join(TEMPLATE_DIR, 'editar_sucursal.html'), {'sucursal': aEditar})

@login_required
@admin_required
def editarEmpleado(request, empleadoId):
    empleado = get_object_or_404(User, id=empleadoId)
    sucursalEmpleado = Sucursal.objects.get(id=empleado.sucursal_id)
    sucursales = Sucursal.objects.all()

    if request.method == 'GET':
        return render(request, os.path.join(TEMPLATE_DIR, "editar_empleado_admin.html"), {
            'empleado': empleado,
            'sucursales': sucursales,
            'sucursalEmpleado': sucursalEmpleado,
            'error': "",
            'exito': ""
        })
    else:
        empleado.first_name = request.POST["nombre"]
        empleado.last_name = request.POST["apellido"]
        empleado.sucursal_id = request.POST["sucursal"]
        sucursalEmpleado = Sucursal.objects.get(id=request.POST["sucursal"])
        empleado.save()
        return render(request, os.path.join(TEMPLATE_DIR, "editar_empleado_admin.html"), {
            'empleado': empleado,
            'sucursales': sucursales,
            'sucursalEmpleado': sucursalEmpleado,
            'error': "",
            'exito': "Empleado actualizado correctamente."
        })
