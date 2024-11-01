from django.db import models
from app.resultado.models import *
# Create your models here.

class CuentaResultado(models.Model):
    idCuentaResultado = models.AutoField(primary_key=True)
    idResultado = models.ForeignKey(Resultado,related_name='cuentas', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=25, default="")
    nombre = models.CharField(max_length=50)
    monto = models.FloatField()

    class Meta:
        managed = True
        db_table = 'cuentaresultado'

    def __str__(self):
        return self.nombre
