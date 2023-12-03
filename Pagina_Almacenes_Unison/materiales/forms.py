from django import forms

from .models import *

class FormularioMaterial(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre_articulo', 'precio_unitario', 'categoria', 'cantidad', 'imagen', 'descripcion', 'umbral', 'Origen']
        
class FormularioTomarProducto(forms.Form):
    cantidad_a_tomar = forms.IntegerField(label = 'Cantidad a tomar', widget = forms.NumberInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Seleccione la cantidad a tomar',
            'required': 'required',
        }
    ))

class FormularioAgregarProducto(forms.Form):
    cantidad_a_agregar = forms.IntegerField(min_value=1,label = 'Cantidad a agregar', widget = forms.NumberInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Seleccione la cantidad a agregar',
            'required': 'required',
        }
    ))

class FormularioAgregarAlCarrito(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label='Cantidad a agregar')
    
    