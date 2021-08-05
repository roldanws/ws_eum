# coding=utf-8

# Parte del Modelo para el programa de comunicación 
# Desarrollado por Sigfrido Oscar Soria Frias
# En Estacionamientos Únicos de México

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import Pmw
import threading
import serial
import time
import serial.tools.list_ports
import traceback

from Comunicacion import Comunicacion

import os
ruta = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ruta)

from Variables.Temporizador import Temporizador

class PuertoSerie (threading.Thread):
    """Clase utilizada para manejar las operaciones de lectura y escritura en distintos procolos serie"""

    
    DIC_PUERTOS = {}
    DIC_BAUD = { "9600" : 9600 , "19200" : 19200 , "38400" : 38400, "57600" : 57600, "115200" : 115200}
    DIC_PARIDAD = { "Ninguna" : serial.PARITY_NONE, "Par" : serial.PARITY_EVEN , "Impar" : serial.PARITY_ODD, "Marca" : serial.PARITY_MARK , "Espacio" : serial.PARITY_SPACE}
    DIC_STOP = {"1" : serial.STOPBITS_ONE, "1.5" : serial.STOPBITS_ONE_POINT_FIVE, "2" : serial.STOPBITS_TWO}
    DIC_BITS = {"5 Bits" : serial.FIVEBITS, "6 Bits" : serial.SIXBITS, "7 Bits" : serial.SEVENBITS, "8 Bits" : serial.EIGHTBITS}    
    
    ARDUINO_NANO = "USB2.0-Serial"
    ADAPTADOR = "USB-Serial Controller"
    ARDUINO_MICRO = "Arduino Micro"

    DIC_DISPOSITIVOS = {"ARDUINO_NANO": "USB2.0-Serial", "ADAPTADOR": "USB-Serial Controller", "ARDUINO_MICRO" : "Arduino Micro"}

    def __init__ (self, nombre):
        threading.Thread.__init__ (self, name = nombre)
        
        self.establecerNombre (nombre)
        
        self.hiloFuncionando = False;        
        self.puertoAbierto = False
        self.puertoListoParaLeer = False

        self.listaDeInterfaces = []
        self.mensajero = None

        self.__puertoSerie = serial.Serial()
        
        self.protocolo = None
        self.protocolo_02 = None
        
        """
        
        self.TON_01 = Temporizador("TON_01",0.003)
        self.M = []
        
        for i in range (0,10,1):
            print ("Imprimiendo ", i)
            self.M.append(0)
        
        print ("Imprimendo M ", self.M)
        """
        
        self.comunicacion = Comunicacion ()
        
        #self.establecerProtocoloDeComunicacion (ProtocoloMuestra())


        #----------- Para el manejo de la interfaz
        
        #self.idSerialDispositivo =  StringVar(value=" ")
        self.idSerialDispositivo =  VariableTexto(value = " ")

        #self.idSerialPuerto = StringVar(value=" ")
        self.idSerialPuerto = VariableTexto(value=" ")
        
        #self.idSerialBaud = StringVar(value=" ")
        self.idSerialBaud = VariableTexto(value=" ")

        self.tuplaBaud = ()
        for k,v in self.DIC_BAUD.items():
            self.tuplaBaud +=(k,)
        
        #self.idSerialParidad = StringVar(value=1)
        self.idSerialParidad = VariableTexto(value = "abc")
        self.tuplaParidad = ()
        for k,v in self.DIC_PARIDAD.items():
            self.tuplaParidad +=(k,)
            
        #self.idSerialStop = StringVar(value=1)
        self.idSerialStop = VariableTexto(value=1)
        self.tuplaStop = ()
        for k,v in self.DIC_STOP.items():
            self.tuplaStop +=(k,)
        
        #self.idSerialBits = StringVar(value=1)
        self.idSerialBits = VariableTexto(value=1)
        self.tuplaBits = ()
        for k,v in self.DIC_BITS.items():
            self.tuplaBits +=(k,)
            
        #self.idTimeout = StringVar(value=0)
        self.idTimeout = VariableTexto(value=0)
            
            
        #self.idEnviarDatos = StringVar(value="")
        self.idEnviarDatos = VariableTexto(value="")
        #self.idEnviarDatosHex =  StringVar(value="")
        self.idEnviarDatosHex =  VariableTexto(value="")
        
    
        self.__puertoSerie.port = ""
        self.__puertoSerie.baudrate = 9600
        self.__puertoSerie.parity = serial.PARITY_NONE
        self.__puertoSerie.timeout = 0
        self.__puertoSerie.stopbits = serial.STOPBITS_ONE
        self.__puertoSerie.bytesize = serial.EIGHTBITS
        
        self.mensajero1 = None


    def abrirPuerto (self):
        if self.hiloFuncionando:
            self.puertoAbierto = True

        else:
            # TODO: Mejorar el proceso de apertura y cierre cuando no esta activo el hilo
            try:
                self.__puertoSerie.open()
            except serial.serialutil.SerialException:
                #print ("Excepcion \n%s" % serialException)
                self.enviarMensaje1 ("\nNo se pudo abrir el puerto >>%s<<" %(self.__puertoSerie.port))
                traceback.print_exc()
                self.puertoAbierto = False

            if self.__puertoSerie.is_open:
                #self.enviarMensaje1 ("\nPuerto %s a %d %s abierto " % (self.__puertoSerie.port, self.__puertoSerie.baudrate, self.__puertoSerie.parity))
                self.enviarMensaje1("\n")
                self.enviarMensaje1(self)
                #print (self)

                for j, elemento in enumerate (self.listaDeInterfaces):
                    self.listaDeInterfaces[j].habilitarControlesFrameConexion(False)
            
        #print ("self.puertoAbierto ", self.puertoAbierto)
        #print ("self.puertoListoParaLeer ", self.puertoListoParaLeer)
                
    def cerrarPuerto (self):
        self.puertoAbierto = False
        if self.protocolo is not None:
            self.protocolo.detenerHilo()
            
        #print ("self.puertoAbierto ", self.puertoAbierto)
        #print ("self.puertoListoParaLeer ", self.puertoListoParaLeer)
        
    def limpiar (self):
        if self.__puertoSerie.is_open:
            self.__puertoSerie.flushOutput()
            #self.__puertoSerie.flushInput()

    def leer(self):
        if self.__puertoSerie.is_open:
            
            texto1 = ""
            texto2 = ""
            
            
            while self.__puertoSerie.inWaiting() :
                
                if not self.puertoAbierto:
                    break
            
                s = self.__puertoSerie.read()


                if s:
                    
                    #self.TON_01.entrada =False;
                    #self.TON_01.actualizar()

                    
                    self.protocolo.mensajeRecibido (s)
                    #print (s)

                    texto1 = texto1 + s.hex().upper() + " "
                    texto2 = texto2 + s.decode("ISO-8859-1")
            

            """
            if self.TON_01.salida & self.M[0] == 0:
                print ("Fin de instruccion")
                self.M[0] =  1
                
                
                
            self.TON_01.entrada = True;                
            self.TON_01.actualizar()
            """
            
            if len (texto1) > 0:
                for j, elemento in enumerate (self.listaDeInterfaces):
                    #self.listaDeInterfaces[j].escribirAreaEntrada1(s.hex().upper())
                    #self.listaDeInterfaces[j].escribirAreaEntrada1(" ")
                    self.listaDeInterfaces[j].escribirAreaEntrada1(texto1)
                    self.listaDeInterfaces[j].escribirAreaEntrada2(texto2)
        
    def escribir (self, mensaje):
        if (self.__puertoSerie.is_open):
            self.__puertoSerie.write(mensaje)
            
            texto1 = ""
            #texto2 = ""
            s = mensaje.hex().upper()
            
            for i in range (0, len(s), 2):
                texto1 = texto1 + s[i:i+2] + " "
            
            for j, elemento in enumerate (self.listaDeInterfaces):    
                self.listaDeInterfaces[j].escribirAreaSalida1(texto1)
                self.listaDeInterfaces[j].escribirAreaSalida2(mensaje)

    def modificarConfiguracion (self, **kwargs):
        for key, value in kwargs.items():
            
            #print ("Imprimiendo el valor en modificar configuracion", key, value)
            
            if key == "puerto":
                self.__puertoSerie.port = value
                #print ("Desde modificar configuracion ", key, self.__puertoSerie.port)

            if key == "baudrate":
                self.__puertoSerie.baudrate = self.DIC_BAUD.get(value)
                #print ("Desde modificar configuracion ", key, self.__puertoSerie.baudrate)

            if key == "paridad":
                
                
                self.__puertoSerie.parity = self.DIC_PARIDAD.get(value)
                #print ("Desde modificar configuracion ", key, self.__puertoSerie.parity)
                
            if key == "stopBits":
                self.__puertoSerie.stopbits = self.DIC_STOP.get(value)
                #print ("Desde modificar configuracion ", key, self.__puertoSerie.stopbits)
             
            if key == "bitsDeDatos":
                self.__puertoSerie.bytesize = self.DIC_BITS.get(value)
                #print ("Desde modificar configuracion ", key, self.__puertoSerie.bytesize)
                
            if key == "timeOut":
                self.__puertoSerie.timeout = float( value)
                #print ("Desde modificar configuracion ", key, self.__puertoSerie.timeout)

            if key == "dispositivo":
                print ("dispositivo >")
                lista = obtenerListaDeDispositivios()
                
                print (lista)

                for elemento in lista:
                    print (elemento, ">%s<" %elemento[2].split(" (")[0])
                    
                    
                    if value == elemento[2].split(" (")[0]:
                        print ("El dispositivo es %s en el puerto %s" %(value, elemento[0]))
                        self.__puertoSerie.port = elemento[0]
                        break;
                        
    def detenerHilo (self):
        """ Utilizada para detener el hilo"""
        self.hiloFuncionando = False
        
        if self.protocolo is not None:
            self.protocolo.detenerHilo()
        
    def establecerMensajero1 (self, mensajero):
        self.mensajero1 = mensajero
        
    def establecerMensajero2 (self, mensajero):
        self.mensajero2 = mensajero
        
    def enviarMensaje1 (self, mensaje):
        if self.mensajero1 is not None:
            self.mensajero1(mensaje)
        else:
            print (mensaje)
            
    def enviarMensaje2 (self, mensaje):
        if self.mensajero2 is not None:
            self.mensajero2(mensaje)
        else:
            print (mensaje)

    def establecerInterfazGrafica (self, interfaz):
        """Agrega un interfaz grafica a a la lista"""
        self.listaDeInterfaces.append(interfaz)
        
    def obtenerInterfazGrafica (self, indice):
        if indice < len(self.listaDeInterfaces):
            return self.listaDeInterfaces[indice]
        else:
            return None;
    
    def enviarTexto (self, datos):
        mensaje = datos.encode('latin-1')
        self.escribir(mensaje)

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
        self.escribir(mensaje)
        
    def enviarBytes (self, mensaje):
        self.escribir (mensaje)
        
    def establecerProtocoloDeComunicacion (self, protocolo):
        self.protocolo = protocolo
        self.protocolo.establecerPuerto(self)
            
    def establecerProtocoloDeComunicacion_02 (self, protocolo):
        self.protocolo_02 = protocolo
        self.protocolo_02.establecerPuerto(self)
            
    def obtenerProtocoloDeComunicacion (self):
        return self.protocolo
    
    def obtenerProtocoloDeComunicacion_02 (self):
        return self.protocolo_02
    
    def establecerComunicacion (self, comunicacion):
        self.comunicacion = comunicacion
        
    def obtenerComunicacion (self):
        return self.comunicacion

    
            
    def is_Open(self):
        return self.puertoAbierto
    
    
    def run (self):

        self.hiloFuncionando = True             # ESCRITURA - utilizado para detener el hilo
        self.puertoAbierto = False              # ESCRITURA - utilizado para abrir o cerrar el puerto
        self.puertoListoParaLeer = False        # LECTURA- indica si el puerto esta abierto
        
        
        while self.hiloFuncionando :
            if self.puertoAbierto :
                if self.puertoListoParaLeer == False:
                    """Abrir puerto"""
                    try:
                        self.__puertoSerie.open()
                    except serial.serialutil.SerialException:
                        #print ("Excepcion \n%s" % serialException)
                        self.enviarMensaje1 ("\nNo se pudo abrir el puerto >>%s<<" %(self.__puertoSerie.port))
                        traceback.print_exc()
                        self.puertoAbierto = False

                    if self.__puertoSerie.is_open:
                        #self.enviarMensaje1 ("\nPuerto %s a %d %s abierto " % (self.__puertoSerie.port, self.__puertoSerie.baudrate, self.__puertoSerie.parity))
                        self.enviarMensaje1("\n")
                        self.enviarMensaje1(self)
                        #print (self)
                        
                        for j, elemento in enumerate (self.listaDeInterfaces):
                            self.listaDeInterfaces[j].habilitarControlesFrameConexion(False)                        

                        
                        self.puertoListoParaLeer = True
                else:
                    
                    try:
                        self.leer()
                    except serial.serialutil.SerialException:
                        self.enviarMensaje1 ("\nError al leer el puerto %s, debido posiblemente a una desconexion del cable de comunicacion" %self.__puertoSerie.port)
                        self.puertoAbierto = False
                    

            else:
                """cerrar Puerto"""
                if (self.__puertoSerie.is_open):
                    if self.protocolo is not None:
                        self.protocolo.detenerHilo()
                    self.__puertoSerie.close()
                    
                    self.enviarMensaje1 ("\nPuerto %s cerrado " % self.__puertoSerie.port)
                    
                    for j, elemento in enumerate (self.listaDeInterfaces):
                        self.listaDeInterfaces[j].habilitarControlesFrameConexion(True)    
                    self.puertoListoParaLeer = False

                time.sleep (0.5)
                    
        print ("Hilo terminado", self.name)
                    
    def obtenerListaDePuertos (self) :
        return obtenerListaDePuertos()
    
    def obtenerListaDeDispositivios (self) :
        return obtenerListaDeDispositivios()    
    
    def establecerNombre (self, nombre):
        self.nombre = nombre
        
    def obtenerNombre (self):
        return self.nombre
    
    def __str__ (self):
        a = ("Puerto %s a %d %s %s %s %d" %(self.__puertoSerie.port, self.__puertoSerie.baudrate, self.__puertoSerie.parity, self.__puertoSerie.stopbits, self.__puertoSerie.bytesize, self.__puertoSerie.timeout))
        
        b = ""
        
        if self.protocolo is not None:
            #print (self.protocolo)
            
            b += ", %s habilitado" %self.protocolo
        
        if self.protocolo_02 is not None:
            b += ", %s habilitado" %self.protocolo_02
        
        return a + b


