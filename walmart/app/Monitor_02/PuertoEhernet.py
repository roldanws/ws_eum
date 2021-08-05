# coding=utf-8

# Parte del Modelo para el programa de comunicación 
# Desarrollado por Sigfrido Oscar Soria Frias
# En Estacionamientos Únicos de México

__author__ = "Sigfrido Oscar Soria Frias"
__date__ = "$22-abr-2019 9:40:00$"


class PuertoEthernet (threading.Thread):
    """Clase utilizada para manejar las operaciones de lectura y escritura en distintos protocolos a través del puerto Ehernet"""
    
    def __init__ (self, nombre):
        threading.Thread.__init__ (self, name = nombre)
        
        self.estado = False
        self.auxiliar = self.estado
        self.funcionando = False;

    def abrirPuerto (hots, puerto):
        self.__host = host
        self.__puerto = puerto
        
    def cerrarPuerto ():
        """_"""

    def leer (self):
        """  """
                
    def escribir (self, mensaje):
        """ """

    def modificarConfiguracion (self, **kargs):
        """ """


        
    def run (self):
        while self.funcionando:
            if self.estado:
                """_"""
                
        print ("Hilo puertoSerie terminado")
                


def main ():
    Inicio2()

if __name__ == "__main__":
    print "Hello World"
