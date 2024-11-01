from django import forms
from app.empresa.models import Empresa

class empresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre','direccion','telefono','sector']