def obtenerNombreDelPuerto (**kwargs):
    lista = obtenerListaDeDispositivios()
    nombreDelPuerto=""
    
    for key, value in kwargs.items(): 
        if key == "dispositivo":
            for elemento in lista:
                if value == elemento[2]:
                    print ("El dispositivo es %s en el puerto %s" %(value, elemento[0]))
                    nombreDelPuerto = elemento[0]
                    break;
                    
    return nombreDelPuerto


def obtenerListaDePuertos () :
    ports = list(serial.tools.list_ports.comports()) 
    cTupla =()
    for port in ports:
        print (port.device)
        cTupla  += port.device,
    #print (cTupla)
    return (cTupla)


def obtenerListaDeDispositivios () :
    ports = list(serial.tools.list_ports.comports()) 
    cTupla =()
    
    for port in ports:
        dTupla = ()
        """
        cLista = []
        cLista.append (port.device)
        cLista.append (port.name)
        cLista.append (port.description)
        """
        
        dTupla += port.device,
        dTupla += port.name,
        dTupla += port.description,
        """
        print ("\n")

        print ("device: ", port.device)
        print ("name: ", port.name)
        print ("description: ", port.description)
        print ("hwid: ", port.hwid)
        print ("hwid: ", port.vid)
        print ("pid: ", port.pid)
        print ("serial_number: ", port.serial_number)
        print ("location: ", port.location)
        print ("manufacturer: ", port.manufacturer)
        print ("product: ", port.product)
        print ("interface: ", port.interface)
        """

        #cTupla  += port.device,
        cTupla  += dTupla,
    #print (cTupla)
    return (cTupla)




