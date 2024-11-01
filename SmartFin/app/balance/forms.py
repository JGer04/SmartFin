from django import forms
from app.balance.models import Balance

class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['nombre','idEmpresa','fecha']
        labels = {
            'nombre':'Ingrese el nombre',
            'idEmpresa': 'Seleccione una empresa',
            'fecha': 'Seleccione la fecha del balance',
        }

        widgets = {
            'idEmpresa': forms.Select(),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del balance'}),
            'fecha': forms.DateInput(attrs={'placeholder': 'Fecha (YYYY-MM-DD)', 'type': 'date'}),
        }