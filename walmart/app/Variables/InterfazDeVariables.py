__author__ = "SIGFRIDO"
__date__ = "$17-sep-2019 9:53:18$"

from PyQt5 import QtWidgets, QtGui
from tkinter import *

import threading

import os
import sys
import platform
sistema = platform.system()
plataforma = platform.uname()
version = ""

caracterDirectorio = ""
if sistema == "Windows":
	caracterDirectorio = '\\'
elif  sistema == "Linux":
    caracterDirectorio = '/'
    if plataforma.node == "raspberrypi":
        version = plataforma.node

ruta =  os.path.dirname(os.path.abspath(__file__)) + caracterDirectorio
rutaUsuario = os.path.expanduser('~') + caracterDirectorio

#ruta = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



sys.path.append(os.path.join(ruta, ".."))
sys.path.append(os.path.join(ruta, ".." + caracterDirectorio + ".."))

ruta = os.path.dirname(os.path.abspath(__file__))

from Variable import Variable
from InterfazGrafica import InterfazGrafica

from Temporizador import Temporizador




class PruebaInterfazQT (threading.Thread):

    etiquetaTag = []
    etiquetaNombre = []
    etiquetaDescripcion = []
    etiquetaValor = []
    etiquetaValor_2 = []

    def __init__(self, objeto = None, name = ""):
        threading.Thread.__init__ (self, name = None)
        self.objeto = objeto

        
    def run (self):
        app = QtWidgets.QApplication(["Default"])

        print("Dentro de QT El tipo de objeto ", type(self.objeto))
        self.area = QtWidgets.QWidget()




        if isinstance (self.objeto, list):
            self.numeroDeObjetos = len(self.objeto)

            for i, elemento in enumerate(self.objeto):

                self.etiquetaTag.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaTag(self.area))
                self.etiquetaTag[i].setStyleSheet("font-size: 14px; background-color: #63b4f4;")
                self.etiquetaTag[i].move(10,20*i)
                
                self.etiquetaNombre.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaNombre(self.area))
                self.etiquetaNombre[i].move(100,20*i)
                
                self.etiquetaDescripcion.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaDescripcion(self.area))
                self.etiquetaDescripcion[i].move(300,20*i)

                self.etiquetaValor.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaValor(self.area))
                self.etiquetaValor[i].setStyleSheet("font-size: 14px; background-color: #63b4f4;")
                self.etiquetaValor[i].move(500,20*i)

                self.etiquetaValor_2.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaValor_2(self.area))
                self.etiquetaValor_2[i].setStyleSheet("font-size: 14px; background-color: #63b4f4;")
                self.etiquetaValor_2[i].move(700,20*i)


                elemento.actualizarInterfaz()


        if isinstance (self.objeto, Variable):
            self.numeroDeObjetos = 1

            elemento = self.objeto
            i = 0

            self.etiquetaTag.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaTag(self.area))


            self.etiquetaTag[i].setStyleSheet("font-size: 14px; background-color: #4075CC;")
            self.etiquetaTag[i].move(10,10)
            
            self.etiquetaNombre.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaNombre(self.area))
            self.etiquetaNombre[i].move(100,10)
            
            self.etiquetaDescripcion.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaDescripcion(self.area))
            self.etiquetaDescripcion[i].move(300,10)

            self.etiquetaValor.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaValor(self.area))
            self.etiquetaValor[i].move(500,10)

            self.etiquetaValor_2.append(elemento.obtenerInterfazGrafica(1).obtenerEtiquetaValor_2(self.area))
            self.etiquetaValor_2[i].move(600,10)
        

        self.area.setWindowTitle('Interfaz QT')
        self.area.setGeometry(1000, 50, 700, 450)
        self.area.show()
        app.exec_()
        #self.objeto.borrarInterfazGrafica(1)
        print ("Fin del metodo RUN en QT")


