"""
Esta clase es utilizada para obtener las señales de entradas y salidas en las diferentes tarjetas

Caso 1: Expedidora con tarjeta de pulso, implementada en tarjeta madre
    Creará un puerto seriales RS-232, el primero para la conexión de la tarjeta controladora, ademas de utilizar un puerto USB para la lectura del boton de expedidora

Caso 2: Expedidora, Validadora, con tarjeta de interfaz blanca implemetada en Raspberry
    Utiliza los pines gpio del raspberry para obtener las señales de entrada y salida

Caso 3: Expedidora, Validadora con tarjeta de interfaz con arduino versión 1.3, implementada en tarjeta madre o raspberry
"""


#import netifaces
#netifaces.interfaces()

__author__ = "Sigfrido"
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
rutaUsuario = os.path.expanduser('~') + caracterDirectorio

# Detectar si tiene instalada la tarjeta de arduino por el puerto serie

sys.path.append(ruta)
sys.path.append(os.path.join(ruta, ".."))
sys.path.append(os.path.join(ruta, ".." + caracterDirectorio + ".."))

print("\nEstamos en {} {}".format(sistema, version))
print("La ruta actual es {}".format(ruta))
print("La ruta de usuario es {}".format(rutaUsuario))

from PuertoSerie import PuertoSerie
from Variables.Variable import Variable
from Variables.Temporizador import Temporizador

from Comunicacion import Comunicacion
from Monedero import Monedero
from Billetero import Billetero
from Hopper import Hopper
from Validador import Validador
from BilleteroJCM import BilleteroJCM


from Variables.InterfazDeVariables import InterfazDeVariables
from GuardarLogs import GuardarLogs

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

        if self.actualizarVariables.sistemaFuncionandoCorrectamente:
            self.actualizarVariables.start()  # Se inicia el hilo principal
        else:
            print ("Se presento un error en la configuración")

        

        #print (self)


    def __str__(self):
        return "\nParemetros configurados: \n\tSeleccionada la {} \
                            \n\tSeleccionada {}\
                            ".format(self.tarjetaSeleccionada, self.TipoDeControladora)

    def valoresPorDefecto(self):
        self.tarjetaSeleccionada = self.TARJETA_DE_INTERFAZ_ARDUINO
        self.TipoDeControladora = self.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA


    def configurar(self, **kwargs):
        for key, value in kwargs.items():
            
            #print ("Imprimiendo el valor en configurar {}, {}".format(key, value))
            
            if key == "tarjeta":
                for i in self.listaDeTarjetas:
                    if value == i:
                        self.tarjetaSeleccionada = i
                        #print ("Se ha seleccionado la {}".format(value))

            if key == "tipoDeControladora":
                self.TipoDeControladora = value
                #print ("Se ha seleccionado la controladora para {}".format(self.TipoDeControladora))

                      


                
