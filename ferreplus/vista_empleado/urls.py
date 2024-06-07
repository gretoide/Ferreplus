from django.urls import path
from . import views as empleado_views

urlpatterns = [
    path('empleado/',empleado_views.pagina_empleado, name='inicio_emp'),
    path('intercambios-pendientes/', empleado_views.listar_intercambios_pendientes, name='intercambios-pendientes'),
    path('intercambio-realizado/<str:intercambio_id>/',empleado_views.aceptarIntercambio,name='aceptar-intercambio'),
    path('intercambio-cancelado/<str:intercambio_id>/',empleado_views.cancelarIntercambio,name='cancelar-intercambio'),
    path('intercambio-ausente/<str:intercambio_id>/', empleado_views.intercambio_ausente, name='ausentar-intercambio'),
    path('marcado-ausente/<str:usuario_id>/<str:intercambio_id>/',empleado_views.marcado_ausente, name ='marcar-ausente'),
    path('menu-pedidos', empleado_views.mostrarMenuPedidos, name='menu_pedidos'),
    path('menu-productos', empleado_views.mostrarMenuProductos, name='menu_productos'),
    path('menu-productos/agregar-producto', empleado_views.agregarProducto, name='agregar_producto')
]


