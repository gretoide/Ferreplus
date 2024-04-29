from django.shortcuts import render

def registro(request):
    if request.method == "POST":
        #Obtengo usuario si el metodo fue un post
        usuario = request.POST.dict()
        #sigue con validacion de campos

    return render(request,"registro_usuario.html")

# Create your views here.
