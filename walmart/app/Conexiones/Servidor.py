
import sys
import socket
import argparse
import datetime, time
import os
import threading
import subprocess
from termcolor import colored

tam_buffer = 150
host = '192.168.1.129'
port = 2324

hosts = ('8.8.8.8', 'kernel.org', 'yahoo.com',host)

'''Operacion 2.- Pago de Boleto'''

			# mensaje = (idBoleto, idexpedidora, fecha boleto)
			#mensaje = str(2) + "," + str(1) + "," + '2017-07-11'
			#configSocket("pago boleto", mensaje)


class Servidor:
    CONECTADO = 1
    DESCONECTADO = 0
    def __init__(self):
        self.estado_internet = self.DESCONECTADO
        self.estado_servidor = self.DESCONECTADO
        self.funcionando = True
        servidor = threading.Thread(target=self.run)
        servidor.start()
    def run (self):
        print("#-------------------- Iniciando Servidor")
        self.funcionando = True
        while (self.funcionando):
            time.sleep(2)
            self.estado_internet = self.net_is_up()
            self.estado_servidor = self.servidor_activo()
            if self.estado_internet:
                text = "[{}] Conectado a internet".format(time.strftime("%Y-%m-%d %H:%M:%S"))
                print(colored(text, 'green'))
            else:
                text = "[{}] [Error1] Sin conexion a internet".format(time.strftime("%Y-%m-%d %H:%M:%S"))
                print(colored(text, 'red'))

            if self.estado_servidor:
                text = "[{}] Conectado al servidor".format(time.strftime("%Y-%m-%d %H:%M:%S"))
                print(colored(text, 'green'))
            else:
                text = "[{}] [Error2] Sin conexion a servidor".format(time.strftime("%Y-%m-%d %H:%M:%S"))
                print(colored(text, 'red'))

        
    def ping(self,host):
        ret = subprocess.call(['ping', '-c', '3', '-W', '5', host],
            stdout=open('/dev/null', 'w'),
            stderr=open('/dev/null', 'w'))
        return ret == 0

    def net_is_up(self):
        estado = False
        for h in hosts:
            if self.ping(h):
                estado = True
                break
        return estado

    def activo(self):
        try:
            self.estado = os.system("ping -c 1 -W 3 192.168.0.4")
            if self.estado:
                return False
            else:
                return True
        except: 
            return self.estado

    def servidor_activo(self):
        mensaje=str("2")+","+str("0")+","+str(21)
        resultado = self.configSocket("log", mensaje)
        if(resultado==-1):
            return False
        else:
            return True

    def pagoBoleto(self,s,operacion,mensaje,msj1):
        #operacion de pago de boleto
        s.send(operacion.encode('utf-8'))
        # espera una trama de confirmacion
        if(s.recv(tam_buffer) == b'ack'):
            #hace el envio del boleto a localizar
            s.send(msj1.encode('utf-8'))
            data = s.recv(tam_buffer)
            print("data: {}".format(data))
            if (data != b'boleto no localizado') :
                print("--> datos recibidos: {}".format(data))
                #idcaj,mediopago,monto, descripcion de las monedas pagadas, descripcion de los billetes pagados, tarifas implementadas
                s.send(mensaje.encode('utf-8'))

                #se recibe la respuesta final del registro del boleto
                data = s.recv(tam_buffer)
                if(data == b'registro exitoso del pago'):
                    print("El Pago del boleto se registro de manera correcta")
                    return 1
                else:
                    print("El pago del boleto NO se registro de manera correcta")
                    return -1
            else:
                print("Datos: tipo, estado y fecha No recibidos")
                return -1
        else:
            print("NO se entrego la operacion")
            return -1
        s.close()



    def pagoBoleto2(self,s,operacion,mensaje):
        #operacion de pago de boleto
        s.send(operacion.encode('utf-8'))
        # espera una trama de confirmacion
        if(s.recv(tam_buffer) == b'ack'):
            #hace el envio del boleto a localizar
            s.send(mensaje.encode('utf-8'))
            data = s.recv(tam_buffer)
            print("data: {}".format(data))
            if (data != b'boleto no localizado') :
                print("--> datos recibidos: {}".format(data))
                # se convierten los datos a string
                datosCodif = data.decode('utf-8')
                # Separacion de la cadena recibida, para que sea almacenada en el objeto boleto
                words = [i for i in str(datosCodif).split(',')]
                print("words: {}".format(words))
                #desc(words[0])
                '''

                    **************   Aplicar calculos y lo necesario para realizar el cobro
                '''
                #idcaj,mediopago,monto, descripcion de las monedas pagadas, descripcion de los billetes pagados, tarifas implementadas
                s.send("1;1;20.00;2:5,1:10;0:0;2,5".encode('utf-8'))

                #se recibe la respuesta final del registro del boleto
                data = s.recv(tam_buffer)
                if(data == b'registro exitoso del pago'):
                    print("El Pago del boleto se registro de manera correcta")
                else:
                    print("El pago del boleto NO se registro de manera correcta")
            else:
                print("Datos: tipo, estado y fecha No recibidos")
        else:
            print("NO se entrego la operacion")
        s.close()


    def solicitudDescuento(self,s,operacion,mensaje):
        # operacion de pago de boleto
        s.send(operacion.encode('utf-8'))
        # espera una trama de confirmacion
        if (s.recv(tam_buffer) == b'ack'):
            # hace el envio del boleto a localizar
            s.send(mensaje.encode('utf-8'))
            data = s.recv(tam_buffer)
            print("data: {}".format(data))
            if (data != b'boleto no localizado'): #agregar errores
                print("--> datos recibidos: {}".format(data))
                # se convierten los datos a string
                datosCodif = data.decode('utf-8')
                # Separacion de la cadena recibida, para que sea almacenada en el objeto boleto
                words = [i for i in str(datosCodif).split(',')]
                print("words: {}".format(words))
                ret = True
            else:
                print(data)
                ret = False
        else:
            ret = False

        if ret:
            print("retorno words")
            return words

        else:
            print("retorno None")
            return -1

        s.close()


    def informacionBoleto(self,s,operacion,mensaje):
        #operacion de pago de boleto
        s.send(operacion.encode('utf-8'))
        # espera una trama de confirmacion
        if(s.recv(tam_buffer) == b'ack'):
            #hace el envio del boleto a localizar
            s.send(mensaje.encode('utf-8'))
            data = s.recv(tam_buffer)
            print("data: {}".format(data))
            if (data != b'boleto no localizado') :
                print("--> datos recibidos: {}".format(data))
                # se convierten los datos a string
                datosCodif = data.decode('utf-8')
                # Separacion de la cadena recibida, para que sea almacenada en el objeto boleto
                words = [i for i in str(datosCodif).split(',')]
                print("words: {}".format(words))



            else:
                print("Datos: tipo, estado y fecha No recibidos")
                return -1
        else:
            print("NO se entrego la operacion")
            return -1
        return words



    def log(self,s,operacion,mensaje):
        # operacion de inicio de sesion
        s.send(operacion.encode('utf-8'))
        # Espera una trama de confirmacion
        if (s.recv(tam_buffer) == b'ack'):
            # Realiza el envio de los datos del boleto a buscar
            s.send(mensaje.encode('utf-8'))
            data = s.recv(tam_buffer)
            #print(data)
            #separar los datos
            #if (data != b'inicio_log registrado):
            if (data == b'Conectado'):
                return 1
            else:
                #print("Error en el log:")
                print(data)
                return data
        else:
            print("NO se entrego la operacion")
            return -1
        s.close()
        
    def logInicial(self,s,operacion,mensaje):
        # operacion de inicio de sesion
        s.send(operacion.encode('utf-8'))
        # Espera una trama de confirmacion
        if (s.recv(tam_buffer) == b'ack'):
            # Realiza el envio de los datos del boleto a buscar
            s.send(mensaje.encode('utf-8'))
            data = s.recv(tam_buffer)
            print(data)
            #separar los datos
            #if (data != b'inicio_log registrado):
            if (data == b'inicio_log registrado'):
                print("Incicio log registrado")
            else:
                print("Error en el inicio log:")
                print(data)
                return -1
        else:
            print("NO se entrego la operacion")
            return -1
        s.close()

    def logFinal(self,s,operacion,mensaje):
        # operacion de inicio de sesion
        s.send(operacion.encode('utf-8'))
        # Espera una trama de confirmacion
        if (s.recv(tam_buffer) == b'ack'):
            # Realiza el envio de los datos del boleto a buscar
            s.send(mensaje.encode('utf-8'))
            data = s.recv(tam_buffer)
            print(data)
            if (data == b'fin_log registrado'):
                print("Fin_log registrado")
            else:
                print("Error en registro log::")
                print(data)
                return -1
        else:
            print("NO se entrego la operacion")
            return -1
        s.close()

    def configSocket(self,operacion,mensaje):
        global host,ip
        #Parseo de argumentos, identifico que se tiene que pasar 2 parametros por consola host:127.0.0.1 puerto: 1234
        '''parser = argparse.ArgumentParser(description='Socket Error Examples')
        parser.add_argument('--host', action="store", dest="host", required=True)
        parser.add_argument('--port', action="store", dest="port", type=int, required=True)
        given_args = parser.parse_args()
        host = given_args.host
        port = given_args.port'''


        # Bloque try - catch para crear el socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
        except socket.error as e:
            print("Error al crear el socket: {}".format(e))
            return -1
            sys.exit(1)

        # Bloque try - catch para conectarse al servidor
        try:
            conn = s.connect((host,port))
            #print("Conexion al host: {} en el puerto: {}".format(host,port))
            #print("--> conn {}".format(conn))
        except socket.gaierror as e:
            print("Error al conectar con el servidor: {}".format(e))
            return -1
            sys.exit(1)
        except socket.error as e:
            print("Error de Conexion: {}".format(e))
            return -1
            sys.exit(1)
        if(operacion=='pago boleto'):
            words = [i for i in str(mensaje).split('*')]
            resultado = self.pagoBoleto(s,operacion,words[1],words[0])
        elif(operacion=='informacion boleto'):
            resultado = self.solicitudDescuento(s,'solicitud de descuento',mensaje)

        else:
            resultado = self.log(s,operacion,mensaje)
        s.close()
        return resultado
