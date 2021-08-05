from django.db import models
from django.utils.timezone import now

# Create your models here.
class Servicio(models.Model):

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
    #sucursal_id = models.ForeignKey(Sucursal, verbose_name = 'Sucursal', related_name='get_servicio', on_delete = models.CASCADE)





    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicio'
        ordering = ['-nombre']

    def __str__(self):
        return str(self.nombre)


