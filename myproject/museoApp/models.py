from django.db import models
from django.contrib.auth.models import User

class Museo(models.Model):
    idMuseo = models.IntegerField(null=True)
    nombre = models.CharField(max_length=128)
    descripcion = models.TextField(null=True)
    horario = models.TextField(null=True)
    transporte = models.TextField(null=True)
    accesibilidad = models.IntegerField(null=True)    #django models
    url = models.URLField(null=True)
    direccion = models.CharField(max_length=32, null=True)
    barrio = models.CharField(max_length=32, null=True)
    distrito = models.CharField(max_length=32, null=True)
    telefono = models.CharField(max_length=32, null=True)
    email = models.EmailField(max_length=64, null=True)
    def __str__(self):
        return self.nombre

class Content_User(models.Model):
    museo = models.ForeignKey(Museo)
    usuario = models.ForeignKey(User)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.usuario.username

class Comentario(models.Model):
    museo = models.ForeignKey(Museo)
    comentario = models.TextField()
    publicacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)    #django models
    def __str__(self):
        return str(self.publicacion)

class Configuracion(models.Model):
    usuario = models.ForeignKey(User)
    fuente = models.CharField(max_length=32)    #posible revision
    color = models.CharField(max_length=32)
    titulo = models.CharField(max_length=128)
    def __str__(self):
        return self.usuario.username
