from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.PositiveIntegerField()  # Valor predeterminado de ejemplo
    email = models.EmailField()  # Valor predeterminado de ejemplo
    fecha_nacimiento = models.DateField()  # Valor predeterminado de ejemplo

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