class ActualizarVariables (threading.Thread): #arduino




    ESCRIBIR_VARIABLE = b'\xCD'

    def __init__(self, listaDeVariables = None, listaDePuertos = None, dispositivos = None, controladora = None ):
        threading.Thread.__init__ (self, name = None)
        self.contador = 0

        self.listaDeVariables = listaDeVariables
        self.listaDePuertos = listaDePuertos
        self.tarjetaSeleccionada = dispositivos
        self.TipoDeControladora = controladora

        self.listaDeFunciones = []
        guardar = GuardarLogs("Prueba", ruta + "logs" + caracterDirectorio)


        self.TON_00 = Temporizador("TON_00",1)
        self.TON_01 = Temporizador("TON_01",10)
        self.TON_02 = Temporizador("TON_01",0.025)
        
        self.sistemaFuncionandoCorrectamente = True



        # unicamente para tarjeta de interfaz con arduino
        self.numeroDeInstruccion = 0
        self.numeroMaximoDeInstruccion = 1

        self.comunicacion = Comunicacion ()

        # unicamente para la tarjeta de pulso
        self.TON_10 = Temporizador("TON_10",1.5)
        self.banderaF3Detectada = False

        # unicamente para la tarjeta de interfaz-blanca/negra
        self.raspberry_X = []
        self.raspberry_Y = []



        self.levantarPuertos()


    def levantarPuertos(self):
        # Se cierran las conexiones anteriores
        # Se abren nuevas conexiones

        #################################################################################################################################
        if self.tarjetaSeleccionada == Controladora.TARJETA_DE_PULSO:
            # puede funcionar con tarjeta madre y raspberry
            # se abre un puerto de comunicación para manejar la comunicación RS-232
            # se utiliza la otra entrada por medio del teclado modificado

            if self.TipoDeControladora == Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA:
                print("\n################################################",
                    "\nIniciando la configuración de Expedidora/Validadora",
                    "\n################################################\n")     

                self.listaDePuertos.append (PuertoSerie("Puerto Serie"))
                self.listaDePuertos[0].modificarConfiguracion(dispositivo = PuertoSerie.COM_0)
                self.listaDePuertos[0].abrirPuerto()

                tarea1 = threading.Thread(target=self.keyloggerIniciar)
                tarea1.start()

                self.aux = 0
                tarea2 = threading.Thread(target=self.keyloggerleerArchivo)
                tarea2.start()

                #TODO:Agregar funcion para modificar la salida de la tarjeta de pulso, admite una sola salida

                self.listaDeVariables.Y[3].establecerFuncion(self.funcion_1)


            elif self.TipoDeControladora == Controladora.CONTROLADORA_PARA_CAJERO:
                raise Exception('La tarjeta de pulso no opera en Cajero')

                print("\n################################################",
                    "\nIniciando la configuración de Cajero",
                    "\n################################################\n")

        #################################################################################################################################
        if self.tarjetaSeleccionada == Controladora.TARJETA_DE_INTERFAZ_BLANCA:
            # unicamente para raspberry
            # se establecen los pines de comunicación GPIO
            # de forma aficional se utilizan los pines de comunicacion RX, TX




            if version != "raspberrypi":
                self.sistemaFuncionandoCorrectamente = False
                raise Exception('Error: la tarjeta de interfaz blanca solamente puede funcionar en Raspberry')


            if self.TipoDeControladora == Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA:
                print("\n################################################",
                    "\nIniciando la configuración de Expedidora/Validadora",
                    "\n################################################\n")                

                if self.sistemaFuncionandoCorrectamente:

                    GPIO.setmode (GPIO.BCM)
                    GPIO.setwarnings (False)

                    self.DI_00 = 18

                    self.DI_01 = 22
                    self.DI_02 = 10
                    self.DI_03 = 27
                    
                    self.DO_03 = 9

                    GPIO.setup(self.DI_00, GPIO.IN)
                    GPIO.setup(self.DI_01, GPIO.IN)
                    GPIO.setup(self.DI_02, GPIO.IN)
                    GPIO.setup(self.DI_03, GPIO.IN)


                    GPIO.setup(self.DO_03, GPIO.OUT)

                    for i in range (4):
                        self.raspberry_X.append(0)
                        self.raspberry_Y.append(0)

                    self.listaDeVariables.Y[3].establecerFuncion(self.funcion_2)


            elif self.TipoDeControladora == Controladora.CONTROLADORA_PARA_CAJERO:

                print("\n################################################",
                    "\nIniciando la configuración de Cajero",
                    "\n################################################\n")

                if self.sistemaFuncionandoCorrectamente:

                    GPIO.setmode (GPIO.BCM)
                    GPIO.setwarnings (False)

                    self.DI_00 = 18

                    self.DI_01 = 22
                    self.DI_02 = 10
                    self.DI_03 = 23
                    
                    self.DO_03 = 9

                    GPIO.setup(self.DI_00, GPIO.IN)
                    GPIO.setup(self.DI_01, GPIO.IN)
                    GPIO.setup(self.DI_02, GPIO.IN)
                    GPIO.setup(self.DI_03, GPIO.IN)

                    GPIO.setup(self.DO_03, GPIO.OUT)

                    for i in range (4):
                        self.raspberry_X.append(0)
                        self.raspberry_Y.append(0)

                    self.listaDePuertos.append (PuertoSerie("Puerto Serie"))
                    self.listaDePuertos[0].modificarConfiguracion(dispositivo = PuertoSerie.COM_0)
                    self.listaDePuertos[0].abrirPuerto()

                    if self.listaDePuertos[0].puertoAbierto: # Se pudo abrir el puerto

                        print ("Se pudo abrir el puerto de la raspberry")



                        self.listaDeVariables.dispositivos[0].establecerPuerto (self.listaDePuertos[0])

                        self.comunicacion.establecerModoDeControlDeParidad(True)

                        self.listaDeVariables.dispositivos[0].establecerComunicacion (self.comunicacion)





                        self.listaDeVariables.dispositivos[1].establecerPuerto (self.listaDePuertos[0])



                        self.listaDeVariables.dispositivos[1].establecerComunicacion (self.comunicacion)

                        print ("******************************Se ha establecido el Monedero")

        #################################################################################################################################
        if self.tarjetaSeleccionada == Controladora.TARJETA_DE_INTERFAZ_NEGRA:
            # unicamente para raspberry
            # se establecen los pines de comunicación GPIO
            # de forma aficional se utilizan los pines de comunicacion RX, TX

            if version != "raspberrypi":
                self.sistemaFuncionandoCorrectamente = False
                raise Exception('Solamente puede funcionar la tarjeta de interfaz negra en Raspberry')



            if self.TipoDeControladora == Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA:
                print("\n################################################",
                    "\nIniciando la configuración de Expedidora/Validadora",
                    "\n################################################\n")

                if self.sistemaFuncionandoCorrectamente:

                    GPIO.setmode (GPIO.BCM)
                    GPIO.setwarnings (False)

                    self.DI_00 = 18

                    self.DI_01 = 22
                    self.DI_02 = 10
                    self.DI_03 = 27
                    
                    self.DO_03 = 9


                    GPIO.setup(self.DI_00, GPIO.IN)
                    GPIO.setup(self.DI_01, GPIO.IN)
                    GPIO.setup(self.DI_02, GPIO.IN)
                    GPIO.setup(self.DI_03, GPIO.IN)

                    GPIO.setup(self.DO_03, GPIO.OUT)

                    for i in range (4):
                        self.raspberry_X.append(0)
                        self.raspberry_Y.append(0)

                self.listaDeVariables.Y[3].establecerFuncion(self.funcion_4)

            elif self.TipoDeControladora == Controladora.CONTROLADORA_PARA_CAJERO:

                print("\n################################################",
                    "\nIniciando la configuración de Cajero",
                    "\n################################################\n")



        #################################################################################################################################
        if self.tarjetaSeleccionada == Controladora.TARJETA_DE_INTERFAZ_ARDUINO:
            # Se abre un solo puerto de comunicación

            self.listaDePuertos.append (PuertoSerie("Puerto Serie"))

            self.listaDePuertos[0].modificarConfiguracion(dispositivo = PuertoSerie.ARDUINO_MICRO, )

            self.contadorDeInstruccion_Arduino = 0
            self.lock = threading.Lock()
            self.listaDePuertos[0].abrirPuerto()


            if self.listaDePuertos[0].puertoAbierto: # Se pudo abrir el puerto
                #TODO: Mejorar esta asignación para que sea dinámica
                #print ("******************************Se ha abierto el puerto tipo de controladora", self.TipoDeControladora)

                if self.TipoDeControladora == Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA:
                    print("\n################################################",
                        "\nIniciando la configuración de Expedidora/Validadora",
                        "\n################################################\n")

                    self.leerBanderas_TarjetaArduino()
                    if not self.listaDeVariables.VD[0].obtenerValor():
                        print ("\nERROR: La tarjeta de interfaz esta configurada como CAJERO, debe cambiar su configuración para que opere como EXPEDIDORA")
                        self.sistemaFuncionandoCorrectamente = False
                        self.listaDeVariables.Z[0].establecerValor(1, MODO="SOLO VARIABLE")

                    self.listaDeVariables.Y[3].establecerFuncion(self.funcion_3)


                elif self.TipoDeControladora == Controladora.CONTROLADORA_PARA_CAJERO:

                    print("\n################################################",
                        "\nIniciando la configuración de Cajero",
                        "\n################################################\n")

                    self.leerBanderas_TarjetaArduino()
                    if self.listaDeVariables.VD[0].obtenerValor():
                        print ("\nERROR: La tarjeta de interfaz esta configurada como EXPEDIDORA, debe cambiar su configuración para que opere como CAJERO")
                        self.sistemaFuncionandoCorrectamente = False
                        self.listaDeVariables.Z[0].establecerValor(1, MODO="SOLO VARIABLE")

                    else:
                        self.listaDeVariables.dispositivos[0].establecerPuerto (self.listaDePuertos[0])
                        self.listaDeVariables.dispositivos[0].establecerComunicacion (self.comunicacion)
                        #print ("******************************Se ha establecido el Monedero")

                        self.listaDeVariables.dispositivos[1].establecerPuerto (self.listaDePuertos[0])
                        self.listaDeVariables.dispositivos[1].establecerComunicacion (self.comunicacion)
                        #print ("******************************Se ha establecido el Billetero")

                        self.listaDeVariables.dispositivos[2].establecerPuerto (self.listaDePuertos[0])
                        self.listaDeVariables.dispositivos[2].establecerComunicacion (self.comunicacion)

                    
                        self.listaDeVariables.dispositivos[3].establecerPuerto (self.listaDePuertos[0])
                        self.listaDeVariables.dispositivos[3].establecerComunicacion (self.comunicacion)

                        self.listaDeVariables.dispositivos[4].establecerPuerto (self.listaDePuertos[0])
                        self.listaDeVariables.dispositivos[4].establecerComunicacion (self.comunicacion)

                        self.listaDeVariables.dispositivos[5].establecerPuerto (self.listaDePuertos[0])
                        self.listaDeVariables.dispositivos[5].establecerComunicacion (self.comunicacion)



                        # Se anexa el segundo puerto de comunicación para controlar el billetero JCM
                        '''                    
                        self.listaDePuertos.append (PuertoSerie("Puerto Serie 2"))
                        self.listaDePuertos[1].modificarConfiguracion(dispositivo = PuertoSerie.CABLE_USB)
                        self.listaDePuertos[1].abrirPuerto()

                        if self.listaDePuertos[0].puertoAbierto:
                            print ("Se abrio el segundo puerto de comunicación")
                            self.listaDeVariables.dispositivos[6].establecerPuerto (self.listaDePuertos[1])
                            self.listaDeVariables.dispositivos[6].establecerComunicacion (self.comunicacion)
                        '''
                            
                        


            else:
                
                self.sistemaFuncionandoCorrectamente = False
                self.listaDeVariables.Z[0].establecerValor(1, MODO="SOLO VARIABLE")


    def run (self):
        print ("Funcionando proceso para actualizar las variables")

        self.funcionando = True
        while (self.funcionando):
            #TODO:Verificar si se pudieron levantar los puertos

            self.TON_00.entrada = not self.TON_00.salida
            self.TON_00.actualizar()

            self.TON_02.entrada = not self.TON_02.salida
            self.TON_02.actualizar()

            if self.TON_00.salida:  # Se actualiza el contador
                self.contador += 1
                #print (end= "")
                #print ("%d." %self.contador, flush=True)

            if self.TON_02.salida:  # Se ejecuta una solicitud de instrucción 

                if self.sistemaFuncionandoCorrectamente:
                    #####################################################################################################################
                    if self.tarjetaSeleccionada == Controladora.TARJETA_DE_PULSO:
                        self.leerEntradas_TarjetaDePulso()


                    #####################################################################################################################
                    if self.tarjetaSeleccionada == Controladora.TARJETA_DE_INTERFAZ_BLANCA:


                        

                        if self.TipoDeControladora == Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA:
                            self.numeroMaximoDeInstruccion = 3
                            self.leerEntradas_TarjetaInterfazBlanca()



                        elif self.TipoDeControladora == Controladora.CONTROLADORA_PARA_CAJERO:
                            self.numeroMaximoDeInstruccion = 4

                            if self.contador == 0:  # inicialización de la tarjeta
                                self.leerEntradas_TarjetaInterfazBlanca()

                            if self.contador == 2:  # Inicializacion del Monedero
                                self.listaDeVariables.dispositivos[0].inicializacion()
                                pass

                            if self.contador == 4:  # Inicializacion del Billetero
                                self.listaDeVariables.dispositivos[1].inicializacion()
                                pass

                            if self.contador > 6:
                                if self.numeroDeInstruccion < self.numeroMaximoDeInstruccion - 1:
                                    self.numeroDeInstruccion +=1
                                else:
                                    self.numeroDeInstruccion = 0
                                #print ("numeroDeInstruccion", self.numeroDeInstruccion, end="\t", flush=True)



                                if self.numeroDeInstruccion == 0:
                                    self.leerEntradas_TarjetaInterfazBlanca()

                                    pass

                                if self.numeroDeInstruccion == 1:
                                    self.listaDeVariables.dispositivos[0].status()
                                    pass
                                    
                                if self.numeroDeInstruccion == 2:
                                    self.listaDeVariables.dispositivos[1].status()
                                    pass

                                if self.numeroDeInstruccion == 3:

                                    self.listaDeVariables.dispositivos[0].desencolarInstruccion()
                                    self.listaDeVariables.dispositivos[1].desencolarInstruccion()

                    #####################################################################################################################
                    if self.tarjetaSeleccionada == Controladora.TARJETA_DE_INTERFAZ_NEGRA:
                        self.leerEntradas_TarjetaInterfazNegra()


                        
                    #####################################################################################################################

                    if self.tarjetaSeleccionada == Controladora.TARJETA_DE_INTERFAZ_ARDUINO:



                        if self.TipoDeControladora == Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA:
                            self.numeroMaximoDeInstruccion = 2

                            if self.contador > 0:
                                if self.numeroDeInstruccion < self.numeroMaximoDeInstruccion - 1:
                                    self.numeroDeInstruccion +=1
                                else:
                                    self.numeroDeInstruccion = 0


                                if self.numeroDeInstruccion == 0:
                                    self.leerEntradas_TarjetaArduino()


                                if self.numeroDeInstruccion == 1:
                                    self.desencolarInstruccion()


                        elif self.TipoDeControladora == Controladora.CONTROLADORA_PARA_CAJERO:
                            self.numeroMaximoDeInstruccion = 6


                            if self.contador == 1:  # inicialización del monedero
                                self.leerEntradas_TarjetaArduino()
                                pass

                            if self.contador == 3:  # Inicializacion del Billetere
                                self.listaDeVariables.dispositivos[0].inicializacion()
                                pass

                            if self.contador == 5:  # Inicializacion del Monedero
                                self.listaDeVariables.dispositivos[1].inicializacion()

                                pass

                            if self.contador == 6:  # Inicializacion del Hopper_1
                                self.listaDeVariables.dispositivos[3].inicializacion()

                            if self.contador == 7:  # Inicializacion del Hopper_2
                                self.listaDeVariables.dispositivos[4].inicializacion()

                            if self.contador == 8:  # Inicializacion del Hopper_3
                                self.listaDeVariables.dispositivos[5].inicializacion()

                            if self.contador == 9:  # Inicializacion del validador
                                self.listaDeVariables.dispositivos[2].inicializacion()


                            if self.contador == 10:  # Inicializacion de Billetero JCM
                                self.listaDeVariables.dispositivos[6].inicializacion()


                            if self.contador > 11:
                                if self.numeroDeInstruccion < self.numeroMaximoDeInstruccion - 1:
                                    self.numeroDeInstruccion +=1
                                else:
                                    self.numeroDeInstruccion = 0
                                #rint ("numeroDeInstruccion", self.numeroDeInstruccion, end="\t", flush=True)

                                if self.numeroDeInstruccion == 0:
                                    self.leerEntradas_TarjetaArduino()
                                    pass


                                if self.numeroDeInstruccion == 1:
                                    #print ("numeroDeInstruccion", self.numeroDeInstruccion)
                                    
                                    
                                    self.listaDeVariables.dispositivos[0].status()
                                    self.listaDeVariables.dispositivos[2].status()
                                    #self.listaDeVariables.dispositivos[0].variables[9].actualizarInterfaz()
                                    pass
                                    
                                if self.numeroDeInstruccion == 2:
                                    
                                    self.listaDeVariables.dispositivos[1].status()
                                    
                                    pass

                                if self.numeroDeInstruccion == 3:
                                    #self.listaDeVariables.dispositivos[2].status()
                                    #self.listaDeVariables.dispositivos[3].status()
                                    self.leerEntradas_TarjetaArduino()
                                    pass

                                if self.numeroDeInstruccion == 4:
                                    
                                    self.listaDeVariables.dispositivos[0].status()
                                    self.listaDeVariables.dispositivos[2].status()
                                    pass


                                if self.numeroDeInstruccion == 5:
                                    self.desencolarInstruccion()
                                    self.listaDeVariables.dispositivos[0].desencolarInstruccion()
                                    self.listaDeVariables.dispositivos[1].desencolarInstruccion()
                                    self.listaDeVariables.dispositivos[2].desencolarInstruccion()
                                    self.listaDeVariables.dispositivos[3].desencolarInstruccion()
                                    self.listaDeVariables.dispositivos[4].desencolarInstruccion()
                                    self.listaDeVariables.dispositivos[5].desencolarInstruccion()
                                    self.listaDeVariables.dispositivos[6].desencolarInstruccion()

                                    pass








        print ("Hilo terminado de actualizarVariables")

    def detener (self):
        self.funcionando = False
        print ("Deteniendo actualizarVariables")

    ############################################### Metodos para leer entradas de la tarjeta con arduino ################################
    """
    def ejecutarInstrucciones_TarjetaArduino(self):
        # Viene de un hilo que lo esta ejecuntado antes por lo tantose asume que hay un bucle atras
        self.contadorDeInstruccion_Arduino += 1
    """








    def leerSenales_Dispositivo(self):
        self.listaDeVariables.dispositivos[0].status()

    def leerBanderas_TarjetaArduino(self):
        #TODO: Verificar se se reunen las condiciones (el puerto esta abierto)
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BANDERAS)
        #print ("Mensaje ", a)
        #print("Funcionando")
        r = False
        self.lock.acquire()
        try:
            self.listaDePuertos[0].write(a)
            time.sleep(.01)	
            r = self.listaDePuertos[0].read(10)
        except:
            self.listaDeVariables.Z[0].establecerValor(1, MODO="SOLO VARIABLE")  # Error de comunicación
            #print ("en entradas no se leyeron datos r=", r)

        else:
            #print ("entradas r = ", r)
            pass
        finally:
            self.lock.release()
        instruccionCorrecta = False
        
        if (r):
            if len(r) == 3:
                if r[0] == ord(Comunicacion.caracterDeInicio):
                    if r[2] == ord(Comunicacion.caracterDeFin):
                        instruccionCorrecta = True
                        print (r)

        if instruccionCorrecta:

            for j in range (1):
                for i in range (8):
                    self.listaDeVariables.VD[i+j*8].establecerValor((r[1+j] >> i) & 1, MODO="SOLO VARIABLE")
                    #print ("VD[{}]={}".format(i+j*8, (r[1+j] >> i) & 1))

        
        

    def leerEntradas_TarjetaArduino(self):
        #TODO: Verificar se se reunen las condiciones (el puerto esta abierto)
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
        #print ("Mensaje ", a)
        #print("Funcionando")
        r = False
        self.lock.acquire()
        try:
            self.listaDePuertos[0].write(a)
            time.sleep(.015)	
            r = self.listaDePuertos[0].read(10)
        except:
            self.listaDeVariables.Z[0].establecerValor(1, MODO="SOLO VARIABLE")  # Error de comunicación
            guardar.print ("en entradas no se leyeron datos r=", r)


        else:
            print ("entradas r = ", r)
            pass
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
            self.listaDeVariables.Z[0].establecerValor(0, MODO="SOLO VARIABLE")  # Error de comunicación
            for j in range (2):
                for i in range (8):
                    self.listaDeVariables.establecerX(i+j*8, (r[1+j] >> i) & 1)

            for j in range (2):
                for i in range (8):
                    self.listaDeVariables.Y[i+j*8].establecerValor((r[3+j] >> i) & 1, MODO="SOLO VARIABLE")
                    #print ("Y[{}]={}".format(i+j*8, (r[3+j] >> i) & 1))
        else:
            self.listaDeVariables.Z[0].establecerValor(1, MODO="SOLO VARIABLE")  # Error de comunicación
            print("**********************Instrucion recibida de forma incorrecta  r = ", r)


    def funcion_3 (self, indice, valor):


        self.listaDeFunciones.append([self.ESCRIBIR_VARIABLE, indice, valor])



        #print ("Recibido en 3 {} = {}".format(indice, valor))
        #TODO: Mejorar la implementación de este sistema para cuando se anexan más tareas simultaneas

        # self.lock.acquire()
        # try:
        #     a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [indice, 1 if valor else 0])
        #     self.listaDePuertos[0].enviarBytes(a)
        # except:
        #     print ("No se pudo enviar la instruccion")
        #     raise("Error No se pudo escribir la instruccion")
        # finally:
        #     self.lock.release()


    def desencolarInstruccion(self):
        while len(self.listaDeFunciones)>0:
            #print("Se imprime la lista de funciones", len(self.listaDeFunciones))
            #print ("Antes de desencolarInstrucción->", len(self.listaDeFunciones))
            funcion = self.listaDeFunciones.pop()
            #print ("Despues de desencolarInstrucción->", len(self.listaDeFunciones))

            # Seleccion de instrucción
            if funcion[0] == self.ESCRIBIR_VARIABLE:
                self.lock.acquire()
                try:
                    a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [funcion[1], 1 if funcion[2] else 0])
                    self.listaDePuertos[0].enviarBytes(a)
                except:
                    print ("No se pudo enviar la instruccion")
                    raise("Error No se pudo escribir la instruccion")
                finally:
                    self.lock.release()



    ############################################### Metodos para leer entradas de la tarjeta de pulso ################################

    def leerEntradas_TarjetaDePulso(self):
        #TODO: Verificar si se reunen las condiciones para que funcione la lectura (El puerto esta abierto y se obtiene lecturas y los hilos del keylogger estan vivos)
        r = self.listaDePuertos[0].read(10)
        #print (r)
        if r == b'\xFE':
            self.listaDeVariables.establecerX(1, 0)
        if r == b'\xF9':
            self.listaDeVariables.establecerX(1, 1)


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
                self.listaDeVariables.establecerX(2, 1)
                self.listaDeVariables.establecerX(3, 1)

            if self.TON_10.salida:
                self.banderaF3Detectada = False
                self.listaDeVariables.establecerX(2, 0)
                self.listaDeVariables.establecerX(3, 0)

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




    ############################################### Metodos para leer entradas de la tarjeta de interfaz blanca unicamente con raspberry###########


    def leerEntradas_TarjetaInterfazBlanca(self):
        #TODO:Verificar si se reunen las condiciones (solo funciona en rasperry)
        # Se leen los valores de los pines 
        
        self.raspberry_X[0] = GPIO.input(self.DI_00)
        self.raspberry_X[1] = GPIO.input(self.DI_02)
        self.raspberry_X[2] = GPIO.input(self.DI_01)
        self.raspberry_X[3] = GPIO.input(self.DI_03)

        # se mapean los valores a la lista de variables
        self.listaDeVariables.establecerX(0, self.raspberry_X[0])
        self.listaDeVariables.establecerX(1, self.raspberry_X[1])
        self.listaDeVariables.establecerX(2, self.raspberry_X[2])
        self.listaDeVariables.establecerX(3, self.raspberry_X[3])
        
        GPIO.output (self.DO_03, self.raspberry_Y[3])            
        self.listaDeVariables.Y[3].establecerValor(self.raspberry_Y[3], MODO="SOLO VARIABLE")

    def funcion_2 (self, indice, valor):
        #print ("Recibido en funcion 2 {} = {}".format(indice, valor))
        self.raspberry_Y[indice] = valor

    ############################################### Metodos para leer entradas de la tarjeta de interfaz negra unicamente con raspberry###########


    def leerEntradas_TarjetaInterfazNegra(self):
        #TODO:Verificar si se reunen las condiciones (solo funciona en rasperry)
        # Se leen los valores de los pines 
        
        self.raspberry_X[0] = GPIO.input(self.DI_00)
        self.raspberry_X[1] = GPIO.input(self.DI_01)
        self.raspberry_X[2] = GPIO.input(self.DI_02)
        self.raspberry_X[3] = GPIO.input(self.DI_03)

        # se mapean los valores a la lista de variables
        self.listaDeVariables.establecerX(0, self.raspberry_X[0])
        self.listaDeVariables.establecerX(1, self.raspberry_X[1])
        self.listaDeVariables.establecerX(2, self.raspberry_X[2])
        self.listaDeVariables.establecerX(3, self.raspberry_X[3])
        
        GPIO.output (self.DO_03, self.raspberry_Y[3])            
        self.listaDeVariables.Y[3].establecerValor(self.raspberry_Y[3], MODO="SOLO VARIABLE")

    def funcion_4 (self, indice, valor):
        #print ("Recibido en funcion 2 {} = {}".format(indice, valor))
        self.raspberry_Y[indice] = valor


