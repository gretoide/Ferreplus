from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.template import loader
import os

def inicio(request):
    return render(request,"pagina_principal.html")

def registro(request):

    return render(request,"registro_usuario.html")
