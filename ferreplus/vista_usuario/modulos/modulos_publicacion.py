from datetime import datetime
import re
from vista_usuario.models import Usuario, Publicacion, Imagen

def verificar_publicacion(publicacion):
    # Lista para almacenar los mensajes de error
    mensajes_error = []

    # Verificar que se hayan proporcionado todos los campos requeridos
    if not publicacion.get("titulo"):
        mensajes_error.append("El campo 'Título' es obligatorio.")

    if not publicacion.get("estado"):
        mensajes_error.append("El campo 'Estado del producto' es obligatorio.")

    if not publicacion.get("categoria"):
        mensajes_error.append("El campo 'Categoría' es obligatorio.")

    if not publicacion.get("sucursal"):
        mensajes_error.append("El campo 'Sucursal' es obligatorio.")

    if not publicacion.get("descripcion"):
        mensajes_error.append("El campo 'Descripción' es obligatorio.")

    # Si hay mensajes de error, se retorna False con la lista de mensajes
    if mensajes_error:
        return False, mensajes_error
    else:
        # Si no hay mensajes de error, se retorna True con un mensaje vacío
        return True, ""

