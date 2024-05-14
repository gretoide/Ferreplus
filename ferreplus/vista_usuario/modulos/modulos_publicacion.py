from vista_usuario.models import Publicacion, Imagen, User

def verificar_campos(datos_publicacion):
    """
    Verifica si todos los campos necesarios están presentes en los datos de la publicación.
    Retorna un booleano que indica si la verificación fue exitosa y un mensaje de error en caso contrario.
    """
    campos_requeridos = ["titulo", "estado", "categoria", "sucursal", "descripcion"]
    
    for campo in campos_requeridos:
        valor_campo = datos_publicacion.get(campo)
        if not valor_campo or valor_campo.strip().lower() == "seleccionar":
            return False, "Debe completar todos los campos."
    return True, None


def crear_publicacion(datos_publicacion, user, imagenes):
    # Crear la nueva publicación
    nueva_publicacion = Publicacion.objects.create(
        titulo=datos_publicacion.get('titulo'),
        estado=datos_publicacion.get('estado'),
        categoria=datos_publicacion.get('categoria'),
        sucursal=datos_publicacion.get('sucursal'),
        descripcion=datos_publicacion.get('descripcion'),
        autor=user
    )

    # Guardar la nueva publicación en la base de datos
    nueva_publicacion.save()

    # Asociar las imágenes con la publicación
    for imagen in imagenes:
        imagen_obj = Imagen.objects.create(imagen=imagen)
        nueva_publicacion.imagenes.add(imagen_obj)

    # Guardar la asociación en la base de datos
    nueva_publicacion.save()

def editar_publicacion(publicacion, datos_publicacion, nuevas_imagenes):
    # Verificar si agregar las nuevas imágenes excede el límite de 5
    if publicacion.imagenes.count() + len(nuevas_imagenes) > 5:
        return False, "No se pueden agregar más de 5 imágenes a la publicación."
    
    # Actualizar los campos de la publicación existente
    publicacion.titulo = datos_publicacion.get('titulo')
    publicacion.estado = datos_publicacion.get('estado')
    publicacion.categoria = datos_publicacion.get('categoria')
    publicacion.sucursal = datos_publicacion.get('sucursal')
    publicacion.descripcion = datos_publicacion.get('descripcion')

    # Guardar los cambios en la base de datos
    publicacion.save()

    # Agregar las nuevas imágenes con la publicación
    for imagen in nuevas_imagenes:
        imagen_obj = Imagen.objects.create(imagen=imagen)
        publicacion.imagenes.add(imagen_obj)

    return True, "La publicación se ha actualizado correctamente."
