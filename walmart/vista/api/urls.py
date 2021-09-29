from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from .views import CorteApiView,consultaBoletoApiView,consultaBoletoEumApiView,notiBoletoPagadoApiView,registroBoletoApiView,revBoletoPagadoApiView
from .views import registroTransaccionApiView,consultaTransaccionEumApiView

app_name = 'admin_app'
urlpatterns = [
    path('corte/', CorteApiView.as_view(), name='corte'),
    path('consultaBoletoRequest/', consultaBoletoApiView.as_view(), name='consulta_boleto'),
    path('consultaBoleto/eum/', consultaBoletoEumApiView.as_view(), name='consulta_boleto_eum'),
    path('consultaTransaccion/eum/', consultaTransaccionEumApiView.as_view(), name='consulta_transaccion_eum'),
    path('registroTransaccion/eum/', registroTransaccionApiView.as_view(), name='registro_transaccion_eum'),
    path('registroBoleto/eum/', registroBoletoApiView.as_view(), name='registro_boleto'),
    path('notiBoletoPagadoRequest/', notiBoletoPagadoApiView.as_view(), name='notiBoletoPagado'),
    path('revBoletoPagadoRequest/', revBoletoPagadoApiView.as_view(), name='revBoletoPagado'),

]