class PruebaInterfazTK (threading.Thread):

    etiquetaTag = []
    etiquetaNombre = []
    etiquetaDescripcion = []
    etiquetaValor = []
    etiquetaValor_2 = []


    def __init__(self, args = (), objeto = None):
        threading.Thread.__init__ (self, name = None)
        self.objeto = objeto

        

    def run (self):
        self.root = Tk()
        
        self.area = Frame (self.root)
        self.area.grid(row = 1, column = 0, sticky=W, pady=5, padx=5)
        
        print("Dentro de TK el tipo de objeto ", type(self.objeto))

        if isinstance (self.objeto, list):

            for i, elemento in enumerate(self.objeto):

                self.etiquetaTag.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaTag(self.area))
                self.etiquetaTag[i].grid(row = i + 1, column = 0, sticky=W, pady=5, padx=5)   
                
                self.etiquetaNombre.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaNombre(self.area))
                self.etiquetaNombre[i].grid(row = i + 1, column = 1, sticky=W, pady=5, padx=5)   
                
                self.etiquetaDescripcion.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaDescripcion(self.area))
                self.etiquetaDescripcion[i].grid(row = i + 1, column = 2, sticky=W, pady=5, padx=5)   

                self.etiquetaValor.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaValor(self.area))
                self.etiquetaValor[i].grid(row = i + 1, column = 3, sticky=W, pady=5, padx=5)   

                self.etiquetaValor_2.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaValor_2(self.area))
                self.etiquetaValor_2[i].grid(row = i + 1, column = 4, sticky=W, pady=5, padx=5)   

        if isinstance (self.objeto, Variable):
            print ("Dentro de objeto")
            elemento = self.objeto
            i = 0

            self.etiquetaTag.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaTag(self.area))
            self.etiquetaTag[i].grid(row = i + 1, column = 0, sticky=W, pady=5, padx=5)   
            
            self.etiquetaNombre.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaNombre(self.area))
            self.etiquetaNombre[i].grid(row = i + 1, column = 1, sticky=W, pady=5, padx=5)   
            
            self.etiquetaDescripcion.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaDescripcion(self.area))
            self.etiquetaDescripcion[i].grid(row = i + 1, column = 2, sticky=W, pady=5, padx=5)   

            self.etiquetaValor.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaValor(self.area))
            self.etiquetaValor[i].grid(row = i + 1, column = 3, sticky=W, pady=5, padx=5)   

            self.etiquetaValor_2.append(elemento.obtenerInterfazGrafica(0).obtenerEtiquetaValor_2(self.area))
            self.etiquetaValor_2[i].grid(row = i + 1, column = 4, sticky=W, pady=5, padx=5)   


        self.root.title("Interfaz TKinter")
        self.root.geometry ("700x450+1000+550")
        self.root.mainloop()

        #self.objeto.borrarInterfazGrafica(0)
        

        print ("Fin del metodo RUN en Tkinter")

