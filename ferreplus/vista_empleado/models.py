from django.db import models
from vista_administrador.models import Sucursal
from vista_usuario.models import User
# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    stock = models.IntegerField()

class Pedido(models.Model):
    codigo = models.IntegerField()
    productos = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    comprador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)