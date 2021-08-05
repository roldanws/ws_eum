import requests
import json,os,sys,time
from datetime import datetime
#from Pila.Pila import Pila


from urllib.request import urlopen
import threading


raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(raiz)

import cliente as Servidor
class Conexiones:
	"""Clase utilizada para guardar los datos 
	en caso un intento de conexion fallido
	"""

	def __init__(self):
		self.items = []
		#cola = Pila()
		self.inicioDeInstruccion = False
		self.conexion_activa = False

	

	def activo(self):
		conexionServ=1
		try:
			conexionServ=os.system("sudo ping -c 1 192.168.1.129")
			if conexionServ:
				return False
			else:
				return True
		except: 
			return conexionServ
	
	def obtenerConfiguracion(self):
		global equipo, sucursal, tipo
		try:
			infile = open(usuario+"eum.conf", 'r')
			c=infile.readline()
			arr=c.split(',')
			equipo=int(arr[0])
			sucursal=int(arr[1])
			tipo=int(arr[2])
			infile.close()
		except:
			equipo=1
			sucursal=1
			tipo=0
			infile = open(usuario+"eum.conf", "w")
			infile. write(str(equipo)+","+str(sucursal)+","+str(tipo))
			infile. close()
		print("equipo,sucursal,tipo ",equipo,sucursal,tipo)
		self.equipo.setValue(equipo)
		self.sucursal.setValue(sucursal)
		self.tipo.setCurrentIndex(tipo)
		
		
	
	def servidorActivo(self):
		timestamp=datetime.now()		
		mensaje=str("2")+","+str("0")+","+str(21)
		resultado=Servidor.configSocket("log", mensaje)
		if(resultado==-1):
			return False
		else:
			return True


	def pedirLogs (self):
		self.inicioDeInstruccion = True
		print ("PedirLogs", end =" ")
		try:
			resultado = Servidor.configSocket("log", mensaje)
			if resultado == -1:
				self.conexion_activa = False
			else:
				self.conexion_activa = True

		except:
			self.conexion_activa = False
			print ("No se pudo obtenerLogs")
		#print ("Imprimiendo LOGS", self.logs, end =" ")	
		self.inicioDeInstruccion = False




	def pollConexion(self,tipo,nodo):
		timestamp=datetime.now()		
		mensaje=str("2")+","+str(tipo)+","+str(nodo)

		if not self.inicioDeInstruccion:
			t = threading.Thread(target=self.pedirLogs, args=())
			t.start()



	def logPrendido(self,nodo):
		mensaje=str("2")+","+str("1")+","+str(nodo)
		resultado = Servidor.configSocket("log", mensaje)
		resultado =  str(resultado.decode('utf-8'))
		print("hora del servidor:", resultado)

		if(resultado==-1):

			return False
		else:
			os.system("echo eum | sudo -S date -s '"+resultado+"'")
			print("hora del servidor:", resultado)
			return True

	def obtenerLogs(self):
		mensaje=str("2")+","+str("4")+","+str(21)
		logs=Servidor.configSocket("log", mensaje)
		if(logs==-1):
			return False
		else:
			logsResult =  []
			logs =  str(logs.decode('utf-8'))
			tmp = len(logs)
			logs = logs[:tmp -1]
			logs = logs.replace("["," ")        
			logs = logs.split(",")
	       	#logs = logs[3]
	       	#logs = logs.split(',')
	        #for log in logs:
	        #    print("Nodo: "+str(log[3])+"  "+"Fecha:"+str(log[1]))
			for log in logs:
				tmp = len(log)
				log = log[2:tmp -1]
				logsResult.append(log)
			return logsResult
			
			
	def buscarTicket(self,mensaje):
		try:
			resultado=Servidor.configSocket("informacion boleto", mensaje)
			if(resultado == "boleto no localizado"):
				print("Registrando boleto no localizado...")
			else:
				print("boleto no localizado, esperando su registro...")
			return resultado
		except:
			print("Error en la busqueda del ticket")
			return -1
			
			
	def registrarPago(self,mensaje):
		try:
			Servidor.configSocket("pago boleto", mensaje)
			if(resultado == "boleto no localizado"):
				print("Registrando boleto no localizado...")
			else:
				print("boleto no localizado, esperando su registro...")
			return resultado
		except:
			print("Error en el registro del pago")
			return -1
			
	def encolarPago(self,mensaje):
		try:
			print(cola.estaVacia())
		except:
			print("Error al encolar el pago")
			return -1


	def estaVacia(self):
		return self.items == []

	def incluir(self, item):
		self.items.append(item)

	def extraer(self):
		return self.items.pop()

	def inspeccionar(self):
		return self.items[len(self.items)-1]

	def tamano(self):
		return len(self.items)
