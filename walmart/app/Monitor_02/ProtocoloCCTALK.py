
__author__ = "PRUEBA"
__date__ = "$09-ago-2019 14:37:20$"

import threading
import time

from tkinter import *
from tkinter import ttk

from Comunicacion import Comunicacion


import os
ruta = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ruta)


class ProtocoloCCTALK ():
    def __init__(self, nombre):
        
        self.establecerNombre (nombre)
        self.listaDeInterfaces = []
        
        self.idEnviarDatosHex =  StringVar(value="")
        
        
 
    def establecerNombre (self, nombre):
        self.nombre = nombre
        
    def obtenerNombre (self):
        return self.nombre
    
    
    
    def __str__(self):
        return self.obtenerNombre()
    
    def establecerPuerto (self, puerto):
        self.puerto = puerto    
    
    def establecerInterfaz (self, interfaz):
        self.listaDeInterfaces.append(interfaz)
    
    def obtenerInterfaz(self, indice):
        if indice < len(self.listaDeInterfaces):
            return self.listaDeInterfaces[indice]    
    
    def enviarInstruccion_4 (self):
        a = self.puerto.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [2, 1])
        
        self.puerto.enviarBytes(a);
        
    def enviarDatos (self, datos):
        
        print ("DEntro de enviarDatos")
        aux1= datos
        aux2 = 0
        i = 0
        while True:
            aux1 = int (aux1 / 256)
            i += 1
            #print ("%s %s %d" %(aux1, datos, i))
            if aux1 < 1:
                break
        mensaje = datos.to_bytes(i, byteorder='big')
        
        print ("El mensa es", mensaje)
        b  =  []
        for i in mensaje:
            print (i)
            b.append (i)
            
        print (b)
        
        
        a = self.puerto.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, mensaje)
        self.puerto.enviarBytes(a)
        
        print ("Boton enviar")
        #TODO: Agregar moficación para la comunicación con arduino
        
        
        
    
        
        
class ProtocoloCCTALKInterfaz ():
    def __init__(self, protocolo):
        self.protocolo = protocolo
        protocolo.establecerInterfaz (self)


    def obtenerFrame (self, master):
        
        self.courierFont = "Courier 10"
        self.frame = LabelFrame (master, text ="CCTALK")
        
        self.botonCCTALK = Button ( self.frame, text ="CCTALK", width = 10, command = self.protocolo.enviarInstruccion_4)
        self.botonCCTALK.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.frameHex = self.obtenerFrameEnviarDatosHexadecimal(self.frame)
        self.frameHex.grid (row = 0, column = 2, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        return self.frame

    def obtenerFrameEnviarDatosHexadecimal (self, master):
        self.frameInstruccionesHexadecimal = LabelFrame (master, borderwidth=2, relief="groove", text ="Hexadecimal")
        #self.frameInstruccionesHexadecimal.grid(row = 3, column = 10, rowspan = 1, columnspan = 2 , padx = 5, pady = 5, sticky = E+W)
        #self.frameBotonesConexion.columnconfigure (0, weight = 1)

        self.txtEnviarHexadecimal = Entry (self.frameInstruccionesHexadecimal, name = "txtEnviarDatos", textvariable = self.protocolo.idEnviarDatosHex)
        self.txtEnviarHexadecimal.grid (row = 0, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 8, sticky = E+W+S+N)
        self.txtEnviarHexadecimal.bind("<Return>", self.enviarHexadecimal)
        
        self.botonEnviarHexadecimal = Button ( self.frameInstruccionesHexadecimal, text ="Enviar Hex", width = 10, command = self.enviarHexadecimal)
        self.botonEnviarHexadecimal.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 8, sticky = S+N)

        self.botonEnviarHexadecimalIniciar = Button ( self.frameInstruccionesHexadecimal, text ="Iniciar", width = 10)
        #self.botonEnviarHexadecimalIniciar.grid (row = 0, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

        self.botonEnviarHexadecimalParar = Button ( self.frameInstruccionesHexadecimal, text ="Parar", width = 10)
        #self.botonEnviarHexadecimalParar.grid (row = 0, column = 4, rowspan = 1, columnspan = 1, padx = 5, pady = 5)        
        
        return self.frameInstruccionesHexadecimal


    def enviarHexadecimal (self, *args):
        #self.controlador.enviarDatos(self.txtEnviarDatos.get(), "HEX")
        #print (int (self.txtEnviarHexadecimal.get(), 16))
        
        
        texto = self.txtEnviarHexadecimal.get()
        
        try:
            numero = int (self.txtEnviarHexadecimal.get(), 16)
        except ValueError:
            #self.puerto.enviarMensaje2 ("\nFormato incorrecto >>%s<<" % self.txtEnviarHexadecimal.get())
            #TODO: Enlazar con la interfaz para enviar mensajes
            pass
        else:
            self.protocolo.enviarDatos(numero)
            self.txtEnviarHexadecimal.delete(0, END)
            

        

