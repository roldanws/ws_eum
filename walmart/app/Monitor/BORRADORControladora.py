"""

Esta clase es utilizada para obtener las señales de entradas y salidas en las diferentes tarjetas

Caso 1: Expedidora con tarjeta de pulso, implementada en tarjeta madre
    Creará un puerto seriales RS-232, el primero para la conexión de la tarjeta controladora, ademas de utilizar un puerto USB para la lectura del boton de expedidora


Caso 2: Expedidora, Validadora, con tarjeta de interfaz blanca implemetada en Raspberry
    Utiliza los pines gpio del raspberry para obtener las señales de entrada y salida

Caso 3: Expedidora, Validadora con tarjeta de interfaz con arduino versión 1.3, implementada en tarjeta madre o raspberry


"""


__author__ = "SIGFRIDO"
__date__ = "$25-ene-2020 12:43:00$"

import threading
import time

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
        import RPi.GPIO as GPIO

	#print (platform.system(), platform.release(),platform.version())
ruta =  os.path.dirname(os.path.abspath(__file__)) + caracterDirectorio

def obtenerUsuario(ruta):
	lista = ruta.split(caracterDirectorio)
	return caracterDirectorio+lista[1]+caracterDirectorio+lista[2]+caracterDirectorio

rutaUsuario = os.path.expanduser('~') + caracterDirectorio

# Detectar si tiene instalada la tarjeta de arduino por el puerto serie

sys.path.append(os.path.join(ruta, ".."))
sys.path.append(os.path.join(ruta, ".." + caracterDirectorio + ".."))

print("\nEstamos en {} {}".format(sistema, version))
print("La ruta actual es {}".format(ruta))
print("La ruta de usuario es {}".format(rutaUsuario))

from PuertoSerie import PuertoSerie
from Variables.Variable import Variable
from Variables.Temporizador import Temporizador
from Comunicacion import Comunicacion


# Keylogger


keylogger_ARCHIVO = ruta + caracterDirectorio + 'teclas.txt'
keylogger_commandoLinux = 'keylogger --clean-file --cancel-key w --log-file ' +  keylogger_ARCHIVO


class Controladora ():


    TARJETA_DE_PULSO = "tarjeta de pulso"
    TARJETA_DE_INTERFAZ_BLANCA = "tarjeta de interfaz blanca"
    TARJETA_DE_INTERFAZ_NEGRA = "tarjeta de interfaz negra"
    TARJETA_DE_INTERFAZ_ARDUINO = "tarjeta de interfaz con arduino"

    listaDeTarjetas = (TARJETA_DE_PULSO, TARJETA_DE_INTERFAZ_BLANCA, TARJETA_DE_INTERFAZ_NEGRA, TARJETA_DE_INTERFAZ_ARDUINO,)
    listaDePuertos = []


    CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA = "Expedidora y validadora"
    CONTROLADORA_PARA_CAJERO = "Cajero"


    def __init__(self, listaDeVariables, **kwargs):
        self.listaDevariables = listaDeVariables

        self.tarjetaSeleccionada = 0
        self.TipoDeControladora = 0
        


        self.valoresPorDefecto()
        self.configurar(**kwargs)

        self.actualizarVariables = ActualizarVariables(self.listaDevariables, self.listaDePuertos, self.tarjetaSeleccionada, self.TipoDeControladora)
        self.actualizarVariables.start()  # Se inicia el hilo principal

        

        print (self)


    def __str__(self):
        return "\nParemetros configurados: \n\tSeleccionada la {} \
                            ".format(self.tarjetaSeleccionada)

    def valoresPorDefecto(self):
        self.tarjetaSeleccionada = self.TARJETA_DE_INTERFAZ_ARDUINO
        self.TipoDeControladora = self.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA


    def configurar(self, **kwargs):
        for key, value in kwargs.items():
            
            #print ("Imprimiendo el valor en configurar", key, value)
            
            if key == "tarjeta":
                for i in self.listaDeTarjetas:
                    if value == i:
                        self.tarjetaSeleccionada = i
                        print ("Se ha seleccionado la {}".format(value))

                      


                
