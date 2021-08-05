from django.test import TestCase

# Create your tests here.
from datetime import datetime, date, time, timedelta


import os,sys,time
import requests,json
from datetime import datetime, timedelta
from termcolor import colored



class Interfaz:
    """
    Clase utulizada para interfazar informacion entre la controladora y la web django 
    haciendo uso de webhooks
    """
    ADMINISTRACION = 1
    PROCESO = 2
    INTERFAZ = 3
    CODIGOS_EXITOSOS = (200,201,206)
    def __init__(self,url):
        self.url = url
        self.encabezado = ""
        self.metodo = ""
        self.datos = ""
        self.status_code = ""
        self.response = ""
        self.lista_de_variables = ""



    
    def obtener_url(self,url):
        return self.url
    def obtener_encabezado(self,encabezado):
        return self.encabezado
    def obtener_metodo(self,metodo):
        return self.metodo

    def establecer_url(self,url):
        self.url = url
    def establecer_encabezado(self,encabezado):
        self.encabezado = encabezado
    def establecer_metodo(self,metodo):
        self.metodo = metodo

    def establecer_lista_de_variables(self,lista_de_variables):
        self.lista_de_variables = lista_de_variables
        
    def establecer_encabezados(self,encabezados):
        self.modo_operacion = modo_operacion
        
    def enviar(self,tipo = 0, *args, **kargs):
        err = 0
        for item in args:
            #print (item)
            #for i, it in enumerate(item):
            #    print(i,it)
        
                
            if self.validar_datos(item):
                self.datos = item
            else:
                self.response =  {"error":"datos invalidos"}

        try:
            if self.metodo == 'GET':
                response = requests.get(
                self.url,
                headers=self.encabezado
                )
                if response.status_code not in self.CODIGOS_EXITOSOS:
                    err = 1
                
            elif self.metodo == 'POST':
                #print("metodo POST: ",self.metodo)
                response = requests.post(
                self.url, data=json.dumps(self.datos),
                headers=self.encabezado
                )
                if response.status_code not in self.CODIGOS_EXITOSOS:
                    err = 1
                
                
            elif self.metodo == 'PUT':
                pass
            elif self.metodo == 'DELETE':
                pass

            self.status_code = response.status_code
            self.response = response.json()

            if err:
                print("Ocurrio un error:",response.status_code)
            else: 
                return self.response
        except:
            self.response = 0
            text = "[{}] [Error3] Vista sin respuesta".format(time.strftime("%Y-%m-%d %H:%M:%S"))
            print(colored(text, 'red'))

    
    def validar_datos(self,datos):
        if datos:
            return 1
        else: 
            return 0



    

def main():
    
    ### ------------------------------- Declarar la interfaz
    interfaz_api = Interfaz('http://127.0.0.1:8000/api/')
    #interfaz_hooks = Interfaz('http://127.0.0.1:8000/hooks/')
    ### ------------------------------- Proceso para calcular una tarifa
    print("#-------------------Prueba Tarifa: ")
    body = ""
    metodo = "GET"
    interfaz_api.establecer_url('http://127.0.0.1:8000/api/tarifa')
    interfaz_api.establecer_metodo('GET')
    interfaz_api.establecer_encabezado({'Content-Type': 'application/json'})
    response = interfaz_api.enviar(Interfaz.PROCESO,body)
    datos = interfaz_api.response[0]
    descuento = datos['descuento']
    tiempo_base = datos['tiempo_base']
    monto_base = datos['monto_base']
    fraccion_tiempo = datos['fraccion_tiempo']
    incremental = datos['incremental']

    tiempo_estacionado =  235
    descuento = 0
    monto = calcular_tarifa(tiempo_estacionado,descuento,tiempo_base,monto_base,fraccion_tiempo,incremental)
    print("Monto: ",monto)
    '''
    ### ------------------------------- Proceso para registrar un pago
    print("#-------------------Prueba Pago: ")
    body = {
    "folio_boleto": 223,
    "expedidor_boleto": 1,
    "fecha_expedicion_boleto": "2020-04-07T12:12:00Z",
    "codigo": 1,
    "registrado": True,
    "monto": 10,
    "cambio": 0,
    "monedas": "0:0",
    "billetes": "0:0",
    "cambio_entregado": "0:0",
    "equipo_id": 1
    }
    metodo = "POST"
    interfaz_api.establecer_url('http://127.0.0.1:8000/api/corte?d1=28-04-2020&t1=19:14:18&d2=29-04-2020&t2=19:17:18')
    interfaz_api.establecer_metodo('GET')
    interfaz_api.establecer_encabezado({'Content-Type': 'application/json'})
    print("Metodo....: ",interfaz_api.obtener_metodo({'Content-Type': 'application/json'}))
    response = interfaz_api.enviar(Interfaz.PROCESO,body)
    print("Respuesta: ",response)
    '''
    ### ------------------------------- Proceso para obtener el corte
    fecha_1 = "28-04-2020"
    hora_1 = "19:14:18"
    fecha_2 = "29-04-2021"
    hora_2 = "19:17:18"
    url = "http://127.0.0.1:8000/api/corte?f1={0}&h1={1}&f2={2}&h2={3}".format(fecha_1,hora_1,fecha_2,hora_2)
    interfaz_api.establecer_url(url)
    interfaz_api.establecer_metodo('GET')
    interfaz_api.establecer_encabezado({'Content-Type': 'application/json'})
    response = interfaz_api.enviar(Interfaz.PROCESO,body)
    print("#-------------------Prueba Corte: ",response)
    print("Exitosos: ",response['exitosos'])
    print("Incidencias: ",response['incidencias'])
    print("Cancelados: ",response['cancelados'])
    print("Ingreso total: ",response['ingreso'])


def calcular_tarifa(tiempo_estacionado,descuento,tiempo_base,monto_base,fraccion_tiempo,incremental):
    monto_total = 0
    if tiempo_base > tiempo_estacionado:
        monto_total = monto_base
        return monto_total
    else:
        monto_total += monto_base
        tiempo_restante = tiempo_estacionado - tiempo_base
        fracciones_de_tiempo =  int(tiempo_restante/fraccion_tiempo)
        print("Fracciones: ",fracciones_de_tiempo)
        monto_total += fracciones_de_tiempo * incremental
        return monto_total

#def registrar_pago(tiempo_estacionado,descuento,tiempo_base,monto_base,fraccion_tiempo,incremental):

if __name__ == "__main__":
    main()


## 1:55