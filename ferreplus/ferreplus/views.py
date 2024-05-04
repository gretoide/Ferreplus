from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from .modulos import modulos_registro
from vista_usuario.models import User
import os



def inicio(request):
    if request.method == "POST":
        correo_electronico = request.POST["correo_electronico"]
        contrasena = request.POST["contraseña"]

        usuario = authenticate(request=request, username=correo_electronico, password=contrasena)

        if usuario is not None:
            login(request, usuario)
            return redirect("pagina-principal")
        else:
            mensaje_error = "Correo electrónico o contraseña inválidos."
            return render(request, "pagina_inicio.html", {"aviso": mensaje_error})

    else:
        return render(request, "pagina_inicio.html")



