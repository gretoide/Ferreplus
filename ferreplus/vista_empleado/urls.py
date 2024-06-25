from django.urls import path
from . import views as empleado_views

urlpatterns = [
    path('empleado/', empleado_views.pagina_empleado, name='inicio_emp'),
    path('intercambios-pendientes/', empleado_views.listar_intercambios_pendientes, name='intercambios-pendientes'),
    path('intercambio-realizado/<str:intercambio_id>/', empleado_views.marcado_realizado, name='aceptar-intercambio'),
    path('intercambio-cancelado/<str:intercambio_id>/', empleado_views.marcado_cancelado, name='cancelar-intercambio'),
    path('intercambio-ausente/<str:intercambio_id>/', empleado_views.intercambio_ausente, name='ausentar-intercambio'),
    path('marcado-ausente/<str:usuario_id>/<str:intercambio_id>/', empleado_views.marcado_ausente, name='marcar-ausente'),
    path('agregar-ganancia/<str:intercambio_id>/', empleado_views.agregar_ganancia, name='agregar-ganancia'),
]
