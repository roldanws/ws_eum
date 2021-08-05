__author__ = "Sigfrido"
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

class Validador (Variable):
    
    IMPRIMIR = 0x0E


    # Instrucciones 
    
    #Esto es lo que estoy haciendo ya estas probadas estas instrucciones con el validador
    SIMPLE_POLL = 0xFE
    ADDRESS_POLL = 0xFD
    REQUEST_POLLING_PRIORITY = 0xF9
    REQUEST_STATUS = 0xF8
    REQUEST_MANUFACTURER_ID = 0xF6
    REQUEST_EQUIPMENT_CATEGORY_ID = 0xF5
    REQUEST_PRODUCT_CODE = 0xF4
    REQUEST_DATABASE_VERSION = 0xF3
    REQUEST_SERIAL_NUMBER = 0xF2
    REQUEST_SOFTWARE_VERSION = 0xF1
    TEST_SOLENOIDS = 0XF0
    READ_INPUT_LINES = 0xED
    READ_OPTO_STATES = 0xEC
    PERFORM_SELF_CHECK = 0XE8
    MODIFY_INHIBIT_STATUS = 0xE7
    REQUEST_INHIBIT_STATUS = 0xE6
    READ_BUFFERED_CREDIT_OR_ERROR_CODES = 0xE5

    #TODO: Falta probar estas instrucciones

    MODIFY_MASTER_INHIBIT_STATUS = 0xE4
    REQUEST_MASTER_INHIBIT_STATUS = 0xE3
    REQUEST_INSERTION_COUNTER = 0xE2
    REQUEST_ACCEPT_COUNTER = 0xE1
    MODIFY_SORTER_OVERRIDE_STATUS = 0xDE
    REQUEST_SORTER_OVERRIDE_STATUS = 0xDD

    MODIFY_SORTER_PATHS =  0xD2
    REQUEST_SORTER_PATHS = 0xD1


    MODIFY_COIN_ID = 0xB9
    REQUEST_COIN_ID = 0xB8

    REQUEST_TEACH_STATUS = 0xC9
    TEACH_MODE_CONTROL = 0xCA


    ENTREGAR_MONEDAS = 0x46



    RESET_DEVICE = 0x01






    TIEMPO_DE_RETARDO_EN_LECTURA = 0.030






    def __init__(self, tag, nombre, descripcion, **kwargs):
        Variable.__init__ (self, tag = tag, nombre = nombre, descripcion = descripcion)
        
        
        self.equipoInicializado = False
        
        self.listaDeFunciones = []

        self.M = []
        for i in range (80):
            self.M.append(0)

        self.RC = []
        for i in range (80):
            self.RC.append(0)


        self.variables = []

        for i in range(80):
            self.variables.append(Variable("X_{:02d}".format(i), "", ""))

        
        self.variables[0]=Variable("X_00", "Direccion", "")
        self.variables[1]=Variable("X_01", "Numero de Serie", "")
        self.variables[2]=Variable("X_02", "", "")
        self.variables[3]=Variable("X_03", "Equipo Maestro", "")
        self.variables[4]=Variable("X_04", "", "")
        self.variables[6]=Variable("X_06", "Número de serie", "")
        self.variables[7]=Variable("X_07", "", "")

        self.variables[8]=Variable("X_08", "Status", "")    # Request Status
        self.variables[9]=Variable("X_09", "", "")
        self.variables[10]=Variable("X_10", "lista de Eventos", "")         # readBufferedCreditOrErrorCodes - Lista de Eventos
        self.variables[11]=Variable("X_11", "Moneda 1", "")         # Moneda_1, valor->Denominación de la moneda
        self.variables[12]=Variable("X_12", "Moneda 2", "")
        self.variables[13]=Variable("X_13", "Moneda 3", "")
        self.variables[14]=Variable("X_14", "Moneda 4", "")
        self.variables[15]=Variable("X_15", "Moneda 5", "")
        self.variables[16]=Variable("X_16", "Moneda 6", "")
        self.variables[17]=Variable("X_17", "Moneda 7", "")
        self.variables[18]=Variable("X_18", "Moneda 8", "")
        self.variables[19]=Variable("X_19", "Moneda 9", "")
        self.variables[20]=Variable("X_20", "Moneda 10", "")
        self.variables[21]=Variable("X_21", "Moneda 11", "")
        self.variables[22]=Variable("X_22", "Moneda 12", "")
        self.variables[23]=Variable("X_23", "Moneda 13", "")
        self.variables[24]=Variable("X_24", "Moneda 14", "")
        self.variables[25]=Variable("X_25", "Moneda 15", "")         # Moneda_15
        self.variables[26]=Variable("X_26", "Moneda 16", "")
        self.variables[27]=Variable("X_27", "", "")
        self.variables[28]=Variable("X_28", "", "")
        self.variables[29]=Variable("X_29", "", "")
        self.variables[30]=Variable("X_30", "Camino 0", "")         # Contador de camino 0
        self.variables[31]=Variable("X_31", "Camino 1 (Almacen)", "")         # Contador de camino 1
        self.variables[32]=Variable("X_32", "Camino 2 (Hopper 5)", "")         # Contador de camino 2
        self.variables[33]=Variable("X_33", "Camino 3 (Hopper 4)", "")         # Contador de camino 3
        self.variables[34]=Variable("X_34", "Camino 4 (Almacén)", "")         # Contador de camino 4
        self.variables[35]=Variable("X_35", "Camino 5 (Hopper 3)", "")         # Contador de camino 5
        self.variables[36]=Variable("X_36", "", "")
        self.variables[37]=Variable("X_37", "", "")
        self.variables[38]=Variable("X_38", "", "")
        self.variables[39]=Variable("X_39", "", "")
        self.variables[40]=Variable("X_40", "", "")

        self.M[10] = self.variables[10].obtenerValor()      # Variable auxiliar para registrar eventos
        

        # Valores por defecto
        self.variables[3].establecerValor(1)    # Se establece el equipo maestro


        #TODO: Crear función para inicializar variables
        self.variables[4].establecerValor(1)       # Se establece el valor de 1 peso
        self.variables[4].establecerValor_2(True)       # Se habilita la moneda

        self.variables[5].establecerValor(2)       # Se establece el valor de 1 peso
        self.variables[5].establecerValor_2(True)       # Se habilita la moneda

        self.variables[6].establecerValor(5)       # Se establece el valor de 1 peso
        self.variables[6].establecerValor_2(True)       # Se habilita la moneda

        self.variables[8].establecerValor(1)       # Se establece el valor de 1 peso
        self.variables[8].establecerValor_2(True)       # Se habilita la moneda


        self.configurarDispositivo (**kwargs)
        self.actualizar()
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
            if key == "direccion":
                self.variables[0].establecerValor(value)

    def actualizar (self):
        pass



    def status(self):
        self.readBufferedCreditOrErrorCodes()
        pass

    def inicializacion(self):
        #print ("Dentro de inicializacion del hopper", end=" ",flush=True)

        if not self.equipoInicializado:
            print ("Inicializando {}".format(self), end=" ",flush=True)

            self.requestStatus()
            self.resetDevice()
            self.simplePoll()
            self.requestManufacturerId()
            self.requestProductCode()
            self.requestSerialNumber()
            self.modifyInhibitStatus()
            #self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 9,  5])
            ##
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 4,  5])  # 1 peso
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 5,  3])  # 2 pesos
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 6,  2])  # 5 pesos
            
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 8,  4])  # 10 pesos
            """
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 1,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 2,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 3,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 4,  1, 2, 3, 4])  # 1 peso
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 5,  1, 2, 3, 4])  # 2 pesos
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 6,  1, 2, 3, 4])  # 5 pesos
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 7,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 8,  1, 2, 3, 4])  # 10 pesos
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 9,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 10,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 11,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 12,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 13,  1, 2, 3, 4])
            self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 14,  1, 2, 3, 4])"""
            #self.modifySorterPaths([self.MODIFY_SORTER_PATHS, 15,  5])


            self.modifyMasterInhibitStatus([self.MODIFY_MASTER_INHIBIT_STATUS, 1])

        #self.puerto.flushInput()
        self.equipoInicializado = True
        




    #------------------------------------------------------------------------#
    #--------------------Metodos referentes al dispositivo-------------------#

    def simplePoll (self, args = None):

        mensaje = [self.SIMPLE_POLL]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("simplePoll ", r)
            if r[0] == 0x00:
                print ("Se recibio un ack")

    def addressPoll (self, args = None):

        mensaje = [self.ADDRESS_POLL]
        
        cctalkInstruccion = [0, len(mensaje) - 1, self.variables[3].obtenerValor()] + mensaje
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, cctalkInstruccion)

        self.puerto.escribir(a)
        time.sleep(3)
        r = self.puerto.leer_2(20)

        if r:
            print(r)
            # Se obtienen unicamente los datos despues de recibir la validación
        else:
            print("Hopper: No se recibio respuesta del puerto")

    def requestPollingPriority (self, args = None):

        mensaje = [self.REQUEST_POLLING_PRIORITY]
        
        r = self.enviarMensajeDispositivo(mensaje)
        
        if r:
            print("Datos recibidos", r)
            if r[0] == 0x00:
                print ("Request polling priority se recibio un ack")
                if r[1] == 0x02:
                    print ("El valor recomendado del polling es {}ms".format(10*r[2])) 


    def requestStatus (self, args = None):

        mensaje = [self.REQUEST_STATUS]
        
        r = self.enviarMensajeDispositivo(mensaje)

        s = ''
        t = 0

        if r:
            print("requestStatus", r)
            if r[1]==0x00:
                s += "Estatus OK"
                t = 1
            if r[1]==0x01:
                s += "Mecanismo de retorno de moneda activada"
                t = 0
            if r[1]==0x02:
                s += "sistema de deteccion de cadena activado"
                t = 0

            self.variables[8].establecerValor(t)
            self.variables[8].establecerValor_2(s)

            print (s)


    def requestManufacturerId (self, args = None):

        mensaje = [self.REQUEST_MANUFACTURER_ID]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("fabricante ", r)



    def requestEquipmentCategory (self, args = None):

        mensaje = [self.REQUEST_EQUIPMENT_CATEGORY_ID]
        r = self.enviarMensajeDispositivo(mensaje, tiempo = 0.040)

        if r:
            print ("Categoria ", r)



    def requestProductCode (self, args = None):

        mensaje = [self.REQUEST_PRODUCT_CODE]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("requestProductCode ", r)

    def requestDatabaseVersion (self, args = None):

        mensaje = [self.REQUEST_DATABASE_VERSION]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("requestDatabaseVersion ", r)


    def requestSerialNumber (self, args = None):

        mensaje = [self.REQUEST_SERIAL_NUMBER]
        r = self.enviarMensajeDispositivo(mensaje, tiempo = 0.035)

        if r:
            print ("requestSerialNumber ", r)
            #s = ["{0:02x}".format(elemento) for elemento in r]
            s = [elemento for elemento in r]
            #print (s)
            #print (["{0:02x}".format(elemento) for elemento in r])
            self.variables[6].establecerValor(s[1:])
            print ("el número de serie es", self.variables[6].obtenerValor())


    def requestSoftwareVersion (self, args = None):

        mensaje = [self.REQUEST_SOFTWARE_VERSION]
        r = self.enviarMensajeDispositivo(mensaje, tiempo = 0.040)

        if r:
            print ("requestSoftwareVersion ", r)


    def testSolenoids (self, args = None):


        #TODO: anexar byte para indicar que solenoides seran activados
        dato = 0x00

        solenoideDeAceptacion  = 1
        solenoideDeOrdenacion01 = 1
        solenoideDeOrdenacion02 = 1
        solenoideDeOrdenacion03 = 1

        dato = solenoideDeAceptacion & 1 | (solenoideDeOrdenacion01 & 1 )<< 1 | (solenoideDeOrdenacion02 & 1 )<< 2 | (solenoideDeOrdenacion03 & 1 )<< 3

        numeroDeBits = 0
        
        # for i in range(8):
        #     if (dato>>i) & 1:
        #         numeroDeBits += 1

        numeroDeBits =  len([i for i in range(8) if (dato>>i) & 1])

        mensaje = [self.TEST_SOLENOIDS] + [dato]
        r = self.enviarMensajeDispositivo(mensaje, tiempo = 0.5 + numeroDeBits*0.5)

        if r:
            print ("testSolenoids ", r)
            if r[0] == 0x00:
                print ("prueba de los solenoides finalizada")



    def readInputLines (self, args = None):

        mensaje = [self.READ_INPUT_LINES]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("readInputLines ", r)


    def readOptoStates (self, args = None):

        mensaje = [self.READ_OPTO_STATES]
        r = self.enviarMensajeDispositivo(mensaje, tiempo = 0.04)


        lista = []

        if r:
            print ("readOptoStates ", r)
            if r[0] == 0:   # indica que la instruccion se recibio correctamente
                for i in range(8):
                    lista.append((r[1]>>i) & 1)
        s = ''

        if lista[1] == 0:
            s += "Fototransistores libres"
        elif lista[1] == 1:
            if lista[1] == 1:
                s += "Fototransistor en salida de la moneda->>Bloquedo"
            if lista[2] == 1:
                s += "Fototransistor en el mecanismo detector->>Bloqueado"

        print (lista, s)
                        

    def performSelfCheck (self, args = None):

        mensaje = [self.PERFORM_SELF_CHECK]
        r = self.enviarMensajeDispositivo(mensaje, tiempo = 0.04)
        
        s = ''
        lista = []

        if r:
            print ("performSelfCheck ", r)
            
            if r[0] == 0:   # indica que la instruccion se recibio correctamente

                if r[1] == 1:
                    s += "Memoria Flash Dañada"

                if r[1] == 2:
                    s += "Falla en sensores electromagnéticos"
                    lista = [(r[2]>>i) & 1 for i in range(8)]

                    if lista[0]:
                        s += " Sensor 1"

                    if lista[1]:
                        s += " Sensor 2"

                    if lista[3]:
                        s += " Sensor 3"

                if r[1] == 3:
                    s += "Falla en sensor de credito"

                if r[1] == 4:
                    s += "Falla en sensor en módulo del sensor piezoelectrico"

                if r[1] == 6:
                    s += "Falla en la lectura del sensor"
                    lista = [(r[2]>>i) & 1 for i in range(8)]

                    if lista[0]:
                        s += " Sensor 1"

                    if lista[1]:
                        s += " Sensor 2"

                    if lista[3]:
                        s += " Sensor 3"

                if r[1] == 20:
                    s += "Error mecanismo detector (esta abierto)"

                if r[1] == 28:
                    s += "No responde el modulo del sensor"
                    
                if r[1] == 33:
                    s += "Falla en la alimentación del modulo del sensor"

                if r[1] == 34:
                    s += "Falla en el sensor de temperatura"

                if r[1] == 255:
                    s += "prueba de hardware no es valido"






    def modifyInhibitStatus (self, args = None):

        lista = [0] * 16
        dato = [0] * 2

        # Se define la lista de las monedas que se activaran
        lista[0] = 1
        lista[1] = 1
        lista[2] = 1
        lista[3] = 1
        lista[4] = 1
        lista[5] = 1
        lista[6] = 1
        lista[7] = 1
        lista[8] = 1
        lista[9] = 1
        lista[10] = 1
        lista[11] = 1
        lista[12] = 1
        lista[13] = 1
        lista[14] = 1
        lista[15] = 1



        for j in range (2):
            for i in range (8):
                dato[j] |= (lista[i+j*8] & 1) << i

        mensaje = [self.MODIFY_INHIBIT_STATUS] + dato

        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("modifyInhibitStatus ", r)
            if r[0] == 0x00:
                print ("Modificado correctamente")



    def requestInhibitStatus (self, args = None):

        mensaje = [self.REQUEST_INHIBIT_STATUS]
        r = self.enviarMensajeDispositivo(mensaje)

        lista = []

        if r:
            print ("requestInhibitStatus ", r, end=" ", flush=True)
            if r[0] == 0x00:    # Se recibio correctamente

                for j in range (1, 3):
                    
                    for i in range(8):
                        lista.append((r[j]>>i) & 1)
            print (lista)

                        

    def readBufferedCreditOrErrorCodes (self, args = None):

        mensaje = [self.READ_BUFFERED_CREDIT_OR_ERROR_CODES]
        r = self.enviarMensajeDispositivo(mensaje, tiempo = 0.04)


        listaDeResultados = [None]*5
        codigoDeError = 0
        codigoDeMonedas = 0
        s = ''
        
        if r:
            print ("readBufferedCreditOrErrorCodes ", r)
            if r[0] == 0x00: # Recibido correctamente
                # contadorDeEventos = r[1]
                for i in range (5):


                    listaDeResultados[i] = [r[2 + 2*i], r[2 + 2*i + 1]]

                    self.variables[10].establecerValor(r[1])


                    while self.M[10] < self.variables[10].obtenerValor():
                        self.M[10] += 1
                        indice = self.variables[10].obtenerValor() - self.M[10]
                        valorDeLaMoneda = 0


                        print ("--------------------------Se registro 1 Evento-------------", self.M[10])


                        print ("Se procesará", listaDeResultados[indice], indice, listaDeResultados)

                        if listaDeResultados[indice][0] != 0: #Se detecto una moneda hacia un camino
                            if listaDeResultados[indice][0] == 1:  # Moneda 1
                                pass
                            if listaDeResultados[indice][0] == 2:  # Moneda 2
                                pass
                            if listaDeResultados[indice][0] == 3:  # Moneda 3
                                pass
                            if listaDeResultados[indice][0] == 4:  # Moneda 4
                                #valorDeLaMoneda = self.variables[25].obtenerValor()
                                valorDeLaMoneda = 1
                                pass
                            if listaDeResultados[indice][0] == 5:  # Moneda 5
                                valorDeLaMoneda = 1
                                pass
                            if listaDeResultados[indice][0] == 6:  # Moneda 6
                                valorDeLaMoneda = 1
                                pass
                            if listaDeResultados[indice][0] == 7:  # Moneda 7
                                pass
                            if listaDeResultados[indice][0] == 8:  # Moneda 8
                                valorDeLaMoneda = 1
                                pass
                            if listaDeResultados[indice][0] == 9:  # Moneda 9
                                pass
                            if listaDeResultados[indice][0] == 10:  # Moneda 10
                                pass
                            if listaDeResultados[indice][0] == 11:  # Moneda 11
                                pass
                            if listaDeResultados[indice][0] == 12:  # Moneda 12
                                pass
                            if listaDeResultados[indice][0] == 13:  # Moneda 13
                                pass
                            if listaDeResultados[indice][0] == 14:  # Moneda 14
                                pass
                            if listaDeResultados[indice][0] == 15:  # Moneda 15
                                pass
                            if listaDeResultados[indice][0] == 16:  # Moneda 16
                                pass
                        
                            if listaDeResultados[indice][1] == 0:     # Se va hacia el camino predeterminado
                                print ("Camino predeterminado")
                            if listaDeResultados[indice][1] == 1:     # Se va hacia el camino 1
                                self.variables[31].establecerValor(self.variables[31].obtenerValor() + valorDeLaMoneda)
                                print ("Camino 1")
                            if listaDeResultados[indice][1] == 2:     # Se va hacia el camino 2
                                self.variables[32].establecerValor(self.variables[32].obtenerValor() + valorDeLaMoneda)
                                print ("Camino 2")
                            if listaDeResultados[indice][1] == 3:     # Se va hacia el camino 3
                                self.variables[33].establecerValor(self.variables[33].obtenerValor() + valorDeLaMoneda)
                                print ("Camino 3")
                            if listaDeResultados[indice][1] == 4:     # Se va hacia el camino 4
                                self.variables[34].establecerValor(self.variables[34].obtenerValor() + valorDeLaMoneda)
                                print ("Camino 4")
                            if listaDeResultados[indice][1] == 5:     # Se va hacia el camino 5
                                self.variables[35].establecerValor(self.variables[35].obtenerValor() + valorDeLaMoneda)
                                print ("Camino 5")


                        else: #Existe un  codigo de error
                            print ("########################################EXITE UN ERROR")
                            codigoDeError = listaDeResultados[i][1]
                            #print ("Leido ",listaDeResultados[i][0], listaDeResultados[i][1])
                            s += '{}-'.format(i)

                            if codigoDeError == 0:
                                s += 'Sin error '

                            if codigoDeError == 1:
                                s += 'Moneda rechazada'

                            if codigoDeError == 2:
                                s += 'Moneda inhibida'

                            if codigoDeError == 5:
                                s += 'timeout error en la validación de la moneda'

                            if codigoDeError == 6:
                                s += 'timeout en la salida'

                            if codigoDeError == 8:
                                s += 'Dos monedas pasaron simultaneamente'

                            if codigoDeError == 13:
                                s += 'Modulo del sensor no funciona correctamente'

                            if codigoDeError == 14:
                                s += 'Moneda atorada en el detector de salida'

                            if codigoDeError == 20:
                                s += 'Detector de cadena ha sido activado'

                            if codigoDeError == 23:
                                s += 'La maneda paso muy rapida a través del detector de salida'
                                
                            for n in range (1, 17):
                                if codigoDeError == 128 + n:
                                    s += 'Moneda {} inhibida por el registro de inhibicion'.format(n)

                            if codigoDeError == 254:
                                s += 'Mecanismo de reembolo activado'
                            
                            if codigoDeError == 255:
                                s += 'Código de error no especificado'

                            self.variables[40].establecerValor(codigoDeError)
                            self.variables[40].establecerValor_2(s)





            print (s)
            print (r[1], listaDeResultados)

    #TODO: Función no programada




    #TODO: A partir de aqui falta probar las funciones


    def modifyMasterInhibitStatus (self, args = None):
        print ("Imrpimiendo args", args)

        if args:
            if len(args) == 2:


                mensaje = [self.MODIFY_MASTER_INHIBIT_STATUS] + args[1:]
                r = self.enviarMensajeDispositivo(mensaje)

                if r:
                    print ("modifyMasterInhibitStatus ", r)

            else:
                print ("Argumentos inválidos")
        else:
            print ("No se proporcionaron argumentos")


    def requestMasterInhibitStatus (self, args = None):

        mensaje = [self.REQUEST_MASTER_INHIBIT_STATUS]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("requestMasterInhibitStatus ", r)

    def requestInsertionCounter (self, args = None):

        mensaje = [self.REQUEST_INSERTION_COUNTER]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("requestInsertionCounter ", r)

    def requestAcceptCounter (self, args = None):

        mensaje = [self.REQUEST_ACCEPT_COUNTER]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("requestAccept ", r)


    def modifySorterOverrideStatus (self, args = None):

        mensaje = [self.MODIFY_SORTER_OVERRIDE_STATUS]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("modifySorterOverrideStatus ", r)


    def requestSorterOverrideStatus (self, args = None):

        mensaje = [self.REQUEST_SORTER_OVERRIDE_STATUS]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("requestSorterOverrideStatus ", r)

    def modifySorterPaths (self, args = None):

        if args:
            if (len(args) >= 2) and (len(args) <= 6):

                moneda = args[0]


                mensaje = [self.MODIFY_SORTER_PATHS] + args[1:]
                r = self.enviarMensajeDispositivo(mensaje)

                if r:
                    print ("modifySorterPaths ", r)

            else:
                print ("Argumentos inválidos")
        else:
            print ("No se proporcionaron argumentos")


    def requestSorterPaths (self, args = None):
        if args:
            if len(args) == 2:

                mensaje = [self.REQUEST_SORTER_PATHS] + args[1:]
                r = self.enviarMensajeDispositivo(mensaje)

                if r:
                    print ("requestSorterPaths ", r)

                    if r[0] == 0x00:
                        print ("Instruccion recibida correctamente")

            else:
                print ("Argumentos inválidos")
        else:
            print ("No se proporcionaron argumentos")



    def resetDevice (self, args = None):

        mensaje = [self.RESET_DEVICE]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("resetDevice ", r)
            if r[0] == 0x00:
                print ("Se reseteo el dispositivo");




    def requestCoinId (self, args = None):

        if args:
            if len(args) == 2:

                mensaje = [self.REQUEST_COIN_ID] + args[1:]
                r = self.enviarMensajeDispositivo(mensaje)

                if r:
                    print ("requestCoinId ", r)

                    if r[0] == 0x00:
                        print ("Instruccion recibida correctamente", r[1:])

                    if r[0] == 0x05:
                        print ("Error")
            else:
                print ("Argumentos inválidos, verifique la sintasis de la instrucción")
        else:
            print ("No se proporcionaron argumentos")



    def teachModeControl (self, args = None):

        if args:
            if len(args) == 2:

                mensaje = [self.TEACH_MODE_CONTROL] + args[1:]
                r = self.enviarMensajeDispositivo(mensaje)

                if r:
                    print ("teachModeControl ", r)

                    if r[0] == 0x00:
                        print ("Instruccion recibida correctamente", r[1:])

                    if r[0] == 0x05:
                        print ("Error")
            else:
                print ("Argumentos inválidos, verifique la sintasis de la instrucción")
        else:
            print ("No se proporcionaron argumentos")



    def requestTeachStatus (self, args = None):

        mensaje = [self.REQUEST_TEACH_STATUS]
        r = self.enviarMensajeDispositivo(mensaje, tiempo = 0.05)

        s = ''
        if r:
            print ("requestTeachStatus ", r)
            if r[0] == 0x00:
                print ("Instucción recibida correctamente", r[1:]);

                if r[2] == 0xFC:
                    s += "Auto programación cancelada"


                if r[2] == 0xFD:
                    s += "Error en auto programación"


                if r[2] == 0xFE:
                    s += "Auto programación en proceso" + "{}".format(r[1])


                if r[2] == 0xFF:
                    s += "Auto programación terminada"

                print (s)






    def entregarMonedas (self, args = None):

        print ("Imrpimiendo args", args)

        if args:
            if len(args) == 2:


                mensaje = [self.ENTREGAR_MONEDAS] + args[1:]
                r = self.enviarMensajeDispositivo(mensaje, origen = 0x50)

                if r:
                    print ("entregarMonedas ", r)
                    if r[0] == 0x00:
                        print ("Se recibio respuesta");

            else:
                print ("Argumentos inválidos")
        else:
            print ("No se proporcionaron argumentos")





    def enableHopper(self, args = None):

        mensaje = [self.ENABLE_HOPPER, 0xA5]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("Imprimiendo r", r)
            if r[0] == 0x00:
                print ("Se habilito el hopper");


    def disableHopper(self, args = None):

        mensaje = [self.ENABLE_HOPPER, 0xA0]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            #print ("Imprimiendo r", r)
            if r[0] == 0x00:
                print ("Se deshabilito el hopper");



    def dispenseCoins(self, args = None):

        mensaje = [self.DISPENSE_COINS] + self.variables[6].obtenerValor() + args[1:]
        r = self.enviarMensajeDispositivo(mensaje)
        
        if r:
            if r[0] == 0x00:
                print ("*******Se dispensaron exitosamente las monedas", r)




    def emergencyStop(self, args = None):

        mensaje = [self.EMERGENCY_STOP]
        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            print ("Imprimiendo r", r)
            if r[0] == 0x00:
                print ("Se solicito un paro de emergencia el hopper");




    """
    Método utilizado para crear la instrucción que se envia a la tarjeta de interfaz
    """
    def enviarMensajeDispositivo (self, mensaje, **kwargs):

        tiempo = self.TIEMPO_DE_RETARDO_EN_LECTURA
        dispositivoOrigen = self.variables[0].obtenerValor()

        for key, value in kwargs.items():
            #print ("Imprimiendo el valor en modificar configuracion", key, value)
            
            if key == "tiempo":
                tiempo = value

            if key == "origen":
                dispositivoOrigen = value



        cctalkInstruccion = [dispositivoOrigen, len(mensaje) - 1, self.variables[3].obtenerValor()] + mensaje
        
        #print("Se enviara el mensaje ", cctalkInstruccion)

        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, cctalkInstruccion)
        #print ("Mensaje a enviar", a)

        self.puerto.escribir(a)
        
        time.sleep(tiempo)

        r = self.puerto.leer_2(50)

        if r:
            # Se obtienen unicamente los datos despues de recibir la validación
            #print("Se recibio la respuesta", r)
            r = self.verificarRespuesta(cctalkInstruccion, r)
        else:
            print("{}: No se recibio respuesta del puerto".format(self))
        return r

    """ 
    Verifica que los datos recibidos por medio del protocolo CCTALK esten correctos,
    si son correctos envia los datos contenidos en el protocolo, en caso contrario regresa 'false'
    """
    def verificarRespuesta(self, mensaje, respuesta):
        aux = 0
        datos = 0
        checksum = 0
        longitud = 0

        checksum_2 = 0

        if len(respuesta) > len(mensaje) +2:
            aux = respuesta[len(mensaje)+1:]        #Mensaje recibido del dispositivo
            datos = respuesta[len(mensaje)+1 +3:-1]  #Datos dentro del mensaje

            # parametros utilizados para validar la respuesta del protocolo CCTALK
            print ("Evaluando ", mensaje, respuesta)

            longitud = respuesta[len(mensaje)+1+1]
            checksum = respuesta[-1:]

            checksum_2 = self.comunicacion.checkSum_2(aux[0:-1])

            #print ("Imprimiendo aux", mensaje, aux, datos, checksum, longitud, "{0:02x}".format(checksum_2), len(aux))

            if longitud + 5 == len(aux):
                if checksum[0]==checksum_2:
                    #print ("La longitud y el checksum de la respuesta estan correctos")
                    return datos

        print ("{} - La longitud o el checksum recibidos no corresponden".format(self))
        return False

        

    #################################


    def instruccionImprimir (self, *args):
        print ("Se solicita imprimir {}".format(self))


    def ejecutarInstruccion(self, numero, *args):

        self.listaDeFunciones.append([numero] + [elemento for elemento in args])
        print ("\n---------------------------------EjecutarInstruccion->", self.listaDeFunciones[len(self.listaDeFunciones)-1], len(self.listaDeFunciones))

    def desencolarInstruccion(self):

        #print ("-----------------------------------------------------Dentro de validador_Desenconlando", len(self.listaDeFunciones))

        while len(self.listaDeFunciones)>0:
            print("Se imprime la lista de funciones VALIDADOR", len(self.listaDeFunciones))
            print ("Antes de desencolarInstrucción->", len(self.listaDeFunciones))
            funcion = self.listaDeFunciones.pop()
            print ("Despues de desencolarInstrucción->", len(self.listaDeFunciones))

            # Seleccion de instrucción

            if funcion[0] == self.SIMPLE_POLL:
                self.simplePoll(funcion)

            if funcion[0] == self.ADDRESS_POLL:
                self.addressPoll(funcion)

            if funcion[0] == self.REQUEST_POLLING_PRIORITY:
                self.requestPollingPriority(funcion)

            if funcion[0] == self.REQUEST_STATUS:
                self.requestStatus(funcion)

            if funcion[0] == self.REQUEST_MANUFACTURER_ID:
                self.requestManufacturerId(funcion)

            if funcion[0] == self.REQUEST_EQUIPMENT_CATEGORY_ID:
                self.requestEquipmentCategory(funcion)

            if funcion[0] == self.REQUEST_PRODUCT_CODE:
                self.requestProductCode(funcion)

            if funcion[0] == self.REQUEST_DATABASE_VERSION:
                self.requestDatabaseVersion(funcion)

            if funcion[0] == self.REQUEST_SERIAL_NUMBER:
                self.requestSerialNumber(funcion)

            if funcion[0] == self.REQUEST_SOFTWARE_VERSION:
                self.requestSoftwareVersion(funcion)

            if funcion[0] == self.TEST_SOLENOIDS:
                self.testSolenoids(funcion)

            if funcion[0] == self.READ_INPUT_LINES:
                self.readInputLines(funcion)

            if funcion[0] == self.READ_OPTO_STATES:
                self.readOptoStates(funcion)

            if funcion[0] == self.PERFORM_SELF_CHECK:
                self.performSelfCheck(funcion)

            if funcion[0] == self.MODIFY_INHIBIT_STATUS:
                self.modifyInhibitStatus(funcion)

            if funcion[0] == self.REQUEST_INHIBIT_STATUS:
                self.requestInhibitStatus(funcion)

            if funcion[0] == self.READ_BUFFERED_CREDIT_OR_ERROR_CODES:
                self.readBufferedCreditOrErrorCodes(funcion)
            
            #TODO: A partir de aqui falta probar las funciones

            if funcion[0] == self.MODIFY_MASTER_INHIBIT_STATUS:
                self.modifyMasterInhibitStatus(funcion)

            if funcion[0] == self.REQUEST_MASTER_INHIBIT_STATUS:
                self.requestMasterInhibitStatus(funcion)

            if funcion[0] == self.REQUEST_INSERTION_COUNTER:
                self.requestInsertionCounter(funcion)

            if funcion[0] == self.REQUEST_ACCEPT_COUNTER:
                self.requestAcceptCounter(funcion)

            if funcion[0] == self.MODIFY_SORTER_OVERRIDE_STATUS:
                self.modifySorterOverrideStatus(funcion)

            if funcion[0] == self.REQUEST_SORTER_OVERRIDE_STATUS:
                self.requestSorterOverrideStatus(funcion)





            if funcion[0] == self.MODIFY_SORTER_PATHS:
                self.modifySorterPaths(funcion)

            if funcion[0] == self.REQUEST_SORTER_PATHS:
                self.requestSorterPaths(funcion)



            if funcion[0] == self.RESET_DEVICE:
                self.resetDevice(funcion)

            if funcion[0] == self.REQUEST_COIN_ID:
                self.requestCoinId(funcion)



            if funcion[0] == self.REQUEST_TEACH_STATUS:
                self.requestTeachStatus(funcion)

            if funcion[0] == self.TEACH_MODE_CONTROL:
                self.teachModeControl(funcion)



            if funcion[0] == self.ENTREGAR_MONEDAS:
                self.entregarMonedas(funcion)


            if funcion[0] == self.IMPRIMIR:
                self.instruccionImprimir(funcion)



    def __str__ (self):
        return "%s " %(self.obtenerNombre())





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
    validador = Validador("Validador 1", "VAL-001", "validador", direccion  = 2)
    validador.establecerPuerto (puerto)
    validador.establecerComunicacion (comunicacion)
    
    
    time.sleep(0.5)

    validador.ejecutarInstruccion (Validador.REQUEST_STATUS)
    validador.desencolarInstruccion()    
    
    time.sleep(0.5)
    
    validador.ejecutarInstruccion (Validador.RESET_DEVICE)
    validador.desencolarInstruccion()    

    time.sleep(0.5)
    
    validador.ejecutarInstruccion (Validador.SIMPLE_POLL)
    validador.desencolarInstruccion()

    time.sleep(0.5)
    
    validador.ejecutarInstruccion (Validador.REQUEST_MANUFACTURER_ID)
    validador.desencolarInstruccion()   

    time.sleep(0.5)
    
    validador.ejecutarInstruccion (Validador.REQUEST_PRODUCT_CODE)
    validador.desencolarInstruccion()   

    time.sleep(0.5)
    
    validador.ejecutarInstruccion (Validador.REQUEST_SERIAL_NUMBER)
    validador.desencolarInstruccion()   

    time.sleep(1)
    
    validador.ejecutarInstruccion (Validador.MODIFY_INHIBIT_STATUS)
    validador.desencolarInstruccion()   

    time.sleep(1)

    for i in range(0, 15):

        
        validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, i)
        validador.desencolarInstruccion()
        print ("Numero ->", i, end=" ")
        time.sleep(1)

    time.sleep(100)

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 1,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 2,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 3,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 4,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 5,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 6,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 7,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 8,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 9,  4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 10, 4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 11, 4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 12, 4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 13, 4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 14, 4, 3, 2, 1)
    validador.desencolarInstruccion()

    validador.ejecutarInstruccion (Validador.MODIFY_SORTER_PATHS, 15, 5)
    validador.desencolarInstruccion()

    time.sleep(1)

    print ("*********")

    validador.ejecutarInstruccion (Validador.MODIFY_MASTER_INHIBIT_STATUS, 1)
    validador.desencolarInstruccion()

    time.sleep(1)

    
    validador.ejecutarInstruccion (Validador.ENTREGAR_MONEDAS, 2)
    validador.desencolarInstruccion()  


    while (True):
        validador.ejecutarInstruccion (Validador.READ_BUFFERED_CREDIT_OR_ERROR_CODES)
        validador.desencolarInstruccion()
        time.sleep(0.1)


    time.sleep(2)
    

    #validador.ejecutarInstruccion (Validador.ENTREGAR_MONEDAS, 2)
    #validador.desencolarInstruccion()  



    """

    

    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 1)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 2)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 3)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 4)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 5)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 6)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 7)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 8)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 9)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 10)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 11)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 12)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 13)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 14)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 15)
    validador.desencolarInstruccion()
    validador.ejecutarInstruccion (Validador.REQUEST_COIN_ID, 16)
    validador.desencolarInstruccion()



    
    #validador.ejecutarInstruccion (Validador.TEACH_MODE_CONTROL, 15)
    #validador.desencolarInstruccion()
    
    
    while (True) :

        validador.ejecutarInstruccion (Validador.REQUEST_TEACH_STATUS)
        validador.desencolarInstruccion()

        time.sleep(1)
    """
    


    
    puerto.cerrarPuerto()
    puerto.detenerHilo()
    

if __name__ == "__main__":
    main()
