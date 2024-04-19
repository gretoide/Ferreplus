from django.http import HttpResponse
import os

# Declaramos una de las vistas de nuestra web, luego hay que agregarla a las urls.
def inicio(request):

    return HttpResponse("Esta sería la página de inicio !!!")