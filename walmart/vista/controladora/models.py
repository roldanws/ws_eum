from django.db import models
from django.utils.timezone import now
from equipo.models import Equipo

# Create your models here.

class Controladora(models.Model):
    TIPO = (
        ("Controladora Arduino", "Controladora Arduino"),
        ("Controladora Raspberry", "Controladora Raspberry"),
        ("Controladora Pulso", "Controladora Pulso"),
    )
    MODO = (
        ("Expedidor", "Expedidor"),
        ("Validador", "Validador"),
        ("Cajero", "Cajero"),
        ("Punto de cobro", "Punto de cobro"),
        ("Servidor", "Servidor"),
    )
    numero_serie = models.CharField(max_length=200, verbose_name = 'Numero de serie', default='-')
    version_tarjeta = models.DecimalField(verbose_name='Version tarjeta', max_digits=15, decimal_places=5)
    version_firmware = models.DecimalField(verbose_name='Version firmware', max_digits=15, decimal_places=5)
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Controladora Arduino')
    modo_operacion = models.CharField(max_length=50, choices=MODO, verbose_name = 'Modo operacion', default='Expedidor')
    created = models.DateTimeField(verbose_name = 'Fecha de pago', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    equipo_id = models.ForeignKey(Equipo, verbose_name = 'Equipo', related_name='get_controladora', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Controladora'
        verbose_name_plural = 'Controladora'
        ordering = ['-tipo']

    def __str__(self):
        return str(self.tipo)


class Sensor(models.Model):
    TIPO = (
        ("Temperatura", "Temperatura"),
        ("Presencia", "Presencia"),
        ("Humedad", "Humedad"),
    )
    UNIDADES = (
        ("Grados", "Grados"),
        ("Centimetros", "Centimetros"),
        ("Otro", "Otro"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default='-')
    unidad_medicion = models.DecimalField(verbose_name='unidad', max_digits=15, decimal_places=5)
    version_firmware = models.DecimalField(verbose_name='Version firmware', max_digits=15, decimal_places=5)
    unidad_medicion = models.CharField(max_length=50, choices=UNIDADES, verbose_name = 'Unidad de medicion', default='grados')
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Controladora Arduino')
    activo = models.BooleanField(verbose_name = 'Activo')
    valor = models.DecimalField(verbose_name='Valor', max_digits=15, decimal_places=5, default=0)    
    created = models.DateTimeField(verbose_name = 'Fecha de pago', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    controladora_id = models.ForeignKey(Controladora, verbose_name = 'Controladora', related_name='get_sensor', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensor'
        ordering = ['-tipo']

    def __str__(self):
        return str(self.tipo)

