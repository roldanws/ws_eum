
from datetime import datetime, date, time, timedelta


import os,sys,time
import requests,json
from datetime import datetime, timedelta
from Interfaz import Interfaz
from Cajero import Cajero
from Expedidora import Expedidora
from Monitor_02.Controladora import Controladora,ListaDeVariables


class Inicio:
    """
    Clase utulizada para inicializar el equipo, cargar configuraciones y detectar dispositivos
    """
    ADMINISTRACION = 1
    PROCESO = 2
    INTERFAZ = 3
    def __init__(self):

        self.url = ""
        self.encabezado = ""
        self.metodo = ""
        self.datos = ""
        self.status_code = ""
        self.response = ""
        self.lista_de_variables = ""

        self.equipo = ""
        self.controladora = ""
        self.dispositivo = ""
        self.tarifa = ""
        self.sensor = ""
        self.vista = ""
        self.leer_configuracion()
        #self.probar_configuracion()
        self.inicializar()



    def inicializar(self):
        ### ------------------------------- Configurar Controladora
        #variables = ListaDeVariables()
        if self.equipo[0]['tipo'] == 'Cajero':
            equipo = Cajero(variables)
            pass
        if self.equipo[0]['tipo'] == 'Expedidor':
            variables = 0
            equipo = Expedidora(variables)
            pass


        #equipo.establecerControladora(self.controladora)
        #equipo.establecerTarifas(self.tarifa)
        #equipo.establecerSensores(self.sensor)
        #equipo.establecerDispositivos(self.dispositivo)
        #equipo.establecerVista(self.vista)

        #if establecido:
        #    print("### -------------------------------Se establecio el tipo de equipo a: {}".format(self.equipo[0]['tipo']) )
        #else:
        #    print("### -------------------------------Ocurrio un error al establecer el tipo de equipo")

        ### ------------------------------- Configurar Equipo
        ### ------------------------------- Configurar Vista
        ### ------------------------------- Configurar Tarifas
        ### ------------------------------- Configurar Sensores
        ### ------------------------------- Configurar Dispositivos


    def probar_configuracion(self):
        try:
            print("Prueba equipo: ",self.equipo[0]['tipo'])
            print("Prueba controladora",self.controladora[0]['tipo'])
            print("Prueba dispositivo",self.dispositivo[0]['nombre'])
            print("Prueba tarifa",self.tarifa[0]['incremental'])
        except:
            print("Ocurrio un error al aplicar configuraciones")
    def leer_configuracion(self):
        interfaz_api = Interfaz('http://127.0.0.1:8000/api/')
        ### ------------------------------- Leer configuracion de equipo
        body = ""
        metodo = "GET"
        interfaz_api.establecer_url('http://127.0.0.1:8000/api/')
        interfaz_api.establecer_metodo('GET')
        interfaz_api.establecer_encabezado({'Content-Type': 'application/json'})
        modelos = interfaz_api.enviar(Interfaz.PROCESO,body)
        #datos = interfaz_api.response[0]
        #print(response)
        if isinstance(modelos, (dict)):
            print("### -------------------------------Configuracion de equipo ")
            for i,modelo in enumerate(modelos):
                if modelo != 'transaccion' and modelo != 'servicio':
                    interfaz_api.establecer_url('http://127.0.0.1:8000/api/{}/'.format(modelo))
                    campos = interfaz_api.enviar(Interfaz.PROCESO,body)
                    if modelo == "equipo":
                        self.equipo = campos
                    if modelo == "controladora":
                        self.controladora = campos
                    if modelo == "dispositivo":
                        self.dispositivo = campos
                    if modelo == "tarifa":
                        self.tarifa = campos

                    if isinstance(campos, (list)):
                        for i,campo in enumerate(campos):
                            print("### -------------------------------Configuracion de {} {}".format(modelo,i+1))
                            for valor in campo:
                                print(valor + " : " + str(campo[valor]))



        return 0


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

        if self.metodo == 'GET':
            response = requests.get(
            self.url,
            headers=self.encabezado
            )
            if response.status_code != 200:
                err = 1

        elif self.metodo == 'POST':
            print("metodo POST: ",self.metodo)
            response = requests.post(
            self.url, data=json.dumps(self.datos),
            headers=self.encabezado
            )
            if response.status_code != 201:
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


    def validar_datos(self,datos):
        if datos:
            return 1
        else:
            return 0





def main():
    inicio =  Inicio()

if __name__ == "__main__":
    main()