class ActualizarVariables (threading.Thread): #arduino

    def __init__(self, listaDeVariables = None, listaDePuertos = None, dispositivos = None, controladora = None ):
        threading.Thread.__init__ (self, name = None)
        self.contador = 0
        

        self.listaDeVariables = listaDeVariables
        self.listaDePuertos = listaDePuertos
        self.dispositivos = dispositivos
        self.TipoDeControladora = controladora

        self.comunicacion = Comunicacion ()

        self.TON_00 = Temporizador("TON_00",1)
        self.TON_01 = Temporizador("TON_01",10)
        self.TON_02 = Temporizador("TON_01",0.04)
        
        self.sistemaFuncionandoCorrectamente = True

        # unicamente para la tarjeta de pulso
        self.TON_10 = Temporizador("TON_10",1.5)
        self.banderaF3Detectada = False


        # unicamente para la tarjeta de interfaz-blanca
        self.raspberry_X = []
        self.raspberry_Y = []


        self.levantarPuertos()


    def levantarPuertos(self):
        # Se cierran las conexiones anteriores

        # Se abren nuevas conexiones
        
        if self.TipoDeControladora == Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA:


            if self.dispositivos == Controladora.TARJETA_DE_PULSO:
                # puede funcionar con tarjeta madre y raspberry
                # se abre un puerto de comunicación para manejar la comunicación RS-232
                # se utiliza la otra entrada por medio del teclado modificado

                self.listaDePuertos.append (PuertoSerie("Puerto Serie"))
                self.listaDePuertos[0].modificarConfiguracion(dispositivo = PuertoSerie.CABLE_USB)
                self.listaDePuertos[0].abrirPuerto()

                tarea1 = threading.Thread(target=self.keyloggerIniciar)
                tarea1.start()

                self.aux = 0
                tarea2 = threading.Thread(target=self.keyloggerleerArchivo)
                tarea2.start()


                #TODO:Agregar funcion para modificar la salida de la tarjeta de pulso, admite una sola salida

                self.listaDeVariables.Y[3].establecerFuncion(self.funcion_1)


            if self.dispositivos == Controladora.TARJETA_DE_INTERFAZ_BLANCA:
                # unicamente para raspberry
                # se establecen los pines de comunicación GPIO

                # de forma aficional se utilizan los pines de comunicacion RX, TX

                if version != "raspberrypi":
                    self.sistemaFuncionandoCorrectamente = False
                    raise Exception('Solamente puede funcionar la tarjeta de interfaz blanca en Raspberry')

                    

                if self.sistemaFuncionandoCorrectamente:

                    GPIO.setmode (GPIO.BCM)
                    GPIO.setwarnings (False)

                    self.DI_00 = 27
                    self.DI_01 = 22
                    self.DI_02 = 10
                    
                    self.DO_03 = 9

                    GPIO.setup(self.DI_00, GPIO.IN)
                    GPIO.setup(self.DI_01, GPIO.IN)
                    GPIO.setup(self.DI_02, GPIO.IN)

                    GPIO.setup(self.DO_03, GPIO.OUT)

                    for i in range (4):
                        self.raspberry_X.append(0)
                        self.raspberry_Y.append(0)

                    self.listaDeVariables.Y[3].establecerFuncion(self.funcion_2)


            if self.dispositivos == Controladora.TARJETA_DE_INTERFAZ_NEGRA:
                # unicamente para raspberry
                # se establecen los pines de comunicación GPIO

                # de forma aficional se utilizan los pines de comunicacion RX, TX

                if version != "raspberrypi":
                    self.sistemaFuncionandoCorrectamente = False
                    raise Exception('Solamente puede funcionar la tarjeta de interfaz blanca en Raspberry')

                    

                if self.sistemaFuncionandoCorrectamente:

                    GPIO.setmode (GPIO.BCM)
                    GPIO.setwarnings (False)

                    self.DI_03 = 27
                    self.DI_01 = 22
                    self.DI_02 = 10
                    
                    self.DO_03 = 9

                    GPIO.setup(self.DI_03, GPIO.IN)
                    GPIO.setup(self.DI_01, GPIO.IN)
                    GPIO.setup(self.DI_02, GPIO.IN)

                    GPIO.setup(self.DO_03, GPIO.OUT)

                    for i in range (4):
                        self.raspberry_X.append(0)
                        self.raspberry_Y.append(0)

                    self.listaDeVariables.Y[3].establecerFuncion(self.funcion_4)

            if self.dispositivos == Controladora.TARJETA_DE_INTERFAZ_ARDUINO:
                # Se abre un solo puerto de comunicación

                self.listaDePuertos.append (PuertoSerie("Puerto Serie"))

                self.listaDePuertos[0].modificarConfiguracion(dispositivo = PuertoSerie.ARDUINO_MICRO)

                self.contadorDeInstruccion_Arduino = 0
                self.lock = threading.Lock()
                #puerto.start()
                #print("", end="\t")
                self.listaDePuertos[0].abrirPuerto()

                self.listaDeVariables.Y[3].establecerFuncion(self.funcion_3)


    def run (self):
        print ("Actualizando las variables")

        if self.sistemaFuncionandoCorrectamente:
            self.funcionando = True
            while (self.funcionando):

                #TODO:Verificar si se pudieron levantar los puertos

                self.TON_00.entrada = not self.TON_00.salida
                self.TON_00.actualizar()


                self.TON_02.entrada = not self.TON_02.salida
                self.TON_02.actualizar()

                if self.TON_00.salida:
                    self.contador += 1

                    #print (end= "")
                    print ("%d." %self.contador, flush=True)

                if self.TON_02.salida:

                    if self.contador > 1:

                        if self.TipoDeControladora == Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA:

                            if self.dispositivos == Controladora.TARJETA_DE_PULSO:
                                self.leerEntradas_TarjetaDePulso()

                            if self.dispositivos == Controladora.TARJETA_DE_INTERFAZ_BLANCA:
                                self.leerEntradas_TarjetaInterfazBlanca()


                            if self.dispositivos == Controladora.TARJETA_DE_INTERFAZ_NEGRA:
                                self.leerEntradas_TarjetaInterfazNegra()

                            if self.dispositivos == Controladora.TARJETA_DE_INTERFAZ_ARDUINO:
                                self.leerEntradas_TarjetaArduino()
        print ("Hilo terminado de actualizarVariables")

    def detener (self):
        self.funcionando = False
        print ("Deteniendo actualizarVariables")


    ############################################### Metodos para leer entradas de la tarjeta de pulso ################################

    def leerEntradas_TarjetaDePulso(self):
        #TODO: Verificar si se reunen las condiciones para que funcione la lectura (El puerto esta abierto y se obtiene lecturas y los hilos del keylogger estan vivos)
        
        r = self.listaDePuertos[0].read(10)
        #print (r)

        if r == b'\xFE':
            self.listaDeVariables.establecerX(0, 0)

        if r == b'\xF9':
            self.listaDeVariables.establecerX(0, 1)


    def keyloggerIniciar (self):
        print ("Iniciando keylogger")
        os.system (keylogger_commandoLinux)

    def keyloggerleerArchivo (self):
        self.funcionando = True
        while (self.funcionando):
            """ """
            time.sleep (0.5)
            self.leerArchivo()

            self.TON_10.entrada = self.banderaF3Detectada
            self.TON_10.actualizar()

            if self.banderaF3Detectada:
                self.listaDeVariables.establecerX(1, 1)

            if self.TON_10.salida:
                self.banderaF3Detectada = False
                self.listaDeVariables.establecerX(1, 0)

        print ("Hilo terminado KeyloggerleerArchivo")

        self.cerrarArchivo()


    def abrirArchivo (self):
        try:
            self.archivo =  open (keylogger_ARCHIVO, "r+")
            self.aux =  True

        except IOError:
            pass
            #print ("El archivo no existe", file = sys.stderr)
			
			
    def cerrarArchivo (self):
        if self.aux:
            self.archivo.close()
            self.aux = False
			
    def leerArchivo (self):
		
        if self.aux: #El archivo esta abierto

            lineas = self.archivo.readlines()
            for linea in lineas :
                #print (linea)
                palabras = linea.split('\n')
                #print (palabras)
                if palabras[0] == 'F3':
                    #print ("Se oprimio la tecla F3")
                    self.banderaF3Detectada = True
        else:
            self.abrirArchivo()


    def funcion_1 (self, indice, valor):
        #print ("Recibido {} = {}".format(indice, valor))
        if valor:
            self.listaDePuertos[0].write("0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&".encode())
            self.listaDePuertos[0].write("0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&".encode())
            self.listaDePuertos[0].write("0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&".encode())
            self.listaDePuertos[0].write("0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&".encode())
            self.listaDePuertos[0].write("0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&".encode())
            self.listaDePuertos[0].write("0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&".encode())
            self.listaDePuertos[0].write("0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&0&".encode())

    ############################################### Metodos para leer entradas de la tarjeta con arduino ################################

    def ejecutarInstrucciones_TarjetaArduino(self):
        # Viene de un hilo que lo esta ejecuntado antes por lo tantose asume que hay un bucle atras

        self.contadorDeInstruccion_Arduino += 1

    def leerEntradas_TarjetaArduino(self):
       



        #TODO: Verificar se se reunen las condiciones (el puerto esta abierto)
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
        #print ("Mensaje ", a)

        #print("Funcionando")

        
        self.lock.acquire()

        try:
            self.listaDePuertos[0].write(a)
            time.sleep(.01)	
            r = self.listaDePuertos[0].read(6)

        finally:
            self.lock.release()

        instruccionCorrecta = False


        if (r):
            if len(r) == 6:
                if r[0] == ord(Comunicacion.caracterDeInicio):
                    if r[5] == ord(Comunicacion.caracterDeFin):
                        instruccionCorrecta = True
                        #print ("Botones", r)


        if instruccionCorrecta:
            for j in range (2):
                for i in range (8):
                    self.listaDeVariables.establecerX(i+j*8, (r[1+j] >> i) & 1)


            for j in range (2):
                for i in range (8):
                    self.listaDeVariables.Y[i+j*8].establecerValor((r[3+j] >> i) & 1, MODO="SOLO VARIABLE")
                    #print ("Y[{}]={}".format(i+j*8, (r[3+j] >> i) & 1))

        else:

            print("Instrucion recibida de forma incorrecta")

    def funcion_3 (self, indice, valor):
        #print ("Recibido en 3 {} = {}".format(indice, valor))

        #TODO: Mejorar la implementación de este sistema para cuando se anexan más tareas simultaneas
        self.lock.acquire()
        try:

            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [indice, 1 if valor else 0])


            self.listaDePuertos[0].enviarBytes(a)
            
        except:
            print ("No se pudo enviar la instruccion")
        finally:
            self.lock.release()







    ############################################### Metodos para leer entradas de la tarjeta de interfaz blanca unicamente con raspberry###########


    def leerEntradas_TarjetaInterfazBlanca(self):
        #TODO:Verificar si se reunen las condiciones (solo funciona en rasperry)

        # Se leen los valores de los pines 
        self.raspberry_X[0] = GPIO.input(self.DI_00)
        self.raspberry_X[1] = GPIO.input(self.DI_01)
        self.raspberry_X[2] = GPIO.input(self.DI_02)

        


        # se mapean los valores a la lista de variables
        self.listaDeVariables.establecerX(0, self.raspberry_X[0])
        self.listaDeVariables.establecerX(1, self.raspberry_X[1])
        self.listaDeVariables.establecerX(2, self.raspberry_X[2])



        
        GPIO.output (self.DO_03, self.raspberry_Y[3])            


        self.listaDeVariables.Y[3].establecerValor(self.raspberry_Y[3], MODO="SOLO VARIABLE")


    def funcion_2 (self, indice, valor):
        #print ("Recibido en funcion 2 {} = {}".format(indice, valor))

        self.raspberry_Y[indice] = valor

        



    ############################################### Metodos para leer entradas de la tarjeta de interfaz negra unicamente con raspberry###########


    def leerEntradas_TarjetaInterfazNegra(self):
        #TODO:Verificar si se reunen las condiciones (solo funciona en rasperry)

        # Se leen los valores de los pines 
        self.raspberry_X[3] = GPIO.input(self.DI_03)
        self.raspberry_X[1] = GPIO.input(self.DI_01)
        self.raspberry_X[2] = GPIO.input(self.DI_02)

        


        # se mapean los valores a la lista de variables
        self.listaDeVariables.establecerX(3, self.raspberry_X[3])
        self.listaDeVariables.establecerX(1, self.raspberry_X[1])
        self.listaDeVariables.establecerX(2, self.raspberry_X[2])



        
        GPIO.output (self.DO_03, self.raspberry_Y[3])            


        self.listaDeVariables.Y[3].establecerValor(self.raspberry_Y[3], MODO="SOLO VARIABLE")


    def funcion_4 (self, indice, valor):
        #print ("Recibido en funcion 2 {} = {}".format(indice, valor))

        self.raspberry_Y[indice] = valor




