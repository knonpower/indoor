from django.db import models


# Create your models here.

class Indoor(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    

class Plan(models.Model):
    nombre = models.CharField(max_length=50)
    hora_encendido = models.DateTimeField()
    hora_apagado = models.DateTimeField()
    temperatura_minima = models.IntegerField(max_length=2)
    temperatura_maxima = models.IntegerField(max_length=2)
    humedad_minima = models.IntegerField(max_length=2)
    humedad_maxima = models.IntegerField(max_length=2)

    def __str__(self):
        return self.nombre
    