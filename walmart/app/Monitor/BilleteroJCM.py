__author__ = "Sigfrido"
__date__ = "$5/18/2019 04:33:30 PM$"


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






#RESET_JCM = [252, 5, 64]
# ACK_JCM = [252, 5, 80]
# ACK_JCM2 = [252, 5, 80, 170, 5, 0, 252, 5, 11, 39, 86]
# STACK_1_JCM = [252, 5, 65]
# STACK_2_JCM = [252, 5, 66]
# STACK_3_JCM = [252, 5, 73]
# ENABLE_SETTING_JCM = [252, 7, 192, 81, 255]
# #ENABLE_SETTING_JCM = [252, 7, 192, 63, 0]
# REQUEST_STATUS_ENABLE = [252, 5, 128]

# SECURITY_SETTING_JCM = [252, 7, 193, 255, 0]
# COMUNICATION_MODE_SETTING_JCM = [252, 6, 194, 0]
# OPTIONAL_FUNCTION_SETTING_JCM = [252, 7, 197, 255, 0]

# INHIBIT_SETTING_JCM = [252, 6, 195, 0]
# INHIBIT_SETTING_DISABLE_JCM = [252, 6, 195, 63]
# STATUS_REQUEST_JCM = [252, 5, 17]


# PAY_OUT_JCM = [252, 9, 240, 32, 74, 1, 1] # 1 Bill to dispense DATA 1: No. Bills  | Data 2: Denom


# #-----------------SETTING STATUS REQUEST (Extension)-------------
# STARUS_REQUEST_EXTENSION_JCM = [252, 7, 240, 32, 26]
# UNIT_INFORMATION_REQUEST_JCM =  [252, 5, 146]
# RECYCLE_CURRENCY_REQUEST_JCM = [252, 7, 240, 32, 144]
# RECYCLE_KEY_REQUEST_JCM = [252, 7, 240, 32, 145]
# RECYCLE_COUNT_REQUEST_JCM = [252, 7, 240, 32, 146]
# RECYCLER_SOFTWARE_VERSION_REQUEST_JCM = [252, 7, 240, 32, 147]

# #-----------------SETTING COMAND (Extension)-------------

# #RECYCLE_CURRENCY_SETTING_JCM = [252, 11, 240, 32, 208, 8, 0, 4, 0]
# RECYCLE_CURRENCY_SETTING_JCM = [252, 13, 240, 32, 208, 8, 0, 1, 4, 0, 2]
# #RECYCLE_CURRENCY_SETTING_JCM = [252, 13, 240, 32, 208, 8, 0, 1, 4, 0, 1]
# #FC 0B F0 20 90 08 00 04 00 

# #RECYCLE_COUNT_SETTING_JCM = [252, 11, 240, 32, 210, 0, 0, 0, 0]
# #FC 0B F0 20 92 00 00 00 00

# RECYCLE_COUNT_SETTING_JCM_1 = [252, 10, 240, 32, 210, 80, 0, 1]
# RECYCLE_COUNT_SETTING_JCM_2 = [252, 10, 240, 32, 210, 80, 0, 2]





