from controladora.models import Controladora, Sensor
from dispositivos.models import Dispositivo
from equipo.models import Equipo, Impresora, Tarifa
from recurso.models import Recurso
from servidores.models import Servidor
from transaccion.models import Transaccion,Tienda,Error,Boleto
from rest_framework.serializers import ModelSerializer


class ControladoraSerializer(ModelSerializer):
    class Meta:
        model = Controladora
        fields = '__all__'

class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class DispositivoSerializer(ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = '__all__'

class EquipoSerializer(ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

class ImpresoraSerializer(ModelSerializer):
    class Meta:
        model = Impresora
        fields = '__all__'

class TarifaSerializer(ModelSerializer):
    class Meta:
        model = Tarifa
        fields = '__all__'

class RecursoSerializer(ModelSerializer):
    class Meta:
        model = Recurso
        fields = '__all__'

class ServidorSerializer(ModelSerializer):
    class Meta:
        model = Servidor
        fields = '__all__'

class TransaccionSerializer(ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'

class TiendaSerializer(ModelSerializer):
    class Meta:
        model = Tienda
        fields = '__all__'

class ErrorSerializer(ModelSerializer):
    class Meta:
        model = Error
        fields = '__all__'

class BoletoSerializer(ModelSerializer):
    class Meta:
        model = Boleto
        fields = '__all__'
        
        
        
        
        