from datetime import datetime
from vista_usuario.models import Publicacion, User, Oferta, Intercambio, Sucursal
from django.shortcuts import get_object_or_404

def procesar_intercambio(oferta):
    # Obtener la sucursal de la oferta.base.sucursal
    sucursal_id = oferta.base.sucursal.id

    publicacion_base = get_object_or_404(Publicacion, id=oferta.base_id)
    publicacion_ofertada = get_object_or_404(Publicacion, id=oferta.oferta_id)

    publicacion_base.parte_oferta = True
    publicacion_ofertada.parte_oferta = True

    publicacion_base.save()
    publicacion_ofertada.save()
    
    # Crear el nuevo objeto Intercambio
    nuevo_intercambio = Intercambio.objects.create(
        base=oferta.base,
        ofer=oferta.oferta,
        hora=oferta.hora,
        fecha_intercambio=oferta.fecha_intercambio,
        sucursal=get_object_or_404(Sucursal, id=sucursal_id),
        estado=Intercambio.PENDIENTE,
        usuario_ausente=None
    )

    # Actualizar el estado de la oferta a 'aceptada' (si es necesario)
    oferta.estado = 'aceptada'
    oferta.save()

    # Eliminar la oferta después de aceptarla
    oferta.delete()

    return "Intercambio creado exitosamente.", True


def procesar_intercambio_rechazado(oferta):
    # Obtener la sucursal de la oferta.base.sucursal
    sucursal_id = oferta.base.sucursal.id

    publicacion_base = get_object_or_404(Publicacion, id=oferta.base_id)
    publicacion_ofertada = get_object_or_404(Publicacion, id=oferta.oferta_id)

    publicacion_base.parte_oferta = False
    publicacion_ofertada.parte_oferta = False

    publicacion_base.save()
    publicacion_ofertada.save()

    # Eliminar la oferta después de aceptarla
    oferta.delete()

    return "Se rechazó la oferta exitosamente.", True

def eliminar_ofertas_relacionadas(oferta_aceptada):
    # Obtener todas las ofertas relacionadas con la misma publicacion_base y publicacion_oferta
    ofertas_base_relacionadas = Oferta.objects.filter(base=oferta_aceptada.base).exclude(pk=oferta_aceptada.pk)
    ofertas_oferta_relacionadas = Oferta.objects.filter(oferta=oferta_aceptada.oferta).exclude(pk=oferta_aceptada.pk)

    # Volver a poner públicas las publicaciones ofertadas relacionadas con la publicacion_base
    for oferta in ofertas_base_relacionadas:
        publicacion_ofertada = get_object_or_404(Publicacion, id=oferta.oferta_id)
        publicacion_ofertada.parte_oferta = False
        publicacion_ofertada.save()

    # Eliminar las ofertas relacionadas con la publicacion_base
    ofertas_base_relacionadas.delete()

    # Eliminar las ofertas relacionadas con la publicacion_oferta
    ofertas_oferta_relacionadas.delete()
