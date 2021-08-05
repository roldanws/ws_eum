

__author__ = "SIGFRIDO"
__date__ = "$02-sep-2019 17:42:52$"


from Variable import Variable


class VariableAlarma(Variable):
    def __init__(self, tag, nombre, descripcion, valorMuyBajo, valorBajo,valorAlto, valorMuyAlto):
        Variable.__init__(self, tag = tag, nombre = nombre, descripcion = descripcion)
        self.__valorMuyAlto = valorMuyAlto
        self.__valorAlto = valorAlto
        self.__valorBajo = valorBajo
        self.__valorMuyBajo = valorMuyBajo
        
    
    def establecerValorMuyAlto (self, valor):
        self.__valorMuyAlto = valor
        
    def obtenerValorMuyAlto (self):
        return self.__valorMuyAlto
    
    def establecerValorAlto (self, valor):
        self.__valorAlto = valor
        
    def obtenerValorAlto (self):
        return self.__valorAlto
    
    def establecerValorBajo (self, valor):
        self.__valorBajo = valor
        
    def obtenerValorBajo (self):
        return self.__valorBajo
    
    def establecerValorMuyBajo (self, valor):
        self.__valorMuyBajo = valor
        
    def obtenerValorMuyBajo (self):
        return self.__valorMuyBajo
        
        
        
    def __str__(self):
        return ("%s %s >>%s<<  %s, %s, %s, %s" %  (self.obtenerTag(), self.obtenerDescripcion(), self.obtenerValor(), 
    self.obtenerValorMuyBajo(), self.obtenerValorBajo(), self.obtenerValorAlto(), self.obtenerValorMuyAlto()))    
    

def main ():
    alarma = VariableAlarma("Al-01","Billetero", "Falla en conexion con equipo ", 1, 2, 6, 7)
    
    print ("Imprimiendo la alarma:", alarma)
    

if __name__ == "__main__":
    main()
