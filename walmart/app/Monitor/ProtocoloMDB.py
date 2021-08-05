# coding=utf-8

# Parte del Modelo para el programa de comunicación 
# Desarrollado por Sigfrido Oscar Soria Frias
# En Estacionamientos Únicos de México

import threading
import time

from tkinter import *
from tkinter import ttk

from Comunicacion import Comunicacion


import os
ruta = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ruta)

from Variables.Temporizador import Temporizador



class ProtocoloMDB ():
    def __init__ (self, nombre):
        #threading.Thread.__init__ (self, name = nombre)
        #print ("iniciado Protocolo MDB")
        
        self.establecerNombre (nombre)
        self.listaDeInterfaces = []
        

        self.__estado = 1
        self.comunicacion = Comunicacion ()
        self.cont = 0
        self.bandera = False;
        self.hiloFuncionando = False;
        
        self.TON_00 = Temporizador("TON_00",2)
        self.TON_01 = Temporizador("TON_01",5)
        
        self.idMDB = []

        for i in range (2):
            self.idMDB.append ("")
            
        self.hilo = None
        
        
        self.listaDeElementos = []
        
        
    def establecerPuerto (self, puerto):
        self.puerto = puerto
                
    def establecerInterfaz (self, interfaz):
        self.listaDeInterfaces.append(interfaz)
                
    def obtenerInterfaz(self, indice):
        if indice < len(self.listaDeInterfaces):
            return self.listaDeInterfaces[indice]
                
            
    def activar (self):
        pass
        print ("Desde activar")
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [30, 1, 26, 0])
        print (a)




    def mensajeRecibido (self, mensaje):
        #print ("Recibido %s" % mensaje)
        if len(mensaje) > 0:
            #self.comunicacion.decodificarInstruccion (mensaje)
            self.comunicacion.colocarBytesEnBuffer(mensaje[0])
            self.comunicacion.leerInstruccionesDeBufferSerial()
            
                
    def establecerNombre (self, nombre):
        self.nombre = nombre
        
    def obtenerNombre (self):
        return self.nombre
    
    def __str__(self):
        return self.obtenerNombre()

    def enviarInstruccion_1 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
        self.puerto.enviarBytes(a);
            
    def enviarInstruccion_2 (self):
        parametros = []
        for i, elementos in enumerate (self.listaDeElementos):
            parametros.append(elemento[0])
            parametros.append(elemento[1])
            
        print ("Imprimiendo listaDeElementos>>", parametros)

        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [8, 1, 8, 0])
        self.puerto.enviarBytes(a);
        
        
    def enviarInstruccion_3 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.TEMPERATURA)
        self.puerto.enviarBytes(a);
        
    def enviarInstruccion_4 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS)
        self.puerto.enviarBytes(a);

        
    def agregarElementoDeLista (self, valor, paridad):
        elemento = [valor, paridad]
        self.listadeElementos.append (elemento)
   
    def stopEnEspera (self):
        self.hiloActivado = False;
        
    def detenerHilo (self):
        self.hiloFuncionando = False;
        
    def iniciar (self):
        if not self.hiloFuncionando:
            self.hilo = threading.Thread(target=self.run)
            #threads.append(t)
            self.hilo.start()
        self.hiloActivado = True
        

            
    def run (self):
        self.hiloFuncionando = True;
        self.hiloActivado = True;
        self.cont=0
        contador = 0
        contador_aux = 0
        
        print ("Desde run protocoloMDB")
        
        self.TON_00.entrada = not self.TON_00.salida
        self.TON_00.actualizar()
        
        while self.hiloFuncionando :
            if self.hiloActivado:
            
                if self.puerto.is_Open():


                    self.TON_00.entrada = not self.TON_00.salida
                    self.TON_00.actualizar()

                    if self.TON_00.salida:# and contador < 500:
                        contador = contador + 1;
                        
                        #a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [8, 1, 8, 0])
                        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
                        self.puerto.enviarBytes(a);



                    """

                    if self.__estado == 1:




                        self.bandera = True                    
                        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [8, 1, 8, 0])
                        #a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
                        self.puerto.enviarBytes(a);
                        time.sleep(.1)

                    if self.__estado == 2:
                        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 0, 0, 15, 0])
                        self.puerto.enviarBytes(a);
                        self.bandera = True
                        time.sleep(.1)

                    if self.__estado == 3:
                        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
                        self.puerto.enviarBytes(a);
                        self.disable_coin()
                        time.sleep(200)
                        #self.bandera = True
                        self.__estado = 4
                        print ("Se cambia estado a 4")

                    if self.__estado == 4:
                        self.bandera = True
                        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 5, 0, 20, 0])
                        self.puerto.enviarBytes(a);
                        time.sleep(0.5)

                    if self.__estado == 5:
                        self.bandera = True
                        print("DESHINIBIENDO!---",self.cont)
                        self.enable_coin()
                        time.sleep(1)




                    print ("RUN Estado ", self.__estado, self.bandera);

                    time.sleep(2)
                    """
            else:
                time.sleep(1)
        print ("Protocolo MDB terminado")
    
    
    def disable_coin(self):

        self.puerto.limpiar()
        """
        self.puerto.escribirInstruccion(0x0C, 1)
        self.puerto.escribirInstruccion(0x00, 0)
        self.puerto.escribirInstruccion(0x00, 0)
        self.puerto.escribirInstruccion(0x00, 0)
        self.puerto.escribirInstruccion(0x00, 0)
        self.puerto.escribirInstruccion(0x00, 0)
        """
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [12, 1, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0])
        self.puerto.enviarBytes(a);
        
    def enable_coin(self):
        global mona,mond
        mona=60
        mond=60
        ba = [0x0C, mona, mond]
        ckInt = self.checkSum(ba)
        print("vals...>>>",mona,mond,ckInt)
        #time.sleep(1)
        """
        self.puerto.escribirInstruccion(0x0C, 1)
        self.puerto.escribirInstruccion(0x00, 0)
        self.puerto.escribirInstruccion(self.int_to_bytes(mona, 8), 0)
        self.puerto.escribirInstruccion(0x00, 0)
        self.puerto.escribirInstruccion(self.int_to_bytes(mond, 8), 0)
        self.puerto.escribirInstruccion(self.int_to_bytes(ckInt, 8),0)
        """

        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 0, 0, mona, 0, 0, 0, mond, 0, ckInt, 0])
        self.puerto.enviarBytes(a);
        
    def checkSum(self, arr):
        j=0
        sum=0
        tam=arr.__len__()
        while(j<tam):
            #print(j, tam)
            sum=sum+arr[j]
            j=j+1
        return 255&sum
        
    
