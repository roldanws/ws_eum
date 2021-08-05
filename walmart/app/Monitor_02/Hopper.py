__author__ = "SIGFRIDO"
__date__ = "$5/12/2019 04:33:30 PM$"


import sys
import os
import time


from PuertoSerie import PuertoSerie
from Comunicacion import Comunicacion


ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(ruta)

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador

ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")

class Hopper (Variable):
    
    # Instrucciones 
    SIMPLE_POLL = '\xFE'
    ADDRESS_POLL = '\xFD'
    ADDRESS_CLASH = '\xFC'
    ADDRESS_CHANGE = '\xFB'
    ADDRESS_RANDOM = '\xFA'
    REQUEST_MANUFACTURER = '\xF6'
    REQUEST_EQUIPMENT_CATEGORY = '\xF5'
    REQUEST_PRODUCT_CODE = '\xF4'
    REQUEST_PRODUCT_SERIAL_NUMBER = '\xDB'
    REQUEST_PRODUCT_SOFTWARE_VERSION = '\xF1'
    ENTER_NEW_PIN_NUMBER = '\xDB'
    REQUEST_BUILD_CODE = '\xC0'
    EMERGENCY_STOP = '\xAC'
    REQUEST_DISPENSE_COUNT = '\xA8'
    DISPENSE_COINS = '\xA7'
    REQUEST_STATUS = '\xA6'
    ENABLE_HOPPER = '\xA4'
    TEST = '\xA3'
    REQUEST_COMM_REVISION = '\x04'
    RESET_DEVICE = '\x01'
    
    
    HOPPER_POLL = b'\xFE'
    HOPPER_ENABLE = b'\xA4'
    HOPPER_SERIE = b'\xDB'
    HOPPER_DISPENSE = b'\xA7'
    HOPPER_RESET = b'\x01'
    HOPPER_STATUS = b'\xA6'
    
    TIEMPO_DE_RETARDO_EN_LECTURA = 0.025
    

    def __init__(self, tag, nombre, descripcion, **kwargs):
        Variable.__init__ (self, tag = tag, nombre = nombre, descripcion = descripcion)
        
        self.variables = []
        
        self.variables.append (Variable("X_00", "Direccion", "Direccion del Hopper"))
        self.variables.append (Variable("X_01", "Numero de Serie", "Numero de serie del Hopper"))
        self.variables.append (Variable("X_02", "Valor Moneda", "Valor de la moneda que contiene"))
        self.variables.append (Variable("X_03", "Equipo Maestro", "Equipo Maestro"))
        self.variables.append (Variable("X_04", "Monedas dispensadas", "Cantidad de Monedas que ha dispensado el hopper"))
        
        # Valores por defecto
        self.variables[3].establecerValor(1)
        



        self.configurarDispositivo (**kwargs)
        
        print ("\n->Se ha configurado el {}".format(self))
    
    def establecerPuerto (self, puerto):
        self.puerto = puerto
        #print ("Puerto establecido en Hopper")
        
        
    def establecerComunicacion (self, comunicacion):
        self.comunicacion = comunicacion
        
    def configurarDispositivo (self, *args, **kwargs):
        #print ("Desde configurarDispositivo", args , kwargs)
        for key, value in kwargs.items():
            #print ("Imprimiendo el valor en modificar configuracion", key, value)
            
            if key == "valorDeMoneda":
                self.variables[2].establecerValor(value)
            if key == "direccion":
                self.variables[0].establecerValor(value)

        
    def status(self):
        self.ejecutarInstruccion (self.HOPPER_POLL)

        
        
    def ejecutarInstruccion (self, instruccion):
        cctalkInstruccion = [self.variables[0].obtenerValor(), len(instruccion) - 1, self.variables[3].obtenerValor(), instruccion[0]]
        #print (cctalkInstruccion, end = " ")
        
        if instruccion == self.HOPPER_POLL:
            #cctalkIntrucccion = [destino, numeroDeBytes, origen, instruccion]
            self.simplePoll(cctalkInstruccion)
            
            
            
            #self.simplePoll ()
        
            
            
    def inicializar (self):
        # Verificar comunicacion
        # Resetear
        # Pedir numero de serie y almacenarlo
        self.ejecutarInstruccion(self.HOPPER_POLL)
        

    def __str__ (self):
        return "%s %s" %(self.obtenerTag(), self.obtenerDescripcion())
    
    #------------------------------------------------------------------------#
    #--------------------Metodos referentes al dispositivo-------------------#
    
    def simplePoll (self, mensaje):
        #print ("Antes")
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, mensaje)

        
        if self.puerto is not None:
            self.puerto.escribir(a)
            
            time.sleep(self.TIEMPO_DE_RETARDO_EN_LECTURA)
            r = self.puerto.leer_2(20)

            if r:
                print ("Hopper ",r[len(mensaje)+1:])
            else:
                print("Hopper: No se recibio respuesta del puerto")
            






class VariablesMicro ():
    def __init__(self):
        pass


def main ():
    
    
    puerto = PuertoSerie("Puerto Serie")
    print ("Imprimiendo Arduino", PuertoSerie.ARDUINO_MICRO)
    puerto.modificarConfiguracion(dispositivo = PuertoSerie.ARDUINO_MICRO)
    #puerto.start()
    puerto.abrirPuerto()
    
    comunicacion = Comunicacion ()
    variablesMicro = VariablesMicro()
    
    
    # Se crea y se configura el dispositivo
    hopper1 = Hopper("Hopper 1", "HOP-003", "para monedas de 5 pesos", direccion = 3, valorDeMoneda = 5)
    hopper1.establecerPuerto (puerto)
    hopper1.establecerComunicacion (comunicacion)
    
    #hopper1.establecerVariablesMicro(variablesMicro)
    
    
    time.sleep(4)
    
    #hopper1.inicializar()
    
    
    
    #print ("Imprimiendo el dispositivo >>", hopper1)
    
    #print (hopper1.variables[2], hopper1.variables[2].obtenerValor())
    
    #time.sleep(4)
    
    hopper1.ejecutarInstruccion (Hopper.HOPPER_POLL)
    
    
    time.sleep(4)
    
    puerto.cerrarPuerto()
    puerto.detenerHilo()
    

if __name__ == "__main__":
    main()
