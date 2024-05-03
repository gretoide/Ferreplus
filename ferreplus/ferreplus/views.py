from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from .modulos import modulos_registro
from vista_usuario.models import Usuario
import os


def inicio(request):
    if request.method == "POST":
        correo_electronico = request.POST.get("correo_electronico")
        contrasenia = request.POST.get("contraseña")
        context = {"aviso": "Correo electrónico o contraseña inválidos"}
        
        try:
            usuario = Usuario.objects.get(email=correo_electronico)
        except Usuario.DoesNotExist:
            return render(request, "pagina_inicio.html", context)

        if usuario.contrasenia == contrasenia:
            login(request, usuario) #Falla aca
            return redirect("pagina-principal")
        else:
            return render(request, "pagina_inicio.html", context)

    else:
        return render(request, "pagina_inicio.html")




