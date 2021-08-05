from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
from braces.views import CsrfExemptMixin
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from chat_app import consumers
from ui.views import UiPageView,UiCancelacionView
class Respuestas:
    def __init__(self):
        self.respuestas = dict (
        cancelar_pago = 0,
        operacion_recarga = 0,
        )
    def obtener_respuestas(self):
        return self.respuestas
    def establecer_respuestas(self,llave,valor):
        self.respuestas[llave] = valor
    def procesar_mensaje(self,mensaje):
        try:
            #-------------------- Cancelar Pago --------------------#
            if mensaje['cancelar_pago'] == 2:
                self.establecer_respuestas("cancelar_pago",0)
            if mensaje['cancelar_pago'] == 1:
                self.establecer_respuestas("cancelar_pago",1)
            #-------------------- Operacion Recarga --------------------#
            if mensaje['operacion_recarga'] == 2:
                self.establecer_respuestas("operacion_recarga",0)
            if mensaje['operacion_recarga'] == 1:
                self.establecer_respuestas("operacion_recarga",1)
        except:
            pass

        
        return self.respuestas

class ProcessHookView(CsrfExemptMixin, View, Respuestas):
    
    respuestas = Respuestas()
    #@method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        conv = request.body.decode('utf-8').replace('\0', '')
        mensaje = json.loads(conv)
        message = json.loads(conv)
        message = str(message).replace("'",'"')
        consumers.ws_message(message)
        self.respuestas.procesar_mensaje(mensaje)
        
        print("Mensaje enviado: ",self.respuestas.obtener_respuestas())
        return JsonResponse(self.respuestas.obtener_respuestas())
        

# Create your views here.
