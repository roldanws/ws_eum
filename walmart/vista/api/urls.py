from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from .views import CorteApiView,consultaBoletoApiView,consultaBoletoEumApiView,notiBoletoPagadoRequestApiView,registroBoletoApiView

app_name = 'admin_app'
urlpatterns = [
    path('corte/', CorteApiView.as_view(), name='corte'), 
    path('consultaBoleto/', consultaBoletoApiView.as_view(), name='consulta_boleto'), 
    path('consultaBoletoEum/', consultaBoletoEumApiView.as_view(), name='consulta_boleto_eum'), 
    path('registroBoleto/', registroBoletoApiView.as_view(), name='registro_boleto'), 
    path('notiBoletoPagadoRequest/', notiBoletoPagadoRequestApiView.as_view(), name='notiBoletoPagadoRequest'), 
    
]