class BilleteroJCM (Variable):
    
    #BILLETERO_IMPRIMIR = b'\xAE'

    #BILLETERO_HABILITAR = b'\xAC'
    #BILLETERO_DESHABILITAR = b'\xAB'



    IMPRIMIR =  0x0E

    RESET = 0x10
    RESET_JCM = [252, 5, 64]


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

        self.configurarDispositivo (**kwargs)
        self.actualizar()

        

        self.puerto = None


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


    def inicializacion(self): 
        #print ("Dentro de inicializacion del billetero", end=" ",flush=True)


        if not self.equipoInicializado:
            print ("Inicializando {}".format(self), end=" ",flush=True)


            """
            r = self.reset()
            if r:

                print ("Imprimiendo respuesta", r, b'\x00')
                if r == b'\x00':
                    print ("es igual")
                    self.poll()
                    self.expansionID()
            else:
                print ("No se recibio respuesta, posiblemente a que no este conectado el dispositivo")
            """


        self.equipoInicializado = True
        #print ("Fin de la rutina de inicialización del billetero")


    def reset (self, args = None):
        mensaje = [self.RESET_JCM]

        r = self.enviarMensajeDispositivo(mensaje)

        if r:
            if r[0] == 0x00:
                print ("Se envio un reset")



    def instruccionImprimir (self, *args):
        print ("Se solicita imprimir {}".format(self))



    def enviarMensajeDispositivo (self, mensaje):
        jcmInstruccion = mensaje

        comandoCRC = self.comunicacion.checkSum_3(mensaje)
        jcmInstruccion.append(comandoCRC.crc_l())
        jcmInstruccion.append(comandoCRC.crc_h())
        print ('Imprimiendo la instruccion para la comunicación con {}'.format(self), jcmInstruccion)


        #lencomando = len(jcmInstruccion)+1
        #a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, comandoJcm)
        #ser.write(a);


        






        ###########################################################
        #cctalkInstruccion = [self.variables[0].obtenerValor(), len(mensaje) - 1, self.variables[3].obtenerValor()] + mensaje
        #print ('Imprimiendo la instruccion para el protocolo CCTALK', cctalkInstruccion)

        #a = self.comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, cctalkInstruccion)


        ######################
        self.puerto.escribir(jcmInstruccion)
        
        time.sleep(self.TIEMPO_DE_RETARDO_EN_LECTURA)
        r = self.puerto.leer_2(20)

        # serJCM.write(comandoJcm)
        # comandoJcm.pop()
        # comandoJcm.pop()
        # time.sleep(.1)
        # r = serJCM.read(20) #Verificar en el simulador se ven 19
        # trama = ''
        # for data in r:
        #     trama = trama + hex(data)+ ' '
        # print("comandoJcm ",comandoJcm, "Res:",r)
        # print(trama)
        # print('')


        ###############################################################
        
        
        # if r:
        #     # Se obtienen unicamente los datos despues de recibir la validación
        #     r = self.verificarRespuesta(jcmInstruccion, r)
        # else:
        #     print("{}: No se recibio respuesta del puerto".format(self))

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
            datos = respuesta[len(mensaje)+1   +3:-1]  #Datos dentro del mensaje

            # parametros utilizados para validar la respuesta del protocolo CCTALK
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



    def ejecutarInstruccion(self, numero, *args):

        self.listaDeFunciones.append([numero] + [elemento for elemento in args])
        print ("\n---------------------------------EjecutarInstruccion->", self.listaDeFunciones[len(self.listaDeFunciones)-1], len(self.listaDeFunciones))


    def desencolarInstruccion(self):
        while len(self.listaDeFunciones)>0:
            #print("Se imprime la lista de funciones", len(self.listaDeFunciones))
            #print ("Antes de desencolarInstrucción->", len(self.listaDeFunciones))
            funcion = self.listaDeFunciones.pop()
            #print ("Despues de desencolarInstrucción->", len(self.listaDeFunciones))

            # Seleccion de instrucción
            if funcion[0] == self.IMPRIMIR:
                self.instruccionImprimir(funcion)

            if funcion[0] == self.RESET:
                self.reset(funcion)




    def __str__ (self):
        return "%s " %(self.obtenerNombre())
    



def main ():
    
    
    puerto = PuertoSerie("Puerto Serie")
    print ("Imprimiendo Arduino", PuertoSerie.ARDUINO_MICRO)
    puerto.modificarConfiguracion(dispositivo = PuertoSerie.ARDUINO_MICRO)
    #puerto.start()
    puerto.abrirPuerto()
    
    comunicacion = Comunicacion ()
    
    
    # Se crea y se configura el dispositivo
    billeteroJCM = BilleteroJCM("BilleteroJCM 1", "BIL-006", "billeteroJCM")
    billeteroJCM.establecerPuerto (puerto)
    billeteroJCM.establecerComunicacion (comunicacion)
    
    
    time.sleep(0.5)



    
    puerto.cerrarPuerto()
    puerto.detenerHilo()
    

if __name__ == "__main__":
    main()
