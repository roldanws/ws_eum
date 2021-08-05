from rest_framework import viewsets
from . import serializers
from controladora.models import Controladora, Sensor
from dispositivos.models import Dispositivo
from equipo.models import Equipo, Impresora, Tarifa
from recurso.models import Recurso
from servidores.models import Servidor
from transaccion.models import Transaccion, Tienda, Error, Boleto
from datetime import datetime, timedelta
from django.db.models import Sum, Q, Count
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from rest_framework.decorators import action

"""

class ControladoraViewset(viewsets.ModelViewSet):
    queryset = Controladora.objects.all()
    serializer_class = serializers.ControladoraSerializer

class SensorViewset(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorSerializer

class DispositivoViewset(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all().order_by('-numero')
    serializer_class = serializers.DispositivoSerializer


class EquipoViewset(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = serializers.EquipoSerializer

class ImpresoraViewset(viewsets.ModelViewSet):
    queryset = Impresora.objects.all()
    serializer_class = serializers.ImpresoraSerializer

class RecursoViewset(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = serializers.RecursoSerializer


class ServidorViewset(viewsets.ModelViewSet):
    queryset = Servidor.objects.all()
    serializer_class = serializers.ServidorSerializer

"""

class TarifaViewset(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all()
    serializer_class = serializers.TarifaSerializer

class TransaccionViewset(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = serializers.TransaccionSerializer

class TiendaViewset(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = serializers.TiendaSerializer

class ErrorViewset(viewsets.ModelViewSet):
    queryset = Error.objects.all()
    serializer_class = serializers.ErrorSerializer

class BoletoViewset(viewsets.ModelViewSet):
    queryset = Boleto.objects.all()
    serializer_class = serializers.BoletoSerializer

'''
class TransaccionViewset(viewsets.ModelViewSet):
    queryset = "Transaccion"
    serializer_class = serializers.TransaccionSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user_count = Transaccion.objects.all().count()
        content = {'user_count': user_count}
        return Response(content)
'''
'''
    def get_queryset(self):
        fecha1 = self.request.GET.get('d1') 
        hora1 = self.request.GET.get('t1') 
        fecha2 = self.request.GET.get('d2') 
        hora2 = self.request.GET.get('t2') 

        #today_min = datetime.combine(fecha1, hora1)
        #today_max = datetime.combine(fecha2, hora2)

        fechahora1 = datetime.strptime(str(fecha1)+" "+str(hora1), '%d-%m-%Y %H:%M:%S')
        fechahora2 = datetime.strptime(str(fecha2)+" "+str(hora2), '%d-%m-%Y %H:%M:%S')
        
        


        print("datetimes:",fechahora1,fechahora2)
        if fechahora1:
            if fechahora2:
                transaccion = Transaccion.objects.filter(created__range=[fechahora1, fechahora2])
                print("Transaccion full: ",transaccion)
                
            else:
                transaccion = Transaccion.objects.filter(
                    Q(created__date=fechahora1)
                    )
                return transaccion
        else:
            transaccion = Tansaccion.objtects.all()

        ingreso=transaccion.aggregate(Sum('monto'))['monto__sum']
        pagos = transaccion.count()
        #boletaje=cortes.aggregate(Sum('boletaje'))['boletaje__sum']
        #recuperados=cortes.aggregate(Sum('recuperados'))['recuperados__sum']
        #tolerancias=cortes.aggregate(Sum('tolerancias'))['tolerancias__sum']
        #locatarios=cortes.aggregate(Sum('locatarios'))['locatarios__sum']

        print(ingreso)
        print("pagos: ", pagos)

        respuesta = {
            'ingreso':ingreso,
            'pagos_exitosos':pagos
        }

        content = {'user_count': pagos }
        self.set_password(self.request)
        #return Response({'status': 'password set'})


    @action(detail=True, methods=['get'])
    def set_password(self, request, pk=None):
        #user = self.get_object()
        #serializer = PasswordSerializer(data=request.data)
        if 1:
        #    user.set_password(serializer.data['password'])
        #    user.save()
            print("OKKKKKKKKKKKKKK")

            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
'''

class TransaccionCountView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user_count = Transaccion.objects.all().count()
        content = {'user_count': user_count}
        return Response(content)

