from django.db import models
from django.utils.timezone import now
from controladora.models import Controladora

class Dispositivo(models.Model):
    TIPO = (
        ("VALIDADOR", "VALIDADOR"),
        ("DISPENSADOR", "DISPENSADOR"),
        ("RECICLADOR", "RECICLADOR"),
        ("LECTOR", "LECTOR"),
    )
    PUERTO = (
        ("COM", "COM"),
        ("USB", "USB"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")    
    prioridad = models.IntegerField(verbose_name='Prioridad', default=1, help_text="Prioridad respecto a los demas dispositivos")
    numero_serie = models.CharField(max_length=200, verbose_name = 'Numero de serie', default="-")
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Controladora Arduino')
    direccion = models.CharField(max_length=200, verbose_name = 'Direccion', default='-')
    puerto = models.CharField(max_length=200, choices=PUERTO,verbose_name = 'Puerto', default='23')
    denominaciones = models.CharField(max_length=200, verbose_name = 'Denominaciones aceptadas', default="-", help_text="Indica las denominaciones aceptadas.separadas por ':' Ejemplo: 1000:500:200")
    capacidades = models.CharField(max_length=200, verbose_name = 'Capacidad maxima por denominacion', default="-",  help_text="Indica la capacidad maxima en el orden de las denominaciones  separada por ':' Ejemplo: 200:250:200")

    activo = models.BooleanField(verbose_name = 'Activo')
    created = models.DateTimeField(verbose_name = 'Fecha de pago', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    controladora_id = models.ForeignKey(Controladora, verbose_name = 'Controladora', related_name='get_dispositivo', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivo'
        ordering = ['-prioridad']

    def __str__(self):
        return str(self.nombre)