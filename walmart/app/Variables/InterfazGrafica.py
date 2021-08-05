# coding=utf-8

__author__ = "Sigfrido"
__date__ = "$10-jun-2019 16:46:57$"


from tkinter import *


import os
ruta = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ruta)
ruta = os.path.join(os.path.dirname(__file__))

from Variables.Variable import Variable


from PyQt5 import QtWidgets, QtGui
#import os
#ruta = os.path.join(os.path.dirname(__file__))

class InterfazGrafica ():
    
    INTERFAZ_TK = 10
    INTERFAZ_QT = 20


    def __init__ (self, variable, **kwargs):

        self.variable = variable
        
        self.etiquetaTag = None
        self.etiquetaNombre = None
        self.etiquetaDescripcion = None
        self.etiquetaTipo = None
        self.etiquetaValor = None
        self.etiquetaValor_2 = None
        self.etiquetaImagen = None
        self.imagenDeFondo = None
        self.etiquetaEstado = None
        self.etiquetaTimeStamp = None
        


        self.imagenPrueba = None
        self.parent = None

        self.listaDeImagenes = []
        for i in range (3):
            self.listaDeImagenes.append("")

        variable.establecerInterfazGrafica(self)
        #print ("Creada interfazGrafica")
        
        self.tipoDeInterfaz = self.INTERFAZ_TK
        for key, value in kwargs.items():
            if key == "tipoDeInterfaz":
                #print ("El valor de interfaz es ", value)
                self.tipoDeInterfaz = value
                

    def establecerTag (self, tag):
        if self.etiquetaTag is not None:
            if (self.tipoDeInterfaz == self.INTERFAZ_QT):
                try:
                    self.etiquetaTag.setText(tag)
                    self.etiquetaTag.adjustSize()
                except:
                    pass
            elif(self.tipoDeInterfaz == self.INTERFAZ_TK):
                try:
                    self.etiquetaTag.config(text = tag)
                except:
                    pass
        
    def obtenerEtiquetaTag (self, master):
        if (self.tipoDeInterfaz == self.INTERFAZ_QT):
            self.etiquetaTag = QtWidgets.QLabel(master)
        elif(self.tipoDeInterfaz == self.INTERFAZ_TK):
            self.etiquetaTag = Label (master, text = "", font ="Verdana 12", bg ="#FFFFFF", borderwidth=1, width=6, relief= FLAT)
        return self.etiquetaTag



    def establecerNombre (self, valor):
        if self.etiquetaNombre is not None:
            if (self.tipoDeInterfaz == self.INTERFAZ_QT):
                try:
                    self.etiquetaNombre.setText(valor)
                    self.etiquetaNombre.adjustSize()
                except:
                    pass
            elif(self.tipoDeInterfaz == self.INTERFAZ_TK):
                try:
                    self.etiquetaNombre.config(text = valor)
                except:
                    pass
        
    def obtenerEtiquetaNombre (self, master):
        try:
            if master.inherits is not None:
                """ print ("Existe el metodo") """
                pass
            else:
                """  print ("El metodo no existe")"""
                pass

            if (master.inherits("QObject")):
                #self.etiquetaNombre = QtWidgets.QLabel(master)
                pass
        except (AttributeError):
            self.etiquetaNombre = Label (master, text = "", font ="Verdana 12", bg ="#FFFFFF", borderwidth=1, width=12, relief= FLAT)
        else:
            self.etiquetaNombre = QtWidgets.QLabel(master)
            #print ("Se coloco la etiqueta QT")
        return self.etiquetaNombre
    



    def establecerDescripcion (self, valor):
        if self.etiquetaDescripcion is not None:
            if (self.tipoDeInterfaz == self.INTERFAZ_QT):
                try:
                    self.etiquetaDescripcion.setText(valor)
                    self.etiquetaDescripcion.adjustSize()
                except:
                    pass
            elif(self.tipoDeInterfaz == self.INTERFAZ_TK):
                try:
                    self.etiquetaDescripcion.config(text = valor)
                except:
                    pass

    def obtenerEtiquetaDescripcion (self, master):
        if (self.tipoDeInterfaz == self.INTERFAZ_QT):
            self.etiquetaDescripcion = QtWidgets.QLabel(master)
        elif(self.tipoDeInterfaz == self.INTERFAZ_TK):
            self.etiquetaDescripcion = Label (master, text = "", font ="Verdana 11", bg ="#FFFFFF", borderwidth=1, width=14, relief= FLAT, anchor=SW)
        return self.etiquetaDescripcion



    
    def establecerTipo (self, tipo):
        if self.etiquetaTipo is not None:
            self.etiquetaTipo.config(text = tipo)
        
    def obtenerEtiquetaTipo (self, master):
        self.etiquetaTipo = Label (master, text = "", font ="Verdana 11", bg ="#FFFFFF", borderwidth=1, width=6, relief= FLAT)
        return self.etiquetaTipo

    
    def establecerValor (self, valor):
        if self.etiquetaValor is not None:
            
            if (self.tipoDeInterfaz == self.INTERFAZ_QT):
                try:
                    self.etiquetaValor.setText(str(valor))
                    self.etiquetaValor.adjustSize()
                except:
                    pass
            elif(self.tipoDeInterfaz == self.INTERFAZ_TK):
                try:
                    self.etiquetaValor.config(text = str(valor))
                except:
                    pass
                    print ("******************************************************************************************\nNo se pudo establecer el valor en variable")
   
    def obtenerEtiquetaValor (self, master):
        
        if (self.tipoDeInterfaz == self.INTERFAZ_QT):
            self.etiquetaValor = QtWidgets.QLabel(master)
        elif(self.tipoDeInterfaz == self.INTERFAZ_TK):

            
            self.etiquetaValor = Label (master, text = "", font ="Verdana 11", bg ="#FFFFFF", borderwidth=1, width=6, relief= FLAT, anchor=SW)
        return self.etiquetaValor



    def establecerValor_2 (self, valor):
        if self.etiquetaValor_2 is not None:
            
            if (self.tipoDeInterfaz == self.INTERFAZ_QT):
                try:
                    self.etiquetaValor_2.setText(str(valor))
                    self.etiquetaValor_2.adjustSize()
                except:
                    pass
            elif(self.tipoDeInterfaz == self.INTERFAZ_TK):
                try:
                    self.etiquetaValor_2.config(text = str(valor))

                except:
                    pass
                    #print ("******************************************************************************************\nNo se pudo establecer el valor en variable")
 
    def obtenerEtiquetaValor_2 (self, master):
        if (self.tipoDeInterfaz == self.INTERFAZ_QT):
            self.etiquetaValor_2 = QtWidgets.QLabel(master)
        elif(self.tipoDeInterfaz == self.INTERFAZ_TK):
            self.etiquetaValor_2 = Label (master, text = "", font ="Verdana 11", bg ="#FFFFFF", borderwidth=1, width=6, relief= FLAT, anchor=SW)
        return self.etiquetaValor_2





    
    def establecerTimeStamp (self, timeStamp):
        if self.etiquetaTimeStamp is not None:
            self.etiquetaTimeStamp.config(text = timeStamp)
        
    def obtenerEtiquetaTimeStamp (self, master):
        self.etiquetaTimeStamp = Label (master, text = "", font ="Verdana 11", bg ="#FFFFFF", borderwidth=1, width=20, relief= FLAT, anchor=SW)
        return self.etiquetaTimeStamp

    def establecerEstado (self, estado):
		
        if estado == Variable.ESTADO_DESHABILITADO:
            self.imagenDeFondo = self.listaDeImagenes[0]

        if estado == Variable.ESTADO_APAGADO:
            self.imagenDeFondo = self.listaDeImagenes[1]
            
        if estado == Variable.ESTADO_ENCENDIDO:
            self.imagenDeFondo = self.listaDeImagenes[2]

       
        if self.parent is not None:
            self.parent.itemconfigure(self.variable.obtenerTag(), image=self.imagenDeFondo)
       
        if self.etiquetaEstado is not None:
            self.etiquetaEstado.config(text = estado)
        
        
        #print ("Se cambia el estado de %s a %s" %(self.variable.obtenerTag(), estado))            

    def obtenerEtiquetaEstado (self, master):
        self.etiquetaEstado = Label (master, text = "", font ="Verdana 11", bg ="#FFFFFF", borderwidth=1, width=6, relief= GROOVE)
        return self.etiquetaEstado
    
    
    def crearEtiquetaImagen (self, imagenDeFondo=None, tipo = "binaria", habilitada = True):
        self.imagenDeFondo = imagenDeFondo 
        
    def anexarImagen (self, imagen, indice):
        self.listaDeImagenes[indice] = imagen
    
    def obtenerEtiquetaImagen (self, parent = None):
        self.parent = parent
        return self.imagenDeFondo
        
    def obtenerCuadroDeEtiquetas(self, parent = None, *args):
        """"""
        frame = Frame(parent, borderwidth=1, relief= GROOVE)
        etiquetas = []

        for i, arg in enumerate(args):

            if arg == "Tag":
                etiquetas.append(self.obtenerEtiquetaTag(frame))
                etiquetas[i].grid(row = 0, column = 0, rowspan = 1, columnspan = 1,  padx = 5, pady = 2,sticky = E+W+S+N)

            if arg == "Nombre":
                etiquetas.append(self.obtenerEtiquetaNombre(frame))
                etiquetas[i].grid(row = 1, column = 0, rowspan = 1, columnspan = 1,  padx = 5, pady = 2,sticky = E+W+S+N)

            if arg == "Descripcion":
                etiquetas.append(self.obtenerEtiquetaDescripcion(frame))
                etiquetas[i].grid(row = 2, column = 0, rowspan = 1, columnspan = 1,  padx = 5, pady = 2,sticky = E+W+S+N)

            if arg == "timeStamp":
                etiquetas.append(self.obtenerEtiquetaTimeStamp(frame))
                etiquetas[i].grid(row = 3, column = 0, rowspan = 1, columnspan = 1,  padx = 5, pady = 2,sticky = E+W+S+N)


        return frame

    def __str__ (self):
        return ("variable grafica de %s" %self.variable)