class ListaDeVariables ():
    X = []
    Y = []

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


        for i, elemento in enumerate(self.X):
            self.establecerX(i, 0)

        
        for i, elemento in enumerate(self.Y):
            self.Y[i].establecerIndice(i)
        
        print ("Se han creado las variables")


    def establecerX(self, indice, valor):
        if indice < len(self.X):
            self.X[indice].establecerValor(valor)
        else:
            print ("El indice es mayor ", indice)

    def obtenerX(self, indice):
        if indice < len(self.X):
            return self.X[indice].obtenerValor()
        else:
            print ("El indice es mayor ", indice)
        return false

    def imprimirX(self, valorMaximo = 0):
        if valorMaximo == 0:
            valorMaximo = len(self.X)
        aux="[ "
        for i , elemento in enumerate(self.X):
            if i >= valorMaximo:
                break
            aux += "{}".format(elemento.obtenerValor())
            if i < valorMaximo-1 :
                aux += ", "
        aux += " ]"                
        print (aux, end="")



    def obtenerY(self, indice):
        if indice < len(self.Y):
            return self.Y[indice].obtenerValor()
        else:
            print ("El indice es mayor ", indice)
        return false

    def imprimirY(self, valorMaximo = 0):
        if valorMaximo == 0:
            valorMaximo = len(self.Y)
        aux="[ "
        for i , elemento in enumerate(self.Y):
            if i >= valorMaximo:
                break
            aux += "{}".format(elemento.obtenerValor())
            if i < valorMaximo-1 :
                aux += ", "
        aux += " ]"                
        print (aux, end="")


