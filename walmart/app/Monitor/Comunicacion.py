# coding=utf-8

__author__ = "SIGFRIDO"
__date__ = "$02-jul-2019 17:07:46$"

from struct import *


INDICE_DATOS = 15
TAMANIO_MINIMO_TRAMA = 17

class Comunicacion ():
    
    caracterDeInicio = '-';
    caracterDeFin = '*';
    
    
    numeroConsecutivoDeInstruccion = 1000
    

    # Tipo de instrucción 
    ADMINISTRACION = 1
    PROCESO = 2

    # Instrucciones para ADMINISTRACION


    # Instrucciones para PROCESO
    MDB_DATOS = 11
    CCTALK_DATOS = 123
    
    BOTON_CANCELAR = 24
    
    TEMPERATURA = 56;
    
    
    def __init__ (self):
        
        self.arregloByte = 1
        self.tamanioInstruccion = 0
        
        
        
        
        
        self.bufferIndiceMaximo = 100
        self.bufferLectura = bytearray (self.bufferIndiceMaximo)
        self.bufferIndice = 0
        
        for i in range (0,100,1):
            self.bufferLectura.append(0)
        

        
    def checkSum(self, datos):
        suma = 0
        for dato in datos:
            suma += dato
        return suma & 255
    
    def checkSum_2 (self, datos):
        return (256-self.checkSum(datos)%256)
    

  
    def crearInstruccion (self, tipo = 0, instruccion = 1, *args, **kargs):
        self.tamanioInstruccion = 0
        
        #print ("Imprimiendo tipo, instruccion", tipo, instruccion)
        
        cadena = bytearray(30) #tamanio propuesto
        
        indice = 0

        self.anexarBytes(cadena, 0, pack('c', self.caracterDeInicio.encode('ascii')))
        self.anexarBytes(cadena, 1, pack('H', 258))
        self.anexarBytes(cadena, 3, pack('H', 1001))
        self.anexarBytes(cadena, 5, pack('<L', self.numeroConsecutivoDeInstruccion))
        self.numeroConsecutivoDeInstruccion +=1
        #print (self.numeroConsecutivoDeInstruccion)
        self.anexarBytes(cadena, 9, pack('H', tipo))
        self.anexarBytes(cadena, 11, pack('H', instruccion))
        
        self.anexarBytes(cadena, 13, pack('H', 0))    # Solo de relleno

        for item in args:
            #print (item)
            for i, it in enumerate(item):
                a = pack ('>B', it)
                #print (i, a)
                self.anexarBytes(cadena, 15 + i, a)

            if instruccion == self.CCTALK_DATOS:
                # print ("El checksum es", self.checkSum_2(item))
                self.anexarBytes(cadena, self.tamanioInstruccion, pack ('>B', self.checkSum_2(item)) )

        self.anexarBytes(cadena, self.tamanioInstruccion, pack('B', 0)) # Solo de relleno

        self.anexarBytes(cadena, self.tamanioInstruccion, pack('c', self.caracterDeFin.encode('ascii')))
        
        self.anexarBytes(cadena, 13, pack('H', self.tamanioInstruccion))
        self.tamanioInstruccion -=2
        
        verificacion = 0
        for i in range (self.tamanioInstruccion-2):
            verificacion ^= cadena[i]
            #print ( (verificacion).to_bytes(1, byteorder='big').hex())
            
        self.anexarBytes(cadena, self.tamanioInstruccion-2, pack('B', verificacion))
        self.tamanioInstruccion -=1
            
        #print ("           ",cadena, len(cadena), self.tamanioInstruccion)
        #print ("           ",cadena[0:self.tamanioInstruccion], len(cadena), self.tamanioInstruccion)
        
        return (cadena[0:self.tamanioInstruccion])
        
    
    def anexarBytes(self, arreglo, indice, a):
        #print ("AnexarBytes", arreglo, a)
        for i in range (len(a)):
            arreglo[indice + i] = a[i]
            self.tamanioInstruccion += 1
            #print ("TamanioInstruccion >>", self.tamanioInstruccion, "<<")
        
        #print ("           ", arreglo, "\n")
        

    def imprimirBuffer (self,instruccion ):
        print (instruccion)
        
        
    def decodificarInstruccion (self, instruccion):
        print ("La longitud de la instruccion es: ", len(instruccion))
        
    
    
    
    
    def colocarBytesEnBuffer (self, caracter):
        self.bufferLectura[self.bufferIndice] = caracter
        self.bufferIndice += 1
        if (self.bufferIndice > self.bufferIndiceMaximo - 25):
            aux = self.bufferIndiceMaximo >> 1
            for i in range (aux, self.bufferIndiceMaximo, 1):
                self.bufferIndice = i-aux;
                self.bufferLectura[self.bufferIndice] = self.bufferLectura[i];  
                
    def leerInstruccionesDeBufferSerial(self):
        encontrado = -1
        resultado = 0
        if self.bufferLectura[self.bufferIndice -1 ] == ord(self.caracterDeFin):
            encontrado = -1
            for k in range (self.bufferIndice - 1, -1, -1):
                #print ("Dentro de leer Intruccciones 1, ",  k, self.bufferIndice, self.bufferLectura[k:self.bufferIndice])
                if self.bufferLectura[k] == ord(self.caracterDeInicio):
                    encontrado = k
                    if encontrado >= 0:
                        #print ("Encontrado = ", k, self.bufferIndice, self.bufferLectura[k:self.bufferIndice])
                        if self.verificarTrama (self.bufferLectura[k:self.bufferIndice]):
                            self.obtenerInstruccion (self.bufferLectura[k:self.bufferIndice])
                            self.bufferIndice = k
                        
                        
    def verificarTrama (self, trama):
        resultado = False
        
        tamanio = len(trama)
        
        if tamanio >= TAMANIO_MINIMO_TRAMA:

            reservado01  = unpack ('H', trama[1:3])[0]
            reservado02  = unpack ('H', trama[3:5])[0]
            numeroConsecutivo  = unpack ('I', trama[5:9])[0]
            tipoDeInstruccion = unpack ('H', trama[9:11])[0]
            numeroDeInstruccion = unpack ('H', trama[11:13])[0]
            longitudDeLaTrama = unpack ('H', trama[13:15])[0]
            verificacion = trama[tamanio-2]
            """
            print ("Imprimiendo reservado01", reservado01)
            print ("Imprimiendo reservado02", reservado02)
            print ("Imprimiendo numeroConsecutivo", numeroConsecutivo)
            print ("Imprimiendo tipoDeInstruccion", tipoDeInstruccion)
            print ("Imprimiendo numeroDeInstruccion", numeroDeInstruccion)
            print ("Imprimiendo longitudDeLaTrama", longitudDeLaTrama)
            print ("Imprimiendo verificacion", verificacion)
            """
            verif = 0
            for i in range (0, tamanio-2, 1):
                verif ^= trama[i]

            #print (trama[1:-1], unpack ('f', trama[1:5])[0])
            
            if longitudDeLaTrama == tamanio:
                #print ("El tamanio es correcto")
                if verificacion == verif:
                    #print ("Verificacion correcta")
                    resultado = True
        return resultado

    def obtenerInstruccion (self, trama):
        tipoDeInstruccion = unpack ('H', trama[9:11])[0]
        numeroDeInstruccion = unpack ('H', trama[11:13])[0]
        
        if tipoDeInstruccion == self.PROCESO:
            if numeroDeInstruccion == self.TEMPERATURA:
                self.enviarTemperatura(trama)
                
            if numeroDeInstruccion == self.BOTON_CANCELAR:
                self.enviarBoton(trama)
                

                
    def enviarTemperatura(self, trama):
        print ("La temperatura es %.1f" %unpack ('f', trama[INDICE_DATOS:INDICE_DATOS+4])[0])
        #print ("Kalman es %.2f" %unpack ('f', trama[INDICE_DATOS+4:INDICE_DATOS+8])[0])
        #print ("Original es %.2f" %unpack ('f', trama[INDICE_DATOS+8:INDICE_DATOS+12])[0])
        
    def enviarBoton(self, trama):
        print ("El estado del boton es ", trama[INDICE_DATOS])

    
def main ():
    comunicacion = Comunicacion ()

    a = comunicacion.crearInstruccion(ADMINISTRACION, MDB_DATOS, [30, 1, 26, 0])
    print (a)
    a = comunicacion.crearInstruccion(ADMINISTRACION, MDB_DATOS, [30, 1, 26, 0])
    print (a)

    
    #comunicacion.crearInstruccion3 (tipo = 3,instruccon = 5)


if __name__ == "__main__":
    main ()
