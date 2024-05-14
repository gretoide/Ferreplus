from django.urls import path
from vista_administrador import views as  admin_view

urlpatterns = [
    path('administrador/', admin_view.inicio_admin, name= "inicio-admin"),
    path('agregar-sucursal/',admin_view.agregar_sucursal, name='agregar-sucursal'),
    path('ver-sucursales/',admin_view.ver_sucursales, name='ver-sucursales'),
    path('detalle-sucursal/<str:sucursal_id>/',admin_view.detalle_sucursal,name='detalle-sucursal'),
    path('cargar-empleado/',admin_view.cargar_empleado,name='cargar-empleado'),
    path('eliminar-sucursal/<str:sucursal_id>/',admin_view.eliminar_sucursal,name='eliminar-sucursal')
    ]
