from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import AbstractUser, PermissionsMixin ,UserManager
from django.db import models
from django.utils import timezone
from vista_administrador.models import Sucursal
from django.core.validators import MaxValueValidator
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
    es_privada = models.BooleanField(default=False)
    parte_oferta = models.BooleanField(default=False)
    imagenes = models.ManyToManyField(
        'Imagen',
        related_name='publicaciones',
        validators=[MaxValueValidator(5, 'Solo se permiten hasta 5 imágenes.')]
    )  # Relación ManyToMany con Imagen

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')

    def __str__(self):
        return os.path.basename(self.imagen.name)



class Oferta(models.Model):
    base = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='ofertas_como_base')
    oferta = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='ofertas_como_oferta')
    hora = models.TimeField() 
    fecha_intercambio = models.DateField()

class Intercambio(models.Model):
    
    REALIZADO = 'realizado'
    CANCELADO = 'cancelado'
    CANCELADO_AUSENTE = 'cancelado_ausente'
    PENDIENTE = 'pendiente'

    ESTADOS_CHOICES = [
        (REALIZADO, 'Intercambio Realizado'),
        (CANCELADO, 'Intercambio Cancelado'),
        (CANCELADO_AUSENTE, 'Cancelado por Ausencia'),
        (PENDIENTE, 'Intercambio Pendiente')
    ]


    base = models.ForeignKey(Publicacion, related_name='base_intercambios', on_delete=models.SET_NULL, null=True)
    hora = models.TimeField() 
    fecha_intercambio = models.DateField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    ofer = models.ForeignKey(Publicacion, related_name='oferta_intercambios', on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default=PENDIENTE)
    usuario_ausente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
