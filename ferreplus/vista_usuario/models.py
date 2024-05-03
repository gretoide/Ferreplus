from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from datetime import date



class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
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
    
    #horario = models.CharField(max_length=100)
    #autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Asumiendo que Usuario es tu modelo de usuario

class Imagen(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes_publicaciones/')  # Asegúrate de tener Pillow instalado para manejar imágenes
