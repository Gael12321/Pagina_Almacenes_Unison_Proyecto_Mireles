from django import forms

from .models import *

class FormularioReporte(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['descripcion', 'estado']

class FormularioDetalleReporte(forms.ModelForm):
    class Meta:
        model = DetalleReporte
        fields = ['producto', 'cantidad']