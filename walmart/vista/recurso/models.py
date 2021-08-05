from django.db import models
from django.utils.timezone import now

# Create your models here.
class Recurso(models.Model):

    TIPO = (
        ("Archivos", "Archivos"),
        ("Videos", "Videos"),
        ("Streaming", "Streaming"),

    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    ancho_resolucion = models.IntegerField(verbose_name='Ancho', default=1)
    alto_resolucion = models.IntegerField(verbose_name='Alto', default=1)
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo')
    reproduccion_automatica = models.BooleanField(verbose_name = 'Reproduccion automatica')
    archivos = models.FileField(verbose_name = 'Archivos', default='default.png')
    created = models.DateTimeField(verbose_name = 'Fecha de creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #sucursal_id = models.ForeignKey(Sucursal, verbose_name = 'Sucursal', related_name='get_recurso', on_delete = models.CASCADE)



    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recurso'
        ordering = ['-nombre']

    def __str__(self):
        return str(self.nombre)



class Contenido(models.Model):

    TIPO = (
        ("Archivos", "Archivos"),
        ("Videos", "Videos"),
        ("Streaming", "Streaming"),

    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    ancho_resolucion = models.IntegerField(verbose_name='Id', default=1)
    alto_resolucion = models.IntegerField(verbose_name='Id', default=1)
    sincronizado_al_servidor = models.BooleanField(verbose_name = 'Sincronizado al servidor')
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Videos')
    reproduccion_automatica = models.BooleanField(verbose_name = 'Reproduccion automatica')
    archivos = models.FileField(verbose_name = 'Archivos', default='default.png')
    created = models.DateTimeField(verbose_name = 'Fecha de creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #sucursal_id = models.ForeignKey(Sucursal, verbose_name = 'Sucursal', related_name='get_recurso', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Contenido'
        verbose_name_plural = 'Contenido'
        ordering = ['-nombre']

    def __str__(self):
        return str(self.nombre)

