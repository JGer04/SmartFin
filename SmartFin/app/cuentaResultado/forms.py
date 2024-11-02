from django import forms
from app.cuentaResultado.models import CuentaResultado

class CuentaResultadoForm(forms.ModelForm):
    class Meta:
        model = CuentaResultado
        fields = ['codigo','nombre','monto']
        labels = {
            'codigo':'Código',
            'nombre':'Nombre',
            'monto':'Monto'
        }

        widgets = {
            'codigo':forms.TextInput(attrs={'placeholder':'Código de la cuenta'}),
            'nombre':forms.TextInput(attrs={'placeholder':'Nombre de la cuenta'}),
            'monto':forms.NumberInput(attrs={'placeholder':'Monto de la cuenta'})
        }

class ExcelUploadForm(forms.Form):
    archivo_excel = forms.FileField(label="Selecciona el archivo Excel")