# ratios/forms.py
from django import forms
from .models import Seccion, SubSeccion, Razon

class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la Sección'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la sección'})
        }

class SubSeccionForm(forms.ModelForm):
    class Meta:
        model = SubSeccion
        fields = ['nombre', 'seccion']
        labels = {
            'nombre': 'Nombre de la SubSección',
            'seccion': 'Sección Principal'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la subsección'}),
            'seccion': forms.Select(attrs={'class': 'form-control'})
        }

class RazonForm(forms.ModelForm):
    class Meta:
        model = Razon
        fields = ['nombre', 'seccion', 'subseccion', 'valor']
        labels = {
            'nombre': 'Nombre de la Razón',
            'seccion': 'Sección',
            'subseccion': 'SubSección',
            'valor': 'Valor Numérico'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la razón'}),
            'seccion': forms.Select(attrs={'class': 'form-control'}),
            'subseccion': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor numérico del ratio'}),
        }
