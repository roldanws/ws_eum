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
from Monitor.Comunicacion import Comunicacion

from Monitor.PuertoSerie import PuertoSerie
from Monitor.Hopper import Hopper
from Monitor.Monedero import Monedero
from Monitor.Billetero import Billetero
from Monitor.Controladora import Controladora,ListaDeVariables



raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"../..")
sys.path.append(raiz)





import Conexiones.cliente as Servidor
from Conexiones.Conexiones import Conexiones

'''DL17'''
from encriptacionQR import codificar
from configParser.viewData import viewData
'''DL17'''


from Interfaz import Interfaz
#from Scanner import Scanner


class Cajero:
    """
    Clase utulizada para administrar el cajero
    """
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
        self.controladora = ""
        #-------------------- Diccionatrios
        self.informacion = "" 
        self.variables = "" 

        self.interfaz = ""
        self.inicializar()
        #-------------------- Secuencia cobro
        self.secuencia_cobro = 0
        self.monto_ingresar = 0
        self.monto_ingresado = 0
        self.monto_a_dispensar = 0
        self.descuento = 0

        #-------------------- Secuencia lectura boleto
        self.boleto = ""
        self.folio= ""
        self.expedidora = ""
        self.hora_entrada = ""
        self.fecha_entrada = ""
        self.tiempo_total = ""

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
            if self.secuencia_cobro == 0:
                #-------------------- Validar lectura de boleto
                boleto_valido = self.validar_lectura_boleto()
                if boleto_valido == 1:
                    self.secuencia_cobro = 1
                else:
                    self.secuencia_cobro = 0

            if self.secuencia_cobro == 1:
                #-------------------- Validar estado de dispositivos
                validacion = self.validar_estado_dispositivos()
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
                    self.secuencia_cobro = 7
                else:
                    self.secuencia_cobro = 5
                
            if self.secuencia_cobro == 5:
                #-------------------- Operacion no valida: Entregar comprobante de error y pedir asistencia
                combrobante_error = self.secuencia_error()
                if combrobante_error == 1:
                    self.secuencia_cobro = 7
                else:
                    print("No se pudo expedir el comprobante de error")

            if self.secuencia_cobro == 7:
                #-------------------- Cajero suspendido
                self.cajero_suspendido()

            if self.secuencia_cobro == 8:
                #-------------------- Ofrecer ticket , registrar operacion y reiniciar valores
                operacion_finalizada = self.finalizar_operacion()
                self.secuencia_cobro = 0


            fecha = time.strftime("%Y-%m-%d %H:%M:%S")
            
            


            self.variables.update(monto_ingresar=self.monto_ingresar)
            self.variables.update(monto_ingresado=self.monto_ingresado)
            self.variables.update(monto_a_dispensar=self.monto_a_dispensar)
            self.variables.update(folio=self.folio)
            self.variables.update(hora_entrada=self.hora_entrada)
            self.variables.update(tiempo_total=self.tiempo_total)
            self.variables.update(descuento=self.descuento)
            self.variables.update(fecha=fecha)
            
            #sensores.update(monto=i)
            #response = cajero.enviar(informacion)
            response = self.enviar(self.variables)


            print(response)



    def inicializar(self):
        
        shutil.copy(ruta+"configParser/configuracion.ini", ruta+"configParser/configuracion_respaldo.ini")
        shutil.copy(ruta+"configParser/sensores.ini", ruta+"configParser/sensores_respaldo.ini")

        self.tipo_controladora = 0
        #-------------------- Leer configuracion        
        self.vizualizar = viewData('configuracion.ini')
        self.leer_configuracion()
        #-------------------- Modo operacion 
        self.controladora = self.establecerControladora(self.listaDeVariables)
        #-------------------- Establecer interfaz 
        self.interfaz = Interfaz('http://127.0.0.1:8000/hook/',{'Content-Type': 'application/json'})
        self.interfaz.establecer_lista_de_variables(self.listaDeVariables)

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
        tiempo_total = "",
        interfaz = 1,
        descuento = 0,
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


    #def establecerControladora(self,listaDeVariables): 
    def establecerControladora(self,tipo): 
        if self.tipo_controladora == 0:
            #controladora = Controladora(listaDeVariable s, tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO)
            controladora = Controladora(self.listaDeVariables, 
                tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO,
                tipoDeControladora = Controladora.CONTROLADORA_PARA_CAJERO)

        if self.tipo_controladora == 1 :
            controladora = Controladora(listaDeVariables, tarjeta = Controladora.TARJETA_DE_PULSO)
        if self.tipo_controladora == 2 :
            controladora = Controladora(listaDeVariables, tarjeta = Controladora.TARJETA_DE_INTERFAZ_BLANCA)
        if self.tipo_controladora == 3 :
            controladora = Controladora(listaDeVariables, tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO)
        return controladora

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

    def enviar(self,datos):
        self.interfaz.enviar(Interfaz.PROCESO,datos)
        print(self.interfaz.response)
        return self.interfaz.response
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

        self.monto_a_dispensar = self.monto_ingresar - self.monto_ingresado
        print("Monto ingresado:",self.monto_ingresado)
        print("Diferencia monto:",self.monto_a_dispensar)
        return self.monto_a_dispensar
        
    def probar(self):
        return 0
    def validar_estado_dispositivos(self):
        return 1
    def validar_operacion(self):
        if self.monto_a_dispensar:
            self.dispensar_dinero(self.monto_a_dispensar)
        return 1

    def calcular_tarifa(self):
        horaBoleto=self.hora_entrada.split(':',2)
        fechaAMD=self.fecha_entrada.split('-')
        print(fechaAMD)
        fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]
        dh=self.restar_hora(horaBoleto,fechaAMD.split('-'))
        dias=dh[0]
        horas=dh[1]
        tiempo_total=dh[2]
        print("Tiempo_total: ",dias,horas)
        self.tiempo_total = tiempo_total
        #self.tiempo_total = str(dias)+" "+str(horas)
        self.monto_ingresar = 15

    def recargar(self):
        return 0
    def dispensar_dinero(self,monto):
        self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_DAR_CAMBIO, monto)
    def recibir_dinero(self):
        return 1
        #self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Monedero.MONEDERO_DAR_CAMBIO, monto)
    def validar_lectura_boleto(self):
        #self.boleto = "M,60,1,26'03'2020,10Ñ30Ñ12"
        leerArch = open(ruta+"lectura.txt", "r")
        folio=leerArch.readline().rstrip("\n")
        if(folio != ''):
            self.boleto = "M,60,1,26'03'2020,10Ñ30Ñ12"
            self.boleto = self.boleto.replace("'",'-')
            self.boleto = self.boleto.replace("Ñ",':')
            boleto_tmp = self.boleto.split(',')
            self.folio = boleto_tmp[1]
            self.expedidora = boleto_tmp[2]
            self.hora_entrada = boleto_tmp[4]
            self.fecha_entrada = boleto_tmp[3]
            print("Boleto detectado: ",self.boleto)
            print("Folio: ",self.folio,self.expedidora,self.hora_entrada,self.fecha_entrada)
            self.calcular_tarifa()
            leerArch.close()
            leerArch = open(ruta+"lectura.txt", "w")
            leerArch.write('')
            leerArch.close()
            return 1
        else:
            leerArch.close()
            return 0
        

        
    def registrar_pago(self):
        return 1
    def ejecutar_programa(self):
        pass
    def secuencia_error(self):
        return 1
    def finalizar_operacion(self):
        return 1
    def cajero_suspendido(self):
        return 1
    def deshabilitar_dispositivos_cobro(self):
        self.listaDeVariables.dispositivos[0].ejecutarInstruccion(self.listaDeVariables.dispositivos[0].MONEDERO_DESHABILITAR)
        self.listaDeVariables.dispositivos[1].ejecutarInstruccion(self.listaDeVariables.dispositivos[1].BILLETERO_DESHABILITAR)
    def habilitar_dispositivos_cobro(self):
        self.listaDeVariables.dispositivos[0].ejecutarInstruccion(self.listaDeVariables.dispositivos[0].MONEDERO_HABILITAR)
        self.listaDeVariables.dispositivos[1].ejecutarInstruccion(self.listaDeVariables.dispositivos[1].BILLETERO_HABILITAR)
    
    def restar_hora(self,horab,fechab):
        fechaBoleto = datetime.strptime(str(fechab[0]) + str(fechab[1]) + str(fechab[2]), '%Y%m%d').date()
        horaBoleto = datetime.strptime(str(horab[0]) +':'+str(horab[1]) +':'+ str(horab[2]), '%H:%M:%S').time()
        fechaActual=datetime.now().date()
        horaActual=datetime.now().time()
        horayFechaBoleto = datetime.now().combine(fechaBoleto, horaBoleto)
        horayFechaActual = datetime.now().combine(fechaActual, horaActual)
        restaFechas = horayFechaActual - horayFechaBoleto
        aux_dif=(str(restaFechas).split('.',1))[0]
        
        dias = int(restaFechas.days)
        horas = int(restaFechas.seconds / 3600)
        print("****RES:",restaFechas)
        return dias,horas,aux_dif

    



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
    #interfazDeVariables = InterfazDeVariables(variables.X)
    #interfazDeVariables = InterfazDeVariables(variables.dispositivos[0].variables)
    '''
    informacion = dict (
        interfaz = 0,
        X_01 = variables.dispositivos[0].variables[1].obtenerValor(),
        X_02 = variables.dispositivos[0].variables[2].obtenerValor(),
        X_03 = variables.dispositivos[0].variables[3].obtenerValor(),
        X_04 = variables.dispositivos[0].variables[4].obtenerValor(),
        X_05 = variables.dispositivos[0].variables[5].obtenerValor(),
        X_06 = variables.dispositivos[0].variables[6].obtenerValor(),
        X_07 = variables.dispositivos[0].variables[7].obtenerValor(),
        )
    sensores = dict (
        X_08 = variables.dispositivos[0].variables[8].obtenerValor(),
        X_09 = variables.dispositivos[0].variables[9].obtenerValor(),
        X_10 = variables.dispositivos[0].variables[10].obtenerValor(),
        X_11 = variables.dispositivos[0].variables[11].obtenerValor(),
        X_12 = variables.dispositivos[0].variables[12].obtenerValor(),
        X_13 = variables.dispositivos[0].variables[13].obtenerValor(),
        X_14 = variables.dispositivos[0].variables[14].obtenerValor(),
        X_15 = variables.dispositivos[0].variables[15].obtenerValor(),
        X_16 = variables.dispositivos[0].variables[16].obtenerValor(),
        X_17 = variables.dispositivos[0].variables[17].obtenerValor(),
        X_18 = variables.dispositivos[0].variables[18].obtenerValor(),
        X_19 = variables.dispositivos[0].variables[19].obtenerValor(),
        X_20 = variables.dispositivos[0].variables[20].obtenerValor(),
        X_21 = variables.dispositivos[0].variables[21].obtenerValor(),
        X_22 = variables.dispositivos[0].variables[22].obtenerValor(),

        )

    datos = dict (
        interfaz = 0,
        test = 0
        )
    
    
    print(informacion)
    print(sensores)
    cajero = Cajero(variables)
    
    #ejecutarPrograma = EjecutarPrograma(variables)

    
    i = 0
    while(1):
        i = i+1
        time.sleep(2)
        fecha = time.strftime("%Y-%m-%d %H:%M:%S")
        sensores.update(fecha=fecha)
        sensores.update(interfaz=2)
        #sensores.update(monto=i)
        #response = cajero.enviar(informacion)
        response = cajero.enviar(sensores)
        #response = cajero.enviar(datos)
        print(response)
    '''
if __name__ == "__main__":
    main()
