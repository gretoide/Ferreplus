from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.template import loader
from .modulos import modulos_sesion
import os



def inicio(request):
    
    return render(request,"pagina_inicio.html",{})
