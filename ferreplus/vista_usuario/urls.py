from django.urls import path
from . import views as user_views

urlpatterns = [
    path('registro/', user_views.registro, name= "registro"),
    path('crear-oferta/', user_views.crear_oferta, name="crear_oferta"),
    path('pagina-principal/', user_views.pagina_principal, name="pagina_principal"),
    path('subir-publicacion/', user_views.subir_publicacion, name="subir_publicacion"),
    path('restablecer-contraseña/', user_views.restablecerContraseña, name="restablecer_contraseña"),
    path('ingresar-codigo/<str:email>', user_views.ingresarCodigo, name="ingresar_codigo"),
    path('cambiar-contraseña/<str:email>/<str:contraseña>', user_views.cambiarContraseña, name="cambiar_contraseña"),
    path('cambiar-contraseña-exito', user_views.cambiarContraseñaExito, name="cambiar_contraseña_exito"),
]
