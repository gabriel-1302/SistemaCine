from django.db import models

# Create your models here.
from django.db import models

class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion = models.DurationField()  # Por ejemplo, 1:30:00 para 1 hora y 30 minutos

    def __str__(self):
        return self.titulo

class Funcion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    horario = models.DateTimeField()
    sala = models.IntegerField()

    def __str__(self):
        return f"{self.pelicula.titulo} - {self.horario}"

class Asiento(models.Model):
    fila = models.CharField(max_length=1)
    numero = models.IntegerField()

    def __str__(self):
        return f"Fila {self.fila} - Asiento {self.numero}"

class Boleto(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    comprado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.funcion} - {self.asiento}"