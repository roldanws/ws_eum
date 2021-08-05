# coding=latin-1

# Parte del Modelo para el programa de comunicación 
# Desarrollado por Sigfrido Oscar Soria Frias
# En Estacionamientos Únicos de México

#import tkinter

#import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import Pmw

from PmwNoteBook import NoteBook # Se utiliza este archivo modificado debido a un error en el archivo de la libreria PmWOriginal/Color

from pyModbusTCP.client import ModbusClient


import os
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)))



class Interfaz (Frame):
    
    COLOR_TEMA = "#F0F0F0"

    
    DIC_PUERTOS = {}
    DIC_BAUD = { "9600" : 9600, "19200" : 19200 , "38400" : 38400, "57600" : 57600, "115200" : 115200}
    DIC_PARIDAD = { "Ninguna" : 0, "Par" : 1 , "Impar" : 2}
    DIC_STOP = {"1" : 1, "1.5" : 1.5, "2" : 2}
    DIC_BITS = {"5 Bits" : 5, "6 Bits" : 6, "7 Bits" : 7, "8 Bits" : 8}    
    

    
    def __init__(self, parent, Control):
        Frame.__init__(self, parent)
        Pmw.initialise()
        
        self.controlador = Control

        if self.controlador is not None:
            parent.protocol("WM_DELETE_WINDOW", self.controlador.terminarAplicacion)
        
        self.pack ( expand = YES, fill = BOTH)
        self.master.title ("Monitor")
        self.master.geometry ("1180x840+10+20")
        self.master.minsize (height=600, width=800)
        
        self.initUI()

        self.initPuertos()

