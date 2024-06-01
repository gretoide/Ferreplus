from vista_usuario.models import Publicacion, Imagen, User, Sucursal
from django.shortcuts import get_object_or_404

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

    sucursal_id = datos_publicacion.get('sucursal')

    # Crear la nueva publicación
    nueva_publicacion = Publicacion.objects.create(
        titulo=datos_publicacion.get('titulo'),
        estado=datos_publicacion.get('estado'),
        categoria=datos_publicacion.get('categoria'),
        sucursal = get_object_or_404(Sucursal, id=sucursal_id),
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

def editar_publicacion_modulo(publicacion, datos_publicacion, nuevas_imagenes, imagenes_existentes):
    # Eliminar las imágenes existentes que no se desean
    imagenes_a_eliminar = imagenes_existentes.exclude(imagen__in=nuevas_imagenes)
    for imagen in imagenes_a_eliminar:
        imagen.delete()

    # Actualizar los campos de la publicación
    publicacion.titulo = datos_publicacion.get('titulo')
    publicacion.estado = datos_publicacion.get('estado')
    publicacion.categoria = datos_publicacion.get('categoria')
    publicacion.sucursal = datos_publicacion.get('sucursal')
    publicacion.descripcion = datos_publicacion.get('descripcion')

    # Guardar las nuevas imágenes
    for nueva_imagen in nuevas_imagenes:
        # Crear la instancia de Imagen y guardarla en la base de datos
        imagen = Imagen.objects.create(imagen=nueva_imagen)
        # Agregar la imagen a la publicación
        publicacion.imagenes.add(imagen)

    publicacion.save()
    return True, "La publicación se ha editado correctamente."
