import threading
import sys
import os
import time
import fechaUTC as hora
#import Conexiones.cliente as Servidor
#from pygame import mixer
import subprocess
from threading import Timer,Thread 
import sched
import termios
import serial
import binascii
#from bitstring import BitArray
from datetime import datetime, timedelta
import calendar
#import psycopg2, psycopg2.extras
#from Botones.Botones import Botones,PuertoDeComunicacion, obtenerNombreDelPuerto
#from Pila.Pila import Pila
from struct import *

import traceback
from Logs.GuardarLogs import GuardarLogs
import shutil
from termcolor import colored




ruta =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
ruta = ruta + "/"
def obtenerUsuario(ruta):
    lista = ruta.split("/")
    return "/"+lista[1]+"/"+lista[2]+"/"	
rutaUsuario = obtenerUsuario(ruta)
print(rutaUsuario)
print(rutaUsuario[6:-1])
usuario = rutaUsuario[6:-1]


raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
sys.path.append(raiz)

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador
from Conexiones.Servidor import Servidor
from Monitor.Comunicacion import Comunicacion

from Monitor.PuertoSerie import PuertoSerie
from Monitor.Hopper import Hopper
from Monitor.Monedero import Monedero
from Monitor.Billetero import Billetero
from Monitor.Controladora import Controladora,ListaDeVariables



raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"../..")
sys.path.append(raiz)





#import Conexiones.cliente as Servidor
#from Conexiones.Conexiones import Conexiones

'''DL17'''
#from encriptacionQR import codificar
#from configParser.viewData import viewData
'''DL17'''


from Interfaz import Interfaz
#from Scanner import Scanner


