from vista_usuario.models import Publicacion, Imagen

def crear_publicacion(datos_publicacion, imagenes):
    """
    Crea una nueva publicación a partir de los datos proporcionados.
    Retorna un booleano que indica si la creación fue exitosa y un mensaje de aviso o error.
    """
    try:
        nueva_publicacion = Publicacion.objects.create(
            titulo=datos_publicacion.get('titulo'),
            estado=datos_publicacion.get('estado'),
            categoria=datos_publicacion.get('categoria'),
            sucursal=datos_publicacion.get('sucursal'),
            descripcion=datos_publicacion.get('descripcion')
        )

        # Guardar las imágenes asociadas a la publicación
        for imagen_file in imagenes:
            imagen = Imagen(publicacion=nueva_publicacion, imagen=imagen_file)
            imagen.save()

        return True, "Publicación creada con éxito."
    except Exception as e:
        return False, str(e)

def verificar_y_crear_publicacion(datos_publicacion, imagenes):
    """
    Verifica y crea una nueva publicación a partir de los datos proporcionados.
    Retorna un booleano que indica si la creación fue exitosa y un mensaje de aviso o error.
    """
    # Verificar la publicación
    condicion, motivo = verificar_publicacion(datos_publicacion)
    
    if condicion:
        # Crear la publicación
        exito, mensaje = crear_publicacion(datos_publicacion, imagenes)
        return exito, mensaje
    else:
        return False, motivo

def verificar_publicacion(publicacion):
    """
    Verifica que se hayan proporcionado todos los campos requeridos para una publicación.
    Retorna un booleano que indica si la verificación fue exitosa y una lista de mensajes de error.
    """
    mensajes_error = []

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

    if mensajes_error:
        return False, mensajes_error
    else:
        return True, ""
