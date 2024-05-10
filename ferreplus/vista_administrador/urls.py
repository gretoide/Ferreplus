from django.urls import path
from . import views as admin_views

urlpatterns = [
    path('administrador/',admin_views.pagina_administrador, name='inicio_admin'),


]