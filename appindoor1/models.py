from django.db import models


# Create your models here.

class Indoor(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    

class Plan(models.Model):
    indoor = models.ForeignKey(Indoor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    hora_encendido = models.TimeField()
    hora_apagado = models.TimeField()
    temperatura_minima = models.IntegerField()
    temperatura_maxima = models.IntegerField()
    humedad_minima = models.IntegerField()
    humedad_maxima = models.IntegerField()

    def __str__(self):
        return self.nombre
    