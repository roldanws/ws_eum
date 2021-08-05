# coding=utf-8

__author__ = "SIGFRIDO"
__date__ = "$02-jul-2019 17:07:46$"

from struct import *


INDICE_DATOS = 15
TAMANIO_MINIMO_TRAMA = 17

class Comunicacion ():
    
    caracterDeInicio = '-'
    caracterDeFin = '*'
    
    numeroConsecutivoDeInstruccion = 7920
    

    # Tipo de instrucci�n 
    ADMINISTRACION = 1
    PROCESO = 2

    # Instrucciones para ADMINISTRACION
    VERSION = 180
    
    PROGRAMA_0 = 167
    PROGRAMA_1 = 168
    SELECCION_DE_PROGRAMA = PROGRAMA_1
    
    MODIFICAR_VD = 78
    GUARDAR_VD = 79

    # Instrucciones para PROCESO
    MDB_DATOS = 11
    MDB_DATOS_INCLUIR_CHECKSUM = 12

    CCTALK_DATOS = 123
    
    BOTON_CANCELAR = 24
    LED = 25
    BANDERAS = 26
    
    RESET = 222
    
    TEMPERATURA = 56
    
    
    IPRO = 80
    
    def __init__ (self):
        
        self.arregloByte = 1
        self.tamanioInstruccion = 0
        
        
        
        self.modoDeControlDeParidad = False
        
        self.bufferIndiceMaximo = 100
        self.bufferLectura = bytearray (self.bufferIndiceMaximo)
        self.bufferIndice = 0
        
        for i in range (0,100,1):
            self.bufferLectura.append(0)
        

    def intercalarLista(self, datos, intercalar=1):
        lista = []
        for i, dato in enumerate (datos):
            if (i%intercalar) == 0:
                lista.append(dato)
        return lista


        
    def checkSum(self, datos):
        #print (datos)
        suma = 0
        for dato in datos:
            suma += dato
        return suma & 255
    
    def checkSum_2 (self, datos):
        return (256-self.checkSum(datos)%256)
    
    def checkSum_3 (self, datos):
        numeroInicial = 0
        for dato in datos:
            for i in range (8):
                bit =  (dato>>i)&1^numeroInicial&1
                #print (bit, end=" ")
                numeroInicial = (numeroInicial>>1)^bit<<15^bit<<10^bit<<3
                
        #print ("{0:b}".format(numeroInicial).rjust( 16 ), hex(numeroInicial) )
        return (numeroInicial)
                
    
    def establecerModoDeControlDeParidad (self, opcion = False):
        self.modoDeControlDeParidad = opcion
            

  
    def crearInstruccion (self, tipo = 0, instruccion = 1, *args, **kargs):
        self.tamanioInstruccion = 0


        #print ("----------------------------------------Imprimiendo tipo, instruccion", tipo, instruccion, args)
        

        if self.modoDeControlDeParidad == True:
            cadena = []


            for item in args:
                #print (item)
                for i, it in enumerate(item):
                    cadena.append(it)

                if instruccion == self.MDB_DATOS_INCLUIR_CHECKSUM:
                    cadena.append(self.checkSum(self.intercalarLista(item,2)))
                    cadena.append(0)

            return cadena




        cadena = bytearray(100) #tamanio propuesto
        #indice = 0
        
        if instruccion == self.IPRO:
  
            for item in args:
                #print (item)
                for i, it in enumerate(item):

                    a = pack ('>B', it)
                    #print (i, a)
                    self.anexarBytes(cadena, 0 + i, a)
                    #print (cadena)

                #if instruccion == self.CCTALK_DATOS:
                #    # print ("El checksum es", self.checkSum_2(item))
                #    self.anexarBytes(cadena, self.tamanioInstruccion, pack ('>B', self.checkSum_2(item)) )

                self.anexarBytes(cadena, self.tamanioInstruccion, pack('H', self.checkSum_3(item)))
        else: 
            
            self.anexarBytes(cadena, 0, pack('c', self.caracterDeInicio.encode('ascii')))
            self.anexarBytes(cadena, 1, pack('H', 258))
            self.anexarBytes(cadena, 3, pack('H', 1001))
            self.anexarBytes(cadena, 5, pack('<L', self.numeroConsecutivoDeInstruccion))
            self.numeroConsecutivoDeInstruccion +=1
            #print (self.numeroConsecutivoDeInstruccion)
            self.anexarBytes(cadena, 9, pack('H', tipo))

            if instruccion == self.MDB_DATOS_INCLUIR_CHECKSUM:
                self.anexarBytes(cadena, 11, pack('H', self.MDB_DATOS))
            else:
                self.anexarBytes(cadena, 11, pack('H', instruccion))


            self.anexarBytes(cadena, 13, pack('H', 0))    # Solo de relleno


            if args:
                item = args[0]

                for i, it in enumerate(item):
                    a = pack ('>B', it)
                    #print (i, a)
                    self.anexarBytes(cadena, 15 + i, a)

                if instruccion == self.CCTALK_DATOS:
                    self.anexarBytes(cadena, self.tamanioInstruccion, pack ('>B', self.checkSum_2(item)) )

                if instruccion == self.MDB_DATOS_INCLUIR_CHECKSUM:
                    self.anexarBytes(cadena, self.tamanioInstruccion, pack ('>B', self.checkSum(self.intercalarLista(item,2))) )
                    self.anexarBytes(cadena, self.tamanioInstruccion, pack('B', 0))  # Necesario para operar el control de paridad

            
            a = pack('B', 0)
            #print ("Antes de anexar", len(cadena), self.tamanioInstruccion, a,len(a))
            self.anexarBytes(cadena, self.tamanioInstruccion, a) # Solo de relleno
            #print ("Depués de anexar", len(cadena), self.tamanioInstruccion, a,len(a))

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
        
        
        #print ("Imprimiendo la cadena ", len(cadena[0:self.tamanioInstruccion]), cadena[0:self.tamanioInstruccion])
        return (cadena[0:self.tamanioInstruccion])
        
    
    def anexarBytes(self, arreglo, indice, a):
        #print ("AnexarBytes", arreglo, a)


        if (indice + len(a) + 1) > len(arreglo):
            print ( "ERORR_Dentro de anexarBytes ", len(arreglo), indice, a,len(a))
        else:
            try:
                for i in range (len(a)):
                    arreglo[indice + i] = a[i]
                    self.tamanioInstruccion += 1
            except IndexError:
                print ("TamanioInstruccion >>", self.tamanioInstruccion, indice, a, "<<")
                
        
        #print ("           ", arreglo, "\n")
        

    def imprimirBuffer (self,instruccion ):
        print ("Imprimendo instruccion", instruccion)
        
        
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
                
            if numeroDeInstruccion == self.IPRO:
                self.checkSum_3(trama)
                

                
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
