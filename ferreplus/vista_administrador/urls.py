from django.urls import path
from . import views as user_views
from vista_administrador import views as  admin_view

urlpatterns = [
    #path('registro/', user_views.registro, name= "registro"),
    path('inicio-administrador/', admin_view.inicio_admin, name= "inicio"),
    path('agregar-sucursal/',admin_view.agregar_sucursal, name='agregar-sucursal')
]
