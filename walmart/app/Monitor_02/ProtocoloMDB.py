# coding=utf-8

# Parte del Modelo para el programa de comunicaci�n 
# Desarrollado por Sigfrido Oscar Soria Frias
# En Estacionamientos �nicos de M�xico

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
        
        self.idEnviarDatosHex =  StringVar(value="")
        
        
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
            
        """    
        if mensaje:
            if self.__estado == 1 and mensaje == b'\x00':
                print ("Se cambia estado a 2")
                self.__estado = 2
                return
                
            if self.__estado == 2 and mensaje == b'\x4D':  # Verificar la respuesta (4D = M, 45 = E, 49 = I) <----------
                self.puerto.escribirInstruccion(0x00, 0)
                self.__estado = 3
                print ("Se cambia estado a 3")

                
            if self.__estado == 3 and mensaje == b'\x00':
                self.__estado = 4
                print ("Deshabilitacion de Monedas Exitosa")
                
                
            if self.__estado == 4:
                
                cont=cont+1
                print("DESHINIBIENDO!---",cont)
                self.__estado = 5
                
                        
            if self.__estado == 5 and mensaje == b'\x00':
                
                print("Habilitacion de Monedas Exitosa")
                print("LISTO!---")
                self.__estado = 6
        """
                

            
            
            
                
    def establecerNombre (self, nombre):
        self.nombre = nombre
        
    def obtenerNombre (self):
        return self.nombre
    
    def __str__(self):
        return self.obtenerNombre()

    def enviarInstruccion_1 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
        self.puerto.enviarBytes(a)
            
    def enviarInstruccion_2 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.ADMINISTRACION, Comunicacion.VERSION)
        self.puerto.enviarBytes(a)
        
    def enviarInstruccion_3 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.TEMPERATURA)
        self.puerto.enviarBytes(a)
        
    def enviarInstruccion_4 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.RESET)
        self.puerto.enviarBytes(a)

    def enviarInstruccion_5 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.ADMINISTRACION, Comunicacion.PROGRAMA_0)
        self.puerto.enviarBytes(a)
        
    def enviarInstruccion_6 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.ADMINISTRACION, Comunicacion.PROGRAMA_1)
        self.puerto.enviarBytes(a);        
        
    

    def enviarInstruccion_7 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [3, 1])
        self.puerto.enviarBytes(a)
        
    def enviarInstruccion_8 (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [3, 0])
        self.puerto.enviarBytes(a)
        
    def enviarInstruccion_9 (self):
        #a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 0, 0, 15, 0])
        #self.puerto.enviarBytes(a)

        monto = 2

        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 2, 0, (monto * 10), 0, self.comunicacion.checkSum([15,2, (monto * 10)]), 0])
        self.puerto.enviarBytes(a) 

    def enviarInstruccion_10 (self):
        #a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BANDERAS)
        #a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])

        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x08, 1, ])
        #self.puerto.write(a)
        #time.sleep(.025)
        #r = self.puerto.read(50) #Verificar en el simulador se ven 19



        print ("Dentro de intruccion 10")
        self.puerto.enviarBytes(a) 




        
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
        

    def enviarDatos (self, datos):
        
        print ("Dentro de enviarDatos")
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
        
        
        a = self.puerto.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, mensaje)
        self.puerto.enviarBytes(a)
        
        print ("Datos enviados MDB")
        #TODO: Agregar moficaci�n para la comunicaci�n con arduino





            
    def run (self):
        self.hiloFuncionando = True;
        self.hiloActivado = True;
        self.cont=0
        contador = 0
        contador_aux = 0
        
        print ("Desde run protocolo")
        
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
                        #a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
                        #self.puerto.enviarBytes(a);



                    

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
    def __init__ (self, protocolo):
        self.protocolo = protocolo
        protocolo.establecerInterfaz (self)
        
    def obtenerFrame (self, master):
 
        self.courierFont = "Courier 10"
 
        self.frame = LabelFrame (master, text ="MDB")
        #self.frame.grid(row = 4, column = 0, rowspan = 1, columnspan = 5 , padx = 5, pady = 5, sticky = E+W)

        self.lblMDBInstruccion = Label(self.frame, text="MDB", width=8)
        self.lblMDBInstruccion.grid(row = 0, column = 0, sticky=W, pady=5, padx=5) 
        
 
        self.botonEnviar01 = Button ( self.frame, text ="BotonCanc", width = 10, command = self.protocolo.enviarInstruccion_1)
        self.botonEnviar01.grid (row = 0, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.botonEnviar02 = Button ( self.frame, text ="Version", width = 10, command = self.protocolo.enviarInstruccion_2)
        self.botonEnviar02.grid (row = 1, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
    
        self.botonEnviar03 = Button ( self.frame, text ="temp", width = 10, command = self.protocolo.enviarInstruccion_3)
        self.botonEnviar03.grid (row = 2, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.botonEnviar04 = Button ( self.frame, text ="RESET", width = 10, command = self.protocolo.enviarInstruccion_4)
        self.botonEnviar04.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

        self.botonEnviar05 = Button ( self.frame, text ="Prog. Cajero", width = 10, command = self.protocolo.enviarInstruccion_5)
        self.botonEnviar05.grid (row = 1, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.botonEnviar06 = Button ( self.frame, text ="Prog. Expedidora", width = 10, command = self.protocolo.enviarInstruccion_6)
        self.botonEnviar06.grid (row = 2, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5)        

        
        self.botonEnviar07 = Button ( self.frame, text ="Prender", width = 10, command = self.protocolo.enviarInstruccion_7)
        self.botonEnviar07.grid (row = 2, column = 2, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.botonEnviar08 = Button ( self.frame, text ="Apagar", width = 10, command = self.protocolo.enviarInstruccion_8)
        self.botonEnviar08.grid (row = 2, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

        self.botonEnviar09 = Button ( self.frame, text ="Solicitar", width = 10, command = self.protocolo.enviarInstruccion_9)
        self.botonEnviar09.grid (row = 3, column = 2, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.botonEnviar10 = Button ( self.frame, text ="Poll", width = 10, command = self.protocolo.enviarInstruccion_10)
        self.botonEnviar10.grid (row = 3, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

        """
        self.txtMDB_01 = Entry (self.frame, textvariable = self.protocolo.idMDB[0], width=15, font = self.courierFont)
        self.txtMDB_01.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)
        self.txtMDB_01.bind ("<Key>", self.capturarTeclado)

        self.txtMDB_02 = Entry (self.frame, textvariable = self.protocolo.idMDB[1], width=15, font = self.courierFont)
        self.txtMDB_02.grid (row = 1, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)
        self.txtMDB_02.bind ("<Key>", self.capturarTeclado)
        
        
        self.botonIniciarMDB = Button ( self.frame, text ="iniciar", width = 10, command = self.protocolo.iniciar)
        self.botonIniciarMDB.grid (row = 0, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        """


        self.frameHex = self.obtenerFrameEnviarDatosHexadecimal(self.frame)
        self.frameHex.grid (row = 0, column = 2, rowspan = 2, columnspan = 2, padx = 5, pady = 5)


        """


        self.botonCCTALK = Button ( self.frame, text ="NUEVA", width = 10, command = self.protocolo.enviarInstruccion_5)
        self.botonCCTALK.grid (row = 0, column = 6, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        """
 
 
 
        
        """
        self.txtMDB_03 = Entry (self.frame, textvariable = self.idMDB[2], width=10)
        self.txtMDB_03.grid (row = 0, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.txtMDB_04 = Entry (self.frame, textvariable = self.idMDB[3], width=10)
        self.txtMDB_04.grid (row = 0, column = 4, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.txtMDB_05 = Entry (self.frame, textvariable = self.idMDB[4], width=10)
        self.txtMDB_05.grid (row = 0, column = 5, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.txtMDB_06 = Entry (self.frame, textvariable = self.idMDB[5], width=10)
        self.txtMDB_06.grid (row = 0, column = 6, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.botonEnviarMDB = Button ( self.frame, text ="enviar", width = 10, command = self.enviarMDB, bg = self.COLOR_TEMA)
        self.botonEnviarMDB.grid (row = 0, column = 7, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        self.botonEnviarMDBIniciar = Button ( self.frame, text ="iniciar", width = 10, bg = self.COLOR_TEMA)
        #self.botonEnviarMDBIniciar.grid (row = 0, column = 6, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

        self.botonEnviarMDBParar = Button ( self.frame, text ="Parar", width = 10)
        #self.botonEnviarMDBParar.grid (row = 0, column = 7, rowspan = 1, columnspan = 1, padx = 5, pady = 5)        
        """

        return self.frame
        
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




