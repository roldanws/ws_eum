# coding=latin-1

# Parte del Modelo para el programa de comunicación 
# Desarrollado por Sigfrido Oscar Soria Frias
# En Estacionamientos Únicos de México

import os
import threading
import time
#import tkinter
from tkinter import *

from Interfaz import Interfaz
from VariablesMicro import VariablesMicro

from PuertoSerie import PuertoSerie, PuertoInterfazGrafica
from ProtocoloMDB import ProtocoloMDB, ProtocoloMDBInterfaz
from ProtocoloCCTALK import ProtocoloCCTALK, ProtocoloCCTALKInterfaz
from Comunicacion import Comunicacion


ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(ruta)

from Variables.Temporizador import Temporizador


ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class Controlador ():
    PUERTO_SERIE = "puertoSerie"
    PUERTO_ETHERNET = "puertoEthernet"
    
    #puertoSerie = PuertoSerie("Puerto Serie")
    #puertoSerie = ""
    
    def __init__ (self):
        print ("Inicio")

        self.root = Tk()
        
        #self.root.option_readfile (ruta + "/" + "../../Opciones/optionDB")
        self.root.title ('Software de monitoreo')

        
        #self.root = tkinter.Tk()
        """
        img = Image.open ("../Imagenes/Icono-01.png")
        imgicon = ImageTk.PhotoImage(img)
        self.root.call('wm','iconphoto',self.root._w,imgicon)
        """
        
        
        self.protocoloMDB = ProtocoloMDB ("protocolo MDB")
        self.protocoloMDBInterfaz = ProtocoloMDBInterfaz(self.protocoloMDB)
        
        self.protocoloCCTALK = ProtocoloCCTALK ("protocolo CCTALK")
        self.protocoloCCTALKInterfaz = ProtocoloCCTALKInterfaz(self.protocoloCCTALK)

        
        
        self.comunicacion = Comunicacion ()
        
        
        self.listadePuertos = []
        
        self.listadePuertos.append(PuertoSerie("Puerto Serie"))
        self.puertoInterfazGrafica = PuertoInterfazGrafica (self.listadePuertos[0])
        self.listadePuertos[0].establecerComunicacion (self.comunicacion)
        self.listadePuertos[0].establecerProtocoloDeComunicacion (self.protocoloMDB)
        self.listadePuertos[0].establecerProtocoloDeComunicacion_02 (self.protocoloCCTALK)
        
        #self.protocoloCCTALK.establecerPuerto(self.listadePuertos[0])
        self.listadePuertos[0].start()
        
        self.listadePuertos.append(PuertoSerie("Puerto Serie2"))
        self.puertoInterfazGrafica = PuertoInterfazGrafica (self.listadePuertos[1])
        self.listadePuertos[1].start()

        self.interfaz = Interfaz (self.root, self)
        self.listadePuertos[0].establecerMensajero1 (self.interfaz.escribirMensajero1)
        self.listadePuertos[0].establecerMensajero2 (self.interfaz.escribirMensajero2)
        
        self.listadePuertos[1].establecerMensajero1 (self.interfaz.escribirMensajero1)
        self.listadePuertos[1].establecerMensajero2 (self.interfaz.escribirMensajero2)
        



        
        

        #self.__puerto = self.PUERTO_ETHERNET
        #self.__protocolo = ProtocoloMDB ()
        #self.puertoSerie.establecerProtocolo (self.__protocolo)


        
        self.variableMicro = VariablesMicro()
        self.actualizarVariables = ActualizarVariables (nombre = "Actualizar Variables", objeto =self.variableMicro, controlador = self)
        self.actualizarVariables.start()
        

        self.interfaz.mainloop()
        
        
    def terminarAplicacion (self):
        #self.cerrarPuerto()
        #self.puertoSerie.detener()
        for i, puerto in enumerate (self.listadePuertos):
            self.listadePuertos[i].cerrarPuerto()
            self.listadePuertos[i].detenerHilo()
            time.sleep(0.3)
            
        self.actualizarVariables.detener()
        self.terminarCiclo()
        time.sleep (0.7)
        
        self.root.destroy()
        #exit()
       
    """
    def abrirPuerto (self, puerto, baud, paridad):
        self.puertoSerie.abrirPuerto(puerto, baud)
        
    def cerrarPuerto (self):
        self.puertoSerie.cerrarPuerto()
    """    
    def enviarDatos  (self, mensaje, opcion = "TEXTO"):
        if opcion == "TEXTO":

#        print ("Se enviardon datos Inicio %s" % mensaje)
            self.puertoSerie.enviarTexto(mensaje)
        else :
            self.puertoSerie.enviarDatos(mensaje)

    def obtenerListaDePuertos(self):

        a = self.puertoSerie.obtenerListaDePuertos ()



        return a

    def puertoSerieSeleccionado (self):
        if self.__puerto == self.PUERTO_SERIE:
            return True
        else: 
            return False

    def escribirMensajero1 (self):
        self.puertoSerie.establecerMensajero (self.interfaz.obtenerAreaEntrada())

    def escribirMensajero2 (self):
        self.puertoSerie.establecerMensajero2 (self.interfaz.obtenerAreaEntrada())
    
    
    
    def iniciarCiclo (self, mensaje):
        self.hilo =  threading.Thread (name = 'hilo', target  = self.ciclo, kwargs={'valor':mensaje})
        self.estadoHilo = True
        self.hilo.start()
        print ("Iniciar ciclo %s" %mensaje)
    
    def terminarCiclo (self):
        self.estadoHilo = False
        print ("Terminar ciclo")
        
    def ciclo (self, **datos):
        while self.estadoHilo:
            #print("Dentro de ciclo %s" % datos['valor'])
#            print ("Dentro de ciclo %d %s" %(num_hilo, datos['mensaje'])
            self.puertoSerie.enviarDatos(datos['valor'])
            time.sleep(0.1)
            
    def enviarDatosProtocolo(self, datos):
        self.puertoSerie.enviarDatosProtocolo (datos)
        
    def iniciarMDB(self):
        self.puertoSerie.iniciarMDB()



class ActualizarVariables (threading.Thread):
    def __init__(self, nombre = None, objeto = None, controlador = None, args=()):
        threading.Thread.__init__ (self, name = nombre)
        
        self.controlador = controlador

        self.contador = 0
        
        self.TON_00 = Temporizador("TON_00", 0.1)        
        self.TON_01 = Temporizador("TON_01", 0.5)

    def run (self):
        self.funcionando = True
        while (self.funcionando):
            
            self.TON_00.entrada = not self.TON_00.salida
            self.TON_00.actualizar()
            if self.TON_00.salida and self.contador < 100:
                self.contador += 1
                
                if self.contador == 2:
                    self.controlador.interfaz.notebook.selectpage(2)
                    self.controlador.interfaz.notebook.selectpage(1)
                    self.controlador.interfaz.notebook.selectpage(0)
                
                #print ("Imprimiendo contador %d" %self.contador)

            self.TON_01.entrada = not self.TON_01.salida
            self.TON_01.actualizar()
            if self.TON_01.salida:
                pass
                #TODO: actualizarFecha()

            
            time.sleep(0.001)
                
            
        print ("Hilo terminado", self.name)

    def detener (self):
        self.funcionando = False




def main ():
    Controlador()


if __name__ == "__main__":
    main ()
