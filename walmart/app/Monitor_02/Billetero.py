__author__ = "PRUEBA"
__date__ = "$5/12/2019 06:42:58 PM$"

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



class Billetero (Variable):
    
    BILLETERO_IMPRIMIR = b'\xAE'

    BILLETERO_HABILITAR = b'\xAC'
    BILLETERO_DESHABILITAR = b'\xAB'


    def __init__(self, tag, nombre, descripcion, **kwargs):
        Variable.__init__ (self, tag = tag, nombre = nombre, descripcion = descripcion)
        
        self.configurarDispositivo (**kwargs)

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
        self.variables[5]=Variable("X_05", "Estado actual del Billetero", "")
        self.variables[6]=Variable("X_06", "", "")
        self.variables[7]=Variable("X_07", "", "")

        self.variables[8]=Variable("X_08", "", "")
        self.variables[9]=Variable("X_09", "", "")
        self.variables[10]=Variable("X_10", "", "")
        self.variables[11]=Variable("X_11", "", "")
        self.variables[12]=Variable("X_12", "", "")
        self.variables[13]=Variable("X_13", "", "")
        self.variables[14]=Variable("X_14", "", "")
        self.variables[15]=Variable("X_15", "", "")
        self.variables[16]=Variable("X_16", "", "")
        self.variables[17]=Variable("X_17", "", "")
        self.variables[18]=Variable("X_18", "", "")
        self.variables[19]=Variable("X_19", "", "")
        self.variables[20]=Variable("X_20", "", "")
        self.variables[21]=Variable("X_21", "", "")
        self.variables[22]=Variable("X_22", "", "")
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
        self.variables[33]=Variable("X_33", "", "")
        self.variables[34]=Variable("X_34", "", "")
        self.variables[35]=Variable("X_35", "", "")
        self.variables[36]=Variable("X_36", "", "")
        self.variables[37]=Variable("X_37", "", "")
        self.variables[38]=Variable("X_38", "", "")
        self.variables[39]=Variable("X_39", "", "")
        self.variables[40]=Variable("X_40", "", "")
        self.variables[41]=Variable("X_41", "", "")
        self.variables[42]=Variable("X_42", "", "")
        self.variables[43]=Variable("X_43", "", "")
        self.variables[44]=Variable("X_44", "", "")
        self.variables[45]=Variable("X_45", "", "")
        self.variables[46]=Variable("X_46", "", "")
        self.variables[47]=Variable("X_47", "", "")
        self.variables[48]=Variable("X_48", "", "")
        self.variables[49]=Variable("X_49", "", "")
        self.variables[50]=Variable("X_50", "", "")
        self.variables[51]=Variable("X_51", "", "")
        self.variables[52]=Variable("X_52", "", "")
        self.variables[53]=Variable("X_53", "", "")
        self.variables[54]=Variable("X_54", "", "")
        self.variables[55]=Variable("X_55", "", "")
        self.variables[56]=Variable("X_56", "", "")
        self.variables[57]=Variable("X_57", "", "")
        self.variables[58]=Variable("X_58", "", "")
        self.variables[59]=Variable("X_59", "", "")
        self.variables[60]=Variable("X_60", "", "")
        self.variables[61]=Variable("X_61", "", "")
        self.variables[62]=Variable("X_62", "", "")
        self.variables[63]=Variable("X_63", "", "")
        self.variables[64]=Variable("X_64", "", "")
        self.variables[65]=Variable("X_65", "", "")
        self.variables[66]=Variable("X_66", "", "")
        self.variables[67]=Variable("X_67", "", "")
        self.variables[68]=Variable("X_68", "", "")
        self.variables[69]=Variable("X_69", "", "")

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
        pass

    def ack(self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0x00, 0])
        self.puerto.write(a)

    def reset(self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x30, 1])
        self.puerto.write(a)

        time.sleep(0.05)
        r = self.puerto.read(1)
        
        print("RE,",r)
        r = self.verficarTramaDeDatos(r)

        return r

  
    def poll(self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x33, 1])
        self.puerto.write(a)
        time.sleep(.015)

        r = self.puerto.read(20)
        self.verficarTramaDeDatos(r)

        
        if r:
            print("bi",r)

            if len(r) > 1:
                print("bi",r, "{0:08b}".format(r[0]), "{0:08b}".format(r[1]))

                if ((r[0] >> 7) == 1):# Se esta aceptando un billete
                    rutaBilletero = (r[0]>>4) & 0x07
                    tipoBillete = r[0] & 0x0f

                    s = ""
                    if rutaBilletero == 0:
                        s += "Billete apilado"
                    if rutaBilletero == 1:
                        s += "Billete en la posición del deposito"
                    if rutaBilletero == 2:
                        s += "Billete regresado"
                    if rutaBilletero == 3:
                        s += "Billete en el reciclador"
                    if rutaBilletero == 4:
                        s += "Billete rechazado "
                    if rutaBilletero == 5:
                        s += "Billete del reciclador al llenado manua"
                    if rutaBilletero == 6:
                        s += "Dispensado manualmente"
                    if rutaBilletero == 7:
                        s += "Trabsferido del reciclador a la caja de cambio"


                    t = ""
                    if tipoBillete == 0:
                        t += "20"
                    if tipoBillete == 1:
                        t += "50"
                    if tipoBillete == 2:
                        t += "100"
                    if tipoBillete == 3:
                        t += "200"
                    if tipoBillete == 4:
                        t += "500"

                    print ("**************************En etapa de aceptación -> Billete de {} {}".format(t, s), tipoBillete, rutaBilletero, "\n****************")

                    self.ack()
                    self.accept_sequence()
                    #self.escrow()

                elif (r[0] > 0 and r[0]<=0x0F):# señal de estatus
                    print ("*****************************************", r[0])
                    if(r[0]==1):
                        status="Error en motor"
                    if(r[0]==2):
                        status="Problema en sensor"
                    if(r[0]==3):
                        status="Billetero ocupado"
                    if(r[0]==4):
                        status="Checksum incorrecto"
                    if(r[0]==5):
                        status="Billete atorado"
                    if(r[0]==6):
                        status="Billetero reseteado"
                    if(r[0]==7):
                        status="Billete regresado"
                    if(r[0]==8):
                        status="Caja de cambio fuera de posición"
                    if(r[0]==9):
                        status="Billetero deshabilitado"
                    if(r[0]==10):
                        status="Respuesta inválida debido a una operación en el Escrow"
                    if(r[0]==11):
                        status="Billete rechazado"
                    if(r[0]==12):
                        status="Billete posiblemente removido"

                    print(status,"\n*************************************")
                    self.ack()
        pass



    def accept_sequence(self):
        #global tiempoBillExc,tiempoLimBill
        estado = 1 	  	
        
        while estado < 2:
            time.sleep(.09)
            #Aceptar billete (Stack) (enviarlo hacia atras)
            if estado==1:
                """
                ser.parity = change_parity(0x35, 1)
                ser.write(b'\x35')
                ser.parity = change_parity(0x01, 0)
                ser.write(b'\x01')
                ser.parity = change_parity(0x36, 0)
                ser.write(b'\x36')
                """

                a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x35, 1, 0x01, 0])
                self.puerto.write(a);
                time.sleep(.01)

                r = self.puerto.read(10)
                print("1: ",r)

                print ("En estado 1")
                time.sleep(.005)
                if(r==b'\x00'):
                    estado=2
            #Preguntar por estado del billete (Poll)
                


    def billTypeEnable(self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x34, 1, 0x00, 0, 0x07, 0, 0x00, 0, 0x07, 0])
        self.puerto.write(a)
        time.sleep(.01)

        r = self.puerto.read(3)
        print("RE,",r)

        if r: # Se recibio respuesta del billetero
            if r[0] == 0x00:
                print ("Se recibio respuesta")
        return r

    def billTypeDisable(self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x34, 1, 0x00, 0, 0x00, 0, 0x00, 0, 0x00, 0])
        self.puerto.write(a)
        time.sleep(.01)

        r = self.puerto.read(3)
        print("RE,",r)

        if r: # Se recibio respuesta del billetero
            if r[0] == 0x00:
                print ("Se recibio respuesta")
        return r
    
    def escrow (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x35, 1, 0x01, 0])
        print ("Verificar el estado de la pila", a)
        self.puerto.write(a)
        time.sleep(.015)

        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0x00, 0])
        self.puerto.write(a)


    def stacker (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x36, 1])
        print ("Verificar el estado de la pila", a)
        self.puerto.write(a)
        time.sleep(.02)

        r = self.puerto.read(5)
        
        print("RE,",r)
        r = self.verficarTramaDeDatos(r)

        if r: # Se recibio respuesta del billetero
            if r[0] == 254:
                print("Pila llena")
                ESTADO_BILLETERO = 1
            elif r[0] == 00:
                print("Pila Vacia")
                time.sleep(.2)

            self.ack()


    def expansionID (self):
        a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS_INCLUIR_CHECKSUM, [0x37, 1, 0x00, 0])  # Instrucción de identificación
        print (a)
        self.puerto.write(a)
        time.sleep(0.05)
        r = self.puerto.read(34)  # Verificar en el simulador se ve que devuelve 34
        self.verficarTramaDeDatos(r)
        print("RE,",r)

        if len(r)>29:
            self.variables[0].establecerValor(r[0:3].decode('utf-8'))
            self.variables[2].establecerValor(r[3:15].decode('utf-8'))
            self.variables[1].establecerValor(r[15:27].decode('utf-8'))
            self.variables[3].establecerValor(r[27:29])

            a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0X00, 0])
            self.puerto.write(a)

    def verficarTramaDeDatos(self, r):
        if r:
            if r==0x00:  #Recibio una respuesta correcta
                pass
            
            elif r[-1]!=self.comunicacion.checkSum(r[:-1]):
                print ("**************************El indice es diferente", r[-1])
                return False
        return r


    ######################################################################################################
    ##################################### Inicio de métodos del billetero ################################






    def inicializacion(self): 
        #print ("Dentro de inicializacion del billetero", end=" ",flush=True)


        if not self.equipoInicializado:
            print ("Inicializando ", end=" ",flush=True)

            r = self.reset()
            if r:
                if r == 0x00:
                    self.poll()
                    self.expansionID()
            else:
                print ("No se recibio respuesta, posiblemente a que no este conectado el dispositivo")
        self.equipoInicializado = True
        #print ("Fin de la rutina de inicialización del billetero")

    def resetSequence(self):
        r = self.reset()
        if r:
            if r[0] == 0x00:
                self.poll()
                self.expansionID()
        else:
            print ("No se recibio respuesta, posiblemente a que no este conectado el dispositivo")

    def status (self):
        self.poll()
        pass

    def enableSequence (self):
        self.stacker()
        self.billTypeEnable()

    def disableSequece(self):
        self.billTypeDisable()

    def acceptSequece(self):
        self.escrow()    

    



    #################################

    def instruccionImprimir (self, *args):
        for arg in args:
            print ("Se solicita imprimir", arg)

    def ejecutarInstruccion(self, numero, *args):
        self.listaDeFunciones.append([numero, args])
        print ("EjecutarInstruccion->", self.listaDeFunciones[len(self.listaDeFunciones)-1])

    def desencolarInstruccion(self):
        while len(self.listaDeFunciones)>0:
            #print("Se imprime la lista de funciones", len(self.listaDeFunciones))
            print ("Antes de desencolarInstrucción->", len(self.listaDeFunciones))
            funcion = self.listaDeFunciones.pop()
            print ("Despues de desencolarInstrucción->", len(self.listaDeFunciones))

            # Seleccion de instrucción
            if funcion[0] == self.BILLETERO_IMPRIMIR:
                self.instruccionImprimir(funcion)

            # if funcion[0] == self.BILLETERO_SOLICITAR_BILLETES:
            #     self.darCambio(funcion)

            if funcion[0] == self.BILLETERO_HABILITAR:
                self.enableSequence()

            if funcion[0] == self.BILLETERO_DESHABILITAR:
                self.disableSequece()


    ####################################### Fin de métodos del Billetero #################################
    ######################################################################################################



    def imprimirArreglo(self, r):
        s = ""
        for i in r:
            s += "{}".format(i).rjust(3)
        return s


    def __str__ (self):
        return "%s %s" %(self.obtenerTag(), self.obtenerDescripcion())
    
def main ():
    
    
    puerto = PuertoSerie("Puerto Serie")
    print ("Imprimiendo Arduino", PuertoSerie.ARDUINO_MICRO)
    puerto.modificarConfiguracion(dispositivo = PuertoSerie.ARDUINO_MICRO)
    #puerto.start()
    puerto.abrirPuerto()
    
    comunicacion = Comunicacion ()
    variablesMicro = VariablesMicro()
    
    # Se crea y se configura el dispositivo
    billetero1 = Billetero("Billetero 1", "MON-001", "En cajero")
    billetero1.establecerPuerto (puerto)
    billetero1.establecerComunicacion (comunicacion)

    
    time.sleep(4)
    

    
    
    time.sleep(4)
    
    puerto.cerrarPuerto()
    puerto.detenerHilo()
    

if __name__ == "__main__":
    main()