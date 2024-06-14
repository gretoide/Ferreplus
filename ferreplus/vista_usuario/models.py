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
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    es_privada = models.BooleanField(default=False)
    parte_oferta = models.BooleanField(default=False)
    imagenes = models.ManyToManyField(
        'Imagen',
        related_name='publicaciones',
    )  # Relación ManyToMany con Imagen

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')

    def __str__(self):
        return os.path.basename(self.imagen.name)



class Oferta(models.Model):
    PENDIENTE = 'Esperando respuesta'
    RECHAZADO = 'Rechazado'
    ACEPTADO = 'Aceptado'

    ESTADOS_CHOICES = [
        (PENDIENTE, 'Esperando respuesta'),
        (RECHAZADO, 'Rechazado'),
        (ACEPTADO, 'Aceptado'),
    ]

    base = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='ofertas_como_base')
    oferta = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='ofertas_como_oferta')
    hora = models.TimeField()
    fecha_intercambio = models.DateField()
    usuario_ofertante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ofertas_hechas')
    usuario_recibe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ofertas_recibidas_oferta')
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default=PENDIENTE)

    def __str__(self):
        return f'Oferta de {self.usuario_ofertante} a {self.usuario_recibe} para {self.base}'

    class Meta:
        ordering = ['fecha_intercambio', 'hora']

class Intercambio(models.Model):
    
    REALIZADO = 'REALIZADO'
    CANCELADO = 'CANCELADO'
    CANCELADO_AUSENTE = 'CANCELADO_AUSENTE'
    PENDIENTE = 'PENDIENTE'

    ESTADOS_CHOICES = [
        (REALIZADO, 'REALIZADO'),
        (CANCELADO, 'CANCELADO'),
        (CANCELADO_AUSENTE, 'CANCELADO_AUSENTE'),
        (PENDIENTE, 'PENDIENTE')
    ]

    base = models.ForeignKey(Publicacion, related_name='base_intercambios', on_delete=models.SET_NULL, null=True)
    ofer = models.ForeignKey(Publicacion, related_name='oferta_intercambios', on_delete=models.SET_NULL, null=True)
    hora = models.TimeField()
    fecha_intercambio = models.DateField(null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default=PENDIENTE)
    usuario_ausente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
