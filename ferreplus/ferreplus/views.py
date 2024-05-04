from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from .modulos import modulos_registro
from vista_usuario.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import os



def inicio(request):
    if request.method == "POST":
        correo_electronico = request.POST["correo_electronico"]
        contrasena = request.POST["contraseña"]


        try:
            user = User.objects.get(email=correo_electronico)
        except User.DoesNotExist:
            user = None
        
        if user:
            login(request, user)
            return redirect("pagina-principal")
        else:
            mensaje_error = "Correo electrónico o contraseña inválidos."
            return render(request, "pagina_inicio.html", {"aviso": mensaje_error})

    else:
        return render(request, "pagina_inicio.html")



