from django.db import models

# Create your models here.

class Empresa(models.Model):
    SECTOR_CHOICES = [
        ('Energía', 'Energía'),
        ('Minería', 'Minería'),
    ]

    idEmpresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES, default='Seleccione el sector',)

    class Meta:
        managed = True
        db_table = 'empresa'

    def __str__(self):
        return self.nombre
