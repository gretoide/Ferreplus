from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import AbstractUser, PermissionsMixin ,UserManager
from django.db import models
from django.utils import timezone
from vista_administrador.models import Sucursal
import os

class User(AbstractUser):
    # ... otros campos personalizados que puedas necesitar ...
    email = models.EmailField(blank=True,default="")
    dni = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    cuil = models.CharField(max_length=13,default="")
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL,default="", null=True)
    
    

class Publicacion(models.Model):

    NUEVO = 'nuevo'
    USADO = 'usado'

    ESTADOS_CHOICES = [
        (NUEVO, 'Nuevo'),
        (USADO, 'Usado'),
    ]

    CATEGORIA_CHOICES = [
        ('Electricidad', 'Electricidad'),
        ('Ferretería general', 'Ferretería general'),
        ('Construcción', 'Construcción'),
        ('Herramientas', 'Herramientas'),
        ('Jardinería', 'Jardinería'),
        ('Protección personal', 'Protección personal'),
    ]

    titulo = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADOS_CHOICES, default=NUEVO)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    sucursal = models.CharField(max_length=100)  # Esto puede cambiarse a ForeignKey si tienes una tabla de sucursales
    descripcion = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagenes = models.ManyToManyField('Imagen', related_name='publicaciones')  # Relación ManyToMany con Imagen

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')

    def __str__(self):
        return os.path.basename(self.imagen.name)