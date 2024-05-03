from django.http import HttpResponse
from datetime import datetime
import re
from vista_usuario.models import Usuario

def validar_dni(dni):
    condicion = True
    motivo = ""

    if validar_espacio_blanco(dni):
        condicion = False
        motivo = "El DNI no puede contener espacios en blanco"

    if len(dni) != 8 or not dni.isdigit():
        condicion = False
        motivo = "Formato de DNI inválido"

    try:
        dni = int(dni)
    except ValueError:
        condicion = False
        motivo = "Se deben ingresar solo dígitos en el campo DNI"
    else:
        try:
            usuario_existente = Usuario.objects.get(dni=dni)
            condicion = False
            motivo = "El DNI ingresado ya corresponde a un usuario"
        except Usuario.DoesNotExist:
            pass

    return condicion, motivo


def validar_correo(correo):
    condicion = True
    motivo = ""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Verificar si el correo coincide con el patrón y si no contiene espacios en blanco
    if validar_espacio_blanco(correo) or not re.match(patron, correo):
        condicion = False
        motivo = "Formato inválido para correo"
    else:
        try:
            # Verificar si el correo ya está en uso por otro usuario
            if Usuario.objects.filter(email=correo).exists():
                condicion = False
                motivo = "Correo electrónico ya en uso"
        except Exception as e:
            motivo = str(e)
            condicion = False

    return (condicion, motivo)
    

def validar_espacio_blanco(cadena):
    return any(i.isspace() for i in cadena)



def validar_contraseña(contraseña):
    condicion = True
    motivo = ""

    if validar_espacio_blanco(contraseña):
        condicion = False
        motivo = "La contraseña no puede contener espacios en blanco"
    
    if condicion and len(contraseña) < 6:
        motivo = "La contraseña debe contener al menos 6 caracteres"
        condicion = False 
    
    if condicion and not re.search(r"[A-Z]", contraseña) :
        motivo = "La contraseña debe contener al menos una letra mayúscula"
        condicion = False
    if  condicion and not re.search(r"\d", contraseña):
        
        motivo = "La contraseña debe contener al menos un número"
        condicion = False
    
    return(condicion,motivo)

def validar_confirmacion(contraseña,contraseña2):
    condicion = True
    motivo = ""
    if validar_espacio_blanco(contraseña2):
        condicion = False
        motivo = "La confirmacion no puede tener espacios en blanco"
    if not condicion or contraseña != contraseña2:
        condicion = False
        motivo = "Las contraseñas no coinciden"

    
    return(condicion,motivo)

def validar_fecha(fecha):
    condicion = True
    motivo = ""
    mayoria_edad = 18
    fecha_actual = datetime.now().date()
    

    try:
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        
        edad = fecha_actual.year - fecha.year - ((fecha_actual.month, fecha_actual.day) < (fecha.month, fecha.day))
        
        if not edad >= mayoria_edad:
            condicion = False
            motivo = "Se debe ser mayor de edad para registrarse"
    except:
        condicion = False
        motivo = "El dato ingresado en la fecha es invalido" 

    return (condicion, motivo)

def validar_nombre(nombre):
    condicion = True
    motivo = ""
    patron = r'^[a-zA-Z]+$'
    
    # Verificar si la cadena coincide con el patrón
    if validar_espacio_blanco(nombre) or not re.match(patron, nombre):
        condicion = False
        motivo = "Formato invalido para el campo nombre"
    return (condicion,motivo)

def validar_apellido(apellido):
    condicion = True
    motivo = ""
    patron = r'^[a-zA-Z]+$'
    
    # Verificar si la cadena coincide con el patrón
    if validar_espacio_blanco(apellido) or not re.match(patron, apellido):
        condicion = False
        motivo = "Formato invalido para el campo apellido"
    return (condicion,motivo)

def verificar(usuario):
    lista_validaciones = [validar_nombre(usuario["nombre"]),validar_apellido(usuario["apellido"]),validar_dni(usuario["dni"]),validar_correo(usuario["correo_electronico"]),
                       validar_contraseña(usuario["contraseña"]),validar_confirmacion(usuario["contraseña"],usuario["confirmar_contraseña"]),validar_fecha(usuario["fecha_nacimiento"])]
    for condicion,motivo in lista_validaciones:
        if not condicion:
            break
    return (condicion,motivo)