class VariableTexto ():
    def __init__(self, value):
        self.texto = value
        
    def set(self, texto):
        self.texto = texto
        
    def get(self):
        return self.texto
        









class PuertoInterfazGrafica ():
    def __init__(self, puerto):
        self.puerto = puerto
        puerto.establecerInterfazGrafica(self)
        self.listaDeDispositivos = []

        #self.initUICampos()
        
        self.TON = []
        
        self.TON.append (Temporizador("TON_00", 0.1))
        self.TON.append (Temporizador("TON_01", 0.1))
        self.TON.append (Temporizador("TON_02", 0.1))
        self.TON.append (Temporizador("TON_03", 0.1))
        
        self.seleccionDeColor = []
        self.seleccionDeColor.append (0)
        self.seleccionDeColor.append (0)
        self.seleccionDeColor.append (0)
        self.seleccionDeColor.append (0)

        


    def initUICampos (self):



        
        """
        def obtenerElementosGraficos (self, *args):
            for key, value in kargs:
                if (key == "Conexion"):
        """
    
    def actualizarPuertos (self, event):
        self.listaDeDispositivos = self.puerto.obtenerListaDeDispositivios()
        c = []
        for dispositivo in self.listaDeDispositivos:
            c.append(dispositivo [0])
        self.comboSerialPuerto ['values'] = c
        
        if len(self.listaDeDispositivos) == 0:
            self.comboSerialPuerto.set("")
            self.frameConexionSerial.config(text =" ")
        #print ("Imprimiendo la lista de puertos- PuertoInterfazGrafica", c, len(c))
        #print ("imprimiendo lista de dispositivios", self.listaDeDispositivos)
        
    def actualizarTextoDispositivo (self, texto):
        
        for dispositivo in self.listaDeDispositivos:
            #print ("imprimiendo dispositivo", dispositivo [2])
            
            if dispositivo [0] == texto:
                #print (dispositivo [2].split("(")[0])
                
                self.puerto.idSerialDispositivo.set(dispositivo [2].split("(")[0])
                self.frameConexionSerial.config(text = self.puerto.idSerialDispositivo.get())
                break
    
    def obtenerFrameConexion (self, master) :
        self.frameConexionSerial = LabelFrame (master, text="Comunicacion Serial", borderwidth=2, relief="groove")
        #self.frameConexionSerial.grid(row = 1, column = 0, rowspan = 1, columnspan = 7, sticky=E+W+S+N, pady=5, padx=5)            

        self.lblSerial01 = Label(self.frameConexionSerial, text="Puerto", width=10, anchor=W)
        self.lblSerial01.grid(row = 1, column = 0, sticky=W, pady=5, padx=5)        
        
        self.comboSerialPuerto = ttk.Combobox (self.frameConexionSerial, textvariable = self.puerto.idSerialPuerto, state="readonly", width=12)
        self.comboSerialPuerto.bind("<<ComboboxSelected>>", self.seleccionaDeCombobox)
        self.comboSerialPuerto.bind("<Enter>", self.actualizarPuertos)
        self.comboSerialPuerto.grid (row=1, column=1, columnspan=1, rowspan=1, padx=5, pady=5)
        
        self.lblSerial02 = Label(self.frameConexionSerial, text="BaudRate", width=12, anchor=W)
        self.lblSerial02.grid(row = 1, column = 2, sticky=W, pady=5, padx=5)        
        
        self.comboSerialBaud = ttk.Combobox(self.frameConexionSerial, textvariable = self.puerto.idSerialBaud, state="readonly", width=12)
        self.comboSerialBaud ['values'] = self.puerto.tuplaBaud
        self.comboSerialBaud.current(0)
        self.comboSerialBaud.bind("<<ComboboxSelected>>", self.seleccionaDeCombobox)
        self.comboSerialBaud.grid (row=1, column=3, columnspan=1, rowspan=1, padx=5, pady=5)


        self.lblSerial03 = Label(self.frameConexionSerial, text="Paridad", width=10, anchor=W)
        self.lblSerial03.grid(row = 1, column = 4, sticky=W, pady=5, padx=5)        
        
        self.comboSerialParidad = ttk.Combobox(self.frameConexionSerial, textvariable = self.puerto.idSerialParidad, state="readonly", width=12)
        self.comboSerialParidad ['values'] = self.puerto.tuplaParidad
        self.comboSerialParidad.current(0)
        self.comboSerialParidad.bind("<<ComboboxSelected>>", self.seleccionaDeCombobox)
        self.comboSerialParidad.grid (row=1, column=5, columnspan=1, rowspan=1, padx=5, pady=5)
        
        self.lblSerial04 = Label(self.frameConexionSerial, text="StopBits", width=10, anchor=W)
        self.lblSerial04.grid(row = 2, column = 0, sticky=W, pady=5, padx=5)        
        
        self.comboSerialStop = ttk.Combobox(self.frameConexionSerial, textvariable = self.puerto.idSerialStop, state="readonly", width=12)
        self.comboSerialStop ['values'] = self.puerto.tuplaStop
        self.comboSerialStop.current(0)
        self.comboSerialStop.bind("<<ComboboxSelected>>", self.seleccionaDeCombobox)
        self.comboSerialStop.grid (row=2, column=1, columnspan=1, rowspan=1, padx=5, pady=5)

        self.lblSerial05 = Label(self.frameConexionSerial, text="Bits de datos", width=12, anchor=W)
        self.lblSerial05.grid(row = 2, column = 2, sticky=W, pady=5, padx=5)        
        
        self.comboSerialBits = ttk.Combobox(self.frameConexionSerial, textvariable = self.puerto.idSerialBits, state="readonly", width=12)
        self.comboSerialBits ['values'] = self.puerto.tuplaBits
        self.comboSerialBits.current(3)
        self.comboSerialBits.bind("<<ComboboxSelected>>", self.seleccionaDeCombobox)
        self.comboSerialBits.grid (row=2, column=3, columnspan=1, rowspan=1, padx=5, pady=5)    
        
        
        self.lblSerial06 = Label(self.frameConexionSerial, text="timeOut", anchor=W)
        self.lblSerial06.grid(row = 2, column = 4, sticky=W, pady=5, padx=5)        
        
        self.txtSerialTiempo = Entry (self.frameConexionSerial, name="txtSerialTiempo", width=15, textvariable = self.puerto.idTimeout)
        self.txtSerialTiempo.grid (row=2, column=5, columnspan=1, rowspan=1, padx=5, pady=5)
        self.txtSerialTiempo.bind("<Return>", self.seleccionaDeCombobox)
        
        """
        self.lblSerial07 = Label(self.frameConexionSerial, text="dispositivo" , textvariable = self.puerto.idSerialDispositivo)
        self.lblSerial07.grid(row = 1, column = 6, sticky=W, pady=5, padx=5)        
        
        self.txtSerialDispositivo = Entry (self.frameConexionSerial, name="txtSerialDispositivo", textvariable = self.puerto.idSerialDispositivo, width=15)
        self.txtSerialDispositivo.grid (row=2, column=6, columnspan=1, rowspan=1, padx=5, pady=5)"""
        

        return self.frameConexionSerial
    
    def habilitarControlesFrameConexion (self, estado):
        if estado:
            self.comboSerialPuerto.config(state = ACTIVE)
            self.comboSerialBaud.config(state = ACTIVE)
            self.comboSerialParidad.config(state = ACTIVE)
            self.comboSerialStop.config(state = ACTIVE)
            self.comboSerialBits.config(state = ACTIVE)
            self.txtSerialTiempo.config(state = NORMAL)
            self.btnConectar.config(state = ACTIVE)
            self.btnDesconectar.config(state = DISABLED)

        else:
            self.comboSerialPuerto.config(state = DISABLED)
            self.comboSerialBaud.config(state = DISABLED)
            self.comboSerialParidad.config(state = DISABLED)
            self.comboSerialStop.config(state = DISABLED)
            self.comboSerialBits.config(state = DISABLED)
            self.txtSerialTiempo.config(state = DISABLED)
            self.btnConectar.config(state = DISABLED)
            self.btnDesconectar.config(state = ACTIVE)
    
    
    def obtenerFrameBotonesConexion (self, master):
        
        self.frameBotonesConexion = Frame (master)
        #self.frameBotonesConexion.grid(row = 1, column = 10, rowspan = 1, columnspan = 2, sticky=S+N, pady=5, padx=5)
        self.frameBotonesConexion.columnconfigure (0, weight = 1)
        self.frameBotonesConexion.columnconfigure (1, weight = 1)
        self.frameBotonesConexion.rowconfigure (1, weight = 1)
        
        self.btnConectar = Button (self.frameBotonesConexion, text = "Conectar", width = 12, command = self.abrirPuerto)
        self.btnConectar.grid (row = 1, column = 0, rowspan = 1, columnspan = 1,  padx = 5, pady = 15)
        
        self.btnDesconectar = Button ( self.frameBotonesConexion, text = "Desconectar", command = self.cerrarPuerto, width = 12)
        self.btnDesconectar.grid (row = 1, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 15)
        
        return self.frameBotonesConexion
    
    
    def obtenerFrameEnviarTexto (self, master):
        self.frameEnviarTexto = LabelFrame ( master,borderwidth=2, relief="groove", text ="Texto")
        #self.frameBotonesEnviar.grid(row = 3, column = 0, rowspan = 1, columnspan = 10, padx = 5, pady = 5, sticky = E+W+S+N)
        self.frameEnviarTexto.columnconfigure (1, weight=1)
        
        self.lblEnviarDatos = Label(self.frameEnviarTexto, text="Texto", width=10)
        #self.lblEnviarDatos.grid(row = 0, column = 0, sticky=W, pady=5, padx=5) 

        self.txtEnviarDatos = Entry (self.frameEnviarTexto, name = "txtEnviarDatos", textvariable = self.puerto.idEnviarDatos)
        self.txtEnviarDatos.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)
        self.txtEnviarDatos.bind("<Return>", self.enviarTexto)
        
        self.botonEnviarDatos = Button (self.frameEnviarTexto, text ="Enviar", width = 12, command = self.enviarTexto)
        self.botonEnviarDatos.grid (row = 0, column = 2, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        return self.frameEnviarTexto
        
    def obtenerFrameEnviarDatosHexadecimal (self, master):
        self.frameInstruccionesHexadecimal = LabelFrame (master, borderwidth=2, relief="groove", text ="Hexadecimal")
        #self.frameInstruccionesHexadecimal.grid(row = 3, column = 10, rowspan = 1, columnspan = 2 , padx = 5, pady = 5, sticky = E+W)
        self.frameBotonesConexion.columnconfigure (0, weight = 1)

        self.txtEnviarHexadecimal = Entry (self.frameInstruccionesHexadecimal, name = "txtEnviarDatos", textvariable = self.puerto.idEnviarDatosHex)
        self.txtEnviarHexadecimal.grid (row = 0, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 8, sticky = E+W+S+N)
        self.txtEnviarHexadecimal.bind("<Return>", self.enviarHexadecimal)
        
        self.botonEnviarHexadecimal = Button ( self.frameInstruccionesHexadecimal, text ="Enviar Hex", width = 10, command = self.enviarHexadecimal)
        self.botonEnviarHexadecimal.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 8, sticky = S+N)

        self.botonEnviarHexadecimalIniciar = Button ( self.frameInstruccionesHexadecimal, text ="Iniciar", width = 10)
        #self.botonEnviarHexadecimalIniciar.grid (row = 0, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

        self.botonEnviarHexadecimalParar = Button ( self.frameInstruccionesHexadecimal, text ="Parar", width = 10)
        #self.botonEnviarHexadecimalParar.grid (row = 0, column = 4, rowspan = 1, columnspan = 1, padx = 5, pady = 5)        
        
        return self.frameInstruccionesHexadecimal

    def obtenerCuadroComunicacion (self, master, arg):
        
        self.courierFont = "Courier 10"
        
        if arg == "TEXTO_ENTRADA_1":
            self.areaEntrada1 = Pmw.ScrolledText (master, hscrollmode = "dynamic", vscrollmode = "dynamic", text_font = self.courierFont, text_wrap = WORD, text_width=21)
            self.areaEntrada1.configure(text_state = 'normal')  

            self.areaEntrada1.tag_configure('color1', foreground='red')
            self.areaEntrada1.tag_configure('color2', foreground='blue')
            self.areaEntrada1.tag_configure('color3', foreground='green')
            self.areaEntrada1.tag_configure('color4', foreground='magenta')
            return self.areaEntrada1
        
        if arg == "TEXTO_ENTRADA_2":
            self.areaEntrada2 = Pmw.ScrolledText ( master, hscrollmode = "dynamic", vscrollmode = "dynamic", text_font = self.courierFont, text_wrap = WORD, text_width=7)
            self.areaEntrada2.configure(text_state = 'normal')
            
            self.areaEntrada2.tag_configure('color1', foreground='red')
            self.areaEntrada2.tag_configure('color2', foreground='blue')
            self.areaEntrada2.tag_configure('color3', foreground='green')
            self.areaEntrada2.tag_configure('color4', foreground='magenta')
            return self.areaEntrada2
       
        if arg == "TEXTO_SALIDA_1":
            self.areaSalida1 = Pmw.ScrolledText ( master,  hscrollmode = "dynamic", vscrollmode = "dynamic", text_font = self.courierFont, text_wrap = WORD, text_width=21)
            self.areaSalida1.configure(text_state = 'normal')  
            
            self.areaSalida1.tag_configure('color1', foreground='green')
            self.areaSalida1.tag_configure('color2', foreground='magenta')
            self.areaSalida1.tag_configure('color3', foreground='green')
            self.areaSalida1.tag_configure('color4', foreground='magenta')
            return self.areaSalida1
        
        if arg == "TEXTO_SALIDA_2":
            self.areaSalida2 = Pmw.ScrolledText ( master, hscrollmode = "dynamic", vscrollmode = "dynamic", text_font = self.courierFont, text_wrap = WORD, text_width=7)
            self.areaSalida2.configure(text_state = 'normal')
            
            self.areaSalida2.tag_configure('color1', foreground='green')
            self.areaSalida2.tag_configure('color2', foreground='magenta')
            self.areaSalida2.tag_configure('color3', foreground='green')
            self.areaSalida2.tag_configure('color4', foreground='magenta')
            return self.areaSalida2
        return None

    
    def seleccionaDeCombobox(self, event):

        if event.widget == self.comboSerialPuerto:
            self.puerto.modificarConfiguracion (puerto = self.comboSerialPuerto.get() )
            self.actualizarTextoDispositivo(self.comboSerialPuerto.get())
        
        if event.widget == self.comboSerialBaud:
            self.puerto.modificarConfiguracion (baudrate = self.comboSerialBaud.get() )
            
        if event.widget == self.comboSerialParidad:
            self.puerto.modificarConfiguracion (paridad = self.comboSerialParidad.get() )
            
        if event.widget == self.comboSerialStop:
            self.puerto.modificarConfiguracion (stopBits = self.comboSerialStop.get() )
            
        if event.widget == self.comboSerialBits:
            self.puerto.modificarConfiguracion (bitsDeDatos = self.comboSerialBits.get() )

        if event.widget == self.txtSerialTiempo:
            self.puerto.modificarConfiguracion (timeOut = self.txtSerialTiempo.get() )

    def abrirPuerto (self):
        self.puerto.abrirPuerto()
        #self.habilitarControlesFrameConexion(False)
            #self.puerto.DIC_PARIDAD.get(self.puerto.idSerialParidad.get()))
            
    def cerrarPuerto (self):
        self.puerto.cerrarPuerto()
        #self.habilitarControlesFrameConexion(True)

    def enviarTexto(self, *args):
        
        print ("Dentro de enviar Texto_01")
        self.puerto.enviarTexto(self.txtEnviarDatos.get())
        print ("Dentro de enviar Texto_02")
        self.txtEnviarDatos.delete(0, END)
        print ("Dentro de enviar Texto_03")
        
        
    def enviarHexadecimal (self, *args):
        #self.controlador.enviarDatos(self.txtEnviarDatos.get(), "HEX")
        #print (int (self.txtEnviarHexadecimal.get(), 16))
        try:
            numero = int (self.txtEnviarHexadecimal.get(), 16)
        except ValueError:
            self.puerto.enviarMensaje2 ("\nFormato incorrecto >>%s<<" % self.txtEnviarHexadecimal.get())
        else:
            self.puerto.enviarDatos(numero)
            self.txtEnviarHexadecimal.delete(0, END)
        
    def escribirAreaEntrada1 (self, mensaje):
        
        self.TON[0].actualizar()
        
        if self.TON[0].salida:
            if self.seleccionDeColor[0] == 0:
                self.seleccionDeColor[0] = 1
            elif self.seleccionDeColor[0] == 1:
                self.seleccionDeColor[0] = 0
        self.TON[0].entrada = False
        self.TON[0].actualizar()
        
        
        if int((self.areaEntrada1.index("end - 1c")).split(".")[1]) > 1500:
            self.areaEntrada1.clear()

        #self.areaEntrada1.appendtext(mensaje)
        #self.areaEntrada1.insert('end', mensaje)

        if self.seleccionDeColor[0] == 0:
            self.areaEntrada1.insert('end', mensaje, 'color1')
            
        if self.seleccionDeColor[0] == 1:
            self.areaEntrada1.insert('end', mensaje, 'color2')
            
        self.areaEntrada1.yview(END)
        
        self.TON[0].entrada = True
        self.TON[0].actualizar()
        
    def escribirAreaEntrada2 (self, mensaje):
        
        self.TON[1].actualizar()
        
       
        
        if self.TON[1].salida:
            if self.seleccionDeColor[1] == 0:
                self.seleccionDeColor[1] = 1
            elif self.seleccionDeColor[1] == 1:
                self.seleccionDeColor[1] = 0
        self.TON[1].entrada = False
        self.TON[1].actualizar()
        
        
        
        if int((self.areaEntrada2.index("end - 1c")).split(".")[1]) > 2000:
            self.areaEntrada2.clear()
        #self.areaEntrada2.appendtext(mensaje)
        
        
        
        if self.seleccionDeColor[1] == 0:
            self.areaEntrada2.insert('end', mensaje, 'color1')
            
        if self.seleccionDeColor[1] == 1:
            self.areaEntrada2.insert('end', mensaje, 'color2')
        
        self.areaEntrada2.yview(END)
        
        self.TON[1].entrada = True
        self.TON[1].actualizar()
        
        
        
        
       
    def escribirAreaSalida1 (self, mensaje):

        self.TON[2].actualizar()
        
        if self.TON[2].salida:
            if self.seleccionDeColor[2] == 0:
                self.seleccionDeColor[2] = 1
            elif self.seleccionDeColor[2] == 1:
                self.seleccionDeColor[2] = 0
        self.TON[2].entrada = False
        self.TON[2].actualizar()
        
        if int((self.areaSalida1.index("end - 1c")).split(".")[1]) > 1500:
            self.areaSalida1.clear()
        #self.areaSalida1.insert('end', mensaje)
        #self.areaSalida1.appendtext(mensaje)
        
        if self.seleccionDeColor[2] == 0:
            self.areaSalida1.insert('end', mensaje, 'color3')
            
        if self.seleccionDeColor[2] == 1:
            self.areaSalida1.insert('end', mensaje, 'color4')
        
        self.areaSalida1.yview(END)
        
        self.TON[2].entrada = True
        self.TON[2].actualizar()
        
        
        #print (int((self.areaSalida1.index("end - 1c")).split(".")[1]))

    def escribirAreaSalida2 (self, mensaje):
        
        self.TON[3].actualizar()
        
        if self.TON[3].salida:
            if self.seleccionDeColor[3] == 0:
                self.seleccionDeColor[3] = 1
            elif self.seleccionDeColor[3] == 1:
                self.seleccionDeColor[3] = 0
        self.TON[3].entrada = False
        self.TON[3].actualizar()
        
        if int((self.areaSalida2.index("end - 1c")).split(".")[1]) > 2000:
            self.areaSalida2.clear()
        #self.areaSalida2.appendtext(mensaje)
        
        
        if self.seleccionDeColor[3] == 0:
            self.areaSalida2.insert('end', mensaje, 'color3')
            
        if self.seleccionDeColor[3] == 1:
            self.areaSalida2.insert('end', mensaje, 'color4')
        
        self.areaSalida2.yview(END)
        
        self.TON[3].entrada = True
        self.TON[3].actualizar()


        
        