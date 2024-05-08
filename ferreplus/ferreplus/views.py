from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, user_logged_in
from vista_usuario.models import User


def inicio(request):
    if request.method == "POST":
        correo_electronico = request.POST["correo_electronico"]
        contrasena = request.POST["contraseña"]
        mensaje_error = "Correo electrónico o contraseña inválidos."

        try:
            user = User.objects.get(email=correo_electronico)
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
                    return redirect('pagina_principal')  
            else:
                mensaje_error = "Correo electrónico o contraseña inválidos."
        
        return render(request, "pagina_inicio.html", {"aviso": mensaje_error})

    else:
        return render(request, "pagina_inicio.html")

