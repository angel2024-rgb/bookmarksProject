from django.db import models
from django.contrib.auth.models import User


class Coleccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='colecciones')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"
    

class Bookmark(models.Model):
    titulo = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    descripcion = models.TextField(blank=True)
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE, related_name='bookmarks')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen_url = models.URLField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
