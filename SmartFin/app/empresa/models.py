from django.db import models

# Create your models here.

class Empresa(models.Model):
    idEmpresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'empresa'

    def __str__(self):
        return self.nombre
