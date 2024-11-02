from django.db import models
from app.balance.models import Balance
# Create your models here.

class CuentaBalance(models.Model):
    idCuentaBalance = models.AutoField(primary_key=True)
    idBalance = models.ForeignKey(Balance, related_name='cuentas', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=25, default="")
    nombre = models.CharField(max_length=100)
    monto = models.FloatField()

    class Meta:
        managed = True
        db_table = 'cuentabalance'

    def __str__(self):
        return self.nombre