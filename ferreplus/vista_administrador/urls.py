from django.urls import path
from . import views as user_views
from vista_administrador import views as  admin_view

urlpatterns = [
    #path('registro/', user_views.registro, name= "registro"),
    path('administrador//', admin_view.inicio_admin, name= "inicio-admin"),
    path('agregar-sucursal/',admin_view.agregar_sucursal, name='agregar-sucursal'),
    path('ver-sucursales/',admin_view.ver_sucursales, name='ver-sucursales'),
    path('detalle-sucursal/<str:sucursal_id>/',admin_view.detalle_sucursal,name='detalle_sucursal')
    ]
