from django.db import models

# Create your models here.


class Museo(models.Model):
    idMuseo = models.IntegerField()
    nombre = models.CharField(max_length=128)
    descripcion = models.TextField()
    horario = models.TextField()
    transporte = models.TextField()
    accesibilidad = models.BinaryField()    #django models
    url = models.URLField()
    distrito = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)

class Content_User(models.Model):
    museo = models.ForeignKey(Museo)
    usuario = models.CharField(max_length=32)

class Comentario(models.Model):
    museo = models.ForeignKey(Museo)
    comentario = models.TextField()
    publicacion = models.DateTimeField()    #django models

class Configuracion(models.Model):
    fuente = models.CharField(max_length=32)    #posible revision
    color = models.CharField(max_length=32)
    titulo = models.CharField(max_length=128)
    usuario = models.CharField(max_length=32)

