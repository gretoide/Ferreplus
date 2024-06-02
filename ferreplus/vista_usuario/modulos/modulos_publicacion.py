from vista_usuario.models import Publicacion, Imagen, User, Sucursal
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

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

# ---------------------------------------- Editar publicación ---------------------------------------------

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

def validar_cantidad_imagenes(publicacion, nuevas_imagenes, imagenes_a_eliminar):

    imagenes_actuales = publicacion.imagenes.count()
    nuevas_imagenes_count = len(nuevas_imagenes)
    imagenes_a_eliminar_count = len(imagenes_a_eliminar)
    imagenes_finales_count = imagenes_actuales - imagenes_a_eliminar_count + nuevas_imagenes_count

    return 1 <= imagenes_finales_count <= 5

def guardar_publicacion(form_publicacion, imagenes_a_eliminar, nuevas_imagenes):
    try:
        publicacion = form_publicacion.save()
        eliminar_imagenes(publicacion, imagenes_a_eliminar)
        agregar_nuevas_imagenes(publicacion, nuevas_imagenes)
        return publicacion
    except ValidationError as e: # type: ignore
        error = '; '.join(str(v[0]) for v in e.message_dict.values())
        raise ValueError(error)

def eliminar_imagenes(publicacion, imagenes_a_eliminar):
    publicacion.imagenes.filter(pk__in=imagenes_a_eliminar).delete()

def agregar_nuevas_imagenes(publicacion, nuevas_imagenes):
    nuevas_instancias_imagen = [Imagen(imagen=imagen) for imagen in nuevas_imagenes]
    Imagen.objects.bulk_create(nuevas_instancias_imagen)
    publicacion.imagenes.add(*nuevas_instancias_imagen)

def render_editar_publicacion(request, form_publicacion, publicacion):
    return render(request, 'vista_usuario/editar_publicacion.html', {
        'form_publicacion': form_publicacion,
        'publicacion': publicacion,
        'sucursales': Sucursal.objects.all()
    })

def render_con_error(request, form_publicacion, publicacion, error):
    return render(request, 'vista_usuario/editar_publicacion.html', {
        'form_publicacion': form_publicacion,
        'publicacion': publicacion,
        'sucursales': Sucursal.objects.all(),
        'error': error
    })