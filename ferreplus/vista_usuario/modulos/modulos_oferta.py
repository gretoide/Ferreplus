from datetime import datetime, time
from vista_usuario.models import Publicacion, Imagen, User, Oferta
from django.shortcuts import get_object_or_404

def validar_fecha_encuentro(fecha_encuentro):
    fecha_encuentro_obj = datetime.strptime(fecha_encuentro, '%Y-%m-%d').date()
    if fecha_encuentro_obj < datetime.now().date():
        return False, 'La fecha del encuentro debe ser a partir del día actual.'
    return True, ''

def validar_hora_encuentro(hora_encuentro):
    hora_encuentro_obj = datetime.strptime(hora_encuentro, '%H:%M').time()
    hora_minima = time(8, 0)
    hora_maxima = time(18, 0)
    if hora_encuentro_obj < hora_minima or hora_encuentro_obj > hora_maxima:
        return False, 'El horario del encuentro debe ser entre las 8 a.m. y las 6 p.m.'
    return True, ''

def validar_categoria(categoria_base, categoria_ofertada):
    if categoria_base == categoria_ofertada:
        return True, ''
    else:
        return False, 'Los productos deben ser de la misma categoría.'

def procesar_oferta(publicacion_base, usuario, publicacion_id, fecha_encuentro, hora_encuentro):

    # Obtén la publicación seleccionada
    publicacion_seleccionada = get_object_or_404(Publicacion, id=publicacion_id)

    # Validar fecha del encuentro
    valido_fecha, mensaje_fecha = validar_fecha_encuentro(fecha_encuentro)
    if not valido_fecha:
        return mensaje_fecha, False

    # Validar hora del encuentro
    valido_hora, mensaje_hora = validar_hora_encuentro(hora_encuentro)
    if not valido_hora:
        return mensaje_hora, False
    
    # Validar que sean de la misma categoría
    valido_categoria, mensaje_categoria = validar_categoria(publicacion_base.categoria, publicacion_seleccionada.categoria)
    if not valido_categoria:
        return mensaje_categoria, False

    # Crear la oferta si todas las validaciones son exitosas
    if publicacion_id and fecha_encuentro and hora_encuentro:
        Oferta.objects.create(
            base=publicacion_base,
            oferta=publicacion_seleccionada,
            usuario_ofertante=usuario,
            usuario_recibe=publicacion_base.autor,
            fecha_intercambio=fecha_encuentro,
            hora=hora_encuentro
        )
        return '', True
    else:
        return 'Debe seleccionar una publicación para el intercambio, fecha y hora válidas.', False

def procesar_oferta_privada(publicacion_base, publicacion_nueva, fecha_encuentro, hora_encuentro):
    # Validar fecha del encuentro
    valido_fecha, mensaje_fecha = validar_fecha_encuentro(fecha_encuentro)
    if not valido_fecha:
        return mensaje_fecha, False

    # Validar hora del encuentro
    valido_hora, mensaje_hora = validar_hora_encuentro(hora_encuentro)
    if not valido_hora:
        return mensaje_hora, False

    if fecha_encuentro and hora_encuentro:
        # Obtén la publicación seleccionada
        publicacion_seleccionada = get_object_or_404(Publicacion, id=publicacion_nueva.id) # type: ignore

        # Crea una nueva oferta
        Oferta.objects.create(
            base=publicacion_base,
            oferta=publicacion_seleccionada,
            usuario_ofertante=publicacion_nueva.autor,
            usuario_recibe=publicacion_base.autor,
            fecha_intercambio=fecha_encuentro,
            hora=hora_encuentro
        )
        return '', True

    return 'Debe seleccionar una publicación para el intercambio.', False