from . import modulos_registro
from vista_usuario.models import User


def validar_espacio_blanco(cadena):
    return any(i.isspace() for i in cadena)


def validar_dni(dni):
    condicion = True
    motivo = ""


    if validar_espacio_blanco(dni) or len(dni) != 8 or not dni.isdigit():
        condicion = False
        motivo = "Formato de DNI inválido, el DNI deben ser 8 números sin espacios en blanco"

    try:
        dni = int(dni)
    except ValueError:
        condicion = False
        motivo = "Formato de DNI inválido, el DNI deben ser 8 números sin espacios en blanco"
    else:
        try:
            usuario_existente = User.objects.get(dni=dni)
            if usuario_existente.is_staff:
                condicion = False
                motivo = "El DNI ingresado ya corresponde a un empleado"
        except User.DoesNotExist:
            pass

    return (condicion, motivo)

import re

def validar_cuil(cuil,dni):
    condicion = True
    motivo = ""
    patron = r'^\d{2}-\d{8}-\d{1}$'
    
    if not re.match(patron, cuil):
        condicion = False
        motivo = "El formato del CUIL es invalido"
        
    
    if condicion and dni != cuil.split("-")[1]:
        condicion = False
        motivo = "El CUIL no coincide con el DNI ingresado"
        
    
    return(condicion,motivo)
    
def validar_correo_personal(correo_personal):

    condicion = True
    motivo = ""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if correo_personal:
       
        if validar_espacio_blanco(correo_personal) or not re.match(patron, correo_personal):
            condicion = False
            motivo = "Formato inválido del correo personal"

    return (condicion,motivo)

def validar_fecha(fecha):
    condicion,motivo = modulos_registro.validar_fecha(fecha)
    if not condicion:
        motivo = "El empleado debe ser mayor de edad para ser cargado en el sistema"
    return(condicion,motivo)


def validar_correo_empleado(correo):
    condicion = True
    motivo = ""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Verificar si el correo coincide con el patrón y si no contiene espacios en blanco
    if validar_espacio_blanco(correo) or not re.match(patron, correo):
        condicion = False
        motivo = "Formato inválido para el correo electrónico."
    else:
        try:
            # Verificar si el correo ya está en uso por otro usuario
            user = User.objects.get(username=correo)
            if user.is_active:
                condicion = False
                motivo = "Correo electrónico ya en uso"
        except Exception as e:
            motivo = str(e)
            condicion = False

    return (condicion, motivo)



def verificar(empleado):
    lista_validaciones = [modulos_registro.validar_nombre(empleado["nombre"]),modulos_registro.validar_apellido(empleado["apellido"]),
                          validar_dni(empleado["dni"]),validar_cuil(empleado["cuil"],empleado["dni"]),
                          validar_correo_empleado(empleado["correo_electronico"]),validar_correo_personal(empleado["correo_personal"])
                          ,validar_fecha(empleado["fecha_nacimiento"])]
    
    for condicion,motivo in lista_validaciones:
        if not condicion:
            break
    return (condicion,motivo)