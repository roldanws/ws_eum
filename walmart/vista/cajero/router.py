from api.viewsets import *
from rest_framework import routers

router = routers.DefaultRouter()
"""
router.register('controladora',ControladoraViewset)
router.register('sensor',SensorViewset)
router.register('dispositivo',DispositivoViewset)
router.register('equipo',EquipoViewset)
router.register('impresora',ImpresoraViewset)
router.register('recurso',RecursoViewset)
router.register('servidor',ServidorViewset)
"""
router.register('tienda',TiendaViewset)
router.register('error',ErrorViewset)
router.register('transaccion',TransaccionViewset)
router.register('boleto',BoletoViewset)
router.register('tarifa',TarifaViewset)
