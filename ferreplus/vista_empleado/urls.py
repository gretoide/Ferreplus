from django.urls import path
from . import views as empleado_views

urlpatterns = [
    path('empleado/',empleado_views.pagina_empleado, name='inicio_emp'),
    path('intercambios-pendientes/', empleado_views.listar_intercambios_pendientes, name='intercambios-pendientes'),
    path('intercambio-realizado/<str:intercambio_id>/',empleado_views.aceptarIntercambio,name='aceptar-intercambio'),
    path('intercambio-cancelado/<str:intercambio_id>/',empleado_views.cancelarIntercambio,name='cancelar-intercambio'),
    path('intercambio-ausente/<int:intercambio_id>/', empleado_views.intercambio_ausente, name='ausentar-intercambio'),
]


