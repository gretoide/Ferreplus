import django.forms as forms
from .models import Sucursal


class formularioSucursal(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion']
        labels = {'nombre': 'Nombre', 'direccion': 'Direccion'}
        widgets = {'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}), 'direccion': forms.TextInput(attrs={'class':'form-control','placeholder':'Direccion'})}
