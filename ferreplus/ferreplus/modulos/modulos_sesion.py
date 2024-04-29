from django.http import HttpResponse
from datetime import datetime

def verificar_dni(dni):
    condicion = True
    motivo = ""
    try:
        dni = int(dni)
        if len(str(dni)) != 11:
            condicion = False
            motivo = "Se debe ingresa digitos en el campo DNI"
    except:
        condicion = False
        motivo = "Se debe ingresa digitos en el campo DNI"
    return(condicion,motivo)

def verificar_correo(correo):
    condicion = True
    motivo = ""

    if not ("@" in correo) or correo.isspace():
        condicion = False
        motivo = "Fromato invalido para correo"
    #chequear si deberia saber si mail existe o no
    return(condicion,motivo)

def verificar_contraseña(contraseña):
    condicion = True
    motivo = ""
    
    
    return(condicion,motivo)

def verificar_confirmacion(contraseña,contraseña2):
    condicion = True
    motivo = ""
    if contraseña != contraseña2:
        condicion = False
        motivo = "Las contraseñas no coinciden"

    
    return(condicion,motivo)

def verificar_fecha(fecha):

    condicion = True
    motivo = ""
    mayoria_edad = 18
    fecha_actual = datetime.now().date()
    formato_string = "%Y-%m-%d"
    fecha = datetime.strptime(fecha,formato_string)
    """try:
        fecha = datetime.strptime(fecha,'%d/%m/%Y')
        edad = fecha_actual.year - fecha.year - ((fecha_actual.month, fecha_actual.day) < (fecha.month, fecha.day))
        if not edad >= mayoria_edad:
            condicion = False
            motivo = "Se debe ser mayor de edad para registrarse"
    except:
        condicion = False
        motivo = "El dato ingresado en la fecha es invalido" """

    
    


    return(condicion,motivo)

def verificar(usuario):
    if usuario["dni"] == "111":
        return (False,"Motivo: ")
    