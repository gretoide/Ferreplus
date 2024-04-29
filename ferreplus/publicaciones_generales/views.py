from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.template import loader

def intercambio(request):
    return render(request,"vista_intercambio.html")