class ListaDeVariables ():
    X = []
    Y = []
    Z = []

    VD = []

    dispositivos = []


    def __init__(self):
        self.inicializarVariables()

    def inicializarVariables(self):
        self.X.append(Variable("X-00", "X-00", 0))
        self.X.append(Variable("X-01", "X-01", 0))
        self.X.append(Variable("X-02", "X-02", 0))
        self.X.append(Variable("X-03", "X-03", 0))
        self.X.append(Variable("X-04", "X-04", 0))
        self.X.append(Variable("X-05", "X-05", 0))
        self.X.append(Variable("X-06", "X-06", 0))
        self.X.append(Variable("X-07", "X-07", 0))
        self.X.append(Variable("X-08", "X-08", 0))
        self.X.append(Variable("X-09", "X-09", 0))
        self.X.append(Variable("X-10", "X-10", 0))
        self.X.append(Variable("X-11", "X-11", 0))
        self.X.append(Variable("X-12", "X-12", 0))
        self.X.append(Variable("X-13", "X-13", 0))
        self.X.append(Variable("X-14", "X-14", 0))
        self.X.append(Variable("X-15", "X-15", 0))


        self.Y.append(Variable("Y-00", "Y-00", 0))
        self.Y.append(Variable("Y-01", "Y-01", 0))
        self.Y.append(Variable("Y-02", "Y-02", 0))
        self.Y.append(Variable("Y-03", "Y-03", 0))
        self.Y.append(Variable("Y-04", "Y-04", 0))
        self.Y.append(Variable("Y-05", "Y-05", 0))
        self.Y.append(Variable("Y-06", "Y-06", 0))
        self.Y.append(Variable("Y-07", "Y-07", 0))
        self.Y.append(Variable("Y-08", "Y-08", 0))
        self.Y.append(Variable("Y-09", "Y-09", 0))
        self.Y.append(Variable("Y-10", "Y-10", 0))
        self.Y.append(Variable("Y-11", "Y-11", 0))
        self.Y.append(Variable("Y-12", "Y-12", 0))
        self.Y.append(Variable("Y-13", "Y-13", 0))
        self.Y.append(Variable("Y-14", "Y-14", 0))
        self.Y.append(Variable("Y-15", "Y-15", 0))

        self.Z.append(Variable("Z-00", "Error en la lectura de entradas y salidas", 0))
        self.Z.append(Variable("Z-01", "Z-01", 0))
        self.Z.append(Variable("Z-02", "Z-02", 0))
        self.Z.append(Variable("Z-03", "Z-03", 0))
        self.Z.append(Variable("Z-04", "Z-04", 0))
        self.Z.append(Variable("Z-05", "Z-05", 0))
        self.Z.append(Variable("Z-06", "Z-06", 0))
        self.Z.append(Variable("Z-07", "Z-07", 0))




class ActualizarVariables (threading.Thread):
    def __init__(self, args = (), objeto = None):
        threading.Thread.__init__ (self, name = None)
        self.contador = 0
        self.objeto = objeto
        print("Actualizar Variables El tipo de objeto ", type(objeto))


        self.TON_00 = Temporizador("TON_00",0.5)
        self.TON_01 = Temporizador("TON_01",10)
        #self.TON_01.iniciar(self)


    def run (self):
        self.funcionando = True
        while (self.funcionando):
            self.TON_00.entrada = not self.TON_00.salida
            self.TON_00.actualizar()
            if self.TON_00.salida:
                self.contador += 1
                print ("%d" %self.contador)
                self.TON_01.entrada = True
                self.TON_01.actualizar()




                if isinstance (self.objeto, list):

                    for i, elemento in enumerate(self.objeto):

                        elemento.establecerValor("%d" %self.contador)
                        elemento.actualizarInterfaz()


                if isinstance (self.objeto, Variable):
                    print ("Dentro de objeto")

                
                    self.objeto.establecerValor("%d" %self.contador)
                    self.objeto.actualizar()

        print ("Hilo terminado")




    def detener (self):
        self.funcionando = False
        print ("Deteniendo variables")



