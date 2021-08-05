from django.db import models
from django.utils.timezone import now
from equipo.models import Equipo

class Servidor(models.Model):
    TIPO = (
        ("DATOS", "DATOS"),
        ("MEDIA", "MEDIA"),
        ("API", "API"),
    )
    MODO = (
        ("EN ESPERA", "EN ESPERA"),
        ("CONTINUO", "CONTINUO"),
        ("MONITOR", "MONITOR"),
    )
    MEDIO = (
        ("LAN", "LAN"),
        ("WEB", "WEB"),
        ("ALMACENAMIENTO INTERNO", "ALMACENAMIENTO INTERNO"),
        ("ALMACENAMIENTO EXTERNO", "ALMACENAMIENTO EXTERNO"),
    )
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='DATOS')
    direccion = models.CharField(max_length=200, verbose_name = 'Direccion', default='-')
    puerto = models.CharField(max_length=200, verbose_name = 'Puerto', default='23',blank=True, null=True)
    access_token = models.CharField(max_length=200, verbose_name = 'Token', default='-', blank=True, null=True)
    medio = models.CharField(max_length=200, choices=MEDIO,verbose_name = 'Medio', default='LAN')
    modo_operacion = models.CharField(max_length=50, choices=MODO, verbose_name = 'Modo operacion', default='EN ESPERA')
    capacidad = models.IntegerField(verbose_name='Capacidad') 
    created = models.DateTimeField(verbose_name = 'Fecha de creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    equipo_id = models.ForeignKey(Equipo, verbose_name = 'Equipo', related_name='get_servidor', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidor'
        ordering = ['-direccion']

    def __str__(self):
        return str(self.direccion)