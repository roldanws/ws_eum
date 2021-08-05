__author__ = "Sigfrido"
__date__ = "$5/12/2019 04:33:30 PM$"

import sys
import os
import time

ruta = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta)

from PuertoSerie import PuertoSerie
from Comunicacion import Comunicacion

ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(ruta)

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador


class Monedero (Variable):
    
    IMPRIMIR = 0x0E


    DAR_CAMBIO = b'\xFD'
    HABILITAR = b'\xFC'
    DESHABILITAR = b'\xFB'

    DISPENSAR_MONEDAS = b'\xFA'


    #TIEMPO_DE_RETARDO_EN_LECTURA = 0.025


    factorDeEscala = .10


    # tipoMoneda == 2 => 1 peso
    # tipoMoneda == 3 => 2 pesos
    # tipoMoneda == 4 => 5 pesos
    # tipoMoneda == 5 => 10 pesos



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
        
        self.variables[0]=Variable("X_00", "Fabricante", "Nombre del fabricante")
        self.variables[1]=Variable("X_01", "Modelo", "")
        self.variables[2]=Variable("X_02", "Número de Serie", "Número de serie")
        self.variables[3]=Variable("X_03", "Versión de Software", "")
        self.variables[4]=Variable("X_04", "", "")
        self.variables[5]=Variable("X_05", "Estado actual del Monedero", "")
        self.variables[6]=Variable("X_06", "", "")
        self.variables[7]=Variable("X_07", "", "")

        self.variables[8]=Variable("X_08", "Valor de moneda en tubo 1", "")
        self.variables[9]=Variable("X_09", "Cantidad de monedas en tubo 1", "")
        self.variables[10]=Variable("X_10", "Cuenta de Monedas software 1", "")

        self.variables[11]=Variable("X_11", "Valor de moneda en tubo 2", "")
        self.variables[12]=Variable("X_12", "Cantidad de monedas en tubo 2", "")
        self.variables[13]=Variable("X_13", "Cuenta de Monedas software 2", "")

        self.variables[14]=Variable("X_14", "Valor de moneda en tubo 3", "")
        self.variables[15]=Variable("X_15", "Cantidad de monedas en tubo 3", "")
        self.variables[16]=Variable("X_16", "Cuenta de Monedas software 3", "")

        self.variables[17]=Variable("X_17", "Valor de moneda en tubo 4", "")
        self.variables[18]=Variable("X_18", "Cantidad de monedas en tubo 4", "")
        self.variables[19]=Variable("X_19", "Cuenta de Monedas software 4", "")

        self.variables[20]=Variable("X_20", "Valor de moneda en tubo 5", "")
        self.variables[21]=Variable("X_21", "Cantidad de monedas en tubo 5", "")
        self.variables[22]=Variable("X_22", "Cuenta de Monedas software 5", "")

        self.variables[23]=Variable("X_23", "", "")
        self.variables[24]=Variable("X_24", "", "")
        self.variables[25]=Variable("X_25", "", "")
        self.variables[26]=Variable("X_26", "", "")
        self.variables[27]=Variable("X_27", "", "")
        self.variables[28]=Variable("X_28", "", "")
        self.variables[29]=Variable("X_29", "", "")
        self.variables[30]=Variable("X_30", "", "")
        self.variables[31]=Variable("X_31", "", "")
        self.variables[32]=Variable("X_32", "", "")

        self.variables[33]=Variable("X_33", "Error", "")
        self.variables[34]=Variable("X_34", "Error en módulo discriminador", "")
        self.variables[35]=Variable("X_35", "Error en módulo de aceptación", "")
        self.variables[36]=Variable("X_36", "Error en modulo separador", "")
        self.variables[37]=Variable("X_37", "Error en módulo dispensador", "")
        self.variables[38]=Variable("X_38", "Error en cassette", "")


        self.variables[8].establecerValor(0) # Valor de la moneda
        self.variables[11].establecerValor(1) # Valor de la moneda
        self.variables[14].establecerValor(2) # Valor de la moneda
        self.variables[17].establecerValor(5) # Valor de la moneda
        self.variables[20].establecerValor(10) # Valor de la moneda


        self.TON = []

        self.TON.append( Temporizador("TON_00",3)) # 15 segundos
        self.TON.append( Temporizador("TON_01",3)) # 15 segundos
        self.TON.append( Temporizador("TON_02",3)) # 15 segundos
        self.TON.append( Temporizador("TON_03",1)) # 15 segundos
        self.TON.append( Temporizador("TON_04",1)) # 15 segundos
        self.TON.append( Temporizador("TON_05",1)) # 15 segundos
        self.TON.append( Temporizador("TON_06",1)) # 15 segundos
        self.TON.append( Temporizador("TON_07",1)) # 15 segundos
        self.TON.append( Temporizador("TON_08",1)) # 15 segundos
        self.TON.append( Temporizador("TON_09",1)) # 15 segundos

        self.TON.append(Temporizador("TON[10]",0.22))
        self.TON[10].entrada = True
        self.TON[10].actualizar()


        self.configurarDispositivo (**kwargs)
        self.actualizar()

        print ("\n->Se ha configurado el {}".format(self))
    
    def establecerPuerto (self, puerto):
        self.puerto = puerto

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


    def actualizar (self):
        # Método utlizado para actualizar banderas de señales de error
        ######
        if self.RC[33] & ~self.M[33]:
            self.variables[33].establecerValor(0)
            self.variables[33].establecerValor_2("")

        self.RC[33] = self.M[33]
        self.M[33] = 0

        ######
        if self.RC[34] & ~self.M[34]:
            self.variables[34].establecerValor(0)
            self.variables[34].establecerValor_2("")

        self.RC[34] = self.M[34]
        self.M[34] = 0

        ######
        if self.RC[35] & ~self.M[35]:
            self.variables[35].establecerValor(0)
            self.variables[35].establecerValor_2("")

        self.RC[35] = self.M[35]
        self.M[35] = 0

        ######
        if self.RC[36] & ~self.M[36]:
            self.variables[36].establecerValor(0)
            self.variables[36].establecerValor_2("")

        self.RC[36] = self.M[36]
        self.M[36] = 0

        ######
        if self.RC[37] & ~self.M[37]:
            self.variables[37].establecerValor(0)
            self.variables[37].establecerValor_2("")

        self.RC[37] = self.M[37]
        self.M[37] = 0

        ######
        if self.RC[38] & ~self.M[38]:
            self.variables[38].establecerValor(0)
            self.variables[38].establecerValor_2("")

        self.RC[38] = self.M[38]
        self.M[38] = 0
  


    def status(self):
        self.estatusTubos()
        self.estatusEquipo()
        self.poll()
        self.actualizar()
        pass





    ######################################################################################################
    ##################################### Inicio de métodos del monedero #################################


    def inicializacion(self):
        #print ("Dentro de inicializacion del monedero", end=" ",flush=True)

        if not self.equipoInicializado:
            print ("Inicializando {}".format(self), end=" ",flush=True)

            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x08, 1])

            
            
            self.puerto.write(a)
            time.sleep(0.05)
            r = self.puerto.read(1)
            print("RE,",r)
            if r:
                if len(r) > 1:
                    #TODO: Enviar mensaje de falta de alimentación en la tarjeta controladora y generar bandera de falla
                    pass
                else:

                    if (r[0] == 0):
                        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x0F, 1, 0x00, 0])  # Instrucción de identificación
                        print (a)
                        self.puerto.write(a)
                        time.sleep(0.05)
                        r = self.puerto.read(34)  # Verificar en el simulador se ve que devuelve 34
                        self.verficarTramaDeDatos(r)

                        print(r)

                        if (r[0] == 77):  # Verificar la respuesta (4D = M, 45 = E, 49 = I) <----------
                            """
                            self.puerto.parity = change_parity(0x00, 0)
                            self.puerto.write(b'\x00')  # Devuelve ACK
                            """
                            #Rellenar datos del Dispositivo
                            self.variables[0].establecerValor(r[0:3].decode('utf-8'))
                            self.variables[2].establecerValor(r[3:15].decode('utf-8'))
                            self.variables[1].establecerValor(r[15:27].decode('utf-8'))
                            self.variables[3].establecerValor(r[27:29])


                            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0X00, 0])
                            self.puerto.write(a)


                            self.disable_coin()
                            cont=0


                            while(1):

                                r = self.estatusEquipo()

                                if(r):
                                    print("rrrrr__:",r)
                                    if(cont==2):
                                        print("LISTO!---")
                                        break
                                    else:
                                        cont=cont+1
                                        print("DESHINIBIENDO!---",cont)
                                        self.enable_coin()
                                        #time.sleep(2)

            else:
                print ("{} - No se recibio respuesta, posiblemente a que no este conectado el dispositivo".format(self))

        self.puerto.flushInput()
        self.equipoInicializado = True
        #hacerPoleo()
        #print ("Fin de la rutina de inicialización del monedero")

    def enable_coin(self):
        mona=0X3C#  60 # 0011 1100
        mond=0X3C#  60 # 0011 1100

        print("vals...>>>",mona,mond)

        while (1):

            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0X0C, 1, 0x00, 0, mona, 0, 0x00, 0, mond, 0]) # Instrucción de habilitacion/Deshabilitación
            self.puerto.write(a)
            time.sleep(.01)
            #time.sleep(.05)
            r = self.puerto.read(1)
            print(r)
            if(r):
                if (r[0] == 0):  # Verificar la respuesta <----------
                    print("Habilitacion de Monedas Exitosa")
                    time.sleep(.005)
                    return r
                    break

    def disable_coin(self):
        while (1):
            print("Deshabilitando Monedero...")
            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0X0C, 1, 0X00, 0, 0X00, 0, 0X00, 0, 0X00, 0]) # Instrucción de habilitacion/Deshabilitación
            
            self.puerto.write(a)
            time.sleep(.025)
            r = self.puerto.read(1)
            print(r)

            if(r):
                if (r[0] == 0X00):  # Verificar la respuesta <----------
                    print("Deshabilitacion de Monedas Exitosa")
                    time.sleep(.005)
                    break


    def dispensarMonedas(self, args):

        print ("Imprimiendo >>{}<< ".format (args))

        if len(args) == 3: # Solo se esta pasando un argumento
            numeroDeMonedas = args[1]
            tipoDeMoneda  = args[2]
            numero = 0

            print ("Se dispensaran {} de {}".format(numeroDeMonedas, tipoDeMoneda))

            if numeroDeMonedas <= 15:
                if tipoDeMoneda <= 15:
            
                    numero = ((numeroDeMonedas & 0x0f) << 4 )| tipoDeMoneda & 0x0f
                    print ("Imprimiendo el numero a enviar ", "{0:02x}".format(numero))

                    a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x0D, 1, numero, 0])
                    self.puerto.write(a)
                    time.sleep(.01)

    def darCambio(self, args = None):

        print ("Imprimiendo >>{}<< ".format (args))

        if len(args) == 2: # Solo se esta pasando un argumento
            monto =  args[1]
            print ("Se dará cambio de ", monto)

            dar=monto/self.factorDeEscala

            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x0F, 1, 0x02, 0, int(dar), 0])
            self.puerto.write(a)
            time.sleep(.01)

            r = self.puerto.read(10)
            time.sleep(.01)
            if  r:
                print ("Respuesta recibida", r)
                


    def estatusTubos(self):
        
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x0A, 1])
        self.puerto.write(a)
        time.sleep(.030)
        r = self.puerto.read(19) #Verificar en el simulador se ven 19
        r = self.verficarTramaDeDatos(r)
        #print("estatusTubos",r, len(r))
        
        if r:
            if len(r)>18:

                self.variables[12].establecerValor(str(r[4]))  # Cantidad de monedas en tubo de moneda tipo 2
                self.variables[15].establecerValor(str(r[5])) # Cantidad de monedas en tubo de moneda tipo 3
                self.variables[18].establecerValor(str(r[6])) # Cantidad de monedas en tubo de moneda tipo 4
                self.variables[21].establecerValor(str(r[7])) # Cantidad de monedas en tubo de moneda tipo 5

                a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0x00, 0])
                self.puerto.write(a)

    def estatusEquipo(self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0X0F, 1, 0X05, 0]) # Instrucción de estado de operación
        self.puerto.write(a)
        time.sleep(.02)
        r = self.puerto.read(3)
        self.verficarTramaDeDatos(r)

        # Lectura de estados del dispositivo

        s = ""
        if r:
            if r[0] == 0x01:
                if r[1] == 0x00:
                    s += "Energizandose"
            if r[0] == 0x02:
                if r[1] == 0x00:
                    s += "Apagandose"
            if r[0] == 0x03:
                if r[1] == 0x00:
                    s += "OK"
            if r[0] == 0x04:
                if r[1] == 0x00:
                    s += "Keypad presionado"
            if r[0] == 0x05:
                if r[1] == 0x10:
                    s += "Llenado manual/pago en proceso"
                if r[1] == 0x20:
                    s += "nueva información disponible"
            if r[0] == 0x06:
                if r[1] == 0x00:
                    s += "Inhibido"
            if r[0] == 0x10:
                s += "Error general del monedero -"
                self.M[33] = 1
                if r[1] == 0x00:
                    s += "Error no especificado"
                if r[1] == 0x01:
                    s += "CheckSum error #1"
                if r[1] == 0x02:
                    s += "CheckSum error #2"
                if r[1] == 0x03:
                    s += "Bajo voltaje en la alimentación"

                self.variables[33].establecerValor(1)
                self.variables[33].establecerValor_2(s)


            if r[0] == 0x11:
                s += "Modulo discriminador - "
                self.M[34] = 1
                if r[1] == 0x00:
                    s += "Error no especificado"
                if r[1] == 0x10:
                    s += "Cubierta de la alimentación de monedas abierta"
                if r[1] == 0x11:
                    s += "deposito retorno abierto"
                if r[1] == 0x30:
                    s += "Moneda atorada en la alimentacion"
                if r[1] == 0x50:
                    s += "Sensor de validación A fuera de rango"
                if r[1] == 0x51:
                    s += "Sensor de validación B fuera de rango"
                if r[1] == 0x52:
                    s += "Sensor de validación C fuera de rango"
                if r[1] == 0x53:
                    s += "Temperatura de operación excedida"
                if r[1] == 0x54:
                    s += "Error en la lectura de las mediciones opticas"

                self.variables[34].establecerValor(1)
                self.variables[34].establecerValor_2(s)


            if r[0] == 0x12:
                s += "Módulo de aceptación - "
                self.M[35] = 1
                if r[1] == 0x00:
                    s += "Error no especificado"
                if r[1] == 0x30:
                    s += "Entraron monesas a la compuerta pero no salieron"
                if r[1] == 0x31:
                    s += "alarma de la compuerta de aceptacion activa"
                if r[1] == 0x40:
                    s += "Compuerta de aceptación abierta, pero no se detecto moneda"
                if r[1] == 0x50:
                    s += "Sensor en la compuerta trasera cubierto"

                self.variables[35].establecerValor(1)
                self.variables[35].establecerValor_2(s)


            if r[0] == 0x13:
                s += "Módulo de separador - "
                self.M[36] = 1
                if r[1] == 0x00:
                    s += "Error no especificado"
                if r[1] == 0x10:
                    s += "Error en el sensor de ordenación"
                self.variables[36].establecerValor(1)
                self.variables[36].establecerValor_2(s)

            if r[0] == 0x14:
                s += "Módulo de dispensador - "
                self.M[37] = 1
                if r[1] == 0x00:
                    s += "Error no especificado"
                self.variables[37].establecerValor(1)
                self.variables[37].establecerValor_2(s)

            if r[0] == 0x15:
                s += "Cassete - "
                self.M[38] = 1

                if r[1] == 0x00:
                    s += "Error No especificado"
                if r[1] == 0x02:
                    s += "retirado"
                if r[1] == 0x03:
                    s += "error en la caja de cambio"
                if r[1] == 0x04:
                    s += "error incide mucha luz en los sensores de los tubos"
                self.variables[38].establecerValor(1)
                self.variables[38].establecerValor_2(s)
                #self.variables[38].actualizarInterfaz()

            #print (s)
        return (r)



    def poll(self):
        ruta = 0
        tipoDeMoneda = 0
        cantidadDeMonedasEnTubo = 0

        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x0B, 1])
        self.puerto.write(a)
        time.sleep(.015)
        r = self.puerto.read(6)
        self.verficarTramaDeDatos(r)

        print("mo",r)
        if(r):
            

            # Metodo para determinar las monedas
            if ((r[0] >> 7) == 1):# monedas dispensadas manualmente
                print ("Se dispenso una moneda")
                #print (0x0F&r[0])
            elif ((r[0] >> 6) == 1):# monedas depositadas manualmente
                a = (r[0]>> 4) & 0x03
                print ("Se depositó una moneda",  "{0:08b}".format(r[0]), "{0:03d}".format((r[0]>>4) & 0x03), "{0:03d}".format((r[0] & 0x0f)), "{0:03d}".format(r[1]))

                rutaTubos = (r[0]>>4) & 0x03
                tipoMoneda = r[0] & 0x0f
                cantidadDeMonedasEnTubo = r[1]
                valorMoneda =0 

                s = ""
                if rutaTubos == 0:
                    s = "ruta: Caja"
                elif rutaTubos == 1:
                    s = "ruta: Tubos"
                elif rutaTubos == 2:
                    s = "ruta: Sin uso"
                elif rutaTubos == 3:
                    s = "ruta: Retornada"

                print("Se procesa y se envia respuesta", s, tipoMoneda, cantidadDeMonedasEnTubo)
                a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0x00, 0])
                self.puerto.write(a)



                    #monedas[0]=monedas[0]+1
                    #monedasPago[0]=monedasPago[0]+1

                if (tipoMoneda == 2): #1 peso
                    valorMoneda=self.variables[11].obtenerValor()
                    self.variables[13].establecerValor(self.variables[13].obtenerValor()+1)
                    #valorMoneda = 2
                    #monedas[1]=monedas[1]+1
                    #monedasPago[1]=monedasPago[1]+1

                if (tipoMoneda == 3): #2 pesos
                    valorMoneda=self.variables[14].obtenerValor()
                    self.variables[16].establecerValor(self.variables[16].obtenerValor()+1)
                    #valorMoneda = 5
                    #monedas[2]=monedas[2]+1
                    #monedasPago[2]=monedasPago[2]+1

                if (tipoMoneda == 4): #5 pesos
                    valorMoneda=self.variables[17].obtenerValor()
                    self.variables[19].establecerValor(self.variables[19].obtenerValor()+1)
                    #valorMoneda = 10
                    #monedas[3]=monedas[3]+1
                    #monedasPago[3]=monedasPago[3]+1

                if(tipoMoneda==5): #10 pesos
                    valorMoneda=self.variables[20].obtenerValor()
                    self.variables[22].establecerValor(self.variables[22].obtenerValor()+1)

                print("Moneda insertada: ",valorMoneda)

                """

                #cambiaColor=1
                #print("Monedas en tubo: ",r2)
                total=total+valorMoneda
                dineroTotal=dineroTotal+valorMoneda
                monedasTotal=monedasTotal+1
                print("Monto actual: ",total)

                """



            elif (r[0] > 0 and r[0]<=0x0F):# señal de estatus
                print ("*****************************************", r[0])

                status = ""
                if(r[0]==1):
                    status="Escrow request --- 1"
                if(r[0]==2):
                    status="Entregaando cambio : "#+str(aux_cambio)
                if(r[0]==3):
                    status="No credit --- 3"
                if(r[0]==4):
                    status="Defective tube sensor --- 4"
                if(r[0]==5):
                    status="Double arrival --- 5"
                if(r[0]==6):
                    status="Aceptor unplugged --- 6"
                if(r[0]==7):
                    status="Tube Jam --- 7"
                if(r[0]==8):
                    status="Checksum Error --- 8"
                if(r[0]==9):
                    status="Coin routing Error --- 9"
                if(r[0]==10):
                    status="Changer Busy --- 10"
                if(r[0]==11):
                    status="El monedero fue reseteado"
                if(r[0]==12):
                    status="Coin Jam in the acceptance path --- 12"
                if(r[0]==13):
                    status="Posible credited coin removal --- 13"

                print(status,"\n*************************************")

                a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0x00, 0])
                self.puerto.write(a)


    def verficarTramaDeDatos(self, r):
        if r:

            if r[0]==0x00:  #Recibio una respuesta correcta
                pass
            
            elif r[-1]!=self.comunicacion.checkSum(r[:-1]):
                print ("{} - La longitud o el checksum recibidos no corresponden".format(self), r[-1])
                return False
        return r

    #################################


    def instruccionImprimir (self, *args):
        print ("Se solicita imprimir {}".format(self))

    def ejecutarInstruccion(self, numero, *args):
        
        self.listaDeFunciones.append([numero] + [elemento for elemento in args])
        print ("EjecutarInstruccion->", self.listaDeFunciones[len(self.listaDeFunciones)-1])

    def desencolarInstruccion(self):
        while len(self.listaDeFunciones)>0:
            #print("Se imprime la lista de funciones", len(self.listaDeFunciones))
            print ("Antes de desencolarInstrucción->", len(self.listaDeFunciones))
            funcion = self.listaDeFunciones.pop()
            print ("Despues de desencolarInstrucción->", len(self.listaDeFunciones))

            # Seleccion de instrucción
            if funcion[0] == self.IMPRIMIR:
                self.instruccionImprimir(funcion)

            if funcion[0] == self.DAR_CAMBIO:
                self.darCambio(funcion)

            if funcion[0] == self.DISPENSAR_MONEDAS:
                self.dispensarMonedas(funcion)

            if funcion[0] == self.HABILITAR:
                self.enable_coin()

            if funcion[0] == self.DESHABILITAR:
                self.disable_coin()


    ####################################### Fin de métodos del monedero ##################################
    ######################################################################################################



    def imprimirArreglo(self, r):
        s = ""
        for i in r:
            s += "{}".format(i).rjust(3)
        return s



    def __str__ (self):
        return "%s" %(self.obtenerNombre())
    
def main ():
    
    
    puerto = PuertoSerie("Puerto Serie")
    print ("Imprimiendo Arduino", PuertoSerie.ARDUINO_MICRO)
    puerto.modificarConfiguracion(dispositivo = PuertoSerie.ARDUINO_MICRO)
    #puerto.start()
    puerto.abrirPuerto()
    
    comunicacion = Comunicacion ()
    variablesMicro = VariablesMicro()
    
    # Se crea y se configura el dispositivo
    monedero1 = Monedero("Monedero 1", "MON-001", "En cajero")
    monedero1.establecerPuerto (puerto)
    monedero1.establecerComunicacion (comunicacion)

    
    time.sleep(4)
    

    
    
    time.sleep(4)
    
    puerto.cerrarPuerto()
    puerto.detenerHilo()
    

if __name__ == "__main__":
    main()