class Cajero:
    """
    Clase utulizada para administrar el cajero
    """
    #-------------------- Identificadores de dispositivos      
    MONEDERO_MDB = 1
    BILLETERO_MDB = 2
    HOPPER_01_CCTALK = 3
    HOPPER_02_CCTALK = 4
    HOPPER_03_CCTALK = 5
    VALIDADOR_CCTALK = 6
    BILLETERO_ACEPTADOR_ID003 = 7
    BILLETERO_RECICLADOR_ID003 = 8
    def __init__(self,variables):
        self.tipo_controladora = ""
        self.encriptacion = ""
        self.nombre_sucursal = ""
        self.localidad_sucursal = ""
        self.server_ip_address = ""
        self.ip_address = ""
        self.id = ""
        self.id_sucursal = ""
        self.politicas = ""


        #-------------------- Leer configuracion        
        self.vizualizar = ""
        #-------------------- Modo operacion 
        self.listaDeVariables = variables
        self.tarjeta_controladora = ""
        #-------------------- Diccionatrios
        self.informacion = "" 
        self.variables = "" 

        
        
        #-------------------- Secuencia cobro
        self.secuencia_cobro = 0
        self.monto_ingresar = 0
        self.monto_ingresado = 0
        self.monto_a_dispensar = 0
        self.descuento = 0
        self.tarifa_seleccionada = 0
        self.cancelar_pago = 0

        #-------------------- Secuencia lectura boleto
        self.boleto = ""
        self.folio= ""
        self.expedidora = ""
        self.hora_entrada = ""
        self.fecha_entrada = ""
        self.tiempo_estacionado = ""

        #-------------------- Modelos
        self.equipo = ""
        self.controladora = ""
        self.dispositivo = ""
        self.tarifa = ""
        self.sensor = ""
        self.servidor = ""

        #-------------------- Interfaces
        self.vista = ""
        self.api = ""

        self.inicializar()

        self.TON_01 = Temporizador("TON_01",2.5)
        
        print("Iniciando Cajero.")
        tarea1 = threading.Thread(target=self.run)
        tarea1.start()

    def run (self):
        self.funcionando = True
        listaDeVariables_tmp = 0
        while (self.funcionando):
            time.sleep(1)
            self.TON_01.entrada = not self.TON_01.salida
            self.TON_01.actualizar()
            print(" #-------------------- Secuencia de cobro: ",self.secuencia_cobro)
            #print(" #-------------------- conexion a internet: ",self.servidor.estado_internet)
            #print(" #-------------------- conexion a servidor: ",self.servidor.estado_servidor)
            if self.secuencia_cobro == 0:
                #-------------------- Validar lectura de boleto
                self.variables.update(cancelar_pago=0)
                self.variables.update(operacion_recarga=0)
                boleto_valido = self.validar_lectura_boleto()
                #self.dispensar_cambio2(583)
                if boleto_valido == 1:
                    self.secuencia_cobro = 1
                else:
                    self.secuencia_cobro = 0

            if self.secuencia_cobro == 1:
                #-------------------- Validar estado de dispositivos
                validacion = self.validar_dispositivos()
                if validacion == 1:
                    self.secuencia_cobro = 2
                else:
                    self.secuencia_cobro = 0

            if self.secuencia_cobro == 2:
                #-------------------- Habilitar dispositivos de cobro
                self.habilitar_dispositivos_cobro()
                resultado = 1
                if resultado == 1:
                    listaDeVariables_tmp = self.listaDeVariables
                    self.secuencia_cobro = 3
                else:
                    self.secuencia_cobro = 0
            if self.secuencia_cobro == 3:
                #-------------------- Actualizar variables
                monto_completado = self.actualiza_cobro(listaDeVariables_tmp)
                self.variables.update(interfaz=2)
                if monto_completado == 1:
                    self.secuencia_cobro = 4
                else:
                    self.secuencia_cobro = 3

            if self.secuencia_cobro == 4:
                #-------------------- Entregar cambio y validar operacion
                operacion_validada = self.validar_operacion()
                if operacion_validada == 1:
                    self.secuencia_cobro = 8
                else:
                    self.secuencia_cobro = 5
                
            if self.secuencia_cobro == 5:
                #-------------------- Operacion no valida: Entregar comprobante de error y pedir asistencia
                combrobante_error = self.secuencia_error()
                if combrobante_error == 1:
                    self.secuencia_cobro = 7
                else:
                    print("No se pudo expedir el comprobante de error")

            if self.secuencia_cobro == 6:
                #-------------------- Operacion cancelada: 
                self.variables.update(interfaz=1)
                self.variables.update(cancelar_pago=2)
                self.cancelar_pago = 1                
                cancelacion_exitosa = self.secuencia_cancelacion()
                if cancelacion_exitosa == 1:
                    self.secuencia_cobro = 8
                else:
                    self.secuencia_cobro = 5
                    print("No se pudo expedir el comprobante de error")


            if self.secuencia_cobro == 7:
                #-------------------- Cajero suspendido
                self.cajero_suspendido()

            if self.secuencia_cobro == 8:
                #-------------------- Ofrecer ticket , registrar operacion y reiniciar valores
                operacion_finalizada = self.finalizar_operacion()
                self.secuencia_cobro = 0
            
            if self.secuencia_cobro == 9:
                #-------------------- Operacion recarga
                self.variables.update(operacion_recarga=2)
                self.variables.update(interfaz=2)
                operacion_finalizada = self.recargar()

            fecha = time.strftime("%Y-%m-%d %H:%M:%S")
            
            


            self.variables.update(monto_ingresar=self.monto_ingresar)
            self.variables.update(monto_ingresado=self.monto_ingresado)
            self.variables.update(monto_a_dispensar=self.monto_a_dispensar)
            self.variables.update(folio=self.folio)
            self.variables.update(hora_entrada=self.hora_entrada)
            print("te",self.tiempo_estacionado)
            self.variables.update(tiempo_estacionado=self.tiempo_estacionado)
            self.variables.update(descuento=self.descuento)
            self.variables.update(fecha=fecha)
            
            #sensores.update(monto=i)
            #response = cajero.enviar(informacion)
            respuesta = self.enviar(self.variables)

            self.validar_respuesta(respuesta)
            print(respuesta)



    def inicializar(self):
        
        #shutil.copy(ruta+"configParser/configuracion.ini", ruta+"configParser/configuracion_respaldo.ini")
        #shutil.copy(ruta+"configParser/sensores.ini", ruta+"configParser/sensores_respaldo.ini")

        #-------------------- Establecer vista 
        self.vista = Interfaz('http://127.0.0.1:8000/hook/')
        self.vista.establecer_lista_de_variables(self.listaDeVariables)
        body = ""
        metodo = "POST"
        self.vista.establecer_metodo(metodo)
        self.vista.establecer_encabezado({'Content-Type': 'application/json'})
        #-------------------- Establecer API 
        self.api = Interfaz('http://127.0.0.1:8000/api/')
        self.api.establecer_lista_de_variables(self.listaDeVariables)
        body = ""
        metodo = "GET"
        self.api.establecer_metodo(metodo)
        self.api.establecer_encabezado({'Content-Type': 'application/json'})

        self.tipo_controladora = 0
        #-------------------- Leer configuracion        
        #self.vizualizar = viewData('configuracion.ini')
        self.leer_configuracion()

        #-------------------- Modo operacion 
        self.tarjeta_controladora = self.establecer_tarjeta_controladora(self.listaDeVariables)

        #-------------------- configurar dispositivos 
        self.configurar_dispositivos()

        #-------------------- configurar servidores 
        self.configurar_servidores()
        
    

        time.sleep(5)

        
        self.informacion = dict (
        interfaz = 0,
        X_02 = self.listaDeVariables.dispositivos[0].variables[2].obtenerValor(),
        X_01 = self.listaDeVariables.dispositivos[0].variables[1].obtenerValor(),
        X_03 = self.listaDeVariables.dispositivos[0].variables[3].obtenerValor(),
        X_04 = self.listaDeVariables.dispositivos[0].variables[4].obtenerValor(),
        X_05 = self.listaDeVariables.dispositivos[0].variables[5].obtenerValor(),
        X_06 = self.listaDeVariables.dispositivos[0].variables[6].obtenerValor(),
        X_07 = self.listaDeVariables.dispositivos[0].variables[7].obtenerValor(),
        )
        self.variables = dict (
        monto_ingresar = 1,
        monto_ingresado = 1,
        monto_a_dispensar = 0,
        folio = 0,
        hora_entrada = 0,
        tiempo_estacionado = "",
        interfaz = 1,
        descuento = 0,
        cancelar_pago = 0,
        operacion_recarga = 0,
        X_08 = self.listaDeVariables.dispositivos[0].variables[8].obtenerValor(),
        X_09 = self.listaDeVariables.dispositivos[0].variables[9].obtenerValor(),
        X_10 = self.listaDeVariables.dispositivos[0].variables[10].obtenerValor(),
        X_11 = self.listaDeVariables.dispositivos[0].variables[11].obtenerValor(),
        X_12 = self.listaDeVariables.dispositivos[0].variables[12].obtenerValor(),
        X_13 = self.listaDeVariables.dispositivos[0].variables[13].obtenerValor(),
        X_14 = self.listaDeVariables.dispositivos[0].variables[14].obtenerValor(),
        X_15 = self.listaDeVariables.dispositivos[0].variables[15].obtenerValor(),
        X_16 = self.listaDeVariables.dispositivos[0].variables[16].obtenerValor(),
        X_17 = self.listaDeVariables.dispositivos[0].variables[17].obtenerValor(),
        X_18 = self.listaDeVariables.dispositivos[0].variables[18].obtenerValor(),
        X_19 = self.listaDeVariables.dispositivos[0].variables[19].obtenerValor(),
        X_20 = self.listaDeVariables.dispositivos[0].variables[20].obtenerValor(),
        X_21 = self.listaDeVariables.dispositivos[0].variables[21].obtenerValor(),
        X_22 = self.listaDeVariables.dispositivos[0].variables[22].obtenerValor(),
        )
        self.deshabilitar_dispositivos_cobro()
        time.sleep(2)
        pass

    def obtenerEquipo(self,equipo): 
        return self.equipo 
    def obtenerControladora(self,controladora): 
        return self.controladora 
    def obtenerTarifas(self,tarifa): 
        return self.tarifa 
    def obtenerSensores(self,sensor): 
        return self.sensor 
    def obtenerDispositivos(self,dispositivo): 
        return self.dispositivo 
    def obtenerVista(self,vista): 
        return self.vista 

    def establecerEquipo(self,equipo): 
        self.equipo = equipo
    def establecerControladora(self,controladora): 
        self.controladora = controladora
    def establecerTarifas(self,tarifa): 
        self.tarifa = tarifa
    def establecerSensores(self,sensor): 
        self.sensor = sensor
    def establecerDispositivos(self,dispositivo): 
        self.dispositivo = dispositivo
    def establecerVista(self,vista): 
        self.vista = vista

    


    def establecer_tarjeta_controladora(self,tipo): 
        if self.controladora[0]['tipo'] == "Controladora Arduino":        
            if self.controladora[0]['modo_operacion'] == "Cajero":
                #controladora = Controladora(listaDeVariable s, tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO)
                controladora = Controladora(self.listaDeVariables, 
                    tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO,
                    tipoDeControladora = Controladora.CONTROLADORA_PARA_CAJERO)

        if self.controladora[0]['tipo'] == "Controladora Pulso": 
            controladora = Controladora(self.listaDeVariables, tarjeta = Controladora.TARJETA_DE_PULSO)
        if self.controladora[0]['tipo'] == "Controladora Blanca": 
            controladora = Controladora(self.listaDeVariables, tarjeta = Controladora.TARJETA_DE_INTERFAZ_BLANCA)
        if self.controladora[0]['tipo'] == "Controladora Raspberry": 
            controladora = Controladora(self.listaDeVariables, tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO)
        return 0


    def leer_configuracion(self):
        #interfaz_api = Interfaz('http://127.0.0.1:8000/api/')
        ### ------------------------------- Leer configuracion de equipo
        body = ""
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/')
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        modelos = self.api.enviar(Interfaz.PROCESO,body)
        #datos = self.api.response[0]
        #print(response)
        if isinstance(modelos, (dict)):
            print("### -------------------------------Configuracion de equipo ")
            for i,modelo in enumerate(modelos):
                if modelo != 'transaccion' and modelo != 'servicio':
                    self.api.establecer_url('http://127.0.0.1:8000/api/{}/'.format(modelo))
                    campos = self.api.enviar(Interfaz.PROCESO,body)
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
    '''
    #-------------------- Leer configuracion archivo configuracion .ini         
    def leer_configuracion(self):
        #self.vizualizar.getInfo()
        self.tipo_controladora = int(self.vizualizar.getValue('CONTROLADORA','tipo_tc'))
        self.encriptacion = int(self.vizualizar.getValue('GENERAL','encriptacion'))
        self.nombre_sucursal = self.vizualizar.getValue('GENERAL','nombre_sucursal')
        self.localidad_sucursal = self.vizualizar.getValue('GENERAL','localidad_sucursal')
        self.server_ip_address = self.vizualizar.getValue('RED','server_ip_address')
        self.ip_address = self.vizualizar.getValue('RED','ip_addeess')
        self.id = int(self.vizualizar.getValue('GENERAL','id'))
        self.id_sucursal = int(self.vizualizar.getValue('GENERAL','id_sucursal'))
        self.politicas = self.vizualizar.getValue('GENERAL','politicas')
    '''
    def enviar(self,datos):
        self.vista.enviar(Interfaz.PROCESO,datos)
        print(self.vista.response)
        return self.vista.response
    def operacion_cobro(self):
        pass
    def actualiza_cobro(self,listaDeVariables_tmp):
        
        variables_tmp = dict (
        X_10_tmp = listaDeVariables_tmp.dispositivos[0].variables[10].obtenerValor(),
        X_13_tmp = listaDeVariables_tmp.dispositivos[0].variables[13].obtenerValor(),
        X_16_tmp = listaDeVariables_tmp.dispositivos[0].variables[16].obtenerValor(),
        X_19_tmp = listaDeVariables_tmp.dispositivos[0].variables[19].obtenerValor(),
        X_22_tmp = listaDeVariables_tmp.dispositivos[0].variables[22].obtenerValor(),
        )

        #ingreso_1 = (int(self.variables.get('X_10')) - int(variables_tmp.get('X_10_tmp')))*int(self.variables.get('X_08'))
        #ingreso_2 = (int(self.variables.get('X_13')) - int(variables_tmp.get('X_13_tmp')))*int(self.variables.get('X_11'))
        #ingreso_3 = (int(self.variables.get('X_16')) - int(variables_tmp.get('X_16_tmp')))*int(self.variables.get('X_14'))
        #ingreso_4 = (int(self.variables.get('X_19')) - int(variables_tmp.get('X_19_tmp')))*int(self.variables.get('X_17'))
        #ingreso_5 = (int(self.variables.get('X_22')) - int(variables_tmp.get('X_22_tmp')))*int(self.variables.get('X_20'))
        
        ingreso_1 = (int(variables_tmp.get('X_10_tmp')) - int(self.variables.get('X_10')))*int(self.variables.get('X_08'))
        ingreso_2 = (int(variables_tmp.get('X_13_tmp')) - int(self.variables.get('X_13')))*int(self.variables.get('X_11'))
        ingreso_3 = (int(variables_tmp.get('X_16_tmp')) - int(self.variables.get('X_16')))*int(self.variables.get('X_14'))
        ingreso_4 = (int(variables_tmp.get('X_19_tmp')) - int(self.variables.get('X_19')))*int(self.variables.get('X_17'))
        ingreso_5 = (int(variables_tmp.get('X_22_tmp')) - int(self.variables.get('X_22')))*int(self.variables.get('X_20'))
        

        print("Denominacion 1:",ingreso_1)
        print("Denominacion 2:",ingreso_2)
        print("Denominacion 3:",ingreso_3)
        print("Denominacion 4:",ingreso_4)
        print("Denominacion 5:",ingreso_5)
        self.monto_ingresado = ingreso_1 + ingreso_2 + ingreso_3 + ingreso_4 + ingreso_5
        #self.monto_ingresado = self.monto_ingresado * (-1)

        print("Monto a ingresar:",self.monto_ingresar)
        print("Monto ingresado:",self.monto_ingresado)
        print("Diferencia monto:",self.monto_a_dispensar)
        if self.monto_ingresado >=  self.monto_ingresar:
            self.monto_a_dispensar = self.monto_ingresar - self.monto_ingresado
            return 1
        else:
            return 0

        return self.monto_a_dispensar
        
    def probar(self):
        return 0
    def configurar_servidores(self):
        self.servidor =  Servidor()
        return 1
    def configurar_dispositivos(self):
        return 1
    def validar_dispositivos(self):
        return 1

    def validar_respuesta(self,respuesta):
        #print("Respuesta: ",respuesta['status'])
        print("Respuesta: ",type(respuesta),respuesta)
        if respuesta['cancelar_pago'] == 1:
            self.secuencia_cobro = 6
            
        if respuesta['operacion_recarga'] == 1:
            self.secuencia_cobro = 9

        #if respuesta['descuento'] > 0:
        #    self.descuento = respuesta['descuento']
        return 1
            
    def validar_operacion(self):
        if self.monto_a_dispensar:
            self.dispensar_cambio2(self.monto_a_dispensar)
        return 1


    def calcular_tarifa2(self):
        horaBoleto=self.hora_entrada.split(':',2)
        fechaAMD=self.fecha_entrada.split('-')
        print(fechaAMD)
        fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]
        dh=self.restar_hora(horaBoleto,fechaAMD.split('-'))
        dias=dh[0]
        horas=dh[1]
        tiempo_estacionado=dh[2]
        print("tiempo_estacionado: ",dias,horas)
        self.tiempo_estacionado = tiempo_estacionado
        #self.tiempo_estacionado = str(dias)+" "+str(horas)
        self.monto_ingresar = 15
    
    def calcular_tarifa(self,hora_ingreso, fecha_ingreso, descuento):
        #-------------------- Seleccionar tarifa y extraer datos --------------------#
        indice = 0
        for i,tarifa_seleccionada in enumerate(self.tarifa):
            if tarifa_seleccionada['descuento'] == descuento:
                indice = i
        descuento = self.tarifa[indice]['descuento']
        tiempo_base = self.tarifa[indice]['tiempo_base']
        monto_base = self.tarifa[indice]['monto_base']
        fraccion_tiempo = self.tarifa[indice]['fraccion_tiempo']
        incremental = self.tarifa[indice]['incremental']
        self.tarifa_seleccionada = self.tarifa[indice]['id']
        # ( monto_base representa el descuento tipo 1 por el tiempo : tiempo_base )
        self.descuento = monto_base

        #-------------------- Calcular tiempo estacionado en minutos --------------------#
        resta = self.restar_hora(self.hora_entrada,self.fecha_entrada)
        dias = resta[0]
        segundos = resta[1]
        tiempo_estacionado = int(segundos/60)
        print("#-------------------- Informacion Boleto --------------------# ")
        print("tarifa_seleccionada: {} ".format(self.tarifa_seleccionada))
        print("tiempo_estacionado: {} dias con {} minutos".format(dias,tiempo_estacionado))
        if dias:
            tiempo_estacionado += dias*1440
        self.tiempo_estacionado = tiempo_estacionado
        print("minutos totales: {}".format(tiempo_estacionado))
        #-------------------- Calcular monto total en base a tiempo estacionado --------------------#
        monto_total = 0
        if tiempo_base > tiempo_estacionado:
            monto_total = monto_base
            self.monto_ingresar = monto_total
            return monto_total
        else:
            monto_total += monto_base
            tiempo_restante = tiempo_estacionado - tiempo_base
            fracciones_de_tiempo =  int(tiempo_restante/fraccion_tiempo)
            monto_total += fracciones_de_tiempo * incremental
            self.monto_ingresar = monto_total
            print("Fracciones: ",fracciones_de_tiempo)
            print("Monto a ingresar: ",self.monto_ingresar)
            return monto_total

    def recargar(self):
        i = 0
        direccion_dispositivo = 0
        for i,dispositivo_seleccionado in enumerate(self.dispositivo):
            if dispositivo_seleccionado['activo'] == True:
                direccion_dispositivo =int( dispositivo_seleccionado['direccion'])
                #self.listaDeVariables.dispositivos[direccion_dispositivo].ejecutarInstruccion(self.listaDeVariables.dispositivos[direccion_dispositivo].HABILITAR)
                print("Dispositivo Habilitado: {} {} ".format(dispositivo_seleccionado['nombre'],dispositivo_seleccionado['direccion']))
        return 1
    def dispensar_dinero(self,monto):
        indice = 0
        for i,dispositivo_seleccionado in enumerate(self.dispositivo):
            if dispositivo_seleccionado['tipo'] == "DISPENSADOR":
                if dispositivo_seleccionado['activo'] == True:
                    if dispositivo_seleccionado['direccion'] == 0:
                        self.listaDeVariables.dispositivos[0].ejecutarInstruccion(self.listaDeVariables.dispositivos[0].MONEDERO_DAR_CAMBIO, monto)
                    elif dispositivo_seleccionado['direccion'] == 2:
                        self.listaDeVariables.dispositivos[2].ejecutarInstruccion(self.listaDeVariables.dispositivos[2].MONEDERO_DAR_CAMBIO, monto)
                    elif dispositivo_seleccionado['direccion'] == 3:
                        self.listaDeVariables.dispositivos[3].ejecutarInstruccion(self.listaDeVariables.dispositivos[3].MONEDERO_DAR_CAMBIO, monto)
                    elif dispositivo_seleccionado['direccion'] == 4:
                        self.listaDeVariables.dispositivos[4].ejecutarInstruccion(self.listaDeVariables.dispositivos[4].MONEDERO_DAR_CAMBIO, monto)
                        
                indice = i
        #self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_DAR_CAMBIO, monto)
    def recibir_dinero(self):
        return 1
        #self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Monedero.MONEDERO_DAR_CAMBIO, monto)
    def buscar_boleto(self):
        mensaje = "{},{},{} {}".format(self.folio,self.expedidora,self.hora_entrada,self.fecha_entrada)
        resultado = self.servidor.configSocket("informacion boleto", mensaje)
        if not self.servidor.estado_servidor:
            self.estado_boleto = 0
            estado = 1
            err = "[{}] [Error2] Sin conexion a servidor".format(time.strftime("%Y-%m-%d %H:%M:%S"))
            print(colored(err, 'red'))
        elif resultado == -1:
            self.estado_boleto = 0
            err = "[{}] [Error5] Datos no encontrados o invalidos".format(time.strftime("%Y-%m-%d %H:%M:%S"))
            print(colored(err, 'red'))
            estado = 1
        else: 
            self.estado_boleto = resultado[1]
            self.informacion_boleto = str(resultado[2])
            estado = self.estado_boleto
            text = "[{}] Boleto encontrado".format(time.strftime("%Y-%m-%d %H:%M:%S"))
            print(colored(text, 'blue'))
        '''
        leerArch = open(ruta+"../../sys/descuento.txt", "r")
        sello=leerArch.readline().rstrip("\n")
        print("sellado =",sello)
        if(int(sello) == 1):
            descuento=2
        else:
            descuento=1
        leerArch.close()
        leerArch = open(ruta+"../../sys/descuento.txt", "w")
        leerArch.write('0')
        leerArch.close()
            #Verificando sello de boleto Fin
        '''
        # [1] No pagado
        # [2] Pagado, tiempo restante
        # [3] Excedido, fecha ultimo pago
        # [4] Obsoleto

        if int(estado)==1:
            tarifa = self.calcular_tarifa(self.hora_entrada,self.fecha_entrada, self.descuento)
        if int(estado)==2:
            tiempo_restante = self.informacion_boleto
        if int(estado)==3:
            ultimo_pago = self.informacion_boleto.split(" ",1)
            self.hora_entrada = ultimo_pago[0]
            self.fecha_entrada = ultimo_pago[1]
            self.calcular_tarifa(self.hora_entrada,self.fecha_entrada, self.descuento)
        if int(estado)==4:
            return estado
        return estado
            
    def validar_datos(self,tipo,datos):
        # [1] Boleto
        # [2] Descuento
        # [3] Fecha [AAAA/MM/DD]
        # [4] 
        if tipo == 1:
            try:
                caracter_inicio = datos[:2]
                if('M,' == caracter_inicio or 'L,' == caracter_inicio):
                    if 'M,' == caracter_inicio:
                        datos = datos[0:-1:]   #Retira caracteres de inicio y de fin
                    datos = datos.replace("'","-")
                    datos = datos.replace("Ñ",":")
                    datos = datos.split(',')
                    datos[1] = int(datos[1])
                    datos[2] = int(datos[2])
                    fecha = datetime.strptime(str(datos[3])+" "+str(datos[4]), '%d-%m-%Y %H:%M:%S')
                    self.boleto = datos
                    self.folio = datos[1]
                    self.expedidora = datos[2]
                    self.hora_entrada = datos[4]
                    self.fecha_entrada = self.validar_datos(3,datos[3])
                    return 1
            except:
                return 0
                
        if tipo == 3:
            datos = datos.split(" ",1)
            datos = datos[0].split('-',2)
            fecha_amd = datos[2]+"-"+datos[1]+"-"+datos[0]
            return fecha_amd

    def validar_lectura_boleto(self):
        #self.boleto = "M,60,1,26'03'2020,10Ñ30Ñ12"
        leerArch = open(ruta+"lectura.txt", "r")
        folio=leerArch.readline().rstrip("\n")
        if(folio != ''):
            self.boleto = "M,60,1,14'05'2020,10Ñ30Ñ12"
            datos_validos = self.validar_datos(1,self.boleto)
            if datos_validos:
                print("Boleto detectado: ",self.folio,self.expedidora,self.hora_entrada,self.fecha_entrada)
                self.buscar_boleto()
            else:
                return 0
            leerArch.close()
            leerArch = open(ruta+"lectura.txt", "w")
            leerArch.write('')
            leerArch.close()
            return 1
        else:
            leerArch.close()
            return 0
        
        

    def registrar_pago(self):
        #------------------------------- Registrar pago en servidor
        print("Solocitando registro del pago ")
        codigo_registro = False
        codigo = 0
        respuestaServidor = 0
        if self.cancelar_pago:
            print("Operacion cancelada")
            codigo = 5
        else:
            if self.servidor.estado_servidor:
                mensaje = "{},{},{} {}*{};1;{};{};{};{};{}".format(self.folio,self.expedidora,self.fecha_entrada,self.hora_entrada,self.equipo[0]['numero'],self.monto_ingresar,"0:0","0:0","0:0",self.tarifa_seleccionada)
                respuestaServidor = self.servidor.configSocket("pago boleto", mensaje)
                if respuestaServidor == -1:
                    text = "[{}] [Error4] No se pudo registrar en servidor".format(time.strftime("%Y-%m-%d %H:%M:%S"))
                    print(colored(text, 'red'))
                else:
                    codigo_registro = 1
                    text = "[{}] Pago registrado".format(time.strftime("%Y-%m-%d %H:%M:%S"))
                    print(colored(text, 'blue'))
            else:
                text = "[{}] [Error2] Sin conexion a servidor, No se registro el boleto".format(time.strftime("%Y-%m-%d %H:%M:%S"))
                print(colored(text, 'red'))
                respuestaServidor = 0

        
        #------------------------------- Registrar pago interno
        body = {
        "folio_boleto": self.folio,
        "expedidor_boleto": self.expedidora,
        "fecha_expedicion_boleto": " {}T{}Z".format(self.fecha_entrada,self.hora_entrada),
        "codigo": codigo,
        "registrado": codigo_registro,
        "monto": self.monto_ingresar,
        "cambio": self.monto_a_dispensar,
        "monedas": "0:0",
        "billetes": "0:0",
        "cambio_entregado": "0:0",
        "equipo_id": 1
        }
        metodo = "POST"
        self.api.establecer_url('http://127.0.0.1:8000/api/transaccion/')
        self.api.establecer_metodo(metodo)
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        print("Metodo....: ",self.api.obtener_metodo({'Content-Type': 'application/json'}))
        response = self.api.enviar(Interfaz.PROCESO,body)
        print("Respuesta: ",response)

    def reiniciar_variables(self):
        #-------------------- Secuencia cobro
        self.secuencia_cobro = 0
        self.monto_ingresar = 0
        self.monto_ingresado = 0
        self.monto_a_dispensar = 0
        self.descuento = 0
        self.cancelar_pago = 0
        self.tarifa_seleccionada = 0

        #-------------------- Secuencia lectura boleto
        self.boleto = ""
        self.folio= ""
        self.expedidora = ""
        self.hora_entrada = ""
        self.fecha_entrada = ""
        self.tiempo_estacionado = ""
        
    def ejecutar_programa(self):
        pass
    def secuencia_error(self):
        return 1
    def secuencia_cancelacion(self):
        return 1
    def finalizar_operacion(self):
        self.registrar_pago()
        self.reiniciar_variables()
        return 1
    def cajero_suspendido(self):
        return 1

    def habilitar_dispositivos_cobro(self):
        self.listaDeVariables.dispositivos[0].ejecutarInstruccion(self.listaDeVariables.dispositivos[0].MONEDERO_HABILITAR)
        self.listaDeVariables.dispositivos[1].ejecutarInstruccion(self.listaDeVariables.dispositivos[1].BILLETERO_HABILITAR)
    def deshabilitar_dispositivos_cobro(self):
        self.listaDeVariables.dispositivos[0].ejecutarInstruccion(self.listaDeVariables.dispositivos[0].MONEDERO_DESHABILITAR)
        self.listaDeVariables.dispositivos[1].ejecutarInstruccion(self.listaDeVariables.dispositivos[1].BILLETERO_DESHABILITAR)
        
    def deshabilitar_dispositivos_cobro2(self):
        i = 0
        direccion_dispositivo = 0
        for i,dispositivo_seleccionado in enumerate(self.dispositivo):
            if dispositivo_seleccionado['tipo'] == "ACEPTADOR" or dispositivo_seleccionado['tipo'] == "RECICLADOR":
                if dispositivo_seleccionado['activo'] == True:
                    direccion_dispositivo = dispositivo_seleccionado['direccion']
                    self.listaDeVariables.dispositivos[direccion_dispositivo].ejecutarInstruccion(self.listaDeVariables.dispositivos[direccion_dispositivo].DESHABILITAR)
                    print("Dispositivo Habilitado: {} {} ".format(dispositivo_seleccionado['nombre'],dispositivo_seleccionado['direccion']))
    
    def habilitar_dispositivos_cobro2(self):
        i = 0
        direccion_dispositivo = 0
        for i,dispositivo_seleccionado in enumerate(self.dispositivo):
            if dispositivo_seleccionado['tipo'] == "ACEPTADOR" or dispositivo_seleccionado['tipo'] == "RECICLADOR":
                if dispositivo_seleccionado['activo'] == True:
                    direccion_dispositivo = dispositivo_seleccionado['direccion']
                    self.listaDeVariables.dispositivos[direccion_dispositivo].ejecutarInstruccion(self.listaDeVariables.dispositivos[direccion_dispositivo].HABILITAR)
                    print("Dispositivo Habilitado: {} {} ".format(dispositivo_seleccionado['nombre'],dispositivo_seleccionado['direccion']))


    def dispensar_cambio2(self,cambio_solicitado):
        print("------------- Cambio Solicitado: ",cambio_solicitado,"-------------------")
        cambio = 0
        i = 0
        direccion_dispositivo = 0
        cambioRestante = cambio_solicitado
        for i,dispositivo_seleccionado in enumerate(self.dispositivo):
            if dispositivo_seleccionado['tipo'] == "DISPENSADOR" or dispositivo_seleccionado['tipo'] == "RECICLADOR":
                if dispositivo_seleccionado['activo'] == True:
                    direccion_dispositivo = dispositivo_seleccionado['direccion']
                    denominaciones = dispositivo_seleccionado['numero_serie']
                    denominaciones = denominaciones.split(".")
                    for denominacion in denominaciones:
                        denominacion = int(denominacion)
                        cambio = int(cambio_solicitado/denominacion)
                        if(cambio):
                            cambio_solicitado = cambio_solicitado%denominacion
                            #self.listaDeVariables.dispositivos[6].ejecutarInstruccion(self.listaDeVariables.dispositivos[6].DISPENSAR,cambio,denominacion)
                            cambioRestante = cambioRestante - (cambio*denominacion)
                            print("Dispositivo seleccionado: {} Direccion: {} ".format(dispositivo_seleccionado['nombre'],dispositivo_seleccionado['direccion']))
                            print("Cambio entregado:  {} unidad(es) de {} = ${} ".format(cambio,denominacion,cambio*denominacion))
                            #print("Cambio restante: ${} ".format(cambioRestante))

        print("Secuencia cambio finalizada")





    def solicitarCambio(cambioSolicitado):
        global PAY_OUT_JCM,SECUENCIA_COBRO
        #cambioSolicitado = 177
        cambioEntregado10 = 0
        cambioEntregado5 = 0
        cambioEntregado1 = 0
        monedasDispensadas = 0
        estatus = 0
        
        HOPPER_MONEDAS_SOLICITADAS = {10:0,5:0,1:0}
        HOPPER_MONEDAS_DISPENSADAS = {10:0,5:0,1:0}
        MONEDAS = [10,5,1]
        BILLETES = [100,50]
        cambioRestante = cambioSolicitado
        i = 0
        print("------------- Cambio Solicitado: ",cambioSolicitado,"-------------------")

        for billete in BILLETES:
            repeticiones = BILLETES.count(billete)
            i = i +1 
            cambio = int(cambioSolicitado/billete)

            if(cambio):

                cambioSolicitado = cambioSolicitado%billete
                
                ###PAY_OUT_JCM = [252, 9, 240, 32, 74, cambio, i]
                ###SECUENCIA_COBRO = 2

                self.listaDeVariables.dispositivos[6].ejecutarInstruccion(self.listaDeVariables.dispositivos[6].DISPENSAR,cambio,bilelte)
                
                print('cambio en billetes de ',billete,' : ', cambio,'cambioSolicitado',cambioSolicitado)
                cambioRestante = cambioRestante - (cambio*billete)


        i = 0
        for moneda in MONEDAS:
            repeticiones = MONEDAS.count(moneda)
            i = i +1 
            #print("reps: ",repeticiones, "iteracion: ", i)
            if(repeticiones > 2):

                #count(ser)
                break
                #exit(0)
                pass
            
            
            #print("Cambio Solicitado: ",cambioSolicitado)
            #print(moneda,cambio)
            cambio = int(cambioSolicitado/moneda)
            if(cambio):
                cambioSolicitado = cambioSolicitado%moneda
                print("\nMonedas solicitadas de ",moneda,": ",cambio)
                codigoCambio = cambioHopper(cambio,HOPPER_MONEDAS_HABILITADAS[moneda])
                dispensandoCambio = 1
                if codigoCambio == [0]:
                    while(dispensandoCambio):
                        time.sleep(.3)
                        estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                        if estatus:
                            if estatus[1]:
                                #cambioRestante = (estatus[1]*moneda)+cambioSolicitado
                                print("*Entrgando Cambio*",(estatus[1]*moneda)+cambioSolicitado,"Restante")
                            else:
                                dispensandoCambio = 0
                    if estatus:
                        if estatus[0]:
                            monedasPorPagar = estatus[1]
                            monedasDispensadas = estatus[2]
                            monedasFaltantes = estatus[3]
                            if monedasFaltantes:
                                MONEDAS.append(moneda)
                                cambioSolicitado = cambioSolicitado + (monedasFaltantes*moneda)
                                #print("monedas por pagar de ",moneda,": ",monedasPorPagar)
                                print("monedas enrtegadas de ",moneda,": ",monedasDispensadas)
                                cambioRestante = cambioRestante - (monedasDispensadas*moneda)
                                print("Cambio incompleto , faltan ",monedasFaltantes," de $",moneda, "Restante: ",cambioRestante)
                                resetHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                                habilitarHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                            else:
                                #print("monedas pendientes en el pago de ",moneda,": ",monedasDispensadas)
                                cambioRestante = cambioRestante - (monedasDispensadas*moneda)
                                print("monedas enrtegadas de ",moneda,": ",monedasDispensadas)
                                print("monedas faltantes: ",monedasFaltantes," monedas",MONEDAS,"Cambio Restante:",cambioRestante)
                                #HOPPER_MONEDAS_DISPENSADAS.update({})

                        else: 
                            print("Hopper ",HOPPER_MONEDAS_HABILITADAS[moneda],"No puede dar cambio: Deshabilitado")

                    else:
                        print("No se pudo obtener el status")
                else:
                        resetHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                        habilitarHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                        print("No se entrego el cambio, Hopper",HOPPER_MONEDAS_HABILITADAS[moneda],"Deshabilitado,","Faltaron",cambio,"monedas de $",moneda)
                        #cambioRestante = cambioRestante+(cambio*moneda)


                #-------------VERIFICACION FINAL DEL STATUSHOPPER ---------------
                

                '''
                estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                print("ultima moneda: ",moneda,cambioSolicitado,estatus,estatus[1],cambioSolicitado)
                if estatus:
                    if estatus[3]:
                        cambioRestante = (estatus[3]*moneda)+cambioSolicitado
                        resetHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                        habilitarHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                        print("Cambio restante...: ",cambioRestante,"Reiniciando hopper")
                    else:
                        if estatus[0]:

                            cambioRestante = (estatus[3]*moneda)+cambioSolicitado
                            print("Cambio restante...: ",cambioRestante,"est0")
                            pass
                        else:
                            print("Cambio restante...: ",cambioRestante,"Reiniciando")
                            resetHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                            habilitarHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
                '''


                print("Cambio restante...: ",cambioRestante)
            
        print("Cambio restante: ",cambioRestante)
        return cambioRestante
    
    def restar_hora(self,horab,fechab):
        horab = horab.split(':',2)
        fechab = fechab.split('-')
        fechaBoleto = datetime.strptime(str(fechab[0]) + str(fechab[1]) + str(fechab[2]), '%Y%m%d').date()
        horaBoleto = datetime.strptime(str(horab[0]) +':'+str(horab[1]) +':'+ str(horab[2]), '%H:%M:%S').time()
        fechaActual=datetime.now().date()
        horaActual=datetime.now().time()
        horayFechaBoleto = datetime.now().combine(fechaBoleto, horaBoleto)
        horayFechaActual = datetime.now().combine(fechaActual, horaActual)
        restaFechas = horayFechaActual - horayFechaBoleto
        aux_dif=(str(restaFechas).split('.',1))[0]
        dias = int(restaFechas.days)
        segundos = restaFechas.seconds 
        return dias,segundos,aux_dif

    
    def generar_corte(self,fecha_1,hora_1,fecha_2,hora_2):
        fecha_1 = "28-04-2020"
        hora_1 = "19:14:18"
        fecha_2 = "29-04-2021"
        hora_2 = "19:17:18"
        body = ""
        url = "http://127.0.0.1:8000/api/corte?f1={0}&h1={1}&f2={2}&h2={3}".format(fecha_1,hora_1,fecha_2,hora_2)
        self.api.establecer_url(url)
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        response = self.api.enviar(Interfaz.PROCESO,body)
        print("#-------------------Prueba Corte: ",response)
        print("Exitosos: ",response['exitosos'])
        print("Incidencias: ",response['incidencias'])
        print("Cancelados: ",response['cancelados'])
        print("Ingreso total: ",response['ingreso'])