class ListaDeVariables ():
    X = []
    Y = []
    Z = []

    VD = []

    dispositivos = []





    def __init__(self):
        self.inicializarVariables()

    def inicializarVariables(self):
        self.X.append(Variable("X-00", "X-00", "Descripción"))
        self.X.append(Variable("X-01", "X-01", "Descripción"))
        self.X.append(Variable("X-02", "X-02", "Descripción"))
        self.X.append(Variable("X-03", "X-03", "Descripción"))
        self.X.append(Variable("X-04", "X-04", "Descripción"))
        self.X.append(Variable("X-05", "X-05", "Descripción"))
        self.X.append(Variable("X-06", "X-06", "Descripción"))
        self.X.append(Variable("X-07", "X-07", "Descripción"))
        self.X.append(Variable("X-08", "X-08", "Descripción"))
        self.X.append(Variable("X-09", "X-09", "Descripción"))
        self.X.append(Variable("X-10", "X-10", "Descripción"))
        self.X.append(Variable("X-11", "X-11", "Descripción"))
        self.X.append(Variable("X-12", "X-12", "Descripción"))
        self.X.append(Variable("X-13", "X-13", "Descripción"))
        self.X.append(Variable("X-14", "X-14", "Descripción"))
        self.X.append(Variable("X-15", "X-15", "Descripción"))


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


        self.VD.append(Variable("VD-00", "Tarjeta de interfaz configurada como expedidora", 0))
        self.VD.append(Variable("VD-01", "VD-01", 0))
        self.VD.append(Variable("VD-02", "VD-02", 0))
        self.VD.append(Variable("VD-03", "VD-03", 0))
        self.VD.append(Variable("VD-04", "VD-04", 0))
        self.VD.append(Variable("VD-05", "VD-05", 0))
        self.VD.append(Variable("VD-06", "VD-06", 0))
        self.VD.append(Variable("VD-07", "VD-07", 0))

        for i, elemento in enumerate(self.X):
            self.establecerX(i, 0)
        
        for i, elemento in enumerate(self.Y):
            self.Y[i].establecerIndice(i)

        monedero1 = Monedero("MON-000", "Monedero", "en cajero")
        billetero1 = Billetero("BIL-001", "Billetero", "en cajero")
        validador = Validador("VAL-002", "Validador", "validador", direccion  = 2)
        hopper1 = Hopper("HOP-003", "Hopper 3", "para monedas de 5 pesos", direccion = 3, valorDeMoneda = 5)
        hopper2 = Hopper("HOP-004", "Hopper 4", "para monedas de 10 pesos", direccion = 4, valorDeMoneda = 10)
        hopper3 = Hopper("HOP-005", "Hopper 5", "para monedas de 1 pesos", direccion = 5, valorDeMoneda = 1)

        billeteroJCM = BilleteroJCM("BIL-006", "BilleteroJCM 1", "billeteroJCM")


        self.dispositivos.append(monedero1)
        self.dispositivos.append(billetero1)
        self.dispositivos.append(validador)
        self.dispositivos.append(hopper1)
        self.dispositivos.append(hopper2)
        self.dispositivos.append(hopper3)
        self.dispositivos.append(billeteroJCM)

        
        print ("\n->Se han creado las variables")

    #-------------------- Entradas
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


    #-------------------- Salidas
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


    #-------------------- Alarmas
    def establecerZ(self, indice, valor):
        if indice < len(self.Z):
            self.Z[indice].establecerValor(valor)
        else:
            print ("El indice es mayor ", indice)

    def obtenerZ(self, indice):
        if indice < len(self.Z):
            return self.Z[indice].obtenerValor()
        else:
            print ("El indice es mayor ", indice)
        return false

    def imprimirZ(self, valorMaximo = 0):
        if valorMaximo == 0:
            valorMaximo = len(self.Z)
        aux="[ "
        for i , elemento in enumerate(self.Z):
            if i >= valorMaximo:
                break
            aux += "{}".format(elemento.obtenerValor())
            if i < valorMaximo-1 :
                aux += ", "
        aux += " ]"                
        print (aux, end="")


    #-------------------- Banderas
    def establecerVD(self, indice, valor):
        if indice < len(self.VD):
            self.VD[indice].establecerValor(valor)
        else:
            print ("El indice es mayor ", indice)

    def obtenerVD(self, indice):
        if indice < len(self.VD):
            return self.VD[indice].obtenerValor()
        else:
            print ("El indice es mayor ", indice)
        return false



                




