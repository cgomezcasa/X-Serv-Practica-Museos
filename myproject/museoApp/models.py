from django.db import models

# Create your models here.


class Museo(models.Model):
    idMuseo = models.IntegerField()
    nombre = models.CharField(max_length=128)
    descripcion = models.TextField()
    horario = models.TextField()
    transporte = models.TextField()
    accesibilidad = models.IntegerField()    #django models
    url = models.URLField()
    distrito = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    def __str__(self):
        return self.nombre

class Content_User(models.Model):
    museo = models.ForeignKey(Museo)
    usuario = models.CharField(max_length=32)
    def __str__(self):
        return self.usuario

class Comentario(models.Model):
    museo = models.ForeignKey(Museo)
    comentario = models.TextField()
    publicacion = models.DateTimeField()    #django models

class Configuracion(models.Model):
    fuente = models.CharField(max_length=32)    #posible revision
    color = models.CharField(max_length=32)
    titulo = models.CharField(max_length=128)
    usuario = models.CharField(max_length=32)
    def __str__(self):
        return self.usuario
