from django.contrib import admin
from django.urls import path, include
from vista_usuario import views as user_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name="inicio"),
    # Incluye las vistas exclusivas de usuario sin tener que repetir todo
    path('', include('vista_usuario.urls')),
    path('',include('vista_administrador.urls'))
]
