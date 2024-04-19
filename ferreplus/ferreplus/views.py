from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.template import loader
import os

def inicio(request):
    # Cargar la plantilla utilizando get_template
    template = loader.get_template('pagina_principal.html')

    # Los datos que se pasan a la plantilla
    context = {
        'nombre': 'Mundo',
    }

    # Renderizar la plantilla con los datos proporcionados
    rendered_template = template.render(context)

    # Devolver la plantilla renderizada como una respuesta HTTP
    return HttpResponse(rendered_template)
