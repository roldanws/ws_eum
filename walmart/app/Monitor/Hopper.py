import sys
import os
import time


#from PuertoSerie import PuertoSerie
from Comunicacion import Comunicacion


ruta = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ruta)

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador

ruta = os.path.join(os.path.dirname(__file__))

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
    
    

    def __init__(self, tag, nombre, descripcion):
        Variable.__init__ (self, tag = tag, nombre = nombre, descripcion = descripcion)
        self.tipoDeMoneda = 0
        
        self.listaDeVariables = []
        
        print ("Creado el dispositivo")
    
    def establecerPuerto (self, puerto):
        self.puerto = puerto
        
    def establecerComunicacion (self, comunicacion):
        self.comunicacion = comunicacion
        
    def configurarDispositivo (self, *args, **kwargs):
        for key, value in kwargs.items():
            #print ("Imprimiendo el valor en modificar configuracion", key, value)
            
            if key == "tipoDeMoneda":
                self. tipoDeMoneda = value



        
        
    def ejecutarInstruccion (self, instruccion):
        if instruccion == self.SIMPLE_POLL:
            
            print ("Falta implementar esta instruccion")
            
            
    #def leerInstruccionDeTrama (self, trama):
        
        
        
    def __str__ (self):
        return "%s %s" %(self.obtenerTag(), self.obtenerDescripcion())








def main ():
    
    
    puerto = PuertoSerie("Puerto Serie")
    print ("Imprimiendo Arduino", PuertoSerie.ARDUINO_MICRO)
    puerto.modificarConfiguracion(dispositivo = PuertoSerie.ARDUINO_MICRO)
    #puerto.start()
    puerto.abrirPuerto()
    
    
    comunicacion = Comunicacion ()
    
    
    hopper1 = Hopper("Hopper 1", "HOP-100", "para monedas de 5 pesos")
    hopper1.establecerPuerto (puerto)
    
    
    
    
    
    # CONFIGURANDO EL HOPPER
    hopper1.configurarDispositivo (tipoDeMoneda = 5)
    
    
    
    


    #print ("Imprimiendo el dispositivo >>", hopper1)
    
    print ("Tipo de moneda", hopper1.tipoDeMoneda)
    
    time.sleep(4)
    
    hopper1.ejecutarInstruccion(Hopper.SIMPLE_POLL)
    
    
    time.sleep(4)
    
    puerto.cerrarPuerto()
    puerto.detenerHilo()
    

if __name__ == "__main__":
    main()
