from vista_usuario.models import Publicacion, Imagen

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


def crear_publicacion(datos_publicacion, imagenes):

    # Crear la nueva publicación
    nueva_publicacion = Publicacion.objects.create(
        titulo=datos_publicacion.get('titulo'),
        estado=datos_publicacion.get('estado'),
        categoria=datos_publicacion.get('categoria'),
        sucursal=datos_publicacion.get('sucursal'),
        descripcion=datos_publicacion.get('descripcion')
    )

    nueva_publicacion.save()

    # Guardar las imágenes asociadas a la publicación
    for imagen_file in imagenes:
        imagen = Imagen(publicacion=nueva_publicacion, imagen=imagen_file)
        imagen.save()

