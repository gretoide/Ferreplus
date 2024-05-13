from django.shortcuts import render, redirect
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

@login_required
@admin_required
def pagina_administrador(request):
    return render(request,os.path.join(TEMPLATE_DIR,'vista_administrador','inicio_administrador.html'))

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")

def cargar_empleado(request):
    
    if request.method == "POST":
        usuario = request.POST.dict()
        
        condicion_validacion, motivo_validacion = modulos_carga_empleado.verificar(usuario)

        if condicion_validacion:
                usuario_creado = User.objects.create(
                    username=usuario["correo_electronico"],
                    first_name=usuario["nombre"],
                    last_name=usuario["apellido"],
                    dni=usuario["dni"],
                    cuil=usuario["cuil"],
                    fecha_nacimiento=usuario["fecha_nacimiento"]
    
                )
                if usuario["correo_personal"]:
                     usuario_creado.email = usuario["correo_personal"]
                else:
                     usuario_creado.email = usuario["correo_electronico"]
                usuario_creado.is_staff = True
                usuario_creado.set_password(usuario["contraseña"])
                #usuario_creado.set_sucursal_id(usuario["sucursal"]) FALTA LA PARTE DE MAURICIO
                usuario_creado.save()

                
                mensaje_exito = "Empleado cargado correctamente." 
                return render(request,os.path.join(TEMPLATE_DIR,'vista_administrador','registro_empleado.html'),{"aviso": mensaje_exito}) 


            
        else:
            return render(request, os.path.join(TEMPLATE_DIR,'vista_administrador','registro_empleado.html'), {"error": motivo_validacion})

    else:
        return render(request,os.path.join(TEMPLATE_DIR,'vista_administrador','registro_empleado.html'))