from django.http import HttpResponse
from datetime import datetime
import re

def validar_dni(dni):
    condicion = True
    motivo = ""
    try:
        dni = int(dni)
        if len(str(dni)) != 8:
            condicion = False
            motivo = "Formato de DNI invalido"
    except:
        condicion = False
        motivo = "Se debe ingresa digitos en el campo DNI"
    return(condicion,motivo)


def validar_correo(correo):
    condicion = True
    motivo = ""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Verificar si el correo coincide con el patrón
    if not validar_espacio_blanco(correo) or not re.match(patron, correo):
        condicion = False
        motivo = "Formato invalido para correo"
    #chequear si deberia saber si mail existe o no
    return(condicion,motivo)

def validar_espacio_blanco(cadena):
    condicion = True
    if any(i.isspace() for i in cadena):
        condicion = False
    return condicion



def validar_contraseña(contraseña):
    condicion = True
    motivo = ""

    if not validar_espacio_blanco(contraseña):
        condicion = False
        motivo = "La contraseña no puede contener espacios en blanco"
    
    if len(contraseña) < 6:
        motivo = "La contraseña debe contener al menos 6 caracteres"
        condicion = False 
    
    if not re.search(r"[A-Z]", contraseña) or condicion:
        motivo = "La contraseña debe contener al menos una letra mayúscula"
        condicion = False
    if not re.search(r"\d", contraseña) or condicion:
        
        motivo = "La contraseña debe contener al menos un número"
        motivo = False
    
    return(condicion,motivo)

def validar_confirmacion(contraseña,contraseña2):
    condicion = True
    motivo = ""
    if not validar_espacio_blanco(contraseña2):
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

def validar_nombre_usuario(nombre):
    condicion = True
    motivo = ""
    patron = r'^[a-zA-Z]+$'
    
    # Verificar si la cadena coincide con el patrón
    if not validar_espacio_blanco(nombre) or not re.match(patron, nombre):
        condicion = False
        motivo = "Formato invalido para nombre de usuario"
    return (condicion,motivo)

def verificar(usuario):
    lista_validaciones = [validar_nombre_usuario(usuario["nombre_completo"]),validar_dni(usuario["dni"]),validar_correo(usuario["correo_electronico"]),
                       validar_contraseña(usuario["contraseña"]),validar_confirmacion(usuario["contraseña"],usuario["confirmar_contraseña"]),validar_fecha(usuario["fecha_nacimiento"])]
    for condicion,motivo in lista_validaciones:
        if not condicion:
            break
    return (condicion,motivo)