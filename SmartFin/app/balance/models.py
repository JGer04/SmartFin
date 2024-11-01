from django.db import models
from app.empresa.models import *
# Create your models here.

class Balance(models.Model):
    idBalance = models.AutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    fecha = models.DateField(default="")

    class Meta:
        managed = True
        db_table = 'balance'

    def __str__(self):
        return self.nombre
