__author__ = "SIGFRIDO"
__date__ = "$20-may-2019 10:33:36$"


class Variable():
    
    ESTADO_DESHABILITADO = 0   
    ESTADO_APAGADO = 1
    ESTADO_ENCENDIDO = 2

    
    def __init__ (self, tag, nombre, descripcion, tipo = 0, indice = 0, valor = 0, unidades = 0):
        self.__tag = tag
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__tipo = tipo
        self.__valor = valor
        self.__valor_2 = None
        self.__unidades = unidades
        self.__indice = indice
        self.__timeStamp = ""
        
        
        self.__estado = 0
        #self.__interfaz = self.funcion
        
        self.listaDeInterfaces = []
        self.__funcion = None
        self.__funcion_2 = None
        
    def actualizar(self):
        for i, elemento in enumerate (self.listaDeInterfaces):
            if elemento:
                self.listaDeInterfaces[i].establecerTag(self.__tag)
                self.listaDeInterfaces[i].establecerNombre(self.__nombre)
                self.listaDeInterfaces[i].establecerDescripcion(self.__descripcion)
                self.listaDeInterfaces[i].establecerValor(self.__valor)



            
            
    def establecerTag (self, tag):
        self.__tag = tag
        #print ("Dentro de Variable -> establecer Tag", tag)
        
        for i, elemento in enumerate (self.listaDeInterfaces):
            if elemento:
                self.listaDeInterfaces[i].establecerTag(self.__tag)
        
    def obtenerTag (self):
        return self.__tag  

    
    def establecerNombre (self, nombre):
        self.__nombre = nombre
        #print ("Dentro de Variable -> establecer Nombre", nombre)
        
        for i, elemento in enumerate (self.listaDeInterfaces):
            if elemento:
                self.listaDeInterfaces[i].establecerNombre(self.__nombre)
        
    def obtenerNombre (self):
        return self.__nombre
    

    def establecerDescripcion (self, descripcion):
        self.__descripcion = descripcion
    
        for i, elemento in enumerate (self.listaDeInterfaces):
            self.listaDeInterfaces[i].establecerDescripcion(self.__descripcion)

        
    def obtenerDescripcion (self):
        return self.__descripcion

    
    def establecerTipo (self, tipo):
        self.__tipo = tipo
    
        for i, elemento in enumerate (self.listaDeInterfaces):
            self.listaDeInterfaces[i].establecerTipo(self.__tipo)
        
    def obtenerTipo (self):
        return self.__tipo
        
    """
    def establecerValor2 (self, valor):
        self.__valor = valor;
            
        for i, elemento in enumerate (self.listaDeInterfaces):
            self.listaDeInterfaces[i].establecerValor(self.__valor)
                
    def obtenerValor2 (self):
        return self.__valor         
    """
    
    def establecerUnidades (self, unidades):
        self.__unidades = unidades
        
        for i, elemento in enumerate (self.listaDeInterfaces):
            self.listaDeInterfaces[i].establecerUnidades(self.__unidades)
        
    def obtenerUnidades (self):
        return self.__unidades
    
    def establecerIndice (self, indice):
        self.__indice = indice
        
        for i, elemento in enumerate (self.listaDeInterfaces):
            self.listaDeInterfaces[i].establecerIndice(self.__indice)
        
    def obtenerIndice (self):
        return self.__indice
    
    
    def establecerTimeStamp (self, timeStamp):
        self.__timeStamp = timeStamp
        #print ("Dentro de Variable -> establecer TimeStamp", timeStamp)
        
        for i, elemento in enumerate (self.listaDeInterfaces):
            self.listaDeInterfaces[i].establecerTimeStamp(self.__timeStamp)
        
    def obtenerTimeStamp (self):
        return self.__timeStamp
    
    
    def establecerEstado (self, estado):
        self.__estado = estado
        
        for i, elemento in enumerate (self.listaDeInterfaces):
            self.listaDeInterfaces[i].establecerEstado(self.__estado)
        
    def obtenerEstado (self):
        return self.__estado
    
    
    #---------------------Para el funcionamiento de la clase Botones
    #TODO implementar los cambios para que funcionen ambas clases
    
    def establecerValor (self, valor, **kwargs):
        if self.__valor != valor:

            self.__valor = valor
            
            aux = True # utilizada para modificar el valor sin ejecutar la funcion que tenga asignada
            for i, elemento in enumerate (self.listaDeInterfaces):
                if elemento:
                    self.listaDeInterfaces[i].establecerValor(self.__valor)

            for key, value in kwargs.items():
                if key == "MODO":
                    if value == "SOLO VARIABLE":
                        aux = False


            if self.__funcion is not None :
                try:
                    if aux:
                        self.__funcion(self.__indice, self.__valor)
                except:
                    print ("Dentro de variable, no se ha establecido la funcion")

    def obtenerValor (self):
        return self.__valor

    
    def establecerFuncion (self, interfaz):
        self.__funcion = interfaz

    def obtenerFuncion (self):
        return self.__funcion
    
    #-----------------------------------------------------
    
    def establecerValor_2 (self, valor, **kwargs):
        if self.__valor != valor:
            self.__valor_2 = valor
        
            aux = True # utilizada para modificar el valor sin ejecutar la funcion que tenga asignada
            for i, elemento in enumerate (self.listaDeInterfaces):
                if elemento:
                    self.listaDeInterfaces[i].establecerValor_2(self.__valor)

            for key, value in kwargs.items():
                if key == "MODO":
                    if value == "SOLO VARIABLE":
                        aux = False

            
            for i, elemento in enumerate (self.listaDeInterfaces):
                self.listaDeInterfaces[i].establecerValor_2(self.__valor_2)


            if self.__funcion_2 is not None :
                try:
                    self.__funcion_2(self.__indice, self.__valor_2)
                except:
                    print ("Dentro de variable, no se ha establecido la funcion")

    def obtenerValor_2 (self):
        return self.__valor_2

    
    def establecerFuncion_2 (self, interfaz):
        self.__funcion_2 = interfaz

    def obtenerFuncion_2 (self):
        return self.__funcion_2   
    
    
    
    #-----------------------------------------------------
    
    
    def establecerInterfazGrafica (self, interfaz):
        """Agrega un interfaz grafica a a la lista"""
        self.listaDeInterfaces.append(interfaz)

    def borrarInterfazGrafica(self, indice):
        if self.listaDeInterfaces[indice] is not None:
            self.listaDeInterfaces[indice] = None

        
    def obtenerInterfazGrafica (self, indice):
        if indice < len(self.listaDeInterfaces):
            return self.listaDeInterfaces[indice]
        else:
            return None
            
    def actualizarInterfaz (self):
        for i, elemento in enumerate (self.listaDeInterfaces):
            self.listaDeInterfaces[i].establecerTag(self.__tag)
            self.listaDeInterfaces[i].establecerNombre(self.__nombre)
            self.listaDeInterfaces[i].establecerDescripcion(self.__descripcion)
            #self.listaDeInterfaces[i].establecerTipo(self.__tipo)
            self.listaDeInterfaces[i].establecerValor(self.__valor)
            self.listaDeInterfaces[i].establecerValor_2(self.__valor_2)
            #self.listaDeInterfaces[i].establecerUnidades(self.__unidades)
		
    

    
    def __str__ (self):
        return ("%s %s" % (self.__tag.ljust( 8 ), str(self.__descripcion).rjust( 10 )))
