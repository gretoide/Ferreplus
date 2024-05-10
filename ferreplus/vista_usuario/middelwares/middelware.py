from django.shortcuts import redirect
from django.urls import reverse

class NoBackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == reverse('cerrar_sesion') and request.user.is_authenticated:
            return redirect('inicio')  # Redirige a la página de inicio después de cerrar sesión
        return response