class ProtocoloMDBInterfaz ():
    def __init__ (self, protocoloMDB):
        self.protocoloMDB = protocoloMDB
        protocoloMDB.establecerInterfaz (self)
        
    def obtenerFrame (self, master):
 
        self.courierFont = "Courier 10"
 
        self.frameMDB = LabelFrame (master, text ="MDB")
        #self.frameMDB.grid(row = 4, column = 0, rowspan = 1, columnspan = 5 , padx = 5, pady = 5, sticky = E+W)

        self.lblMDBInstruccion = Label(self.frameMDB, text="MDB", width=8)
        self.lblMDBInstruccion.grid(row = 0, column = 0, sticky=W, pady=5, padx=5) 
        

 
        self.botonEnviarMDB_01 = Button ( self.frameMDB, text ="BotonCanc", width = 10, command = self.protocoloMDB.enviarInstruccion_1)
        self.botonEnviarMDB_01.grid (row = 0, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.botonEnviarMDB_02 = Button ( self.frameMDB, text ="Instruccion", width = 10, command = self.protocoloMDB.enviarInstruccion_2)
        self.botonEnviarMDB_02.grid (row = 1, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 5)


        self.txtMDB_01 = Entry (self.frameMDB, textvariable = self.protocoloMDB.idMDB[0], width=15, font = self.courierFont)
        self.txtMDB_01.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)
        self.txtMDB_01.bind ("<Key>", self.capturarTeclado)

        self.txtMDB_02 = Entry (self.frameMDB, textvariable = self.protocoloMDB.idMDB[1], width=15, font = self.courierFont)
        self.txtMDB_02.grid (row = 1, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)
        self.txtMDB_02.bind ("<Key>", self.capturarTeclado)
        
        
        
        
        self.botonIniciarMDB = Button ( self.frameMDB, text ="iniciar", width = 10, command = self.protocoloMDB.iniciar)
        self.botonIniciarMDB.grid (row = 0, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
 
 
        self.botonTemperatura = Button ( self.frameMDB, text ="temp", width = 10, command = self.protocoloMDB.enviarInstruccion_3)
        self.botonTemperatura.grid (row = 0, column = 4, rowspan = 1, columnspan = 1, padx = 5, pady = 5)


        self.botonCCTALK = Button ( self.frameMDB, text ="CCTALK", width = 10, command = self.protocoloMDB.enviarInstruccion_4)
        self.botonCCTALK.grid (row = 0, column = 5, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

 
 
 
        
        """
        self.txtMDB_03 = Entry (self.frameMDB, textvariable = self.idMDB[2], width=10)
        self.txtMDB_03.grid (row = 0, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.txtMDB_04 = Entry (self.frameMDB, textvariable = self.idMDB[3], width=10)
        self.txtMDB_04.grid (row = 0, column = 4, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.txtMDB_05 = Entry (self.frameMDB, textvariable = self.idMDB[4], width=10)
        self.txtMDB_05.grid (row = 0, column = 5, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.txtMDB_06 = Entry (self.frameMDB, textvariable = self.idMDB[5], width=10)
        self.txtMDB_06.grid (row = 0, column = 6, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.botonEnviarMDB = Button ( self.frameMDB, text ="enviar", width = 10, command = self.enviarMDB, bg = self.COLOR_TEMA)
        self.botonEnviarMDB.grid (row = 0, column = 7, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.botonEnviarMDBIniciar = Button ( self.frameMDB, text ="iniciar", width = 10, bg = self.COLOR_TEMA)
        #self.botonEnviarMDBIniciar.grid (row = 0, column = 6, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

        self.botonEnviarMDBParar = Button ( self.frameMDB, text ="Parar", width = 10)
        #self.botonEnviarMDBParar.grid (row = 0, column = 7, rowspan = 1, columnspan = 1, padx = 5, pady = 5)        
        """

        return self.frameMDB
        
    def capturarTeclado(self, event):
        if event.widget == self.txtMDB_01:
            print ("Recibido 1>>", event)
            a = self.txtMDB_01.get()
            print (a, len(a))
            if len(a) % 3 == 2:
                event.widget.insert(END, "*")
        
        if event.widget == self.txtMDB_02:
            print ("Recibido 2>>", event)
            a = self.txtMDB_02.get()
            print (a, len(a))
            if len(a) % 3 == 1:
                event.widget.insert(END, "**")

        
    def terminarMDB (self):
        self.protocolo.stop()


    def obtenerListaDePuertos (self) :
        ports = list(serial.tools.list_ports.comports()) 
        cTupla =()
        for port in ports:
            #print (port.device)
            cTupla  += port.device,
        #print (cTupla)
        return (cTupla)

        
    def escribirInstruccion (self, instruccion, paridad):
        try:
            self.__puertoSerie.parity = self.cambiarParidad3(instruccion, paridad)
            instruccion = instruccion.to_bytes(1, byteorder='big')
            self.escribir(instruccion)
        except serial.serialutil.SerialException:
            print ("SerialException")
            
    def cambiarParidad3 (self, comando, paridad):
        b=128
        cont=0
        while b != 0:
            if b&comando!=0:
                cont=+cont+1
            b=b>>1

        if paridad == 1:
            if cont % 2 == 0:
                return serial.PARITY_ODD
            else:
                return serial.PARITY_EVEN
        elif paridad == 0:
            if cont % 2 == 0:
                return serial.PARITY_EVEN
            else:
                return serial.PARITY_ODD