#        self.initUISerie()

        self.initUIPaginas()

        #self.initUIModbus()
        
    def initUI (self):
        self.colorSeleccionado = StringVar()        

        self.myBalloon = Pmw.Balloon (self)
        barra = Pmw.MenuBar ( self, balloon = self.myBalloon)
        barra.pack (fill = X)

        self.area = Frame ( self)
        self.area.pack (expand = YES, fill = BOTH )
        self.area.rowconfigure(0, weight = 1)
        self.area.columnconfigure(0, weight = 1)
        
        self.areaTrabajo = Frame ( self.area)
        self.areaTrabajo.rowconfigure(0, weight = 1)
        self.areaTrabajo.columnconfigure(0, weight = 1)
        self.areaTrabajo.grid (row = 0, column = 0, rowspan = 1, columnspan = 1 , padx = 5, pady = 2, sticky = E+W+S+N)

        self.imagenes=[]
        self.canvas = Canvas (self.areaTrabajo, bg='#faf0e6')
        self.canvas.grid(row = 0, column = 0, rowspan = 1, columnspan = 1,  sticky = E+W+S+N)
        
        img = Image.open (ruta + "/Imagenes/Tijuana_Salida.jpg")
        #print ("Image size %d %d" % img.size)
        img = img.resize((2049, 703), Image.ANTIALIAS)
        self.imagenes.append (ImageTk.PhotoImage(img))
        self.canvas.create_image(-350,0, anchor = NW, image=self.imagenes[0])         
        
        img = Image.open (ruta +  "/Imagenes/Logo EUM.png").resize((150, 150), Image.ANTIALIAS)
        self.imagenes.append (ImageTk.PhotoImage(img))
        self.canvas.create_image(20,20, anchor = NW, image=self.imagenes[1])
        
        #img = Image.open ("../Imagenes/Logo EUM.png")
        #img = img.resize((150, 150), Image.ANTIALIAS)
        #self.photoImage = ImageTk.PhotoImage(img)
        #self.panel = Label(self.areaTrabajo, image = self.photoImage)
        #self.panel.image = self.photoImage
        #self.panel.place (x=400, y=400)
        #self.panel.pack()

        #-------------------#
        #Dependientes de areaMensajero
        self.frameMensajero = Frame ( self.area)
        self.frameMensajero.grid (row = 1, column = 0, rowspan = 1, columnspan = 1 , padx = 5, pady = 2, sticky = E+W+S+N)
        self.frameMensajero.columnconfigure (0, weight = 5)
        self.frameMensajero.columnconfigure (1, weight = 4)
        
        self.areaMensajero1 = Pmw.ScrolledText ( self.frameMensajero, text_height = 3, text_wrap = WORD, hscrollmode = "dynamic", vscrollmode = "dynamic")
        self.areaMensajero1.grid (row = 0, column = 0, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        
        self.areaMensajero2 = Pmw.ScrolledText ( self.frameMensajero, text_height = 3, text_wrap = WORD, hscrollmode = "dynamic", vscrollmode = "dynamic")
        self.areaMensajero2.grid (row = 0, column = 1, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)

        self.areaMensajero3 = Pmw.ScrolledText ( self.frameMensajero, text_height = 3, text_width = 15, text_wrap = WORD, hscrollmode = "dynamic", vscrollmode = "dynamic")
        self.areaMensajero3.grid (row = 0, column = 2, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        self.areaMensajero3.tag_configure('color1', foreground='red')
        self.areaMensajero3.tag_configure('color2', foreground='blue')
        self.areaMensajero3.tag_configure('color3', foreground='green')
        self.areaMensajero3.tag_configure('color4', foreground='magenta')


        barra.addmenu ('Archivo', 'Salir', font=('Arial', 10))
        barra.addmenuitem ('Archivo', 'command', command = self.controlador.terminarAplicacion, label = 'Salir')
        
        barra.addmenu ('Comunicación', 'Parametros Comunicación', font=('Arial', 10))
        barra.addmenuitem ('Comunicación', 'command', label = 'Puerto Serie', command = self.seleccionarInterfazSerie)
        barra.addmenuitem ('Comunicación', 'command', label = 'Puerto Ethernet', command = self.seleccionarInterfazEthernet)

        barra.addmenu ('Ayuda', 'Ayuda', font=('Arial', 10))
        barra.addmenuitem ('Ayuda', 'command', label = 'Acerca de...')
        barra.addmenuitem ('Ayuda', 'command', label = 'Notas de la versión')

        #----------------------------------------------------------------------------------------------------------
        #Dependientes de areaTrabajo

        


        """
        self.areaTrabajoModbus = Frame ( self.areaTrabajo, bg = self.COLOR_TEMA)
        self.areaTrabajoModbus.columnconfigure(2, weight=1)
        #self.areaTrabajoModbus.columnconfigure(5, weight=1)
        self.areaTrabajoModbus.rowconfigure(5, weight = 1)
        """
        



        
        
    def initPuertos (self):
        """Panel destinado para la organización de la comunicación por diferentes puertos de comunicación"""

        self.notebook = NoteBook(self.areaTrabajo)
        self.notebook.grid(row = 0, column = 0, rowspan = 1, columnspan = 1,  sticky = E+W+S+N)


        self.idnumero = StringVar(value=" ")

        self.paginas = []
        self.paginas.append(self.notebook.add('Serie'))
        self.paginas.append(self.notebook.add('Serie 2'))
        self.paginas.append(self.notebook.add('TCP/IP'))


        for i in range (len(self.paginas)):
            self.paginas[i].grid (row = 0, column = 0, rowspan = 1, columnspan = 1 , sticky = E+W+S+N)
            self.paginas[i].columnconfigure(0, weight=1)
            self.paginas[i].rowconfigure(0, weight=1)


    def initUIPaginas(self):
        areaTrabajoSerie1 = Frame (self.paginas[0])
        areaTrabajoSerie1.grid (row = 0, column = 0, rowspan = 1, columnspan = 1 , sticky = E+W+S+N)
        areaTrabajoSerie1.columnconfigure(0, weight=1)
        areaTrabajoSerie1.columnconfigure(5, weight=1)
        areaTrabajoSerie1.rowconfigure(5, weight = 1)
        
        frameConexion2 =  self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).obtenerFrameConexion(areaTrabajoSerie1)
        frameConexion2.grid(row = 1, column = 0, rowspan = 1, columnspan = 7, sticky=E+W+S+N, pady=5, padx=5)            
        frameBotonesConexion2 =  self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).obtenerFrameBotonesConexion(areaTrabajoSerie1)
        frameBotonesConexion2.grid(row = 1, column = 10, rowspan = 1, columnspan = 2, sticky=S+N, pady=5, padx=5)
        frameEnviarTexto = self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).obtenerFrameEnviarTexto(areaTrabajoSerie1)
        frameEnviarTexto.grid(row = 3, column = 0, rowspan = 1, columnspan = 10, padx = 5, pady = 5, sticky = E+W+S+N)
        frameEnviarDatosHexadecimal = self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).obtenerFrameEnviarDatosHexadecimal(areaTrabajoSerie1)
        frameEnviarDatosHexadecimal.grid(row = 3, column = 10, rowspan = 1, columnspan = 2 , padx = 5, pady = 5, sticky = E+W)

        frameDatos = Frame (areaTrabajoSerie1)
        frameDatos.grid (row = 5, column = 0, rowspan = 1, columnspan = 12 , pady = 3, sticky = E+W+S+N)
        frameDatos.columnconfigure (0, weight = 3)
        frameDatos.columnconfigure (1, weight = 1)
        frameDatos.rowconfigure (0, weight = 1)
        frameDatos.rowconfigure (1, weight = 1)        
        
        areaEntrada1 = self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).obtenerCuadroComunicacion(frameDatos, "TEXTO_ENTRADA_1")
        areaEntrada1.grid (row = 0, column = 0, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        areaEntrada2 = self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).obtenerCuadroComunicacion(frameDatos, "TEXTO_ENTRADA_2")
        areaEntrada2.grid (row = 0, column = 1, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        areaSalida1 = self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).obtenerCuadroComunicacion(frameDatos, "TEXTO_SALIDA_1")
        areaSalida1.grid (row = 1, column = 0, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        areaSalida2 = self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).obtenerCuadroComunicacion(frameDatos, "TEXTO_SALIDA_2")
        areaSalida2.grid (row = 1, column = 1, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        

        
        
        
        #------------------------------------------------
        frameProtocolos = Frame (areaTrabajoSerie1) 
        frameProtocolos.grid(row = 4, column = 0, rowspan = 1, columnspan = 12 , padx = 5, pady = 5, sticky = E+W)
        
        
        frameProtocolo = self.controlador.listadePuertos[0].obtenerProtocoloDeComunicacion().obtenerInterfaz(0).obtenerFrame(frameProtocolos) 
        frameProtocolo.grid(row = 0, column = 0, rowspan = 1, columnspan = 1 , padx = 5, pady = 5, sticky = E+W)
        
        frameProtocolo_02 = self.controlador.listadePuertos[0].obtenerProtocoloDeComunicacion_02().obtenerInterfaz(0).obtenerFrame(frameProtocolos) 
        frameProtocolo_02.grid(row = 0, column = 1, rowspan = 1, columnspan = 1 , padx = 5, pady = 5, sticky = E+W)

        frameProtocolo_03 = self.controlador.listadePuertos[0].obtenerProtocoloDeComunicacion_03().obtenerInterfaz(0).obtenerFrame(frameProtocolos) 
        frameProtocolo_03.grid(row = 0, column = 2, rowspan = 1, columnspan = 1 , padx = 5, pady = 5, sticky = E+W)
        
        
        #------------------------------------------------

        areaTrabajoSerie2 = Frame (self.paginas[1])
        areaTrabajoSerie2.grid (row = 0, column = 0, rowspan = 1, columnspan = 1 , sticky = E+W+S+N)
        areaTrabajoSerie2.columnconfigure(0, weight=1)
        areaTrabajoSerie2.columnconfigure(5, weight=1)
        areaTrabajoSerie2.rowconfigure(5, weight = 1)
        
        frameConexion2 =  self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).obtenerFrameConexion(areaTrabajoSerie2)
        frameConexion2.grid(row = 1, column = 0, rowspan = 1, columnspan = 7, sticky=E+W+S+N, pady=5, padx=5)            
        frameBotonesConexion2 =  self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).obtenerFrameBotonesConexion(areaTrabajoSerie2)
        frameBotonesConexion2.grid(row = 1, column = 10, rowspan = 1, columnspan = 2, sticky=S+N, pady=5, padx=5)
        frameEnviarTexto = self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).obtenerFrameEnviarTexto(areaTrabajoSerie2)
        frameEnviarTexto.grid(row = 3, column = 0, rowspan = 1, columnspan = 10, padx = 5, pady = 5, sticky = E+W+S+N)
        frameEnviarDatosHexadecimal = self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).obtenerFrameEnviarDatosHexadecimal(areaTrabajoSerie2)
        frameEnviarDatosHexadecimal.grid(row = 3, column = 10, rowspan = 1, columnspan = 2 , padx = 5, pady = 5, sticky = E+W)

        frameDatos = Frame (areaTrabajoSerie2)
        frameDatos.grid (row = 5, column = 0, rowspan = 1, columnspan = 12 , padx = 5, pady = 3, sticky = E+W+S+N)
        frameDatos.columnconfigure (0, weight = 3)
        frameDatos.columnconfigure (1, weight = 1)
        frameDatos.rowconfigure (0, weight = 1)
        frameDatos.rowconfigure (1, weight = 1)        
        
        areaEntrada1 = self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).obtenerCuadroComunicacion(frameDatos, "TEXTO_ENTRADA_1")
        areaEntrada1.grid (row = 0, column = 0, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        areaEntrada2 = self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).obtenerCuadroComunicacion(frameDatos, "TEXTO_ENTRADA_2")
        areaEntrada2.grid (row = 0, column = 1, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        areaSalida1 = self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).obtenerCuadroComunicacion(frameDatos, "TEXTO_SALIDA_1")
        areaSalida1.grid (row = 1, column = 0, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        areaSalida2 = self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).obtenerCuadroComunicacion(frameDatos, "TEXTO_SALIDA_2")
        areaSalida2.grid (row = 1, column = 1, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)


        self.controlador.listadePuertos[0].obtenerInterfazGrafica(0).habilitarControlesFrameConexion(True)
        self.controlador.listadePuertos[1].obtenerInterfazGrafica(0).habilitarControlesFrameConexion(True)


    def initUIModbus (self):
        """Panel para la comunicación por un puerto Ethernet"""
        
        
        #------------------#

        self.frameConexionEthernet = LabelFrame ( self.areaTrabajoModbus, bg = self.COLOR_TEMA, text="Ethernet", borderwidth=2, relief="groove")
        self.frameConexionEthernet.grid(row = 1, column = 0, rowspan = 1, columnspan = 5, sticky=E+W+S+N, pady=5, padx=5)
        
        self.lblEther00 = Label(self.frameConexionEthernet, text="Puerto Ethernet", bg = self.COLOR_TEMA)
        #self.lblEther00.grid(row = 0, column = 0, columnspan=2, rowspan=1, sticky=W, pady=5, padx=5)
        
        self.lblEther01 = Label(self.frameConexionEthernet, text="Direccion", width=10, justify=LEFT, bg = self.COLOR_TEMA)
        self.lblEther01.grid(row = 1, column = 0, sticky=W, pady=5, padx=5)
        
        self.txtEtherDireccion = Entry (self.frameConexionEthernet, name="txtEtherDireccion", width=15)
        self.txtEtherDireccion.grid (row=1, column=1, columnspan=1, rowspan=1, padx=5, pady=5)
        
        self.lblEther02 = Label(self.frameConexionEthernet, text="Puerto", width=10, bg = self.COLOR_TEMA)
        self.lblEther02.grid(row = 1, column = 2, pady=5, padx=5)
        
        self.txtEtherPuerto = Entry (self.frameConexionEthernet, name="txtEtherPuerto", width=15)
        self.txtEtherPuerto.grid (row=1, column=3, columnspan=1, rowspan=1, padx=5, pady=5)
        
        #------------------#
        
        
        self.frameBotonesConexion = Frame ( self.areaTrabajoModbus, bg = self.COLOR_TEMA )
        self.frameBotonesConexion.grid(row = 1, column = 5, rowspan = 2, columnspan = 2, sticky=S+N, pady=5, padx=5)
        self.frameBotonesConexion.columnconfigure (0, weight = 1)
        self.frameBotonesConexion.columnconfigure (1, weight = 1)
        self.frameBotonesConexion.rowconfigure (1, weight = 1)
        
        self.btnConectar = Button (self.frameBotonesConexion, text = "Conectar", width = 12, command = self.abrirPuerto, bg = self.COLOR_TEMA)
        self.btnConectar.grid (row = 1, column = 0, rowspan = 1, columnspan = 1,  padx = 5, pady = 15)
        
        self.btnDesconectar = Button ( self.frameBotonesConexion, text = "Desconectar", command = self.controlador.cerrarPuerto, width = 12, bg = self.COLOR_TEMA)
        self.btnDesconectar.grid (row = 2, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 15)

        #------------------#

        self.frameBotonesEnviar = LabelFrame ( self.areaTrabajoModbus, bg = self.COLOR_TEMA, borderwidth=2, relief="groove", text ="Texto")
        self.frameBotonesEnviar.grid(row = 3, column = 0, rowspan = 1, columnspan = 7, padx = 5, pady = 5, sticky = E+W+S+N)
        self.frameBotonesEnviar.columnconfigure (1, weight=1)
        
        self.lblEnviarDatos = Label(self.frameBotonesEnviar, text="Texto", width=10, bg = self.COLOR_TEMA)
        #self.lblEnviarDatos.grid(row = 0, column = 0, sticky=W, pady=5, padx=5) 

        self.txtEnviarDatos = Entry (self.frameBotonesEnviar, name = "txtEnviarDatos", textvariable = self.idEnviarDatos)
        self.txtEnviarDatos.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)
        self.txtEnviarDatos.bind("<Return>", self.enviarDatos2)
        
        self.botonEnviarDatos = Button ( self.frameBotonesEnviar, text ="Enviar", width = 12, command = self.enviarDatos, bg = self.COLOR_TEMA)
        self.botonEnviarDatos.grid (row = 0, column = 2, rowspan = 1, columnspan = 1, padx = 5, pady = 5)
        
        #-------------------#
        
        self.frameInstruccionesHexadecimal = LabelFrame ( self.areaTrabajoModbus, bg = self.COLOR_TEMA, borderwidth=2, relief="groove", text ="Hexadecimal")
        self.frameInstruccionesHexadecimal.grid(row = 2, column = 0, rowspan = 1, columnspan = 5 , padx = 5, pady = 5, sticky = E+W+N+S)
        self.frameBotonesConexion.columnconfigure (0, weight = 1)

        self.txtEnviarHexadecimal = Entry (self.frameInstruccionesHexadecimal, name = "txtEnviarDatos", textvariable = self.idEnviarDatosHex)
        self.txtEnviarHexadecimal.grid (row = 0, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 8, sticky = E+W+S+N)
        
        self.botonEnviarHexadecimal = Button ( self.frameInstruccionesHexadecimal, text ="Enviar Hex", width = 10, bg = self.COLOR_TEMA, command = self.enviarHexadecimal)
        self.botonEnviarHexadecimal.grid (row = 0, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 8, sticky = S+N)

        self.botonEnviarHexadecimalIniciar = Button ( self.frameInstruccionesHexadecimal, text ="Iniciar", width = 10, command = self.iniciarCiclo, bg = self.COLOR_TEMA)
        #self.botonEnviarHexadecimalIniciar.grid (row = 0, column = 3, rowspan = 1, columnspan = 1, padx = 5, pady = 5)

        self.botonEnviarHexadecimalParar = Button ( self.frameInstruccionesHexadecimal, text ="Parar", width = 10, command = self.terminarCiclo, bg = self.COLOR_TEMA)
        #self.botonEnviarHexadecimalParar.grid (row = 0, column = 4, rowspan = 1, columnspan = 1, padx = 5, pady = 5)        
        
        #-------------------#

        self.idModbusUnidad = StringVar(value=" ")
        tuplaIdModbusUnidad = ()
        for i in range (10):
            tuplaIdModbusUnidad += (i,)
        #print (tuplaIdModbusUnidad)

        self.idModbusFuncion = StringVar(value=" ")
        tuplaIdModbusFuncion = ()
        for i in range (10):
            tuplaIdModbusFuncion += (i,)
        #print (tuplaIdModbusFuncion)

        
        self.idModbusRegistroInicial = StringVar(value=" ")
        tuplaIdModbusRegistroInicial = ()
        for i in range (10):
            tuplaIdModbusRegistroInicial += (i,)
        #print (tuplaIdModbusRegistroInicial)
        
        self.idModbusNumeroDeRegistros = StringVar(value=" ")
        tuplaIdModbusNumeroDeRegistros = ()
        for i in range (255):
            tuplaIdModbusNumeroDeRegistros += (i,)
        #print (tuplaIdModbusNumeroDeRegistros)
        
        self.idModbusEnviar = StringVar(value=" ")
        
        
        self.frameModbusInstruccion = LabelFrame ( self.areaTrabajoModbus, bg = self.COLOR_TEMA, borderwidth=2, relief="groove", text ="Instrucción")
        self.frameModbusInstruccion.grid(row = 4, column = 2, rowspan = 1, columnspan = 5 , padx = 5, pady = 5, sticky = E+W+S+N)

        self.modbusBotonUnidad = Spinbox (self.frameModbusInstruccion, values = tuplaIdModbusUnidad, textvariable = self.idModbusUnidad, command = self.seleccionarModbusInstruccion, width = 8)
        self.modbusBotonUnidad.grid(row = 1, column = 1, rowspan = 1, columnspan = 1 , padx = 5, pady = 5, sticky = E+W)
        
        #self.modbusBotonUnidad.bind("<<ComboboxSelected>>", self.seleccionarModbusInstruccion)

        self.modbusBotonFuncion = Spinbox (self.frameModbusInstruccion, values = tuplaIdModbusFuncion, textvariable = self.idModbusFuncion, command = self.seleccionarModbusInstruccion, width = 8)
        self.modbusBotonFuncion.grid(row = 1, column = 3, rowspan = 1, columnspan = 1 , padx = 5, pady = 5, sticky = E+W)

        self.modbusBotonRegistroInicial = Spinbox (self.frameModbusInstruccion, values = tuplaIdModbusRegistroInicial, textvariable = self.idModbusRegistroInicial, command = self.seleccionarModbusInstruccion, width = 8)
        self.modbusBotonRegistroInicial.grid(row = 1, column = 5, rowspan = 1, columnspan = 1 , padx = 5, pady = 5, sticky = E+W)

        self.modbusBotonNumeroDeRegistros = Spinbox (self.frameModbusInstruccion, values = tuplaIdModbusNumeroDeRegistros, textvariable = self.idModbusNumeroDeRegistros, command = self.seleccionarModbusInstruccion, width = 8)
        self.modbusBotonNumeroDeRegistros.grid(row = 1, column = 7, rowspan = 1, columnspan = 1 , padx = 5, pady = 5, sticky = E+W)
        
        
        self.lblModbusUnidad = Label(self.frameModbusInstruccion, text="Unidad", width=8, bg = self.COLOR_TEMA)
        self.lblModbusUnidad.grid(row = 0, column = 1, sticky=W, pady=0, padx=5) 
        
        self.lblModbusFuncion = Label(self.frameModbusInstruccion, text="Función", width=8, bg = self.COLOR_TEMA, wraplength = 50)
        self.lblModbusFuncion.grid(row = 0, column = 3, sticky=W, pady=0, padx=5) 

        self.lblModbusRegistroInicial = Label(self.frameModbusInstruccion, text="Registro Inicial", width=8, bg = self.COLOR_TEMA, wraplength = 50)
        self.lblModbusRegistroInicial.grid(row = 0, column = 5, sticky=W, pady=0, padx=5) 

        self.lblModbusNumeroDeRegistros = Label(self.frameModbusInstruccion, text="Num de Registros", width=8, bg = self.COLOR_TEMA, wraplength = 50)
        self.lblModbusNumeroDeRegistros.grid(row = 0, column = 7, sticky=W, pady=0, padx=5) 


        self.txtModbusEnviar = Entry (self.frameModbusInstruccion, name = "txtModbusEnviar", textvariable = self.idModbusEnviar)
        self.txtModbusEnviar.grid (row = 2, column = 0, rowspan = 1, columnspan = 6, padx = 5, pady = 8, sticky = E+W+S+N)
        
        self.botonModbusEnviar = Button ( self.frameModbusInstruccion, text ="Enviar", width = 10, bg = self.COLOR_TEMA, command = self.enviarModbus)
        self.botonModbusEnviar.grid (row = 2, column = 6, rowspan = 1, columnspan = 2, padx = 5, pady = 8, sticky = S+N)

        
        
        
        self.tree = ttk.Treeview(self.areaTrabajoModbus)
        self.tree.grid(row = 1, column = 7, rowspan = 4, columnspan = 5, padx = 5, pady = 5, sticky = E+W+N+S)
        
        self.tree["columns"]=("one","two","three")
        
        
        self.tree.column("#0", width=150, minwidth=150, stretch=NO)
        self.tree.column("one", width=150, minwidth=150, stretch=NO)
        self.tree.column("two", width=150, minwidth=150)
        self.tree.column("three", width=150, minwidth=150, stretch=NO)
        
        # Level 1
        folder1 = self.tree.insert("", 1, text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
        
        self.tree.insert("", 2, text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
        # Level 2
        self.tree.insert(folder1, "end", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
        self.tree.insert(folder1, "end", text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
        self.tree.insert(folder1, "end", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))
        
        
        #-------------------#
        
        self.frameDatos = Frame ( self.areaTrabajoModbus , bg = self.COLOR_TEMA)
        self.frameDatos.grid (row = 5, column = 0, rowspan = 1, columnspan = 12 , padx = 5, pady = 3, sticky = E+W+S+N)
        self.frameDatos.columnconfigure (0, weight = 3)
        self.frameDatos.columnconfigure (1, weight = 1)
        self.frameDatos.rowconfigure (0, weight = 1)
        self.frameDatos.rowconfigure (1, weight = 1)
        
        self.boton1 = Button ( self.frameDatos, text ="iniciar", width = 10, bg = self.COLOR_TEMA)
        #self.boton1.grid (row = 2, column = 0, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)

        self.boton2 = Button ( self.frameDatos, text ="Parar", width = 10)
        #self.boton2.grid (row = 2, column = 1, rowspan = 1, columnspan = 1, padx = 5, pady = 5, sticky = E+W+S+N)        

        
        """
        self.courierFont = "Courier 10"
			
        self.areaEntrada1 = Pmw.ScrolledText ( self.frameDatos, hscrollmode = "dynamic", vscrollmode = "dynamic", text_font = self.courierFont, text_wrap = WORD, text_width=21)
        self.areaEntrada1.grid (row = 0, column = 0, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        self.areaEntrada1.configure(text_state = 'disabled')
        
        self.areaEntrada2 = Pmw.ScrolledText ( self.frameDatos, hscrollmode = "dynamic", vscrollmode = "dynamic", text_font = self.courierFont, text_wrap = WORD, text_width=7)
        self.areaEntrada2.grid (row = 0, column = 1, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        self.areaEntrada2.configure(text_state = 'disabled')

        self.areaSalida1 = Pmw.ScrolledText ( self.frameDatos,  hscrollmode = "dynamic", vscrollmode = "dynamic", text_font = self.courierFont, text_wrap = WORD, text_width=21)
        self.areaSalida1.grid (row = 1, column = 0, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        self.areaSalida1.configure(text_state = 'disabled')

        self.areaSalida2 = Pmw.ScrolledText ( self.frameDatos, hscrollmode = "dynamic", vscrollmode = "dynamic", text_font = self.courierFont, text_wrap = WORD, text_width=7)
        self.areaSalida2.grid (row = 1, column = 1, columnspan = 1, rowspan = 1, padx = 5, pady = 5, sticky=E+W+S+N)
        self.areaSalida2.configure(text_state = 'disabled')
		"""
        
        
 
    def escribirMensajero1(self, mensaje):
        if len(self.areaMensajero1.get(0.0, END)) > 1500:
            self.areaMensajero1.clear()
        self.areaMensajero1.appendtext(mensaje)
        self.areaMensajero1.yview(END)

    def escribirMensajero2 (self, mensaje):
        if len(self.areaMensajero2.get(0.0, END)) > 1500:
            self.areaMensajero2.clear()
        self.areaMensajero2.appendtext(mensaje)
        self.areaMensajero2.yview(END)

    def escribirMensajero3 (self, mensaje):
        self.areaMensajero3.appendtext(mensaje)
        self.areaMensajero3.yview(END)


        
    #-------Para el protocolo Modbus
    def enviarModbus ( self ):
        print ("Se enviará el valor de  %s"  % self.idModbusEnviar.get())
         
    def seleccionarModbusInstruccion(self):
        #print("El valor obtenido es %s %s %s %s" % (self.idModbusUnidad.get(), self.idModbusFuncion.get(), self.idModbusRegistroInicial.get(), self.idModbusNumeroDeRegistros.get()) )
        datos = []
        datos.append (int (self.idModbusUnidad.get()))
        datos.append (int (self.idModbusFuncion.get()))
        datos.append (int (self.idModbusRegistroInicial.get()))
        datos.append (int (self.idModbusNumeroDeRegistros.get()))
        
        
        self.convertirInstruccion(datos)
        
        instruccion = self.idModbusUnidad.get() + self.idModbusFuncion.get()+ self.idModbusRegistroInicial.get() + self.idModbusNumeroDeRegistros.get()
        self.escribirModbusInstruccion (instruccion)
        

        
    def convertirInstruccion (self, datos):
        arregloByte  = bytearray(12)
        
        arregloByte[6] = datos[0].to_bytes(1, byteorder='big')[0]
        arregloByte[7] = datos[1].to_bytes(1, byteorder='big')[0]
        #arregloByte[8] = datos[2].to_bytes(1, byteorder='big')[1]
        arregloByte[9] = datos[2].to_bytes(1, byteorder='big')[0]
        #arregloByte[10] = datos[3].to_bytes(1, byteorder='big')[1]
        arregloByte[11] = datos[3].to_bytes(1, byteorder='big')[0]
        
        print ("ArregloByte ", arregloByte)
            
        
        
    def escribirModbusInstruccion (self, mensaje):
        if mensaje:
            self.txtModbusEnviar.delete (0, END)
            self.txtModbusEnviar.insert(0, mensaje)
        
        
    #-------Seleccionar el menú de comunicación-------#
    
    def seleccionarInterfazSerie (self):
        """Mostrar pantalla para comunicación serie"""
        
        #self.areaTrabajoModbus.grid_forget();        
        self.areaTrabajoSerie.grid (row = 0, column = 0, rowspan = 1, columnspan = 1 , padx = 5, pady = 2, sticky = E+W+S+N)

        print ("Seleccionado menu Serie")
        
    def seleccionarInterfazEthernet (self):
        """Mostrar pantalla para comunicacion ethernet"""
        
        self.areaTrabajoSerie.grid_forget();
        #self.areaTrabajoModbus.grid (row = 0, column = 0, rowspan = 1, columnspan = 1 , padx = 5, pady = 2, sticky = E+W+S+N)

        print ("Seleccionado menu TCP")
        

def main ():
    Interfaz().mainloop()

if __name__ == "__main__":
    main()

