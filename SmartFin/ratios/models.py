from django.db import models

class Seccion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class SubSeccion(models.Model):
    nombre = models.CharField(max_length=100)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='subsecciones')

    def __str__(self):
        return self.nombre

class Razon(models.Model):
    nombre = models.CharField(max_length=100)
    subseccion = models.ForeignKey(SubSeccion, on_delete=models.CASCADE, related_name='razones', null=True, blank=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='razones', null=True, blank=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    analisis = models.CharField(max_length=300, default="Sin análisis")

    def __str__(self):
        return self.nombre

# Create your models here.
