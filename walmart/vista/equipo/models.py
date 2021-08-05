from django.db import models
from django.utils.timezone import now

# Create your models here.

class Equipo(models.Model):
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
    numero = models.IntegerField(verbose_name='Id', default=1)
    ubicacion = models.CharField(max_length=200, verbose_name = 'Ubicacion', default="-")
    nombre_sucursal = models.CharField(max_length=200, verbose_name = 'Nombre sucursal', default="-")
    localidad_sucursal = models.CharField(max_length=200, verbose_name = 'Localidad sucursal', default="-")
    licencia = models.CharField(max_length=200, verbose_name = 'Licencia', default="-")
    modo_operacion = models.CharField(max_length=50, choices=MODO, verbose_name = 'Modo operacion', default="EN RED")
    numero_serie = models.CharField(max_length=200, verbose_name = 'Numero de serie', default="-")
    politicas = models.TextField(max_length=200, verbose_name = 'Politicas', default="-")
    tolerancia = models.IntegerField(verbose_name='Tolerancia', default=0)
    version_app = models.DecimalField(verbose_name='Costo', max_digits=15, decimal_places=5, default=0)
    sincronizado_al_servidor = models.BooleanField(verbose_name = 'Sincronizado al servidor')
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Expedidor')
    actualizacion_automatica = models.BooleanField(verbose_name = 'Actualizacion automatica')
    #gateway = models.GenericIPAddressField() 
    #ip_address = models.GenericIPAddressField() 
    created = models.DateTimeField(verbose_name = 'Fecha de pago', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')

    id_sucursal = models.IntegerField(verbose_name='Sucursal')
    id_impresora = models.IntegerField(verbose_name='Imprsora')
    #sucursal_id = models.ForeignKey(Sucursal, verbose_name = 'Sucursal', related_name='get_equipo', on_delete = models.CASCADE)





    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipo'
        ordering = ['-numero']

    def __str__(self):
        return str(self.numero)+" "+str(self.ubicacion)




class Impresora(models.Model):

    TIPO = (
        ("Rollo", "Rollo"),
        ("Fanfold", "Fanfold"),
        ("Pvc", "Pvc")
    )
    MODELO = (
        ("TUP", "TUP"),
        ("Epson", "Epson"),
        ("Eltra", "Eltra"),
        ("Otro", "Otro")
    )
    numero_serie = models.CharField(max_length=200, verbose_name = 'Numero de serie', default="-")
    modelo = models.CharField(max_length=200, choices=MODELO, verbose_name = 'Modelo', default="-")
    direccion = models.CharField(max_length=200, verbose_name = 'direccion', default="-")
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Rollo')
    ancho_papel = models.IntegerField(verbose_name='Ancho de papel', default=80)
    created = models.DateTimeField(verbose_name = 'Fecha de pago', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    equipo_id = models.ForeignKey(Equipo, verbose_name = 'Equipos', related_name='get_impresora', on_delete = models.CASCADE)


    class Meta:
        verbose_name = 'Impresora'
        verbose_name_plural = 'Impresora'
        ordering = ['-modelo']

    def __str__(self):
        return str(self.modelo)

class Tarifa(models.Model):
    DIA = (
        ("ninguno", "ninugno"),
        ("lunes", "lunes"),
        ("martes", "MARTES"),
        ("miercoles", "miercoles"),
        ("jueves", "jueves"),
        ("viernes", "viernes"),
        ("sabado", "sabado"),
        ("domingo", "domingo")
    )
    tiempo_base = models.IntegerField(verbose_name='Tiempo base', default=2)
    monto_base = models.IntegerField(verbose_name='Monto base', default=5)
    fraccion_tiempo = models.IntegerField(verbose_name='Fraccion de tiempo', default=0)
    incremental = models.IntegerField(verbose_name='Incremental', default=0)
    descuento = models.IntegerField(verbose_name='Descuento', default=0)
    prioridad = models.IntegerField(verbose_name='Prioridad', default=1)
    fecha_inicio = models.TimeField(verbose_name = 'Fecha inicio',blank=True, null=True)
    fecha_fin = models.TimeField(verbose_name = 'Fecha fin',blank=True, null=True)
    horario_inicio = models.TimeField(verbose_name = 'Horario inicio',blank=True, null=True)
    horario_fin = models.TimeField(verbose_name = 'Horario fin',blank=True, null=True)
    dia_semana = models.CharField(max_length=200, choices=DIA, verbose_name = 'Dia de la semana',blank=True, null=True)
    created = models.DateTimeField(verbose_name = 'Fecha de pago',default = now)
    updated = models.DateField(auto_now=True, verbose_name = 'Ultima modificacion')
    equipo_id = models.ForeignKey(Equipo, verbose_name = 'Equipos', related_name='get_tarifa', on_delete = models.CASCADE)


    class Meta:
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifa'
        ordering = ['-created']

    def __str__(self):
        return "Descuento: "+str(self.descuento)+" Incremental: "+str(self.incremental)