class EjecutarPrograma():
    def __init__(self, listaDeVariables):

        self.listaDeVariables = listaDeVariables

        self.TON_01 = Temporizador("TON_01",0.5)
        self.TON_02 = Temporizador("TON_02",0.5)
        self.TON_03 = Temporizador("TON_03",0.5)
        self.TON_04 = Temporizador("TON_04",15)

        self.aux = 0
        self.aux_2 = 0

        tarea1 = threading.Thread(target=self.run)
        tarea1.start()

        self.estadoDeLaSecuencia = 0
        self.secuenciaBilleteroJCM = 0

    def run (self):
        self.funcionando = True

        while (self.funcionando):
            self.TON_02.entrada = not self.TON_02.salida
            self.TON_02.actualizar()

            if self.TON_02.salida:
                """
                print ("\n", end='')
                self.listaDeVariables.imprimirX(8)
                print ("", end="\t")
                self.listaDeVariables.imprimirY(8)
                print ("", end="\t")
                self.listaDeVariables.imprimirZ()
                print ("", end=" ")


                """

                """
                if self.estadoDeLaSecuencia == 9:
                    self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Validador.MODIFY_MASTER_INHIBIT_STATUS, 0)
                    self.estadoDeLaSecuencia = 1

                if self.estadoDeLaSecuencia == 8:
                    if self.listaDeVariables.dispositivos[5].variables[34].obtenerValor() == 3:



                        self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Validador.ENTREGAR_MONEDAS, 1)
                        self.listaDeVariables.dispositivos[5].variables[34].establecerValor(0)

                        self.estadoDeLaSecuencia = 9



                if self.estadoDeLaSecuencia == 7:
                    self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Validador.MODIFY_SORTER_PATHS, 15, 4)
                    self.estadoDeLaSecuencia = 8




                if self.estadoDeLaSecuencia == 6:
                    if self.listaDeVariables.dispositivos[5].variables[31].obtenerValor() == 2:



                        self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Validador.ENTREGAR_MONEDAS, 2)
                        self.listaDeVariables.dispositivos[5].variables[31].establecerValor(0)

                        self.estadoDeLaSecuencia = 7



                if self.estadoDeLaSecuencia == 5:
                    self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Validador.MODIFY_SORTER_PATHS, 15, 1)
                    self.estadoDeLaSecuencia = 6



                if self.estadoDeLaSecuencia == 4:
                    if self.listaDeVariables.dispositivos[5].variables[32].obtenerValor() == 5:
                        self.listaDeVariables.dispositivos[4].ejecutarInstruccion(Hopper.DISPENSE_COINS, 5)
                        self.listaDeVariables.dispositivos[5].variables[32].establecerValor(20)

                        self.estadoDeLaSecuencia = 5


                if self.estadoDeLaSecuencia == 3:
                    self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Validador.MODIFY_SORTER_PATHS, 15, 2)
                    self.estadoDeLaSecuencia = 4


                if self.estadoDeLaSecuencia == 2:
                    if self.listaDeVariables.dispositivos[5].variables[33].obtenerValor() == 6:
                        self.listaDeVariables.dispositivos[3].ejecutarInstruccion(Hopper.DISPENSE_COINS, 4)
                        self.listaDeVariables.dispositivos[5].variables[33].establecerValor(2)

                        self.estadoDeLaSecuencia = 3




                if self.estadoDeLaSecuencia == 1:
                    #self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Validador.MODIFY_SORTER_PATHS, 15, 3)
                    self.estadoDeLaSecuencia = 2


                if self.estadoDeLaSecuencia == 0:
                    if self.listaDeVariables.dispositivos[5].variables[35].obtenerValor() == 5:
                        self.listaDeVariables.dispositivos[2].ejecutarInstruccion(Hopper.DISPENSE_COINS, 3)
                        self.listaDeVariables.dispositivos[5].variables[35].establecerValor(2)


                        #self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Validador.ENTREGAR_MONEDAS, 2)
                        #self.listaDeVariables.dispositivos[5].variables[34].establecerValor(0)

                        self.estadoDeLaSecuencia = 1

                """

                if self.listaDeVariables.dispositivos[2].variables[35].obtenerValor() == 5:
                        self.listaDeVariables.dispositivos[3].ejecutarInstruccion(Hopper.DISPENSE_COINS, 3)
                        self.listaDeVariables.dispositivos[2].variables[35].establecerValor(2)

                        self.listaDeVariables.dispositivos[2].ejecutarInstruccion(Validador.ENTREGAR_MONEDAS, 2)
                        self.listaDeVariables.dispositivos[2].variables[34].establecerValor(0)


                if self.listaDeVariables.dispositivos[2].variables[33].obtenerValor() == 6:
                    self.listaDeVariables.dispositivos[4].ejecutarInstruccion(Hopper.DISPENSE_COINS, 4)
                    self.listaDeVariables.dispositivos[2].variables[33].establecerValor(2)

                if self.listaDeVariables.dispositivos[2].variables[32].obtenerValor() == 5:
                    self.listaDeVariables.dispositivos[5].ejecutarInstruccion(Hopper.DISPENSE_COINS, 5)
                    self.listaDeVariables.dispositivos[2].variables[32].establecerValor(0)

                if self.listaDeVariables.dispositivos[2].variables[34].obtenerValor() == 1:
                    self.listaDeVariables.dispositivos[2].ejecutarInstruccion(Validador.ENTREGAR_MONEDAS, 2)
                    self.listaDeVariables.dispositivos[2].variables[34].establecerValor(0)



                self.TON_01.entrada = self.aux
                self.TON_01.actualizar()

                if self.TON_01.salida:
                    self.aux = 0





                
                # if self.listaDeVariables.X[3].obtenerValor() and not self.aux:
                #     ########################################################################################################
                #     # Instrucción para dispensar la cantidad de dinero descrita en el monedero
                #     # self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_DAR_CAMBIO, 2)
                    
                #     ########################################################################################################
                #     # Instrucción para dispensar monedas por medio de un tubo determinado   , cantidadDeMonedas, tipoDeMoneda
                #     # tipoMoneda == 2 => 1 peso
                #     # tipoMoneda == 3 => 2 pesos
                #     # tipoMoneda == 4 => 5 pesos
                #     # tipoMoneda == 5 => 10 pesos
                #     self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_DISPENSAR_MONEDAS, 3,3)

                #     self.aux = 1


                if self.listaDeVariables.X[0].obtenerValor() and not self.aux:

                    self.listaDeVariables.dispositivos[2].ejecutarInstruccion(Hopper.DISPENSE_COINS, 10)
                    self.listaDeVariables.dispositivos[3].ejecutarInstruccion(Hopper.DISPENSE_COINS, 10)
                    self.listaDeVariables.dispositivos[4].ejecutarInstruccion(Hopper.DISPENSE_COINS, 10)
                    # self.listaDeVariables.dispositivos[2].ejecutarInstruccion(Hopper.SIMPLE_POLL)
                    # self.listaDeVariables.dispositivos[2].ejecutarInstruccion(Hopper.REQUEST_MANUFACTURER)
                    # self.listaDeVariables.dispositivos[2].ejecutarInstruccion(Hopper.REQUEST_SERIAL_NUMBER)

                    self.aux = 1


                

                
            self.TON_03.entrada = not self.TON_03.salida
            self.TON_03.actualizar()    

            if self.TON_03.salida:
                
                

                if self.listaDeVariables.X[3].obtenerValor() and not self.aux:


                    print ("Se oprimio el botón")
                    self.listaDeVariables.dispositivos[6].ejecutarInstruccion(BilleteroJCM.RESET)


                    self.aux = 1

                    pass

                if self.secuenciaBilleteroJCM == 0:


                    pass
                
                # print (">>>>>>>>>>>>>>>>>>>>>>>>>Cambiando Estado", end='', flush=True)
                # print (">>>>>>>>>>>>>>>>>>>>>>>>>Valor actual ", self.listaDeVariables.Y[3].obtenerValor())

                # self.listaDeVariables.Y[3].establecerValor(not self.listaDeVariables.Y[3].obtenerValor())

                
            
            self.TON_04.entrada = not self.TON_04.salida
            self.TON_04.actualizar()

            if self.TON_04.salida:
                print ("Se activo TON_04")

                """
                if self.aux_2:
                    self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_HABILITAR)
                    self.listaDeVariables.dispositivos[1].ejecutarInstruccion(Billetero.BILLETERO_HABILITAR)

                    self.aux_2 = 0

                else:
                    self.listaDeVariables.dispositivos[0].ejecutarInstruccion(Monedero.MONEDERO_DESHABILITAR)
                    self.listaDeVariables.dispositivos[1].ejecutarInstruccion(Billetero.BILLETERO_DESHABILITAR)
                    self.aux_2 = 1

                """

                # for variable in self.listaDeVariables.dispositivos[0].variables:
                #     print ("{} {} {}".format(variable.obtenerTag().ljust(6), variable.obtenerNombre().ljust( 25 ), str(variable.obtenerValor()).ljust( 10 )))

                



