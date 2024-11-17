from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser # Se importan las clases BaseUserManager y AbstractBaseUser de django para manejar la creación de usuarios

class UsuarioManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        return self.create_user( password=password, **extra_fields)

class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)  # CHAR(2)
    nom_usuario = models.CharField(unique=True ,max_length=30)  # VARCHAR(30)
    password = models.CharField(max_length=128)  # CHAR(5)
    
    objects = UsuarioManager()
    USERNAME_FIELD = 'nom_usuario'
    REQUIRED_FIELDS = ['password']

    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return self.nom_usuario


class OpcionForm(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('ADM', 'Administrador'),
        ('AFE', 'Analista Financiero del Área de Energía'),
        ('AFM', 'Analista Financiero del Área de Minería'),
    ]
    id_opcion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=30)
    tipo_usuario = models.CharField(max_length=3, choices=TIPO_USUARIO_CHOICES, default='ADM')

    def __str__(self):
        return self.descripcion


class AccesoUsuario(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="accesos")
    id_opcion = models.ForeignKey(OpcionForm, on_delete=models.CASCADE, related_name="accesos")

    class Meta:
        unique_together = ('id_usuario', 'id_opcion')
        db_table = 'acceso_usuario'

    def __str__(self):
        return f"{self.id_usuario} -> {self.id_opcion}"


