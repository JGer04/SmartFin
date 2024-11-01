from django import forms
from app.empresa.models import Empresa

class empresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre','direccion','telefono','sector']

        labels = {
            'nombre':'Nombre',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'sector':'Sector',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la empresa'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección de la empresa'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono de la empresa'}),
            'sector': forms.TextInput(attrs={'placeholder': 'Sector de la empresa'}),
            
        }