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
    id_usuario = models.CharField(max_length=2, primary_key=True)  # CHAR(2)
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
    id_opcion = models.CharField(max_length=3, primary_key=True)  # CHAR(3)
    des_opcion = models.CharField(max_length=30)  # VARCHAR(30)
    num_form = models.IntegerField()  # INTEGER

    class Meta:
        managed = True
        db_table = 'optionForm'

    def __str__(self):
        return self.des_opcion


class AccesoUsuario(models.Model):
    id_opcion = models.ForeignKey(OpcionForm, on_delete=models.CASCADE)  # FK hacia OpcionForm
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # FK hacia Usuario

    class Meta:
        managed = True
        db_table = 'accesoUsuario'
        unique_together = ('id_opcion', 'id_usuario')  # Llave compuesta

    def __str__(self):
        return f"{self.id_usuario} - {self.id_opcion}"