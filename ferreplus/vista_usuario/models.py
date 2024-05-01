from django.core.exceptions import ValidationError
from django.db import models
from datetime import date


class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    dni = models.CharField(max_length= 8,primary_key=True, unique=True) 
    contrasenia = models.CharField(max_length=20,default='')
    email = models.EmailField(unique=True)  
    fecha_nacimiento = models.DateField()  

class Publicacion(models.Model):
    NUEVO = 'nuevo'
    USADO = 'usado'
    ESTADOS_CHOICES = [
        (NUEVO, 'Nuevo'),
        (USADO, 'Usado'),
    ]

    nombre_producto = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADOS_CHOICES, default=NUEVO)
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField()
    sucursal_a_retirar = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    # Una publicación está ligada a un usuario
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)
