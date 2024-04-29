from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from .modulos import modulos_sesion
import os



def inicio(request):
    
    return render(request,"pagina_principal.html",{})

def registro(request):
    if request.method == "POST":
        #Obtengo usuario si el metodo fue un post
        usuario = request.POST.dict()
        print(usuario["fecha_nacimiento"])
        condicion,motivo = modulos_sesion.verificar_fecha(usuario["fecha_nacimiento"])
        if not condicion:    
            print(motivo)
        return redirect("vista_intercambio.html")


    return render(request,"registro_usuario.html")

def intercambio(request):
    return render(request,"vista_intercambio.html")

def crear_oferta(request):
    return render(request,"crear_oferta.html")
    