class EjecutarPrograma():
    def __init__(self, listaDeVariables):

        self.listaDeVariables = listaDeVariables

        self.TON_01 = Temporizador("TON_01",0.5)
        self.TON_02 = Temporizador("TON_02",0.5)
        self.TON_03 = Temporizador("TON_03",2)
        self.TON_04 = Temporizador("TON_04",15)

        self.aux = 0
        self.aux_2 = 0

        tarea1 = threading.Thread(target=self.run)
        tarea1.start()

    def run (self):
        self.funcionando = True

        while (self.funcionando):
            self.TON_02.entrada = not self.TON_02.salida
            self.TON_02.actualizar()

            if self.TON_02.salida:
                """
                print ("\n", end='')
                self.listaDeVariables.imprimirX(8)
                print ("", end="\t")
                self.listaDeVariables.imprimirY(8)
                print ("", end="\t")
                self.listaDeVariables.imprimirZ()
                print ("", end=" ")
                """

                self.TON_01.entrada = self.aux
                self.TON_01.actualizar()

                if self.TON_01.salida:
                    self.aux = 0
                
                if self.listaDeVariables.X[3].obtenerValor() and not self.aux:
                    #print ("Se enviara instruccion")
                    
                    #self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_IMPRIMIR)
                    self.listaDeVariables.dispositivos[0].ejecutarInstruccion(self.listaDeVariables.dispositivos[0].MONEDERO_SOLICITAR_CAMBIO, 2)
                    self.aux = 1
                
                

                
            self.TON_03.entrada = not self.TON_03.salida
            self.TON_03.actualizar()    

            if self.TON_03.salida:
                
                

                
                # print (">>>>>>>>>>>>>>>>>>>>>>>>>Cambiando Estado", end='', flush=True)
                # print (">>>>>>>>>>>>>>>>>>>>>>>>>Valor actual ", self.listaDeVariables.Y[3].obtenerValor())

                # self.listaDeVariables.Y[3].establecerValor(not self.listaDeVariables.Y[3].obtenerValor())

                


                pass

            
            self.TON_04.entrada = not self.TON_04.salida
            self.TON_04.actualizar()

            if self.TON_04.salida:
                print ("Se activo TON_04")


                if self.aux_2:
                    self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_HABILITAR)
                    self.listaDeVariables.dispositivos[1].ejecutarInstruccion(Billetero.BILLETERO_HABILITAR)

                    self.aux_2 = 0

                else:
                    self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_DESHABILITAR)
                    self.listaDeVariables.dispositivos[1].ejecutarInstruccion(Billetero.BILLETERO_DESHABILITAR)
                    self.aux_2 = 1



                # for variable in self.listaDeVariables.dispositivos[0].variables:
                #     print ("{} {} {}".format(variable.obtenerTag().ljust(6), variable.obtenerNombre().ljust( 25 ), str(variable.obtenerValor()).ljust( 10 )))

                



def main():
    variables = ListaDeVariables()
    Cajero(variables)

if __name__ == "__main__":
    main()
