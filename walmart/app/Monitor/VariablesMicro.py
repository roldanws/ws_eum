# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "SIGFRIDO"
__date__ = "$12-jun-2019 17:27:48$"

import threading
#import time
import sys

import Interfaz
from PIL import Image, ImageTk


import os
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(ruta)

ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)))
from Variables.Variable import Variable
from Variables.InterfazGrafica import InterfazGrafica


#ruta = os.path.dirname(__file__)
#ruta = os.path.join(os.path.dirname(__file__), "/")




class VariablesMicro ():
    def __init__(self):
        """Se crean las variables que van ca controlar el flujo del programa"""
        self.comunicacion = []
        
        self.comunicacion.append(Variable("Exp-01","Expedidora_01","En zona 1","DIGITAL",0,"",0))
        self.comunicacion.append(Variable("Exp-02","Expedidora_02","En zona 2","ANALOGICA",0,"",0))
        self.comunicacion.append(Variable("Val-01","Validadora_01","En zona 3","DIGITAL",0,"",0))
        self.comunicacion.append(Variable("Val-02","Validadora_02","En zona 4","DIGITAL",0,"",0))
        self.comunicacion.append(Variable("Caj-01","Cajero_01","En zona 5","DIGITAL",0,"",0))
        self.comunicacion.append(Variable("Caj-02","Cajero_02","En zona 6","DIGITAL",0,"",0))
        self.comunicacion.append(Variable("Caj-02","Cajero_03","En zona 6","DIGITAL",0,"",0))

       
        for i, elemento in enumerate(self.comunicacion):
            InterfazGrafica(self.comunicacion[i])


        """
            
        print ("Inicio de carga de imagenes_01")

        self.imagenes_0=[]
        
        self.imagenes_0.append (ImageTk.PhotoImage(Image.open (ruta + "/Imagenes/Interfaz/Expedidora/Expedidora_gris2.png")))
        self.imagenes_0.append (ImageTk.PhotoImage(Image.open (ruta + "/Imagenes/Interfaz/Expedidora/Expedidora_rojo2.png")))
        self.imagenes_0.append (ImageTk.PhotoImage(Image.open (ruta + "/Imagenes/Interfaz/Expedidora/Expedidora_verde2.png")))
        
        print ("Inicio de carga de imagenes_02")
        
        self.imagenes_1=[]
        img = Image.open (ruta + "/Imagenes/Interfaz/Validadora/validadora_gris.png")
        self.imagenes_1.append (ImageTk.PhotoImage(img))
        
        img = Image.open (ruta + "/Imagenes/Interfaz/Validadora/validadora_rojo.png")
        self.imagenes_1.append (ImageTk.PhotoImage(img))
        
        img = Image.open (ruta + "/Imagenes/Interfaz/Validadora/validadora_verde.png")
        self.imagenes_1.append (ImageTk.PhotoImage(img))
        
        print ("Inicio de carga de imagenes_03")
        
        self.imagenes_2=[]
        img = Image.open (ruta + "/Imagenes/Interfaz/Cajero/Cajero_gris.png")
        self.imagenes_2.append (ImageTk.PhotoImage(img))
        
        img = Image.open (ruta + "/Imagenes/Interfaz/Cajero/Cajero_rojo.png")
        self.imagenes_2.append (ImageTk.PhotoImage(img))
        
        img = Image.open (ruta + "/Imagenes/Interfaz/Cajero/Cajero_verde.png")
        self.imagenes_2.append (ImageTk.PhotoImage(img))
        
        print ("Inicio de carga de imagenes_04")
        
        self.imagenes_3=[]
        img = Image.open (ruta + "/Imagenes/Interfaz/Barrera/Barrera_gris.png")
        self.imagenes_3.append (ImageTk.PhotoImage(img))
        
        img = Image.open (ruta + "/Imagenes/Interfaz/Barrera/Barrera_rojo.png")
        self.imagenes_3.append (ImageTk.PhotoImage(img))
        
        img = Image.open (ruta + "/Imagenes/Interfaz/Barrera/Barrera_verde.png")
        self.imagenes_3.append (ImageTk.PhotoImage(img))
        
        
        print ("Cargadas las imagenes")
        
        self.obtenerComunicacion(0).obtenerInterfazGrafica(0).crearEtiquetaImagen (imagenDeFondo = self.imagenes_0[0])
        self.obtenerComunicacion(0).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_0[1], Variable.ESTADO_APAGADO)
        self.obtenerComunicacion(0).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_0[2], Variable.ESTADO_ENCENDIDO)
        self.obtenerComunicacion(0).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_0[0], Variable.ESTADO_DESHABILITADO)

        self.obtenerComunicacion(1).obtenerInterfazGrafica(0).crearEtiquetaImagen (imagenDeFondo = self.imagenes_0[0])
        self.obtenerComunicacion(1).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_0[1], Variable.ESTADO_APAGADO)
        self.obtenerComunicacion(1).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_0[2], Variable.ESTADO_ENCENDIDO)
        self.obtenerComunicacion(1).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_0[0], Variable.ESTADO_DESHABILITADO)
        
        self.obtenerComunicacion(2).obtenerInterfazGrafica(0).crearEtiquetaImagen (imagenDeFondo = self.imagenes_1[0])
        self.obtenerComunicacion(2).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_1[1], Variable.ESTADO_APAGADO)
        self.obtenerComunicacion(2).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_1[2], Variable.ESTADO_ENCENDIDO)
        self.obtenerComunicacion(2).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_1[0], Variable.ESTADO_DESHABILITADO)

        self.obtenerComunicacion(3).obtenerInterfazGrafica(0).crearEtiquetaImagen (imagenDeFondo = self.imagenes_1[0])
        self.obtenerComunicacion(3).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_1[1], Variable.ESTADO_APAGADO)
        self.obtenerComunicacion(3).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_1[2], Variable.ESTADO_ENCENDIDO)
        self.obtenerComunicacion(3).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_1[0], Variable.ESTADO_DESHABILITADO)
        
        self.obtenerComunicacion(4).obtenerInterfazGrafica(0).crearEtiquetaImagen (imagenDeFondo = self.imagenes_2[0])
        self.obtenerComunicacion(4).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[1], Variable.ESTADO_APAGADO)
        self.obtenerComunicacion(4).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[2], Variable.ESTADO_ENCENDIDO)
        self.obtenerComunicacion(4).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[0], Variable.ESTADO_DESHABILITADO)

        self.obtenerComunicacion(5).obtenerInterfazGrafica(0).crearEtiquetaImagen (imagenDeFondo = self.imagenes_2[0])
        self.obtenerComunicacion(5).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[1], Variable.ESTADO_APAGADO)
        self.obtenerComunicacion(5).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[2], Variable.ESTADO_ENCENDIDO)
        self.obtenerComunicacion(5).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[0], Variable.ESTADO_DESHABILITADO)
        
        self.obtenerComunicacion(6).obtenerInterfazGrafica(0).crearEtiquetaImagen (imagenDeFondo = self.imagenes_2[0])
        self.obtenerComunicacion(6).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[1], Variable.ESTADO_APAGADO)
        self.obtenerComunicacion(6).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[2], Variable.ESTADO_ENCENDIDO)
        self.obtenerComunicacion(6).obtenerInterfazGrafica(0).anexarImagen (self.imagenes_2[0], Variable.ESTADO_DESHABILITADO)


        print ("Creado variablesMicro")
        """
        
    def obtenerComunicacion(self, indice):
        return (self.comunicacion[indice])
  

