from django.urls import path
from . import views as empleado_views

urlpatterns = [
    path('empleado/',empleado_views.pagina_empleado, name='inicio_emp'),
    path('intercambios-pendientes/', empleado_views.listar_intercambios_pendientes, name='intercambios-pendientes'),
]


