from datetime import datetime
from vista_usuario.models import Publicacion, User, Oferta, Intercambio, Sucursal
from django.shortcuts import get_object_or_404

def procesar_intercambio(oferta):
    # Obtener la sucursal de la oferta.base.sucursal
    sucursal = oferta.base.sucursal
    
    # Crear el nuevo objeto Intercambio
    nuevo_intercambio = Intercambio.objects.create(
        base=oferta.base,
        hora=oferta.hora,
        fecha_intercambio=oferta.fecha_intercambio,
        sucursal=None,
        ofer=oferta.oferta,
        estado=Intercambio.PENDIENTE,
        usuario_ausente=None
    )

    # Actualizar el estado de la oferta a 'aceptada' (si es necesario)
    oferta.estado = 'aceptada'
    oferta.save()

    return "Intercambio creado exitosamente.", True