from django.db import models
from django.utils.timezone import now
from equipo.models import Equipo
# Create your models here.


class Tienda(models.Model):
    id_tienda = models.IntegerField(verbose_name='Id tienda')
    ubicacion = models.CharField(max_length=200, verbose_name = 'Ubicacion')
    activo = models.BooleanField(verbose_name = 'Activa')
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Tienda'
        verbose_name_plural = 'Tienda'
        ordering = ['-created']

    def __str__(self):
        return str(self.id_tienda)


class Boleto(models.Model):
    MODO = (
        ("EN RED", "EN RED"),
        ("EN LOCAL", "EN LOCAL"),
        ("STAND ALONE", "STAND ALONE"),
    )
    TIPO = (
        ("Expedidor", "Expedidor"),
        ("Validador", "Validador"),
        ("Cajero", "Cajero"),
        ("Punto de cobro", "Punto de cobro"),
        ("Servidor", "Servidor"),
    )

    folio_boleto = models.IntegerField(verbose_name='Folio boleto')
    entrada = models.IntegerField(verbose_name='Numero de entrada')
    fecha_expedicion_boleto = models.DateTimeField(verbose_name = 'Fecha de expedicion boleto', default = now)
    codigo = models.IntegerField(verbose_name='Codigo de registro')
    registrado = models.BooleanField(verbose_name = 'Registrado', default = True)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    equipo_id = models.ForeignKey(Equipo, verbose_name = 'Equipo', related_name='get_boleto', on_delete = models.CASCADE)
    tienda_id = models.ForeignKey(Tienda, verbose_name = 'Tienda', related_name='get_boleto', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Boleto'
        verbose_name_plural = 'Boleto'
        ordering = ['-created']

    def __str__(self):
        return str(self.created)


class Transaccion(models.Model):
    MODO = (
        ("EN RED", "EN RED"),
        ("EN LOCAL", "EN LOCAL"),
        ("STAND ALONE", "STAND ALONE"),
    )
    TIPO = (
        ("Expedidor", "Expedidor"),
        ("Validador", "Validador"),
        ("Cajero", "Cajero"),
        ("Punto de cobro", "Punto de cobro"),
        ("Servidor", "Servidor"),
    )

    #folio_boleto = models.IntegerField(verbose_name='Folio boleto', null=True, blank=True)
    folio_boleto = models.OneToOneField(Boleto, verbose_name = 'Folio boleto', related_name='get_transaccion', on_delete = models.CASCADE, null=True, blank=True)

    no_provedor = models.CharField(max_length=200, verbose_name = 'Proveedor')
    fecha_expedicion_boleto = models.DateTimeField(verbose_name = 'Fecha de expedicion boleto', default = now)
    det_estacionamiento = models.CharField(max_length=200, verbose_name = 'Determinante estacionamiento')
    expedidor_boleto = models.IntegerField(verbose_name='Expedidor boleto')
    codigo = models.IntegerField(verbose_name='Codigo')
    registrado = models.BooleanField(verbose_name = 'Registrado')
    monto = models.IntegerField(verbose_name='Monto')
    cambio = models.IntegerField(verbose_name='Cambio')
    monedas = models.CharField(max_length=200, verbose_name = 'Monedas')
    billetes = models.CharField(max_length=200, verbose_name = 'Billetes')
    cambio_entregado = models.CharField(max_length=200, verbose_name = 'Cambio entregado')
    created = models.DateTimeField(verbose_name = 'Fecha transaccion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')

    equipo_id = models.ForeignKey(Equipo, verbose_name = 'Equipo', related_name='get_transaccion', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Transaccion'
        verbose_name_plural = 'Transaccion'
        ordering = ['-created']

    def __str__(self):
        return str(self.created) + " " + str(self.monto) + " " + str(self.codigo) 



class Terminal(models.Model):
    id_terminal = models.IntegerField(verbose_name='Id terminal')
    #ultima_transaccion = models.IntegerField(verbose_name='Ultima transaccion')
    clave = models.CharField(max_length=200, verbose_name = 'Clave')
    activo = models.BooleanField(verbose_name = 'Activa')
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    equipo_id = models.ForeignKey(Tienda, verbose_name = 'Tienda', related_name='get_terminal', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'Terminal'
        verbose_name_plural = 'Terminal'
        ordering = ['-created']

    def __str__(self):
        return str(self.id_terminal)

class Error(models.Model):
    id_error = models.IntegerField(verbose_name='Id error')
    descripcion = models.CharField(max_length=200, verbose_name = 'Descripcion')
    created = models.DateTimeField(verbose_name = 'Fecha transaccion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Error'
        verbose_name_plural = 'Error'
        ordering = ['-created']

    def __str__(self):
        return str(self.descripcion)

class Respuesta(models.Model):
    id_respuesta = models.IntegerField(verbose_name='Id resupesta')
    descripcion = models.CharField(max_length=200, verbose_name = 'Descripcion')
    created = models.DateTimeField(verbose_name = 'Fecha transaccion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuesta'
        ordering = ['-created']

    def __str__(self):
        return str(self.descripcion)