def main ():
    variables = ListaDeVariables()

    #interfazDeVariables = InterfazDeVariables(variables.X)
    interfazDeVariables = InterfazDeVariables(variables.dispositivos[5].variables)
    

    time.sleep(5)

    opcion = 5

    #---------------------------------------- Tarjeta de interfaz arduino
    if opcion == 1:
        controladora = Controladora(variables, 
            tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO,
            tipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)

    if opcion == 5:
        controladora = Controladora(variables, 
            tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO,
            tipoDeControladora = Controladora.CONTROLADORA_PARA_CAJERO)
    

    #---------------------------------------- tarjeta de pulso
    if opcion == 2:

        controladora = Controladora(variables, 
            tarjeta = Controladora.TARJETA_DE_PULSO,
            tipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)


    #---------------------------------------- tarjeta de interfaz pines GPIO de la raspberry
    if opcion == 3:
        controladora = Controladora(variables, 
            tarjeta = Controladora.TARJETA_DE_INTERFAZ_BLANCA, 
            tipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)
    
    if opcion == 4:
        controladora = Controladora(variables, 
            tarjeta = Controladora.TARJETA_DE_INTERFAZ_NEGRA, 
            TipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)

    if opcion == 6:
        controladora = Controladora(variables, 
            tarjeta = Controladora.TARJETA_DE_INTERFAZ_BLANCA, 
            tipoDeControladora = Controladora.CONTROLADORA_PARA_CAJERO)


    #---------------------------------------- Programa a ejecutar
    ejecutarPrograma = EjecutarPrograma(variables)



if __name__ == "__main__":
    main ()
