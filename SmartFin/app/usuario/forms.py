from django import forms
from app.usuario.models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña",
        max_length=128
    )

    class Meta:
        model = Usuario
        fields = ['nom_usuario', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'nom_usuario': 'Nombre de Usuario',
        }
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Cifrar la contraseña
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario
