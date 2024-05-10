
from vista_usuario.models import User
from django.http import HttpResponse

def direccion(user):
    direc = "pagina_principal"
    if user.is_staff:
        direc = "inicio_emp"
    elif user.is_superuser:
        direc = "inicio_admin"
    return direc



def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponse("No tienes permiso para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponse("No tienes permiso para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return wrapper


def normal_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_staff or request.user.is_superuser:
            return HttpResponse("No tienes permiso para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return wrapper
