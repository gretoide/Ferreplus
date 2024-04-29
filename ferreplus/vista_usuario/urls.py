from django.urls import path
from . import views as user_views

urlpatterns = [
    path('registro/', user_views.registro, name= "registro"),
    path('crear-oferta/', user_views.crear_oferta, name="crear-oferta"),
    path('pagina-principal/', user_views.principal, name="intercambio"),
]