class EjecutarPrograma():
    def __init__(self, listaDeVariables):

        self.listaDeVariables = listaDeVariables


        self.TON_02 = Temporizador("TON_02",0.05)

        self.TON_03 = Temporizador("TON_03",4)


        tarea1 = threading.Thread(target=self.run)
        tarea1.start()
        
                
    
    def run (self):
        self.funcionando = True

        while (self.funcionando):
            self.TON_02.entrada = not self.TON_02.salida
            self.TON_02.actualizar()

            if self.TON_02.salida:
                
                self.listaDeVariables.imprimirX()
                print ("", end="\t")
                self.listaDeVariables.imprimirY()
                print ("")
                
            self.TON_03.entrada = not self.TON_03.salida
            self.TON_03.actualizar()    

            if self.TON_03.salida:
                print (">>>>>>>>>>>>>>>>>>>>>>>>>Cambiando Estado")
                #print (">>>>>>>>>>>>>>>>>>>>>>>>>Valor actual ", self.listaDeVariables.Y[3].obtenerValor())

                self.listaDeVariables.Y[3].establecerValor(not self.listaDeVariables.Y[3].obtenerValor())



def main ():
    variables = ListaDeVariables()

    #---------------------------------------- Tarjeta de interfaz arduino
    """
    controladora = Controladora(variables, 
        tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO,
        TipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)

    """
    #---------------------------------------- tarjeta de pulso
    #controladora = Controladora(variables, tarjeta = Controladora.TARJETA_DE_PULSO)

    #---------------------------------------- tarjeta de interfaz pines GPIO de la raspberry
    """
    controladora = Controladora(variables, 
        tarjeta = Controladora.TARJETA_DE_INTERFAZ_BLANCA, 
        TipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)
    """

    controladora = Controladora(variables, 
        tarjeta = Controladora.TARJETA_DE_INTERFAZ_NEGRA, 
        TipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)


    #---------------------------------------- Programa a ejecutar
    ejecutarPrograma = EjecutarPrograma(variables)



if __name__ == "__main__":
    main ()
