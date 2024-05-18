from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, user_logged_in
from vista_usuario.models import User
from .modulos import modulos_inicio_sesion
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

@csrf_protect
@never_cache
def inicio(request):
    try:
        if request.method == "POST":
            correo_electronico = request.POST["correo_electronico"]
            contrasena = request.POST["contraseña"]
            mensaje_error = "Correo electrónico o contraseña inválidos."

            try:
                user = User.objects.get(username=correo_electronico)
            except User.DoesNotExist:
                user = None
            
            if user:
                if user.check_password(contrasena):
                    # Autenticación exitosa
                    login(request, user)
                    next_page = request.GET.get('next')  
                    if next_page:
                        return redirect(next_page)
                    else:
                        return redirect(modulos_inicio_sesion.direccion(user))  
                else:
                    mensaje_error = "Correo electrónico o contraseña inválidos."
            
            return render(request, "pagina_inicio.html", {"aviso": mensaje_error})

        else:
            return render(request, "pagina_inicio.html")
    except Exception as e:
        return render(request, "pagina_inicio.html", {"error": str(e)})
