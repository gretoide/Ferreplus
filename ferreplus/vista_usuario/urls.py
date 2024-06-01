from django.urls import path
from . import views as user_views

urlpatterns = [
    path('registro/', user_views.registro, name= "registro"),
    path('crear-oferta/', user_views.crear_oferta, name="crear_oferta"),
    path('pagina-principal/', user_views.pagina_principal, name="pagina_principal"),
    path('subir-publicacion/', user_views.subir_publicacion, name="subir_publicacion"),
    path('restablecer-contraseña/', user_views.restablecerContraseña, name="restablecer_contraseña"),
    path('ingresar-codigo', user_views.ingresarCodigo, name="ingresar_codigo"),
    path('cambiar-contraseña', user_views.cambiarContraseña, name="cambiar_contraseña"),
    path('cambiar-contraseña-cliente', user_views.cambiarContraseñaCliente, name="cambiar_contraseña_cliente"),
    path('cambiar-contraseña-exito', user_views.cambiarContraseñaExito, name="cambiar_contraseña_exito"),
    path('mi-cuenta', user_views.mostrarPerfilCliente, name="mi_cuenta"),
    path('editar-perfil-cliente', user_views.editarPerfilCliente, name="editar_perfil_cliente"),
    path('mis-publicaciones', user_views.mis_publicaciones, name="mis_publicaciones"),
    path('publicacion/<int:pk>/editar/', user_views.editar_publicacion, name='editar_publicacion'),
    path('publicacion/<int:publicacion_id>/', user_views.detalle_publicacion, name='detalle_publicacion'),
    path('publicacion/<int:publicacion_id>/publicacion-existente', user_views.publicacion_existente, name='publicacion_existente'),
    path('publicacion/<int:publicacion_id>/oferta-privada', user_views.oferta_privada, name='oferta_privada'),
    path('solicitudes-de-intercambios/', user_views.mis_ofertas, name='mis_ofertas'),
]