class InterfazDeVariables():

    def __init__(self, listaDeVariables):

        #variable = Variable("TAG", "Nombre", "Descripcion")
        """
        listaDeVariables = []

        listaDeVariables.append(Variable("X-00", "X-00", 0))
        listaDeVariables.append(Variable("X-01", "X-01", 0))
        listaDeVariables.append(Variable("X-02", "X-02", 0))
        listaDeVariables.append(Variable("X-04", "X-04", 0))
        listaDeVariables.append(Variable("X-05", "X-05", 0))
        listaDeVariables.append(Variable("X-06", "X-06", 0))
        listaDeVariables.append(Variable("X-03", "X-03", 0))
        listaDeVariables.append(Variable("X-03", "X-03", 0))
        listaDeVariables.append(Variable("X-07", "X-07", 0))
        listaDeVariables.append(Variable("X-08", "X-08", 0))
        listaDeVariables.append(Variable("X-09", "X-09", 0))
        listaDeVariables.append(Variable("X-10", "X-10", 0))
        listaDeVariables.append(Variable("X-11", "X-11", 0))
        listaDeVariables.append(Variable("X-12", "X-12", 0))
        listaDeVariables.append(Variable("X-13", "X-13", 0))
        listaDeVariables.append(Variable("X-14", "X-14", 0))
        listaDeVariables.append(Variable("X-15", "X-15", 0))
        """

        for i in range(len(listaDeVariables)):
            interfaz = InterfazGrafica(listaDeVariables[i], tipoDeInterfaz = InterfazGrafica.INTERFAZ_TK)
            interfaz = InterfazGrafica(listaDeVariables[i], tipoDeInterfaz = InterfazGrafica.INTERFAZ_QT)


        #interfaz = InterfazGrafica(variable, tipoDeInterfaz = InterfazGrafica.INTERFAZ_TK)
        #interfaz = InterfazGrafica(variable, tipoDeInterfaz = InterfazGrafica.INTERFAZ_QT)
        
        
        pruebaInterfazTK = PruebaInterfazTK("Hilo para la interfaz con TKinter", objeto = listaDeVariables)
        pruebaInterfazTK.start()
        
        pruebaInterfazQT = PruebaInterfazQT(name = "Hilo para la interfaz con QT", objeto = listaDeVariables)
        pruebaInterfazQT.start()





def main ():

    variable = Variable("TAG", "Nombre", "Descripcion")
    
    listaDeVariables = []
    
    listaDeVariables.append(Variable("X-00", "X-00", "Descripcion"))
    listaDeVariables.append(Variable("X-01", "X-01", "Descripcion"))
    listaDeVariables.append(Variable("X-02", "X-02", "Descripcion"))
    listaDeVariables.append(Variable("X-04", "X-04", "Descripcion"))
    listaDeVariables.append(Variable("X-05", "X-05", "Descripcion"))
    listaDeVariables.append(Variable("X-06", "X-06", "Descripcion"))
    listaDeVariables.append(Variable("X-03", "X-03", "Descripcion"))
    listaDeVariables.append(Variable("X-03", "X-03", "Descripcion"))
    listaDeVariables.append(Variable("X-07", "X-07", "Descripcion"))
    listaDeVariables.append(Variable("X-08", "X-08", "Descripcion"))
    listaDeVariables.append(Variable("X-09", "X-09", "Descripcion"))
    listaDeVariables.append(Variable("X-10", "X-10", "Descripcion"))
    listaDeVariables.append(Variable("X-11", "X-11", "Descripcion"))
    listaDeVariables.append(Variable("X-12", "X-12", "Descripcion"))
    listaDeVariables.append(Variable("X-13", "X-13", "Descripcion"))
    listaDeVariables.append(Variable("X-14", "X-14", "Descripcion"))
    listaDeVariables.append(Variable("X-15", "X-15", "Descripcion"))


    for i in range(len(listaDeVariables)):
        interfaz = InterfazGrafica(listaDeVariables[i], tipoDeInterfaz = InterfazGrafica.INTERFAZ_TK)
        interfaz = InterfazGrafica(listaDeVariables[i], tipoDeInterfaz = InterfazGrafica.INTERFAZ_QT)

    

    
    
    
    interfaz = InterfazGrafica(variable, tipoDeInterfaz = InterfazGrafica.INTERFAZ_TK)
    interfaz = InterfazGrafica(variable, tipoDeInterfaz = InterfazGrafica.INTERFAZ_QT)

    actualizarVariables = ActualizarVariables (objeto = listaDeVariables)
    actualizarVariables.start()    
    
    pruebaInterfazTK = PruebaInterfazTK("Hilo para la interfaz con TKinter", objeto = listaDeVariables)
    pruebaInterfazTK.start()
    
    pruebaInterfazQT = PruebaInterfazQT(name = "Hilo para la interfaz con QT", objeto = listaDeVariables)
    pruebaInterfazQT.start()
    

if __name__ == "__main__":
    main ()
