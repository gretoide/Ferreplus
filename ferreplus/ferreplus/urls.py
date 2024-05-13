from django.contrib import admin
from django.urls import path, include
from vista_usuario import views as user_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from vista_empleado.views import pagina_empleado

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name="inicio"),
    # Incluye las vistas exclusivas de usuario sin tener que repetir todo
    path('', include('vista_usuario.urls')),
    path('', include('vista_empleado.urls')),
    path('', include('vista_administrador.urls')),
    path('logout/', user_views.cerrar_sesion, name='cerrar_sesion'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)