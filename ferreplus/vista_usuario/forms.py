from django import forms
from .models import Publicacion
from django.core.validators import MaxValueValidator

class PublicacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'required': True})
        self.fields['estado'].widget.attrs.update({'required': True})
        self.fields['categoria'].widget.attrs.update({'required': True})
        self.fields['descripcion'].widget.attrs.update({'required': True})

    class Meta:
        model = Publicacion
        fields = ['titulo', 'estado', 'categoria', 'sucursal', 'descripcion']