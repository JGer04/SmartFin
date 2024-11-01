from django import forms
from app.resultado.models import Resultado

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['nombre','idEmpresa','fecha']
        labels = {
            'nombre':'Ingrese el nombre',
            'idEmpresa': 'Seleccione una empresa',
            'fecha': 'Seleccione la fecha del E. Resultado',
        }

        widgets = {
            'idEmpresa': forms.Select(),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del E. Resultado'}),
            'fecha': forms.DateInput(attrs={'placeholder': 'Fecha (YYYY-MM-DD)', 'type': 'date'}),
        }