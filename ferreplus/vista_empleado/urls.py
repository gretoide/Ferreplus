from django.urls import path
from . import views as empleado_views

urlpatterns = [
    path('empleado/',empleado_views.pagina_empleado, name='inicio_emp'),


]