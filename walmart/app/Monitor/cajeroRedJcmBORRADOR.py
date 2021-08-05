#!/usr/bin/env python3
import sys
import os
import time
import fechaUTC as hora
#from pygame import mixer
import subprocess
#import imprimirBoleto as impresora
from threading import Timer,Thread 
import sched
import termios
import serial
import binascii
from bitstring import BitArray
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox
from PyQt5 import QtCore, QtGui, uic
from datetime import datetime, timedelta
import calendar
import psycopg2, psycopg2.extras
from Botones.Botones import Botones,PuertoDeComunicacion, obtenerNombreDelPuerto
from Pila.Pila import Pila

from Comunicacion import Comunicacion
from struct import *


ruta = os.path.join(os.path.dirname(__file__))
sys.path.append(ruta)

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador
from Monitor.Hopper import Hopper
from PuertoSerie import PuertoSerie
from CRC import CRC


raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"../..")
sys.path.append(raiz)

import Conexiones.cliente as Servidor
from Conexiones.Conexiones import Conexiones



#import leerBotones as botones

PATH_ARCHIVO_CONFIGURACION_TERMINAL_SERIAL="/home/cajero/numeroSerial.txt"

clock = sched.scheduler(time.time, time.sleep)
cp=0
#global ser
DA=1166
Sinpago=0
ser=0
total = 0
bill = 0
a=0
ma=0
factorDeEscala = .10
tarifa=1
aux_tarifa=0
cambio=0
aux_cambio = 0
aux_cambio1 = 0
estatus=0
rep=0
kill = 0
killer = 0
kill_aux = 0
killbill=0
leido = 0
cajeroSuspendido=0
conteoPantallaPrincipal = 0
aux_tarifa1 =0
aux_dif=""
fo=""
fe=""
pe=""
costillo=0
hh=""
hsalida=""
avis=""
pagado=0
w=0
mona=0
mond=0
cs1=0
cs2=0
config=0
ser=0
monedas=[85,78,69,58]
monedasPago=[0,0,0,0]
monedasCambio=[0,0,0,0]
billetesPago=[0,0,0,0]
tarifasAplicadas=""
monedasTotal=290
dineroTotal=1166
dineroTotalB=0
billetesTotales=0
billetes=[0,0,0,0]
mensajeBoletoUsado=0
mensajeBoletoSellado=0
mensajeBoletoPerdido=0
mensajeError=0
suspenderCajero=0
tiempoBillExc=0
tiempoLimBill=0
tl=0
mensajeAyuda=0
cartuchoRemovido=0
preguntarPorEstado=0
mostrarTiempoDeSalidaRestante=[0,'']
conn = psycopg2.connect(database='CajerOk',user='postgres',password='Postgres3UMd6', host='localhost')
cur = conn.cursor()
tarifaVoluntaria=0
vvol=""
comienzaCambio=0
nivelDeCambio=0
nivelActual=[0,0,0,0]
nom=""
loc=""
contadorCartuchos=1
opcionAdmin=0
cambiaColor=0
imprime=0
accesoAcaja=0
inicioPago=0
tiempoAgotadoDePago=0
y=0
z=0
p=0
w=0
q=0
v=0
c=0
sel=0
USUARIO=0
correoUSUARIO=""
NoCajero=0
tarifaSeleccionada=0
varc=0
#red=117
#green=248
#blue=148
rrr=0
"""red=59
green=109
blue=153
"""
red=125
green=181
blue=215
comienzaLectura=0
varl=0
comienzaCobro=0
registraPago=0


configuracion = []
camInicial=''
USUARIO=''
host=''
ip=''
noEquipo = 0
plaza = ""
localidad = ""
user="eum"
pswd="pi"

valoresMonedas=[1,2,5,10]
valoresBilletes=[20,50,100,200]
MONEDAS_POR_HW = [0,0,0,0]
MONEDAS_POR_SW = [85,78,69,58]
conexion_activa = False
aportacionConfirmada=0

OP_EXITOSA = 1
OP_CAMBIO_INCOMPLETO = 2
OP_CAMBIO_INCOMPLETO_SUSPENDIDO = 3
OP_EXITOSA_SUSPENDIDO = 4
OP_CANCELADA = 5
OP_CANCELADA_CAMBIO_INCOMPLETO = 6
OP_CANCELADA_CAMBIO_INCOMPLETO_SUSPENDIDO = 7
OP__CANCELADA_SUSPENDIDO = 8

def interface():
	class Ventana(QDialog):
		conteo_final=0
		global ser,gui,total,conn,cur,nivelActual,NoCajero,cp
		def __init__(self):
			QDialog.__init__(self)
			gui = uic.loadUi("/home/cajero/Documentos/eum/app/cajeroF/rb.ui", self)
			#Leyendo stream de video...
			self.secuenciaCobro(0)
			self.montos()
			#self.pollingConexion()
			self.logPrender()
			#gui.leerBotones()
			#gui.boleto_leido()
			gui.contadorSegundos()
			gui.contadorMiliSegundos()
			fehoy=str(datetime.now().date()).split('-',2)
			fehoy=fehoy[2]+"/"+fehoy[1]+"/"+fehoy[0]
			#self.ldate.setText(fehoy)
			self.ldate2.setText(fehoy)

			self.current_timer = None
			self.prioridad=0
			#self.alerta.setVisible(False)
			self.lerror1.setVisible(False)

			self.salirAdmin.clicked.connect(self.saliendoAdmin)

			self.bntarifa.clicked.connect(lambda:self.cambia(7))
			self.bcancelar.clicked.connect(lambda:self.cambia(6))
			self.benter.setShortcut('Return')
			self.bcancelarPago.setShortcut('c')
			self.bsalirTarifas.clicked.connect(lambda:self.cambia(9))
			self.bsalirntarifas.clicked.connect(lambda:self.cambia(9))
			self.bconfirmartarifa.clicked.connect(self.tarifaConfirmada)
			self.bquitar.clicked.connect(self.elimina2)
			self.bhabilitar.clicked.connect(self.habilitaTarifa)
			self.bconfirmavol.clicked.connect(self.volConfirmado)
			self.bn1.clicked.connect(lambda:self.tecladoSum(1))
			self.bn2.clicked.connect(lambda:self.tecladoSum(2))
			self.bn3.clicked.connect(lambda:self.tecladoSum(3))
			self.bn4.clicked.connect(lambda:self.tecladoSum(4))
			self.bn5.clicked.connect(lambda:self.tecladoSum(5))
			self.bn6.clicked.connect(lambda:self.tecladoSum(6))
			self.bn7.clicked.connect(lambda:self.tecladoSum(7))
			self.bn8.clicked.connect(lambda:self.tecladoSum(8))
			self.bn9.clicked.connect(lambda:self.tecladoSum(9))
			self.bn0.clicked.connect(lambda:self.tecladoSum(0))
			self.bnborrar.clicked.connect(lambda:self.tecladoSum(10))
			#self.lnom.editingFinished.connect(lambda:self.holi(3))
			#self.llol.editingFinished.connect(lambda:self.holi(6))

			#self.bconfirmarplaza.clicked.connect(self.cambiaNombre)
			self.salirplaza.clicked.connect(lambda:self.cambia(9))
			self.salirCalibracion.clicked.connect(self.finalizarCalibracion)
			self.salirCajon.clicked.connect(self.finalizarCorteCaja)
			self.salirAyuda.clicked.connect(self.finalizarSoporteTecnico)
			self.salirReportes.clicked.connect(lambda:self.cambia(9))
			self.bsalirLogin.clicked.connect(lambda:self.cambia(9))
			self.idtar2.valueChanged.connect(self.actualizaMensaje)
			self.idtar1.valueChanged.connect(self.actualizaMensaje2)

			"""self.btarifas.clicked.connect(self.seccionTarifas)
			self.bcorte.clicked.connect(self.cortandoLaCaja)
			self.bcalibracion.clicked.connect(self.calibrando)
			self.bplaza.clicked.connect(self.llenaCamposPlaza)
			self.bpapel.clicked.connect(self.reemplazoPapel)
			self.bpublicidad.clicked.connect(self.menuPublicidad)
			self.breporte.clicked.connect(lambda:self.cambia(12))
			"""
			self.btarifas.clicked.connect(lambda:self.mueveyManda(1))
			self.bcorte.clicked.connect(lambda:self.mueveyManda(2))
			self.bcalibracion.clicked.connect(lambda:self.mueveyManda(3))
			self.bplaza.clicked.connect(lambda:self.mueveyManda(4))
			self.bpapel.clicked.connect(lambda:self.mueveyManda(5))
			self.bpublicidad.clicked.connect(lambda:self.mueveyManda(6))
			self.breporte.clicked.connect(lambda:self.mueveyManda(7))
			self.bayuda.clicked.connect(lambda:self.mueveyManda(8))
			self.bcancelarPago.clicked.connect(self.cancelandoPago)
			self.bnoserie.clicked.connect(self.mostrarNoSerie)
			#self.bcam.clicked.connect(self.activaCamara)


			self.bentrar.clicked.connect(self.validaLogin)
			self.bboletoPerdido.clicked.connect(self.boletoPerdido)
			self.reporteTar.clicked.connect(self.imprimeReporteTarifas)
			self.bayudaCliente.clicked.connect(self.ayudando2)
			self.bayudaCliente2.clicked.connect(self.ayudando)

			self.bimprimeEventos.clicked.connect(self.imprimeReporteEventos)
			self.bpdf.clicked.connect(self.imprimeReporteEventosPDF)
			self.bimpReporteCaja.clicked.connect(self.imprimeReporte)
			self.secuenciaCobro(1)



			self.tablatarifas.setColumnCount(12)
			self.tablatarifas.setHorizontalHeaderLabels(['','Id','Prioridad','Fecha_ini','Fecha_fin','Hora_ini','Hora_fin','Dia_semana','Descripcion','costo','intervalo_1','intervalo_2'])

			self.tablaMantenimiento.setColumnCount(4)
			self.tablaMantenimiento.setHorizontalHeaderLabels(['Nombre','Tipo','Descripcion','Fecha y hora'])

			"""
			cur.execute("select MAX(\"idCajero\") from \"CAJERO\"")
			for reg in cur:
				idc=reg[0]

			cur.execute("update \"CAJERO\" set \"idCajero\"="+NoCajero+" where \"idCajero\"="+str(idc))
			"""
			conn.commit()



	################MODS########
			self.bapagar.clicked.connect(self.apagarRasp)
			self.breiniciar.clicked.connect(self.reiniciarRasp)
			self.bconfirmarIP.clicked.connect(self.cambiaIp)
			self.bpanelconf.clicked.connect(self.muestraPanel)
			self.bsalirConfig.clicked.connect(lambda:self.secuenciaCobro(1))
			self.bsalirLogin.clicked.connect(lambda:self.secuenciaCobro(1))
			self.bsalirsucursal.clicked.connect(lambda:self.cambia(17))
			self.bsalirred.clicked.connect(lambda:self.cambia(17))
			self.bsalirCambiarFecha.clicked.connect(lambda:self.cambia(17))
			self.bsucursal.clicked.connect(lambda:self.cambia(16))
			self.bred.clicked.connect(lambda:self.cambia(15))
			self.breporte.clicked.connect(lambda:self.secuenciaCobro(1))
			self.bhora.clicked.connect(lambda:self.cambia(19))
			
			self.lerror1.setVisible(False)
			self.bentrar.clicked.connect(self.validaLogin)
			self.bcambiarFecha.clicked.connect(self.cambiaFecha)
			#self.bguardar.clicked.connect(self.setConfig)
			#self.bsalirConfig.clicked.connect(self.salirConf)
			self.bconfirmarplaza.clicked.connect(self.setConfig)
			self.panelConfig()
			self.datosEstacionamiento()
			self.bcam.clicked.connect(self.scan)
			self.bcam.setShortcut("Return")
			
			
			
		"""	
		def scan(self):
			global mensajeBoletoUsado
			#thread3 = Thread(target=leerCodQR, args = ())
			text=self.lscan.text()
			codigo=text[0:1]
			print(codigo)
			if(codigo == 'M' or codigo == 'L'):
				text=text.replace("'","-")
				text=text.replace("Ñ",":")
				text=text.split(',')
				#os.system("sudo nice -n -19 python3 archimp.py")
				try:
					
					leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
					leerArch.write(str(text[0])+"\n"+str(text[1])+"\n"+str(text[2])+"\n"+str(text[3])+"\n"+str(text[4]))
					leerArch.close()
					self.lscan.setText('')
				except Exception as e:
					print(e)
					pass
				print('boleto valido')

			else:
				mensajeBoletoUsado = 1
				self.lscan.setText('')
				print('boleto invalido')
		"""
		
		def secuenciaCobro(self,secuencia):
			#thread3 = Thread(target=leerCodQR, args = ())
			global SECUENCIA_COBRO
			#SECUENCIA_COBRO = secuencia
			if(secuencia == 0):
				#self.cambia(0)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,0,1,0,2,0])
				ser.write(a);
			if(secuencia == 1):
				self.cambia(0)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,1,1,0,2,0])
				ser.write(a);
			if(secuencia == 2):
				self.cambia(1)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,0,1,1,2,0])
				ser.write(a);
			if(secuencia == 3):
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,0,1,0,2,1])
				ser.write(a);


		def scan(self):
			#thread3 = Thread(target=leerCodQR, args = ())
			text=self.lscan.text()
			text2char=text[:2]
			if('M,' == text2char or 'L,' == text2char):
				text=text.replace("'","-")
				text=text.replace("Ñ",":")
				text=text.split(',')
				#os.system("sudo nice -n -19 python3 archimp.py")
				#os.system("sudo nice -n -19 python3 archimp.py")
				try:
					print(str(text[3])+" "+str(text[4]),'datetime...')
					fecha = datetime.strptime(str(text[3])+" "+str(text[4]), '%d-%m-%Y %H:%M:%S')
					leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
					leerArch.write(str(text[0])+"\n"+str(text[1])+"\n"+str(text[2])+"\n"+str(text[3])+"\n"+str(text[4])[:8])
					leerArch.close()
					self.lscan.setText('')
				except Exception as e:
					print(e,'datetime incorrecto')
					self.lscan.setText('')
					pass
			else:
				mensajeBoletoUsado = 1
				self.lscan.setText('')
				print('boleto invalido',text,text2char)
		
		def validaLogin(self):
			global cur,accesoAcaja,USUARIO,correoUSUARIO,user,pswd
			nom=self.lusu.text()
			rol_us=""
			indice=0
			contr=self.lcont.text()
			if(nom=="eum"):
				if(contr=="pi"):
					self.cambia(18)
				else:
					self.lerror1.setText("usuario o contraseña incorrectos")
					self.lerror1.setVisible(True)
			else:
				self.lerror1.setText("usuario o contraseña incorrectos")
				self.lerror1.setVisible(True)
			"""cur.execute("SELECT * FROM \"USUARIO\" WHERE usuario=%s and contra=%s order by \"idUsuario\" ASC",(nom,contr))

			print("nom,contr=",nom,contr)
			for reg in cur:
				print(reg[1],reg[2],reg[3],reg[4],reg[5],reg[6])
				rol_us=reg[1]
				indice=1
			if(indice==0):
				self.lerror1.setText("usuario o contraseña incorrectos")
				self.lerror1.setVisible(True)
			else:
				USUARIO=str(reg[0])
				self.cambia(5)"""
		
		def cambiaFecha(self):
			a=self.dtime.dateTime()
			b=self.dtime.textFromDateTime(a)
			print(b,type(b))
			os.system("sudo date -s '"+b+"' ")
			
		def setConfig(self):
			global plaza,localidad,noEquipo,host,ip,pol,pol1,pol2,pol3,pol4,pol5,impresora,anchoPapel
			lenn=0
			plaza=str(self.lnom.text())
			localidad=str(self.lloc.text())
			noEquipo=str(self.leq.text())
			
			
			print(plaza,localidad)
			dat=plaza+","+localidad+","+str(noEquipo)
			infile = open("/home/cajero/Documentos/eum/app/cajeroF/cajero/archivos_config/datos.txt", 'w')
			c=infile.write(dat)
			
			self.datosEstacionamiento()
			self.secuenciaCobro(1)
			
		
			
			
			
			
		def datosEstacionamiento(self):
			global plaza,localidad,noEquipo,host,ip,pol,pol1,pol2,pol3,pol4,pol5,impresora,anchoPapel
			lenn=0
			self.lnom.setText(plaza)
			self.lloc.setText(localidad)
			self.leq.setText(str(noEquipo))
			self.nomPlaza_2.setText(plaza)
			self.nomLoc_2.setText(localidad)
			self.lhost.setText(host)
			self.lip.setText(ip)
			
			
		def panelConfig(self):
			global plaza,localidad,noEquipo,host,ip
			infile = open('/home/cajero/Documentos/eum/app/cajeroF/cajero/archivos_config/datos.txt','r')
			datos= infile.readline()
			arr=datos.split(',')
			plaza=arr[0]
			localidad=arr[1]
			noEquipo=arr[2]
			infile.close()
			
			infile = open('/home/cajero/Documentos/eum/app/cajeroF/cajero/archivos_config/red.txt','r')
			datos= infile.readline()
			arr=datos.split(',')
			host=arr[0]
			ip=arr[1]
			infile.close()
			
			
		def salirConf(self):
			global panelConf
			panelConf=0
			self.secuenciaCobro(1)
			

		
		
		
		def sustituye(self,archivo,buscar,reemplazar):
			"""

			Esta simple función cambia una linea entera de un archivo

			Tiene que recibir el nombre del archivo, la cadena de la linea entera a

			buscar, y la cadena a reemplazar si la linea coincide con buscar

			"""
			with open(archivo, "r") as f:

				# obtenemos las lineas del archivo en una lista

				lines = (line.rstrip() for line in f)
				print(lines)

		 

				# busca en cada linea si existe la cadena a buscar, y si la encuentra

				# la reemplaza

				

				altered_lines = [reemplazar if line==buscar else line for line in lines]
				f= open(archivo, "w+")
				print(altered_lines[0],len(altered_lines))
				for i in range(len(altered_lines)):
					if(buscar in altered_lines[i]):
						print (altered_lines[i])
						cambia=altered_lines[i]
						f.write(reemplazar+"\n")
					else:
						f.write(altered_lines[i]+"\n")
				f.close()
				
				
		def cambiaIp(self):
			global host,ip
			host=self.lhost.text()
			ip=self.lip.text()

			self.sustituye("/home/cajero/Documentos/eum/app/cajeroF/cajero/cliente.py","192.168","host = '"+host+"'")
			self.sustituye("/etc/dhcpcd.conf","ip_address","static ip_address="+ip+"/24")
			ip=ip.split(".")
			ip=ip[0]+"."+ip[1]+"."+ip[2]+".1"
			self.sustituye("/etc/dhcpcd.conf","routers","static routers="+ip)

			
			host=str(self.lhost.text())
			ip=str(self.lip.text())
			
			
			print(plaza,localidad)
			dat=host+","+ip
			infile = open("/home/cajero/Documentos/eum/app/cajeroF/cajero/archivos_config/red.txt", 'w')
			c=infile.write(dat)
			
			self.datosEstacionamiento()
			self.secuenciaCobro(1)
			
			
		def muestraPanel(self):
			self.cambia(17)
			#datos=obtenerPlazaYLocalidad()
			#self.lno.setText(str(datos[0]))
			#self.llo.setText(str(datos[1]))
			#datos=obtenerTerminal()
			self.lusu.setText('')
			self.lcont.setText('')
			self.lerror1.setText('')
			
		def cambia(self,val):
			self.stackedWidget.setCurrentIndex(val)
		
		def apagarRasp(self):
			print("apagando...")
			os.system("sudo shutdown -P 0")
		def reiniciarRasp(self):
			print("apagando...")
			os.system("sudo shutdown -r 0")
			############################MODS FIN#################

		def activaCamara(self):
			#thread3 = Thread(target=leerCodQR, args = ())
			thread3 = Thread(target=leerCodQR, args = ())
			#os.system("sudo nice -n -19 python3 archimp.py")
			try:
			
				thread3.start()



			except Exception as e:
				pass
			#p=subprocess.Popen(['/home/cajero/scanner/dsreader -l 1 -s 20 > /home/cajero/Documentos/ticket.txt'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
			
			#so=os.popen('~/bin/dsreader -l 1 -s 20 > /home/cajero/Documentos/ticket.txt')
			
			
		def mostrarNoSerie(self):
			global accesoAcaja,NoCajero,mensajeAyuda
			os.system("sudo grep Serial /proc/cpuinfo >> /home/cajero/Escritorio/numeroSerial.txt")
			configuracion=[]
			archivo=open(PATH_ARCHIVO_CONFIGURACION_TERMINAL_SERIAL, "r")
			c=archivo.readline()
			serie=c.split(':', 1 )
			archivo.close()
			self.lserie.setText("No. Serie: "+str(serie[1]))

			self.lmodelo.setVisible(True)
			self.lserie.setVisible(True)

		def ayudando(self):
			global accesoAcaja,NoCajero,mensajeAyuda
			descripciones=self.obtenerDineroActual()
			mensaje=str("ayuda@ayuda.com")+","+str(NoCajero)+",3,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)

			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				#botones.apagarMonedero()
				mensajeAyuda=1
				pass

		def ayudando2(self):
			global accesoAcaja,NoCajero,mensajeAyuda
			descripciones=self.obtenerDineroActual()
			mensaje=str("ayuda@ayuda.com")+","+str(NoCajero)+",3,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)

			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				#botones.apagarMonedero()
				mensajeAyuda=1
				self.aviso1.setText("Tu peticion esta siendo atendida")
				pass

		def cancelandoPago(self):
			global cp
			print("BOTON CANCEL PRESIONADO")
			cp=1

		def finalizarCalibracion(self):
			global cartuchoRemovido,NoCajero,correoUSUARIO,cajeroSuspendido
			cajeroSuspendido=0
			if(cartuchoRemovido==0):
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",1"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
			else:
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass

		def finalizarCorteCaja(self):
			global cartuchoRemovido,NoCajero,correoUSUARIO
			if(cartuchoRemovido==0):
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",1"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
			else:
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
				#no sabria que hacer

		def finalizarSoporteTecnico(self):
			global cartuchoRemovido,NoCajero,correoUSUARIO
			if(cartuchoRemovido==0):
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",1"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
			else:
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
				#no sabria que hacer

		def imprimeReporteEventosPDF(self):
			dia=str(self.fechaInicio.date().day())
			mes=str(self.fechaInicio.date().month())
			anio=str(self.fechaInicio.date().year())

			dia2=str(self.fechaFin.date().day())
			mes2=str(self.fechaFin.date().month())
			anio2=str(self.fechaFin.date().year())

			fecha1=dia+"/"+mes+"/"+anio+" 00:00:00"
			fecha2=dia2+"/"+mes2+"/"+anio2+" 23:59:59"
			fechaFinal=fecha1+","+fecha2
			leerArch = open("/home/cajero/Documentos/fechaEventos.txt", "a+")
			leerArch.write(fechaFinal)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/eum/app/cajeroF/cajero/reporteEventosPDF.py")

		def imprimeReporteEventos(self):
			dia=str(self.fechaInicio.date().day())
			mes=str(self.fechaInicio.date().month())
			anio=str(self.fechaInicio.date().year())

			dia2=str(self.fechaFin.date().day())
			mes2=str(self.fechaFin.date().month())
			anio2=str(self.fechaFin.date().year())

			fecha1=dia+"/"+mes+"/"+anio+" 00:00:00"
			fecha2=dia2+"/"+mes2+"/"+anio2+" 23:59:59"
			fechaFinal=fecha1+","+fecha2
			leerArch = open("/home/cajero/Documentos/fechaEventos.txt", "a+")
			leerArch.write(fechaFinal)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/cajero/reporteEventos.py")

		def imprimeReporteTarifas(self):
			dia=str(self.fechaInicio2.date().day())
			mes=str(self.fechaInicio2.date().month())
			anio=str(self.fechaInicio2.date().year())

			dia2=str(self.fechaFin2.date().day())
			mes2=str(self.fechaFin2.date().month())
			anio2=str(self.fechaFin2.date().year())

			fecha1=dia+"/"+mes+"/"+anio+" 00:00:00"
			fecha2=dia2+"/"+mes2+"/"+anio2+" 23:59:59"
			fechaFinal=fecha1+","+fecha2
			leerArch = open("/home/cajero/Documentos/fechaTarifas.txt", "a+")
			leerArch.write(fechaFinal)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/cajero/reporteTarifas.py")


		def leerBotones(self):
			global cp,leido,opcionAdmin,accesoAcaja,NoCajero,accesoAcaja,aux_tarifa,cambio
			botones.configurarPinesGPIO()
			#botones.prenderMonedero()
			chapaMagnetica = botones.leerBotonesEntrada()
			bnCancelar = botones.botonCancelar()
			chapaMagnetica2=botones.leerBotonesEntrada2()
			if(bnCancelar):
			#if(bnCancelar and aux_tarifa!=0):
				cp=1
				print("BOTON CANCELAR PRESIONADOO")
			"""
			if(chapaMagnetica==True):
				print("Magnetizado")
				if(chapaMagnetica2==True):
					print("cerrado y magnetizado")
				else:
					print("abierto y magnetizado")
					if(accesoAcaja=1):
						#Mostrar mensaje en pantalla... Cerrar puerta!!!  , ALERTA
					else:
						#ALERTA: CAJERO ABIERTO SIN AUTORIZACION
						mensaje=str("ASALTO@ayuda.com")+","+str(NoCajero)+",4,"+"0:0"+","+"0:0"
						resultado=Servidor.configSocket("log inicial", mensaje)
						if(resultado==-1):
							self.lerror1.setText("Problema en la conexion")
							self.lerror1.setVisible(True)
						else:
							pass
			else:
				if(chapaMagnetica2==True):
					print("cerrado y DESmagnetizado")
					#Sin significado, NO ACCION.
				else:
					print("abierto y DESmagnetizado")
					#Se esta retirando el dinero posiblemente... 10 segeundos limite para magnetizar....
			if(sensorMovimiento==True):
				print("OK")
			else:
				if(opcionAdmin==2):
					print("OK2")
				else:
					print("Caja levantada")
					descripciones=self.obtenerDineroActual()
					mensaje=str("sensorCaja@ayuda.com")+","+str(NoCajero)+",4,"+"0:0"+","+"0:0"
					resultado=Servidor.configSocket("log inicial", mensaje)
					if(resultado==-1):
						self.lerror1.setText("Problema en la conexion")
						self.lerror1.setVisible(True)
					else:
						pass
				
			"""
				#self.avisoInserta.setText("Puerta cerrada")
			QtCore.QTimer.singleShot(100, self.leerBotones)

		def imprimeReporte(self):
			global contadorCartuchos
			fec=datetime.now().date()
			fec=str(fec.day)+"/"+str(fec.month)+"/"+str(fec.year)
			k1=self.m1.text()
			k2=self.m2.text()
			k3=self.m5.text()
			k4=self.m10.text()
			k5=self.mt.text()
			k6=self.b20.text()
			k7=self.b50.text()
			k8=self.b100.text()
			k9=self.b200.text()
			k10=self.bt.text()
			k11=self.dm.text()
			k12=self.db.text()
			k13=self.dt.text()
			datos=fec+','+k1+','+k2+','+k3+','+k4+','+k5+','+k6+','+k7+','+k8+','+k9+','+k10+','+k11+','+k12+','+k13+','+str(contadorCartuchos)
			leerArch = open("/home/cajero/Documentos/reporteCorteCaja.txt", "a+")
			leerArch.write(datos)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/cajero/imprimeCorte.py")
		def mueveyManda(self,valor):
			global opcionAdmin
			opcionAdmin=valor
			self.cambia(11)
			self.lerror1.setVisible(False)
			self.lusu.setText("")
			self.lcont.setText("")

		


		def calibrando(self):
			global contadorCartuchos,monedas,monedasTotal,dineroTotal,correoUSUARIO,accesoAcaja,NoCajero
			fecha=hora.mostrarFechayHora()
			i=-1
			descripciones=self.obtenerDineroActual()
			mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)
			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				fecha=hora.mostrarFechayHora()
				accesoAcaja=1
				botones.abrirPuerta()
				contadorCartuchos=contadorCartuchos+1
				self.lnumc.setText(str(contadorCartuchos))
				self.lniv.setText(""+str(nivelActual[0])+","+str(nivelActual[1])+","+str(nivelActual[2])+","+str(nivelActual[3]))
				self.cambia(5)
				monedas[0]=monedas[0]+85
				monedas[1]=monedas[1]+78
				monedas[2]=monedas[2]+69
				monedas[3]=monedas[3]+58
				monedasTotal=monedasTotal+290
				dineroTotal=dineroTotal+1166

				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",5,'"+str(contadorCartuchos)+"','"+fecha+"')"
				cur.execute(consu)
				conn.commit()

			#REPORTAR LOG A SERVIDOR....

		def menuPublicidad(self):
			global USUARIO,accesoAcaja
			fecha=hora.mostrarFechayHora()
			accesoAcaja=1
			botones.abrirPuerta()
			botones.configurarPublicidad()
			botones.manteniendoElCero()
			consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",8,'Publicidad','"+fecha+"')"
			cur.execute(consu)
			conn.commit()

		def reemplazoPapel(self):
			global correoUSUARIO,accesoAcaja,NoCajero
			descripciones=self.obtenerDineroActual()
			mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)
			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				fecha=hora.mostrarFechayHora()
				accesoAcaja=1
				botones.abrirPuerta()
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",9,'rollo reemplazado','"+fecha+"')"
				cur.execute(consu)
				conn.commit()

		def seccionAyuda(self):
			global correoUSUARIO,accesoAcaja,NoCajero
			descripciones=self.obtenerDineroActual()
			mensaje=str(correoUSUARIO)+","+str(NoCajero)+",3,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)
			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				fecha=hora.mostrarFechayHora()
				accesoAcaja=1
				botones.abrirPuerta()
				self.cambia(4)
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",9,'rollo reemplazado','"+fecha+"')"
				cur.execute(consu)
				conn.commit()

		def llenaCamposPlaza(self):
			global rep,nom,loc,nivelDeCambio
			infile = open("/home/cajero/Documentos/plaza.txt", 'r')
			c=infile.readline()
			arr=c.split(',', 1 )
			infile.close()
			nom=str(arr[0])
			loc=str(arr[1])
			self.lnom.setText(nom)
			self.llol.setText(loc)
			self.cambia(10)
		
		def sustituye(self,archivo,buscar,reemplazar):
			"""

			Esta simple función cambia una linea entera de un archivo

			Tiene que recibir el nombre del archivo, la cadena de la linea entera a

			buscar, y la cadena a reemplazar si la linea coincide con buscar

			"""
			with open(archivo, "r") as f:

				# obtenemos las lineas del archivo en una lista

				lines = (line.rstrip() for line in f)
				print(lines)

		 

				# busca en cada linea si existe la cadena a buscar, y si la encuentra

				# la reemplaza

				

				altered_lines = [reemplazar if line==buscar else line for line in lines]
				f= open(archivo, "w+")
				print(altered_lines[0],len(altered_lines))
				for i in range(len(altered_lines)):
					if(buscar in altered_lines[i]):
						print (altered_lines[i])
						cambia=altered_lines[i]
						f.write(reemplazar+"\n")
					else:
						f.write(altered_lines[i]+"\n")
				f.close()
		

		def cambiaNombre(self):
			global nom,loc,USUARIO
			fecha=hora.mostrarFechayHora()
			outfile = open("/home/cajero/Documentos/plaza.txt", 'w')
			nn=self.lnom.text()
			ln=self.llol.text()
			outfile.write(str(nn)+","+str(ln))
			outfile.close()
			
			nocaj=self.lcaj.text()
			
			outfile = open("/home/cajero/Documentos/NoCajero.txt", 'w')
			outfile.write(str(nocaj))
			outfile.close()
			host=self.lhost.text()
			ip=self.lip.text()
			
			self.sustituye("/home/cajero/Documentos/eum/app/cajeroF/cajero/cliente.py","192.168","	host = '"+host+"'")
			self.sustituye("/etc/dhcpcd.conf","ip_address","static ip_address="+ip+"/24")
			ip=ip.split(".")
			ip=ip[0]+"."+ip[1]+"."+ip[2]+".1"
			self.sustituye("/etc/dhcpcd.conf","routers","static routers="+ip)
			
			nom=self.lnom.text()
			loc=self.llol.text()
			self.cambia(9)
			consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",6,'"+str(nn)+","+str(ln)+"','"+fecha+"')"
			cur.execute(consu)
			conn.commit()


		def holi(self,val):
			print(val)
			if(val==3):
				self.lnom.setText("hola")
				self.llol.setText("")
			if(val==6):
				self.llol.setText("hola")
				self.lnom.setText("")


		def tecladoSum(self,val):
			if(val==10):
				self.valvol.setText("$")
			else:
				self.valvol.setText(self.valvol.text()+str(val))


		def volConfirmado(self):
			global aux_tarifa,cambio,aportacionConfirmada
			aportacionConfirmada=1
			if(self.valvol.text()=="$" or self.valvol.text()=="$0"):
				aux_tarifa=0
				#cambio=0
			else:
				valPropuesto=self.valvol.text()[1:]
				print("valvol: ",valPropuesto)
				aux_tarifa=int(self.valvol.text()[1:])
			self.secuenciaCobro(2)
			"""if(valPropuesto!=0):
				print("ACA")
				self.alerta.setVisible(True)
			else:
				print("ALLA")
				aux_tarifa=int(self.valvol.text()[1:])
				self.secuenciaCobro(2)"""







		def actualizaMensaje2(self):
			global cur
			vac=2
			idt=self.idtar1.value()
			cur.execute("select estado from \"TARIFA\" where \"idTarifa\"="+str(idt))
			for reg in cur:
				vac=reg[0]
				print(reg[0])
			if(vac==2):
				self.bquitar.setEnabled(False)
				self.bquitar.setText("No existente")
				print("K1",vac)
			else:
				self.bquitar.setEnabled(True)
				self.bquitar.setText("Eliminar")
				print("K2",vac)

		def actualizaMensaje(self):
			global cur
			vac=2
			idt=self.idtar2.value()
			cur.execute("select estado from \"TARIFA\" where \"idTarifa\"="+str(idt))
			for reg in cur:
				vac=reg[0]
				print(reg[0])
			if(vac==1):
				self.bhabilitar.setEnabled(True)
				self.bhabilitar.setText("Deshabilitar")
				print("simon1")
			if(vac==0):
				self.bhabilitar.setEnabled(True)
				self.bhabilitar.setText("Habilitar")

				print("simon0")
			if(vac==2):
				self.bhabilitar.setEnabled(False)
				self.bhabilitar.setText("No existente")
				print("simon2")



		def habilitaTarifa(self):
			global cur,conn,USUARIO
			idt=self.idtar2.value()
			fecha=hora.mostrarFechayHora()
			vac=0
			cur.execute("select estado from \"TARIFA\" where \"idTarifa\"="+str(idt))
			for reg in cur:
				vac=reg[0]
				print(reg[0])

			if(vac==0):

				cur.execute("update \"TARIFA\" set estado=1 where \"idTarifa\"="+str(idt))
				self.bhabilitar.setText("Deshabilitar")
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",1,'"+str(idt)+"','"+fecha+"')"
				cur.execute(consu)
				conn.commit()
			else:
				cur.execute("update \"TARIFA\" set estado=0 where \"idTarifa\"="+str(idt))
				self.bhabilitar.setText("Habilitar")
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",2,'"+str(idt)+"','"+fecha+"')"
				cur.execute(consu)
				conn.commit()


			self.llenaTabla()


		def seccionTarifas(self):
			global cur
			self.cambia(6)
			self.llenaTabla()

		def llenaTabla(self):
			global cur
			cur.execute("select * from \"TARIFA\" order by prioridad Desc")
			rowc=self.tablatarifas.rowCount()
			k=0
			while(k<rowc):
				self.tablatarifas.removeRow(0)
				#del self.CB2[0]
				k=k+1
			row=0
			for reg in cur:
				#print(reg[0],reg[1],reg[2],reg[3],reg[4],reg[5],reg[6],reg[7],reg[8],reg[9],reg[10],reg[11])
				self.tablatarifas.insertRow(row)
				idt=QTableWidgetItem(str(reg[0]))
				pri=QTableWidgetItem(str(reg[12]))
				fi=QTableWidgetItem(str(reg[2]))
				ff=QTableWidgetItem(str(reg[3]))
				hi=QTableWidgetItem(str(reg[4]))
				hf=QTableWidgetItem(str(reg[5]))
				ds=QTableWidgetItem(str(reg[6]))
				des=QTableWidgetItem(str(reg[7]))
				cos=QTableWidgetItem(str(reg[8]))
				i1=QTableWidgetItem(str(reg[9]))
				i2=QTableWidgetItem(str(reg[10]))
				if(reg[11]==1):
					state=QTableWidgetItem("Habilitada")
				else:
					state=QTableWidgetItem("Deshabilitada")
				self.tablatarifas.setItem(row,0,state)
				self.tablatarifas.item(row,0).setTextAlignment(4)

				self.tablatarifas.setItem(row,1,idt)
				self.tablatarifas.item(row,1).setTextAlignment(4)
				self.tablatarifas.setItem(row,2,pri)
				self.tablatarifas.item(row,2).setTextAlignment(4)
				self.tablatarifas.setItem(row,3,fi)
				self.tablatarifas.item(row,3).setTextAlignment(4)
				self.tablatarifas.setItem(row,4,ff)
				self.tablatarifas.item(row,4).setTextAlignment(4)
				self.tablatarifas.setItem(row,5,hi)
				self.tablatarifas.item(row,5).setTextAlignment(4)
				self.tablatarifas.setItem(row,6,hf)
				self.tablatarifas.item(row,6).setTextAlignment(4)
				self.tablatarifas.setItem(row,7,ds)
				self.tablatarifas.item(row,7).setTextAlignment(4)
				self.tablatarifas.setItem(row,8,des)
				self.tablatarifas.item(row,8).setTextAlignment(4)
				self.tablatarifas.setItem(row,9,cos)
				self.tablatarifas.item(row,9).setTextAlignment(4)
				self.tablatarifas.setItem(row,10,i1)
				self.tablatarifas.item(row,10).setTextAlignment(4)
				self.tablatarifas.setItem(row,11,i2)
				self.tablatarifas.item(row,11).setTextAlignment(4)
				row=row+1



		def elimina2(self):
			global cur,conn,USUARIO
			fecha=hora.mostrarFechayHora()
			idt=self.idtar1.value()
			print("Eliminado Caon")
			cur.execute("delete from \"TARIFA\" where \"idTarifa\"="+str(idt))
			consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",3,'"+str(idt)+"','"+fecha+"')"
			cur.execute(consu)
			conn.commit()
			self.llenaTabla()





		def tarifaConfirmada(self):
			global USUARIO
			fecha=hora.mostrarFechayHora()
			int1=""
			int2=""
			dia1=""
			mes1=""
			anio1=""
			dia2=""
			mes2=""
			anio2=""
			hora1=""
			minuto1=""
			hora2=""
			minuto2=""
			self.prioridad=0
			cons=""
			intok=""
			fecok=""
			horok=""
			dsemok=""
			costo=0
			dsem=""
			dsem2=""
			descr=""
			destar=""
			segundoIndicador=""

			print(cons)
			if(self.ch1.checkState()==2):
				self.prioridad=self.prioridad+1
				int1=","+str(self.i1.value())
				int2=","+str(self.i2.value())
				intok=",int_1,int_2"
				#segundoIndicador=segundoIndicador+"A"
			if(self.ch2.checkState()==2):
				self.prioridad=self.prioridad+1
				mes1=",'"+str(self.f1.date().month())
				dia1="/"+str(self.f1.date().day())
				anio1="/"+str(self.f1.date().year())
				mes2="','"+str(self.f2.date().month())
				dia2="/"+str(self.f2.date().day())
				anio2="/"+str(self.f2.date().year())+"'"
				fecok=",fec_ini,fec_fin"
				#segundoIndicador=segundoIndicador+"B"
			if(self.ch3.checkState()==2):
				self.prioridad=self.prioridad+1
				hora1=",'"+str(self.h1.time().hour())
				minuto1=":"+str(self.h1.time().minute())
				hora2="','"+str(self.h2.time().hour())
				minuto2=":"+str(self.h2.time().minute())+"'"
				horok=",hor_ini,hor_fin"
				#segundoIndicador=segundoIndicador+"C"
			if(self.ch4.checkState()==2):
				self.prioridad=self.prioridad+1
				dsem2=dsem2+",'"
				if(self.chlunes.checkState()==2):
					dsem=dsem+",lunes"
				if(self.chmartes.checkState()==2):
					dsem=dsem+",martes"
				if(self.chmiercoles.checkState()==2):
					dsem=dsem+",miercoles"
				if(self.chjueves.checkState()==2):
					dsem=dsem+",jueves"
				if(self.chviernes.checkState()==2):
					dsem=dsem+",viernes"
				if(self.chsabado.checkState()==2):
					dsem=dsem+",sabado"
				if(self.chdomingo.checkState()==2):
					dsem=dsem+",domingo"
				dsem=dsem.lstrip(",")
				dsem2=dsem2+dsem
				dsem2=dsem2+"'"
				#segundoIndicador=segundoIndicador+"D"





				dsem=dsem.rstrip(",")
				dsemok=",dia_sem"
				print(dsem)

			print(self.prioridad)

			#Determinando prioridad compuesta
			if(self.prioridad!=0):
				#self.prioridad=str(self.prioridad)+segundoIndicador+"'"
				self.prioridad=str(self.prioridad)+"'"
				cost=","+str(self.costo.value())
				descr=",'"+str(self.descripcion.toPlainText())+"'"
				archivo = open("/home/cajero/Documentos/NoCajero.txt", "r")
				idCajero=str(archivo.readline().rstrip("\n"))
				archivo.close()
				cur.execute("select * from \"CAJERO\" where \"idCajero\"=%s",(idCajero))
				for reg in cur:
					print(reg[0],reg[1])
				plaza=reg[1]


				cons="INSERT INTO \"TARIFA\" (prioridad,des_tar"+intok+fecok+horok+dsemok+",costo,estado,plaza) values ('"+str(self.prioridad)+descr+int1+int2+mes1+dia1+anio1+mes2+dia2+anio2+hora1+minuto1+hora2+minuto2+dsem2+cost+",1,"+str(plaza)+")"
				print("PK",cons)
				cur.execute(cons)
				conn.commit()

				cur.execute("select MAX(\"idTarifa\") from \"TARIFA\"")
				for reg in cur:
					idtar=reg[0]

				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",7,'"+str(idtar)+"','"+fecha+"')"
				cur.execute(consu)
				conn.commit()
				self.cambia(6)
				self.llenaTabla()


		def saliendoAdmin(self):
			global config
			self.secuenciaCobro(1)
			config=0
			self.lusu.setText('')
			self.lcont.setText('')
			fecha=hora.mostrarFechayHora()
			self.lmodelo.setVisible(False)
			self.lserie.setVisible(False)

		def obtenerDineroActual(self):
			global monedas,billetes
			descripcionMonedas=str(monedas[0])+":1;"+str(monedas[1])+":2;"+str(monedas[2])+":5;"+str(monedas[3])+":10"
			descripcionBilletes=str(billetes[0])+":20;"+str(billetes[1])+":50;"+str(billetes[2])+":100;"+str(billetes[3])+":200"
			return descripcionMonedas,descripcionBilletes

		def cortandoLaCaja(self):
			global accesoAcaja,correoUSUARIO,contadorCartuchos,monedas,monedasTotal,dineroTotal,dineroTotalB,billetesTotales,billetes,NoCajero
			fecha=hora.mostrarFechayHora()
			i=-1
			descripciones=self.obtenerDineroActual()
			mensaje=str(correoUSUARIO)+","+str(NoCajero)+",1,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)
			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				accesoAcaja=1
				botones.abrirPuerta()
				self.cambia(3)
				botones.abrirPuerta()
				self.m1.setText(str(monedas[0]))
				self.m2.setText(str(monedas[1]))
				self.m5.setText(str(monedas[2]))
				self.m10.setText(str(monedas[3]))
				self.mt.setText(str(monedas[0]+monedas[1]+monedas[2]+monedas[3]))
				self.b20.setText(str(billetes[0]))
				self.b50.setText(str(billetes[1]))
				self.b100.setText(str(billetes[2]))
				self.b200.setText(str(billetes[3]))
				self.bt.setText(str(billetes[0]+billetes[1]+billetes[2]+billetes[3]))
				self.dm.setText(str(dineroTotal))
				self.db.setText(str(dineroTotalB))
				self.dt.setText(str(dineroTotal+dineroTotalB))
				self.imprimeReporte()
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",4,'CC','"+fecha+"')"
				cur.execute(consu)
				conn.commit()
				monedas=[85,78,69,58]
				monedasTotal=290
				dineroTotal=1166
				dineroTotalB=0
				billetesTotales=0
				billetes=[0,0,0,0]
				contadorCartuchos=1

		def generaReporte(self):
			global config
			self.secuenciaCobro(1)
			config=0

		def boletoPerdido(self):
			global mensajeBoletoPerdido
			mensajeBoletoPerdido=1

		def pollingConexion(self):
			global conexion_activa
			#conexion_activa = conexion.obtenerLogs()
			#print("conexion:",conexion_activa)
			try:
				#conexion_activa = conexion.pollConexion()
				conexion_activa = conexion.servidorActivo()
				print("conexion:",conexion_activa)
			except:
				print("ocurrio un error")

			QtCore.QTimer.singleShot(5000,self.pollingConexion)


		def logPrender(self):
			try:

				prendido = conexion.logPrendido()
				print("Se registro log de prendido")
			except:
				print("Error al registrar log de prendido")


		def montos(self):
			global conexion_activa,mensajeBoletoSellado,cp,registraPago,comienzaLectura,comienzaCambio,NoCajero,cajeroSuspendido,suspenderCajero,w,conteoPantallaPrincipal,inicioPago,imprime,cambiaColor,nom,loc,nivelDeCambio,cambio,leido,total,aux_cambio,aux_cambio1,pagado,config,monedas,monedasTotal,dineroTotal,avis,dineroTotalB,billetesTotales,billetes,tarifaVoluntaria,mensajeBoletoUsado,mensajeBoletoPerdido,mostrarTiempoDeSalidaRestante,mensajeError,mensajeAyuda
			#self.cambio.display(aux_cambio)
			#entrada0 = pulsos.X[0].obtenerValor()

			
			#print (a, b)
			self.lcobrar.setText("$"+str(aux_tarifa))
			self.ldepositar.setText("$"+str(total))
			#self.fol.setText(fo)
			#self.pen.setText(pe)
			self.he.setText(hh)
			self.hs.setText(hsalida)
			self.ttotal.setText(aux_dif)
			self.he2.setText(hh)
			self.hs2.setText(hsalida)
			self.ttotal2.setText(aux_dif)

			#self.nomPlaza.setText(nom)
			#self.nomLoc.setText(loc)
			#self.nomPlaza_2.setText(nom)
			#self.nomLoc_2.setText(loc)

			#self.aviso.setText(str(avis))
			if(cambiaColor==1):
				cambiaColor=0
				self.gdepositar.setStyleSheet("background-color: rgb(48, 48, 48,80%);")
				self.gfp.setStyleSheet("background-color: rgb(48, 48, 48,80%);border-radius:10%;")
				self.gp.setStyleSheet("background-color:rgb(101, 179, 0);border-radius:10%;")
				self.gav.setStyleSheet("background-color:rgb(101, 179, 0);border-radius:10%;")

			if(conexion_activa):
				#DESHABILITAR CAJERO LUEGO DE UN TIEMPO
				#inicioPago=1
				self.bwifi.setEnabled(True)
			else:
				self.bwifi.setEnabled(False)
				
				
			if(leido == 1):
				#DESHABILITAR CAJERO LUEGO DE UN TIEMPO
				#inicioPago=1
				self.secuenciaCobro(2)
				comienzaLectura=1
				leido = 0
				
			#if(entrada0 == 1 and aux_tarifa>0):
			#	cp = 1
				
			if(comienzaCambio==1):
				
				"""self.gcambio.setStyleSheet("background-color:rgb(17, 58, 8);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(27, 68, 18);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(37, 78, 28);")
				self.gcambio.setStyleSheet("background-color:rgb(47, 88, 38);")
				self.gcambio.setStyleSheet("background-color:rgb(57, 98, 48);")
				self.gcambio.setStyleSheet("background-color:rgb(67, 10, 58);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(67, 10, 58);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(77, 118, 68);")
				self.gcambio.setStyleSheet("background-color:rgb(87, 128, 78);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(97, 138, 88);")
				self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				self.gdepositar.setStyleSheet("background-color:rgb(255, 255, 255);")
				self.lcobrar.setStyleSheet("background-color:rgb(255, 255, 255);")"""
				#pagado=1
				pass
			if(cajeroSuspendido==1):
				self.stackedWidget.setCurrentIndex(14)
				cajeroSuspendido=0
				
				
			if(pagado==1):
				
				pagado=0
			
			if(pagado==2):
				pagado=0
				if(cajeroSuspendido==1):
					self.stackedWidget.setCurrentIndex(14)
					conteoPantallaPrincipal=1
					inicioPago=0
					w=0
				else:
					if(cp==1):
						self.stackedWidget.setCurrentIndex(13)
					else:
						self.stackedWidget.setCurrentIndex(2)
					conteoPantallaPrincipal=1
					inicioPago=0
					w=0
			if(config==1):
				config=2
				self.lmodelo.setVisible(False)
				self.lserie.setVisible(False)
				self.stackedWidget.setCurrentIndex(9)

			if(mostrarTiempoDeSalidaRestante[0]==1):
				self.avisoInserta.setText(mostrarTiempoDeSalidaRestante[1]+" MINUTOS PARA SALIR")

			if(mensajeBoletoSellado==1):
				self.avisoInserta.setText("DESCUENTO APLICADO")
			
			if(mensajeBoletoUsado==1):
				self.avisoInserta.setText("Este boleto ya fue usado")

			if(mensajeBoletoPerdido==1):
				self.avisoInserta.setText("Acude a atencion a clientes")

			if(mensajeError==1):
				self.avisoInserta.setText("Lo sentimos, intentelo de nuevo")

			if(mensajeAyuda==1):
				self.avisoInserta.setText("Tu peticion esta siendo procesada")
				self.bayudaCliente.setEnabled(False)
				self.bayudaCliente2.setEnabled(False)

			if(nivelDeCambio!=0):
				self.aviso2.setText("No cuento con mucho cambio")
				#self.gav.setStyleSheet("background-color: rgb(134, 0, 0);border-radius:10%;")
				
			if(nivelDeCambio==0):
				self.aviso2.setText("")
				#self.gav.setStyleSheet("background-color:rgb(101, 179, 0);border-radius:10%;")
			if(tarifaVoluntaria==1):
				os.system("wmctrl -a 'Dialog'")
				self.stackedWidget.setCurrentIndex(8)
				self.valvol.setText("$")
				tarifaVoluntaria=0

			QtCore.QTimer.singleShot(5,self.montos)

			if(self.chtodos.checkState()==2):
				self.chlunes.setCheckState(2)
				self.chmartes.setCheckState(2)
				self.chmiercoles.setCheckState(2)
				self.chjueves.setCheckState(2)
				self.chviernes.setCheckState(2)
				self.chsabado.setCheckState(2)
				self.chdomingo.setCheckState(2)

			if(self.ch1.checkState()==2):
				self.i1.setEnabled(True)
				self.i2.setEnabled(True)
			if(self.ch1.checkState()==0):
				self.i1.setEnabled(False)
				self.i2.setEnabled(False)
			if(self.ch2.checkState()==2):
				self.f1.setEnabled(True)
				self.f2.setEnabled(True)
			if(self.ch2.checkState()==0):
				self.f1.setEnabled(False)
				self.f2.setEnabled(False)
			if(self.ch3.checkState()==2):
				self.h1.setEnabled(True)
				self.h2.setEnabled(True)
			if(self.ch3.checkState()==0):
				self.h1.setEnabled(False)
				self.h2.setEnabled(False)
			if(self.ch4.checkState()==2):
				self.chtodos.setEnabled(True)
				self.chlunes.setEnabled(True)
				self.chmartes.setEnabled(True)
				self.chmiercoles.setEnabled(True)
				self.chjueves.setEnabled(True)
				self.chviernes.setEnabled(True)
				self.chsabado.setEnabled(True)
				self.chdomingo.setEnabled(True)
			if(self.ch4.checkState()==0):
				self.chtodos.setEnabled(False)
				self.chlunes.setEnabled(False)
				self.chmartes.setEnabled(False)
				self.chmiercoles.setEnabled(False)
				self.chjueves.setEnabled(False)
				self.chviernes.setEnabled(False)
				self.chsabado.setEnabled(False)
				self.chdomingo.setEnabled(False)
			#botones.manteniendoElCero()



		def contadorSegundos(self):
			global tiempoBillExc,tl,tiempoLimBill,cp,varc,comienzaCambio,cajeroSuspendido,suspenderCajero,tarifasAplicadas,ma,preguntarPorEstado,accesoAcaja,c,conteoPantallaPrincipal,aux_cambio,cambio,total,w,killer,aux_tarifa,inicioPago,tiempoAgotadoDePago,cs2,cs1,v,a,p,q,y,z,mostrarTiempoDeSalidaRestante,mensajeBoletoPerdido,mensajeBoletoUsado,mensajeBoletoSellado,sel,mensajeError,mensajeAyuda
			#QtCore.QTimer.singleShot(1000,self.contadorSegundos)
			
			fehoy=str(datetime.now().date()).split('-',2)
			fehoy=fehoy[2]+"/"+fehoy[1]+"/"+fehoy[0]
			#self.ldate.setText(fehoy)
			self.ldate2.setText(fehoy)
			#self.ltime.setText(time.strftime("%H:%M:%S"))
			self.ltime2.setText(time.strftime("%H:%M:%S"))
			
			if(suspenderCajero==1):
				cs2=cs2+1
				if(cs2==7): #3 MINUTOS TOLERANCIA
					cs2=0
					suspenderCajero=0
					cajeroSuspendido=1
					
			if(tiempoLimBill==1):
				tl=tl+1
				if(tl==10): #3 MINUTOS TOLERANCIA
					tl=0
					tiempoLimBill=0
					tiempoBillExc=1
					print("Tiempo EXcedido Billetero")
					
			if(preguntarPorEstado==0):
				cs1=cs1+1
				if(cs1==1): #3 MINUTOS TOLERANCIA
					cs1=0
					preguntarPorEstado=1
			if(mensajeError==1):
				v=v+1
				if(v==3): #3 MINUTOS TOLERANCIA
					v=0
					mensajeError=0
					self.avisoInserta.setText("---> PAGO DE ESTACIONAMIENTO <---")

			if(mensajeAyuda==1):
				ma=ma+1
				if(ma==3): #3 MINUTOS TOLERANCIA
					ma=0
					mensajeAyuda=0
					self.bayudaCliente.setEnabled(True)
					self.bayudaCliente2.setEnabled(True)
					#botones.prenderMonedero()
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(mensajeBoletoUsado==1):
				p=p+1
				if(p==3): #3 MINUTOS TOLERANCIA
					p=0
					mensajeBoletoUsado=0
					self.avisoInserta.setText("INSERTE EL TICKET")
					
			if(mensajeBoletoSellado==1):
				sel=sel+1
				if(sel==3): #3 MINUTOS TOLERANCIA
					sel=0
					mensajeBoletoSellado=0
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(mensajeBoletoPerdido==1):
				c=c+1
				if(c==3): #3 MINUTOS TOLERANCIA
					c=0
					mensajeBoletoPerdido=0
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(mostrarTiempoDeSalidaRestante[0]==1):
				q=q+1
				if(q==3): #3 MINUTOS TOLERANCIA
					q=0
					mostrarTiempoDeSalidaRestante[0]=0
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(inicioPago==1):
				w=w+1
				if(w==300): #3 MINUTOS TOLERANCIA
					w=0
					tiempoAgotadoDePago=1
					inicioPago=0
					aux_tarifa = 0
					aux_tarifa1 = 0
					total = 0
					aux_tarifa=0
					aux_cambio=0
					registraPago=0
					tarifasAplicadas=""
					self.aviso1.setText("")
					self.secuenciaCobro(1)
					leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()
					killer=0
			if(conteoPantallaPrincipal == 1):
				y=y+1
				if(y==4):
					y=0
					conteoPantallaPrincipal=0
					aux_tarifa = 0
					aux_tarifa1 = 0
					total = 0
					cp=0
					tiempoBillExc=0
					self.lscan.setText('')
					registraPago=0
					aux_tarifa=0
					aux_cambio=0
					tarifasAplicadas=""
					self.aviso1.setText("")
					self.lcambio.setText("$0")
					os.system("wmctrl -a 'zbar'")
					#self.labelCambio.setText("$0")
					print("AQUI ANDAMOS")
					if(cajeroSuspendido==1):
						self.stackedWidget.setCurrentIndex(14)
						print("AQUI ANDAMOS3")
						self.secuenciaCobro(0)
					else:
						self.cambia(14)
						print("AQUI ANDAMOS2")
						self.secuenciaCobro(1)
					leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()
					killer=0

			if(accesoAcaja==1):
				z=z+1
				if(z==60):
					z=0
					accesoAcaja=0
					botones.cerrarPuerta()

			QtCore.QTimer.singleShot(1000,self.contadorSegundos)
			
		def contadorMiliSegundos(self):
			global varl,comienzaCobro,comienzaCambio,varc,red,green,blue,leido,comienzaLectura,rrr
			
			if(comienzaLectura==1):
				self.aviso1.setText("")
				varl=varl+1
				if(red<59):
					rrr=1
				if(red>150):
					rrr=0
				if(rrr==0):
					red=red-10
					green=green-10
					blue=blue-10
				else:
					red=red+5
					green=green+5
					blue=blue+5
				self.gcambio.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.lcambio.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				#self.gcobrar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.lcobrar.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#self.lcobrar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#print("red",red,green,blue)
				#self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				if(varl==30):
					varl=0
					
			if(comienzaCobro==1):
				self.aviso1.setText("")
				comienzaLectura=0
				varl=varl+1
				if(red<59):
					rrr=1
				if(red>105):
					rrr=0
				if(rrr==0):
					red=red-5
					green=green-5
					blue=blue-5
				else:
					red=red+5
					green=green+5
					blue=blue+5
				"""self.gcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.lcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.gdepositar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.ldepositar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				"""
				self.gcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.lcobrar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.ldepositar.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#print("red",red,green,blue)
				#self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				if(varl==30):
					varl=0
					
			
					
					
			
			if(comienzaCambio==1):
				self.secuenciaCobro(3)
				comienzaCambio=0
				comienzaLectura=0
				comienzaCobro=0
				self.aviso1.setText("Espere su cambio... "+str(aux_cambio))
				#self.labelCambio.setText("$"+str(aux_cambio))
				self.lcambio.setText("$"+str(aux_cambio))
				varc=varc+1
				if(red<59):
					rrr=1
				if(red>105):
					rrr=0
				if(rrr==0):
					red=red-5
					green=green-5
					blue=blue-5
				else:
					red=red+5
					green=green+5
					blue=blue+5
				"""self.gdepositar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.ldepositar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.gcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.lcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.gcambio.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.lcambio.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")"""
				self.gdepositar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.ldepositar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.gcobrar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.lcobrar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.lcambio.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.aviso1.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.avisoInserta_2.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				
				#print("red",red)
				#self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				if(varc==10):
					varc=0
					pagado=1
					#red=17
					#green=58
					#blue=8
			if(aux_tarifa==0):
				comienzaCambio=0
				varl=varl+1
				if(red<50):
					rrr=1
				if(red>150):
					rrr=0
				if(rrr==0):
					red=red-10
					green=green-10
					blue=blue-10
				else:
					red=red+10
					green=green+10
					blue=blue+10
				
				#self.gbol.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#self.avisoInserta.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.avisoInserta.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");background-color:transparent;")
				#print("red",red)
			QtCore.QTimer.singleShot(.005,self.contadorMiliSegundos)
			


		def actualiza(self,val):
			print(val)

		def cambia(self,num):
			self.stackedWidget.setCurrentIndex(num)



	app = QApplication(sys.argv)
	_ventana = Ventana()
	_ventana.show()
	app.exec_()



def restar_hora(horab,fechab):
		global aux_dif
		"""formato = "%H:%M:%S"
		h1 = datetime.strptime(hora1, formato)
		h2 = datetime.strptime(hora2, formato)
		resultado = h1 - h2
		aux_dif=str(resultado)
		print("res:",h1,h2,resultado,type(str(resultado)))
		return str(resultado)"""
		fechaBoleto = datetime.strptime(str(fechab[0]) + str(fechab[1]) + str(fechab[2]), '%Y%m%d').date()
		horaBoleto = datetime.strptime(str(horab[0]) +':'+str(horab[1]) +':'+ str(horab[2]), '%H:%M:%S').time()
		fechaActual=datetime.now().date()
		horaActual=datetime.now().time()
		horayFechaBoleto = datetime.now().combine(fechaBoleto, horaBoleto)
		horayFechaActual = datetime.now().combine(fechaActual, horaActual)
		restaFechas = horayFechaActual - horayFechaBoleto
		aux_dif=(str(restaFechas).split('.',1))[0]
		dias = int(restaFechas.days)
		horas = int(restaFechas.seconds / 3600)
		print("****RES:",restaFechas)
		return dias,horas



def calculaTarifa(tiempoEstacionado,descuento):
	global costillo,tarifa,aux_tarifa,aux_tarifa1,aux_dif,tarifaVoluntaria,tarifaSeleccionada
	aplicaDescuento=0
	indicador=0
	costillo=0
	horasRestantes=0
	dicdias = {'LUNES':'lunes','MARTES':'martes','MIERCOLES':'miercoles','JUEVES':'jueves','VIERNES':'viernes','SABADO':'sabado','DOMINGO':'domingo'}
	#dicdias = {'MONDAY':'lunes','TUESDAY':'martes','WEDNESDAY':'miercoles','THURSDAY':'jueves','FRIDAY':'viernes','SATURDAY':'sabado','SUNDAY':'domingo'}
	fechaActual = datetime.now().date()
	tiempoActual = datetime.now().time()
	#print("222",ahora,ahora2)
	t=time.localtime()
	dias=time.strftime("%A",t)
	#diaDeLaSemana=dicdias[dias.upper()]
	diaDeLaSemana="lunes"
	print("cuatro datos:)----->",fechaActual,tiempoActual,tiempoEstacionado,diaDeLaSemana)
	print("El descuento ES:::::::::",descuento,type(descuento))
	if(descuento==1):
		print("-.-.-.NO DESCUENTO",descuento)
		#cur.execute("select * from \"TARIFA\" where estado=1 order by costo Asc")
		cur.execute("select * from \"TARIFA\" where estado=1 and descuento=%s order by prioridad Desc",(str(descuento)))
	else:
		print("-.-.-.SI DESCUENTO",descuento)
		cur.execute("select * from \"TARIFA\" where estado=1 and descuento=%s order by prioridad Desc",(str(descuento)))
		#aplicaDescuento=1


	for reg in cur:
		print(reg[0],reg[1],reg[2],reg[3],reg[4],reg[5],reg[6],reg[7],reg[8],reg[9],reg[10],reg[11])
		if(str(reg[2])!="None"):
			if(fechaActual>=reg[2] and fechaActual<=reg[3]):
				print("FECHA ENTRA")
			else:
				indicador=indicador+1
		if(str(reg[4])!="None"):
			if(tiempoActual>=reg[4] and tiempoActual<=reg[5]):
				print("HORA ENTRA")
			else:
				indicador=indicador+1

		if(str(reg[6])!="None"):
			if(diaDeLaSemana in str(reg[6])):
				print("Dia de la semana entra")
			else:
				indicador=indicador+1

		if(str(reg[9])!="None"):
			if(tiempoEstacionado>=int(reg[9]) and tiempoEstacionado<int(reg[10])):
				print("INTERVALO ENTRA")
			else:
				indicador=indicador+1

		print("!!!!!",indicador)
		if(aplicaDescuento==1):
			indicador=0
		if(indicador==0):
			aplicaDescuento=0
			cantidadDeHor=reg[10]
			horasRestantes=tiempoEstacionado-cantidadDeHor
			tarifaSeleccionada=reg[0]
			costillo=reg[8]
			break
		else:
			indicador=0



	print("costillo=",costillo)
	if(costillo!=0):
		aux_tarifa=aux_tarifa+costillo
	else:
		print("NO SE APLICO NINGUNA TARIFA")
		#aux_tarifa=0
		tarifaVoluntaria=1
	print(aux_tarifa)
	print("respuesta: ")
	return tarifaSeleccionada,horasRestantes


def buscaCamara():
	global camInicial
	while(1):
		lee2 = os.system("sudo find /dev -name 'video*' > cam.txt")
		a = open("cam.txt", "r")
		cam=(a.readline().rstrip("\n")).lstrip("\x00")
		a.close()
		a = open("cam.txt", "w")
		a.write('')
		#time.sleep(1)
		#print('Cammmmmmmmm',cam,camInicial)
		if(cam!=camInicial):
			#print('Camara desconectadaaaaaaaaa')
			os.system("sudo pkill zbarcam")

def leerArchivo():
	global conexion_activa,aportacionConfirmada,tarifaVoluntaria,cajeroSuspendido,preguntarPorEstado,leido,fo,pe,fe,hh,hsalida,kill,killer,killbill,config,fechaAMD,nivelDeCambio,h,nivelActual,aux_tarifa,imprime,NoCajero,tarifaSeleccionada,mostrarTiempoDeSalidaRestante,mensajeBoletoPerdido,mensajeBoletoUsado,mensajeBoletoSellado,tarifasAplicadas,mensajeError
	tarifaSeleccionada=0
	A=0
	estadoConexion = 0
	#mixer.init()
	#mixer.music.load('/home/pi/Downloads/beep-08b.wav')
	while(kill == 0):
		#if(imprime==1):
		if(imprime==5):
			#imp()
			fe=fe+" "+hh
			fec=datetime.now().date()
			fec=str(fec.day)+"/"+str(fec.month)+"/"+str(fec.year)+','+hh+','+str(aux_tarifa)+','+fo+','+pe
			leerArch = open("/home/cajero/Documentos/pago.txt", "a+")
			leerArch.write(fec)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/cajero/archimp.py")
			
			

			imprime=0


		while(killer == 0 and kill == 0):
			leerArch = open("/home/cajero/Documentos/ticket.txt", "r")
			folio=leerArch.readline().rstrip("\n")
			#time.sleep(.2)
			if(folio != ''):
				print("{}  ==  {}".format(folio,"Estacionamientos unicos de Mexico"))
				#booleana=str("Estacionamientos unicos de Mexico") in str(folio)
				if(str("M") in str(folio)):
					#os.system('sudo python3 /home/pi/scanner/buz.py')
					#mixer.music.play()
					#time.sleep(1)
					pass
					print(folio)
					if(folio == 'boleto perdido'):
						leerArch.close()
						leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
						leerArch.write('')
						leerArch.close()

						cur.execute("select * from \"TARIFA\" where des_tar='boleto perdido' order by prioridad Desc")
						for reg in cur:
							print(reg[0],reg[1],reg[2],reg[3],reg[4],reg[5],reg[6],reg[7],reg[8],reg[9],reg[10],reg[11])
							if(str(reg[7])=="boleto perdido"):
								aux_tarifa=reg[8]
								leido = 1
								killbill = 0
								habilitarDispositivosCobro(estadoConexion)
					else:

						#impresora.imprimirBoletoC2("12/12/17","02:00:00",9)
						killer = 1
						leerArch.close()
						leerArch = open("/home/cajero/Documentos/ticket.txt", "r")
						leyenda=(leerArch.readline().rstrip("\n")).lstrip("\x00")
						folio=(leerArch.readline().rstrip("\n")).lstrip("\x00")
						inTerminal=leerArch.readline().rstrip("\n")
						inFecha=leerArch.readline().rstrip("\n")
						inHora=leerArch.readline().rstrip("\n")
						readQR = []
						readQR.append(folio)
						readQR.append(inTerminal)
						readQR.append(inFecha)
						readQR.append(inHora)
						print(readQR,"len=",readQR.__len__())
						fo=readQR[0]
						pe=readQR[1]
						hh=readQR[3]
						hsalida=hora.mostrarHoraSinFormato()[0]+":"+hora.mostrarHoraSinFormato()[1]+":"+hora.mostrarHoraSinFormato()[2]
						h=readQR[3].rstrip("\n")
						fe = readQR[2].rstrip("\n")
						
						print(h)
						leerArch.close()
						leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
						leerArch.write('')
						leerArch.close()
						print("FEEEE>>>>>",fo)
						#Verificar nivel de cambio
						while(1):
							#print(ser.inWaiting())
							ser.limpiar()
							#ser.flushInput()
							time.sleep(.1) #Para completar los 500 ms

							a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [10 , 1, 10 , 0])
							ser.write(a);
							time.sleep(.1)
							r = ser.read(18) #Verificar en el simulador se ven 19
							if(r):
								print("h", r)
								if (r[0] == 0):
									nivelActual[0]=r[4]
									nivelActual[1]=r[5]
									nivelActual[2]=r[6]
									nivelActual[3]=r[7]

									#Si el nivel es bajo , se muestra advertencia en pantalla

									if(r[4]<20):
										nivelDeCambio=1
									elif(r[5]<20):
										nivelDeCambio=1
									elif(r[6]<20):
										nivelDeCambio=1
									elif(r[7]<20):
										nivelDeCambio=1
									else:
										nivelDeCambio=0
									
									if(nivelDeCambio!=0):
										mensaje=str("ayuda@ayuda.com")+","+str(NoCajero)+",3,"+"Cambio bajo"+","+"0:0"
										#resultado=Servidor.configSocket("log inicial", mensaje)
									

									##Si el nivel es muy bajo , se muestra advertencia en pantalla

									if(r[4]<10):
										suspenderCajero=1
									elif(r[5]<10):
										suspenderCajero=1
									elif(r[6]<10):
										suspenderCajero=1
									elif(r[7]<10):
										suspenderCajero=1
									else:
										pass



									a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
									ser.write(a);
									break

						if(str("Admin") in str(fo)):
						#if(int(fo)==1566):

							print("Modo admin ON")
							config=1
							while(config!=0):
								if(preguntarPorEstado==1):
									monitorearChanger()
									preguntarPorEstado=0
								time.sleep(.5)
								killer=0
							print("Modo admin OFF")
							break
						else:
							if(cajeroSuspendido==1):
								A=-1
								#self.cambia(13)
								pass
							else:
								h1=str(hora.mostrarHoraSinFormato()[0])+":"+str(hora.mostrarHoraSinFormato()[1])+":"+str(hora.mostrarHoraSinFormato()[2])
								#Se obtiene la cantidad de horas y minutos que el cliente estuvo en el estacionamiento
								horaBoleto=h.split(':',2)
								fechaAMD=fe.split('-',2)
								print("fechas----->",fe,fechaAMD)
								fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]
								mensaje = str(fo) + "," + str(pe) + "," + fechaAMD +" "+h
								print(mensaje,type(mensaje))
								#return 2
								if(not conexion_activa):
									estadoConexion = 0
									#print("ERROR EN LA COMUNICACION")
									#A=-1
									#mensajeError=1
									
									
									leerArch = open("/home/cajero/Documentos/eum/sys/descuento.txt", "r")
									sello=leerArch.readline().rstrip("\n")
									print("sellado =",sello)
									if(int(sello) == 1):
										descuento=2
									else:
										descuento=1
									leerArch.close()
									leerArch = open("/home/cajero/Documentos/eum/sys/descuento.txt", "w")
									leerArch.write('0')
									leerArch.close()
									#Verificando sello de boleto Fin
									estadoBoleto=1
									
									
									
									#fechaBoleto=resultado[2]
									print(fechaAMD,horaBoleto)
									dh=restar_hora(horaBoleto,fechaAMD.split('-'))
									#ESTE IF ES PARA APLICAR TARIFA MAXIMA
									dias=dh[0]
									horas=dh[1]
									tiempoEstacionado=horas
									if(dias!=0):
										tiempoEstacionado=15
									if(descuento==2):
										A=0
										respuesta=calculaTarifa(tiempoEstacionado,2)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
									elif(int(estadoBoleto)==1):
										A=0
										print("<<<<>>>> DIAS, TE , Estado B,descuento :",dias,tiempoEstacionado,estadoBoleto,descuento)
										#BOLETO NO PAGADO, SI PAGADO=AUN TIENES TIEMPO X PARA SALIR, TIEMPO EXCEDIDO, BOLETO USADO
										respuesta=calculaTarifa(tiempoEstacionado,descuento)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
										print(tarifasAplicadas)
										if(respuesta[1]<0):
											print("respuesta de tarifa =",respuesta)
										else:
											segundaRespuesta=calculaTarifa(respuesta[1],1)
											tarifasAplicadas=tarifasAplicadas+";"+str(segundaRespuesta[0])
									elif(int(estadoBoleto)==2):
										A=-1
										mostrarTiempoDeSalidaRestante[0]=1
										mostrarTiempoDeSalidaRestante[1]=str(resultado[2])
									elif(int(estadoBoleto)==3):
										A=0
										fechaBoleto=fechaBoleto.split(" ",1)
										fechaAMD=fechaBoleto[0].split('-',2)
										fechaAMD=fechaAMD[0]+"-"+fechaAMD[1]+"-"+fechaAMD[2]
										#fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]
										print(fechaBoleto[1].split(':',2),fechaAMD)
										dh2=restar_hora(fechaBoleto[1].split(':',2),fechaAMD.split('-'))
										dias=dh2[0]
										horas=dh2[1]
										if(dias!=0):
											tiempoEstacionado=23
										tiempoEstacionado=horas
										r=calculaTarifa(tiempoEstacionado,1)
										tarifasAplicadas=str(r[0])
									elif(int(estadoBoleto)==4):
										A=-1
										mensajeBoletoUsado=1
									elif(int(estadoBoleto)==5):
										A=0
										respuesta=calculaTarifa(tiempoEstacionado,1)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
								
								#elif(resultado[0]==''):
								#	A=-1
								#	mensajeBoletoUsado=1
								else:
									estadoConexion = 1
									boleterasConectadas = 1
									
									
									"""
									Aqui se verifica el estado de conexion de las boleteras , en caso de estar conectadas y no existir el boleto,
									no se iniciara el proceso de pago,
									
									
									en caso contrario puede que exista el boleto y aun no ha sido registrado, por lo tanto se iniciara el pago 
									pasando como argumento el estado de la conexion.
									
									estadoConexionBoleteras = conexion.obtenerEstadoBoleteras()
									
									"""
									if(boleterasConectadas): 
										resultado=Servidor.configSocket("informacion boleto", mensaje)
										print("resultado",resultado)
									else:
										resultado = [1,fechaAMD]
									#Verificando sello de boleto
									leerArch = open("/home/cajero/Documentos/eum/sys/descuento.txt", "r")
									sello=leerArch.readline().rstrip("\n")
									print("sellado =",sello)
									if(int(sello) == 1):
										descuento=2
									else:
										descuento=1
									leerArch.close()
									leerArch = open("/home/cajero/Documentos/eum/sys/descuento.txt", "w")
									leerArch.write('0')
									leerArch.close()
									#Verificando sello de boleto Fin
									estadoBoleto=int(resultado[1])#ESTADO=2,FECHA=MINUTOS RESTANTES PARA SALIR....E=4,F=NULL,D=0....E=1,COBRAR NORMAL....
									
									fechaBoleto=resultado[2]
									print(fechaAMD,horaBoleto)
									dh=restar_hora(horaBoleto,fechaAMD.split('-'))
									#ESTE IF ES PARA APLICAR TARIFA MAXIMA
									dias=dh[0]
									horas=dh[1]
									tiempoEstacionado=horas
									if(dias!=0):
										tiempoEstacionado=15
									if(descuento==2):
										A=0
										respuesta=calculaTarifa(tiempoEstacionado,2)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
									elif(int(estadoBoleto)==1):
										A=0
										print("<<<<>>>> DIAS, TE , Estado B,descuento :",dias,tiempoEstacionado,estadoBoleto,descuento)
										#BOLETO NO PAGADO, SI PAGADO=AUN TIENES TIEMPO X PARA SALIR, TIEMPO EXCEDIDO, BOLETO USADO
										respuesta=calculaTarifa(tiempoEstacionado,descuento)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
										print(tarifasAplicadas)
										if(respuesta[1]<0):
											print("respuesta de tarifa =",respuesta)
										else:
											segundaRespuesta=calculaTarifa(respuesta[1],1)
											tarifasAplicadas=tarifasAplicadas+";"+str(segundaRespuesta[0])
									elif(int(estadoBoleto)==2):
										A=-1
										mostrarTiempoDeSalidaRestante[0]=1
										mostrarTiempoDeSalidaRestante[1]=str(resultado[2])
									elif(int(estadoBoleto)==3):
										A=0
										fechaBoleto=fechaBoleto.split(" ",1)
										fechaAMD=fechaBoleto[0].split('-',2)
										fechaAMD=fechaAMD[0]+"-"+fechaAMD[1]+"-"+fechaAMD[2]
										#fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]
										print(fechaBoleto[1].split(':',2),fechaAMD)
										dh2=restar_hora(fechaBoleto[1].split(':',2),fechaAMD.split('-'))
										dias=dh2[0]
										horas=dh2[1]
										if(dias!=0):
											tiempoEstacionado=23
										tiempoEstacionado=horas
										r=calculaTarifa(tiempoEstacionado,1)
										tarifasAplicadas=str(r[0])
									elif(int(estadoBoleto)==4):
										A=-1
										mensajeBoletoUsado=1
									elif(int(estadoBoleto)==5):
										A=0
										respuesta=calculaTarifa(tiempoEstacionado,1)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
								#A=calculaTarifa(tiempoEstacionado)

								#A=calculaTarifa("10:01:00")
						if(A!=-1):
							print("Iniciando cobro....",aux_tarifa,tarifasAplicadas)
							#REGISTRA BOLETO EN BD C/CONEXION
							tarifasAplicadas = 13
							tarifaSeleccionada = 13
							#consu="insert into \"BOLETO\"(tarifa,cajero,tipo,estado,conexion,estado_final,folio,expedidora,\"fechaExpedicion\") values("+str(tarifaSeleccionada)+","+str(NoCajero)+",1,"+str(estadoBoleto)+","+str(estadoConexion)+","+str(0)+","+str(fo)+",'"+str(pe)+"','"+fe+" "+h+"')"
							#cur.execute(consu)
							#conn.commit()
							while(aux_tarifa==0):
								time.sleep(.5)
								if(aportacionConfirmada==1):
									aportacionConfirmada=0
									
									break
							
							if(aux_tarifa==0):
								count(ser,estadoConexion)
							else:
								leido = 1
								os.system("wmctrl -a 'Dialog'")
								#enable_coin(ser)
								#enable_sequence(ser)
								killbill = 0
								habilitarDispositivosCobro(estadoConexion)
								
							
						else:
							killer=0

				elif(str("L") in str(folio)):
					#Si existe el descuento entonces 1
					descuento = 1
					leerArch = open("/home/cajero/Documentos/eum/sys/descuento.txt", "w")
					if (descuento):
						mensajeBoletoSellado = 1
						leerArch.write('1')
						leerArch.close()
					else:
						leerArch.write('0')
						leerArch.close()
					leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()

				else:
					leerArch.close()
					leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()
			else:
				leerArch.close()
				#time.sleep(.5)




def aceptarBilletes(estadoConexion,TON):
	global cp,cambio,tarifa,aux_cambio,aux,rep,ser,aux_tarifa,total,bill,killbill
	#print("Otra y otra")
	
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51 , 1 , 51 , 0])
	ser.write(a);
	time.sleep(.01)
	rBill = ser.read(6)
	print("bi",rBill)
	if(rBill):
		if(rBill[0]==144 or rBill[0]==145 or rBill[0]==146 or rBill[0]==147 or rBill[0]==148):
			billeteConfirmado=1
			#cambiaColor=1
			#disable_coin(ser)
			cambio = 0
			if(rBill[0]==144):
				bill = 20
				billetes[0]=billetes[0]+1
				billetesPago[0]=billetesPago[0]+1
			if(rBill[0]==145):
				bill = 50
				billetes[1]=billetes[1]+1
				billetesPago[1]=billetesPago[1]+1
			if(rBill[0]==146):
				bill = 100
				billetes[2]=billetes[2]+1
				billetesPago[2]=billetesPago[2]+1
			if(rBill[0]==147):
				bill = 200
				billetes[3]=billetes[3]+1
				billetesPago[3]=billetesPago[3]+1
			if(rBill[0]==148):
				bill = 500

			total = total+ bill
			#dineroTotalB=dineroTotalB+bill

			print(total)
			#time.sleep(.005)
			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
			ser.write(a);
			cambio = total - aux_tarifa
			accept_sequence(ser)
			count(ser,estadoConexion)
			#if(aux_cambio<0):
			#	enable_coin(ser)
			#	enable_coin(ser)
			#	enable_coin(ser)
				#enable_sequence(ser)

		'''
		else:
			if iniciarTemporizador(TON):
				break
				
	else:
		if iniciarTemporizador(TON):
			break
		'''
		


def aceptarBilletes2(estadoConexion,TON):
	global cp,cambio,tarifa,aux_cambio,aux,rep,ser,aux_tarifa,total,bill,killbill
	print("Otra y otra")
	TON = Temporizador("aceptarBilletes", 5)
	#while(1):
	#print("killbill",killbill)
	while(killbill == 0):
		#count(ser)
		#time.sleep(.050)
		time.sleep(.05)
		if(cp==1):
			count(ser)
		else:	
			if(killbill==1):
				pass
			else:
				#print("bill")
				time.sleep(.002)
				time.sleep(.002)

				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51 , 0 , 51 , 1])
				ser.write(a);

				time.sleep(.05)
				rBill = ser.read(6)
				print("bi",rBill)
				if(rBill):
					if(rBill[0]==144 or rBill[0]==145 or rBill[0]==146 or rBill[0]==147 or rBill[0]==148):
						billeteConfirmado=1
						#cambiaColor=1
						#disable_coin(ser)
						cambio = 0
						if(rBill[0]==144):
							bill = 20
							billetes[0]=billetes[0]+1
							billetesPago[0]=billetesPago[0]+1
						if(rBill[0]==145):
							bill = 50
							billetes[1]=billetes[1]+1
							billetesPago[1]=billetesPago[1]+1
						if(rBill[0]==146):
							bill = 100
							billetes[2]=billetes[2]+1
							billetesPago[2]=billetesPago[2]+1
						if(rBill[0]==147):
							bill = 200
							billetes[3]=billetes[3]+1
							billetesPago[3]=billetesPago[3]+1
						if(rBill[0]==148):
							bill = 500

						total = total+ bill
						#dineroTotalB=dineroTotalB+bill

						print(total)
						#time.sleep(.005)
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
						ser.write(a);
						cambio = total - aux_tarifa
						accept_sequence(ser)
						count(ser,estadoConexion)
						#if(aux_cambio<0):
						#	enable_coin(ser)
						#	enable_coin(ser)
						#	enable_coin(ser)
							#enable_sequence(ser)
					else:
						if iniciarTemporizador(TON):
							break
							
				else:
					if iniciarTemporizador(TON):
						break

			
			
def aceptarMonedas(estadoConexion,TON):
	global cp,cambio,tarifa,aux_cambio,aux,rep,ser,aux_tarifa,killbill
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
	ser.write(a);
	time.sleep(.05)
	r = ser.read(6)
	print("mo",r)
	if(r):
		print("A")
		if(r.__sizeof__() > 18):
			print("B")
			if (r[0] == 11):
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
				ser.write(a);
			elif(r[0] != 0 and r[0] !=11 and r[0]!=2 and r.__sizeof__() > 18):
				print("C")
				print(r)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
				ser.write(a);
				if (rep == 0):
					print("D")
					palPoll(ser,r[0], r)

					cambio = total - aux_tarifa
					aux_cambio=cambio
					count(ser,estadoConexion)

					rep = 0
					#rep=1
			if (r[0] == 0):
				rep = 0
	
			
def habilitarDispositivosCobro(estadoConexion):
	global tarifaVoluntaria,cp,tiempoAgotadoDePago,cambiaColor,total,bill,cambio,tarifa,aux_cambio,aux,rep,estatus,ser,killbill,aux_tarifa,bill,pagado,billetesTotales,dineroTotal,billetes,dineroTotalB,billetesPago
	

	#r = comunicacionJcm(INHIBIT_SETTING_DISABLE_JCM)
	r = comunicacionJcm(INHIBIT_SETTING_JCM)

	resultadoConfiguracionMonedero = enable_coin(ser)
	#resultadoConfiguracionBilletero = enable_sequence(ser)
	
	#print("Habilitando aceptacion de dispositivos M/B",resultadoConfiguracionMonedero,resultadoConfiguracionBilletero)
	TON_01 = Temporizador("Aceptar Billetes", 3)
	TON_02 = Temporizador("Aceptar Monedas", 3)
	while(killbill == 0):
		time.sleep(.01)
		ser.limpiar()
		
		'''
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
		ser.write(a);
		#time.sleep(.01)	

		
		r = ser.read(3)
		if (r):
			#print ("BOTON", r, r[0], ord(Comunicacion.caracterDeInicio))

			if len(r) == 3:
				if r[0] == ord(Comunicacion.caracterDeInicio):
					if r[2] == ord(Comunicacion.caracterDeFin):
						#print ("Boton", r[1])

						cp = (r[1] - ord('0')) & 1

		#############################Solicitando la temperatura ###################################
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.TEMPERATURA)
		ser.write(a);	
		r = ser.read(29)

		if (r):
			
			if comunicacion.verificarTrama(r):
				comunicacion.obtenerInstruccion(r)

			#if len(r) == 21:
			#	temp = unpack ('f', r[15: 15 + 4])[0]
			#	print ("temp ", temp)


		###########################################################################################


		'''
		


		if(cp==1):
			print("calculando montos...")
			count(ser, estadoConexion)
		else:
			if(resultadoConfiguracionMonedero == b'\x00'):
				aceptarMonedas(estadoConexion,TON_01)
			
			'''if(killbill==1):
				pass
			else:
				if(resultadoConfiguracionBilletero == b'\x00'):
					#print("aceptacion de billetes...")
					aceptarBilletes(estadoConexion,TON_02)
			'''



		



def billf():
	global tarifaVoluntaria,cp,tiempoAgotadoDePago,cambiaColor,total,bill,cambio,tarifa,aux_cambio,aux,rep,estatus,ser,killbill,aux_tarifa,bill,pagado,billetesTotales,dineroTotal,billetes,dineroTotalB,billetesPago
	contadorErrorBilletero=0
	contadorErrorMonedero=0
	print("Otra y otra")
	while(killbill == 0):
		#count(ser)

		#time.sleep(.050)

		


		if(cp==1):
			#count(ser)
			calcularCambio(ser)
		
		else:	
			"""
			ser.parity = change_parity(0x0B, 1)
			ser.write(b'\x0B')
			ser.parity = change_parity(0x0B, 0)
			ser.write(b'\x0B')
			"""
			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
			ser.write(a);
			


			#time.sleep(.05) Tiempo Pred CajeroRed
			time.sleep(.05)
			#time.sleep(.002)
			r = ser.read(6)
			print("mo",r)
			
			if(r):
				print("A")
				if(r.__sizeof__() > 18):
					print("B")
					if (r[0] == 11):
						"""
						ser.parity = change_parity(0x00, 0)
						ser.write(b'\x00')
						"""
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);

					elif(r[0] != 0 and r[0] !=11 and r[0]!=2 and r.__sizeof__() > 18):
						print("C")
						print(r)
						"""
						ser.parity = change_parity(0x00, 0)
						ser.write(b'\x00')
						"""
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);

						if (rep == 0):
							print("D")
							palPoll(ser,r[0], r)

							cambio = total - aux_tarifa
							aux_cambio=cambio
							#count(ser)
							calcularCambio(ser)
							rep = 0
							#rep=1
					if (r[0] == 0):
						rep = 0
			else:
				contadorErrorMonedero = contadorErrorMonedero + 1
				print("No se recibieron datos en monedero: ",contadorErrorMonedero)

			if(killbill==1):
				pass
			else:
			
				print("c")
				time.sleep(.002)
				time.sleep(.002)
				"""
				ser.parity = change_parity(0x33, 1)
				ser.write(b'\x33')
				ser.parity = change_parity(0x33, 0)
				ser.write(b'\x33')
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51, 1, 51, 0])
				ser.write(a);


				time.sleep(.05)
				rBill = ser.read(6)
				print("bi",rBill)
				if(rBill):
					if(rBill[0]==144 or rBill[0]==145 or rBill[0]==146 or rBill[0]==147 or rBill[0]==148):
						billeteConfirmado=1
						#cambiaColor=1
						disable_coin(ser)
						cambio = 0
						if(rBill[0]==144):
							bill = 20
							billetes[0]=billetes[0]+1
							billetesPago[0]=billetesPago[0]+1
						if(rBill[0]==145):
							bill = 50
							billetes[1]=billetes[1]+1
							billetesPago[1]=billetesPago[1]+1
						if(rBill[0]==146):
							bill = 100
							billetes[2]=billetes[2]+1
							billetesPago[2]=billetesPago[2]+1
						if(rBill[0]==147):
							bill = 200
							billetes[3]=billetes[3]+1
							billetesPago[3]=billetesPago[3]+1
						if(rBill[0]==148):
							bill = 500

						total = total+ bill
						dineroTotalB=dineroTotalB+bill

						print(total)
						#time.sleep(.005)
						"""
						ser.parity = change_parity(0x00, 0)
						ser.write(b'\x00')
						"""
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);
						time.sleep(.01)


						cambio = total - aux_tarifa
						accept_sequence(ser)
						#count(ser)
						calcularCambio(ser)
						if(aux_cambio<0):
							enable_coin(ser)
							#enable_coin(ser)
							#enable_coin(ser)
							#enable_sequence(ser)
				else: 
					contadorErrorBilletero = contadorErrorBilletero + 1
					print("No se recibieron datos en billetero: ",contadorErrorBilletero)

def monitorearChanger():
	global cartuchoRemovido
	ba = [0x0F, 0x05]
	ckInt = checkSum(ba)

	"""
	ser.parity = change_parity(0x0F, 1)
	ser.write(b'\x0F')
	ser.parity = change_parity(0x05, 0)
	ser.write(b'\x05')
	ser.parity = change_parity(int(ckInt), 0)
	ser.write(bytes([int(ckInt)]))
	"""

	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 5, 0])
	ser.write(a);
	time.sleep(.01)


	time.sleep(.005)
	r = ser.read(8)
	print("rut->",r)
	if(r):
		if(r[0]==21 and r[1]==2):
			cartuchoRemovido=1


def actualizaTubos():
	global cartuchoRemovido


def enable_sequence(ser):
	#STAKER
	print("Configurando billetero")
	TON = Temporizador("enable_sequence", 5)
	while(1):
		
		ser.limpiar()
		#ser.flushInput()
		
		'''
		time.sleep(.09)
		ser.parity = change_parity(0x36, 1)ser.parity = change_parity(0x36, 1)
		ser.write(b'\x36')
		ser.parity = change_parity(0x36, 0)
		ser.write(b'\x36')
		time.sleep(.09)
		
		'''

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [54, 1, 54, 0])
		ser.write(a);
		time.sleep(.01)
		ask = ser.read(1)
		#ask = b'\x03'
		
		
		
		print("eseq:",ask)
		if (ask):
			if(ask[0]==254):
				print("Pila llena")
			elif(ask[0]==00):
				print("Pila Vacia")
				time.sleep(.2)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				#return ask
				break
			else:
				if iniciarTemporizador(TON):
					break
		else:
			if iniciarTemporizador(TON):
				break




	
	
	while(1):
		"""
		time.sleep(.09)
		ser.parity = change_parity(0x34, 1)
		ser.write(b'\x34')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x42, 0)
		ser.write(b'\x42')
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [52, 1, 0, 0, 7, 0, 0, 0, 7, 0, 66, 0 ])
		ser.write(a);
		time.sleep(.01)


		ask = ser.read(1)
		print(ask)
		if (ask):
			print("Bill Habilitado",ask)
			if(ask==b'\x00'):
				time.sleep(.09)
				return ask
				break




def enable_sequence2(ser):
		#STAKER
	print("Stacker")
	while(1):
		ser.limpiar()
		#ser.flushInput()

		"""
		time.sleep(.09)
		ser.parity = change_parity(0x36, 1)
		ser.write(b'\x36')
		ser.parity = change_parity(0x36, 0)
		ser.write(b'\x36')
		time.sleep(.09)
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [54, 1, 54, 0])
		ser.write(a);
		time.sleep(.01)



		ask = ser.read(2)
		print(ask)
		if (ask):
			if(ask[0]==254):
				print("Pila llena")
			elif(ask[0]==00):
				print("Pila Vacia")
				"""
				time.sleep(.2)
				ser.parity = change_parity(0x00, 0)
				ser.write(b'\x00')
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				time.sleep(.01)




				break

	#Bill-type
	
	while(1):
		"""
		time.sleep(.09)
		ser.parity = change_parity(0x34, 1)
		ser.write(b'\x34')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x42, 0)
		ser.write(b'\x42')
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [52, 1, 0, 0, 7, 0, 0, 0, 7, 0, 66, 0 ])
		ser.write(a);
		time.sleep(.01)


		ask = ser.read(1)
		print(ask)
		if (ask):
			print("Bill Habilitado",ask)
			if(ask==b'\x00'):
				time.sleep(.09)
				return ask
				break



def enable_sequence3(ser):
		#STAKER
	print("Stacker")
	while(1):
		ser.limpiar()

		"""
		time.sleep(.09)
		ser.parity = change_parity(0x36, 1)
		ser.write(b'\x36')
		ser.parity = change_parity(0x36, 0)
		ser.write(b'\x36')
		time.sleep(.09)
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [54, 1, 54, 0])
		ser.write(a);
		time.sleep(.01)



		ask = ser.read(2)
		print(ask)
		if (ask):
			if(ask[0]==254):
				print("Pila llena")
			elif(ask[0]==00):
				print("Pila Vacia")
				"""
				time.sleep(.2)
				ser.parity = change_parity(0x00, 0)
				ser.write(b'\x00')
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				time.sleep(.01)




				break

	#Bill-type
	
	while(1):
		"""
		time.sleep(.09)
		ser.parity = change_parity(0x34, 1)
		ser.write(b'\x34')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x42, 0)
		ser.write(b'\x42')
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [52, 1, 0, 0, 7, 0, 0, 0, 7, 0, 66, 0 ])
		ser.write(a);
		time.sleep(.01)


		ask = ser.read(1)
		print(ask)
		if (ask):
			print("Bill Habilitado",ask)
			if(ask==b'\x00'):
				time.sleep(.09)
				return ask
				break

def palPoll(ser,r1,r):
	global cambiaColor,total,tarifa,cambio,rep,monedas,monedasTotal,dineroTotal,avis,aux_cambio,monedasPago
	entregadas=0
	tipoMoneda=0
	valorMoneda=0
	status=""
	if (128&r1 == 0 and 64&r1 != 0):
		if(32&r1==0 and 16&r1==0):
			print("ruta: Caja")
		elif (32 & r1 == 0 and 16 & r1 != 0):
			print("ruta: Tubos")
		elif (32 & r1 != 0 and 16 & r1 == 0):
			print("ruta: Sin uso")
		elif (32 & r1 != 0 and 16 & r1 != 0):
			print("ruta: Retornada")

	else:
		if(r1==1):
			status="Escrow request --- 1"
		if(r1==2):
			status="Entregaando cambio : "+str(aux_cambio)
		if(r1==3):
			status="No credit --- 3"
		if(r1==4):
			status="Defective tube sensor --- 4"
		if(r1==5):
			status="Double arrival --- 5"
		if(r1==6):
			status="Aceptor unplugged --- 6"
		if(r1==7):
			status="Tube Jam --- 7"
		if(r1==8):
			status="Checksum Error --- 8"
		if(r1==9):
			#status=""
			ms="Coin routing Error --- 9"
		if(r1==10):
			status="Changer Busy --- 10"
		if(r1==12):
			status="Coin Jam in the acceptance path --- 12"
		if(r1==13):
			status="Posible credited coin removal --- 13"
		print(status)
		avis=status
		return
	b=8
	while (b != 0):
		if (b & r1 != 0):
			tipoMoneda+=b
		b=b>>1
	if(tipoMoneda==2):
		valorMoneda=1
		monedas[0]=monedas[0]+1
		monedasPago[0]=monedasPago[0]+1
	if (tipoMoneda == 3):
		valorMoneda = 2
		monedas[1]=monedas[1]+1
		monedasPago[1]=monedasPago[1]+1
	if (tipoMoneda == 4):
		valorMoneda = 5
		monedas[2]=monedas[2]+1
		monedasPago[2]=monedasPago[2]+1
	if (tipoMoneda == 5):
		valorMoneda = 10
		monedas[3]=monedas[3]+1
		monedasPago[3]=monedasPago[3]+1
	print("Moneda insertada: ",valorMoneda)

	#cambiaColor=1
	#print("Monedas en tubo: ",r2)
	total=total+valorMoneda
	dineroTotal=dineroTotal+valorMoneda
	monedasTotal=monedasTotal+1
	print("Monto actual: ",total)


def accept_sequence(ser):
	global tiempoBillExc,tiempoLimBill
	estado=1 	  	
	while(estado<4):
		time.sleep(.09)
		#Aceptar billete (Stack) (enviarlo hacia atras)
		if(estado==1):
			"""
			ser.parity = change_parity(0x35, 1)
			ser.write(b'\x35')
			ser.parity = change_parity(0x01, 0)
			ser.write(b'\x01')
			ser.parity = change_parity(0x36, 0)
			ser.write(b'\x36')
			"""

			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [53, 1, 1, 0, 54, 0])
			ser.write(a);
			time.sleep(.01)


			r = ser.read(1)
			print("1: ",r)
			time.sleep(.005)
			if(r==b'\x00'):
				estado=2
		#Preguntar por estado del billete (Poll)
		if(estado==2):
			"""
			ser.parity = change_parity(0x33, 1)
			ser.write(b'\x33')
			ser.parity = change_parity(0x33, 0)
			ser.write(b'\x33')
			"""

			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51, 1, 51, 0])
			ser.write(a);
			time.sleep(.01)


			r = ser.read(1)
			if(r):
				print("2:",r)
				time.sleep(.05)
				aux = BitArray(r)
				if(aux.bin[0:4]=="1000"):
					ser.parity = change_parity(0x00,0)
					#ser.write(b'\x00')
					estado=3
				elif(aux.bin[0:4]=="1001"):
					ser.parity = change_parity(0x00,0)
					#ser.write(b'\x00')
					estado=3
				elif(aux.bin[0:4]=="1010"):
					ser.parity = change_parity(0x00,0)
					#ser.write(b'\x00')
					estado=3
				elif(aux.bin[0:4]=="1100"):
					ser.parity = change_parity(0x00,0)
					#ser.write(b'\x00')
					estado=3
				elif(aux.bin[0:4]=="1111"):
					estado=1

						
		if(estado==3):
			"""
			ser.parity = change_parity(0x33, 1)
			ser.write(b'\x33')
			ser.parity = change_parity(0x33, 0)
			ser.write(b'\x33')
			"""

			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51, 1, 51, 0])
			ser.write(a);
			time.sleep(.01)


			r = ser.read(50)
			#print("Espera Otra respuesta: ",r)
			if(r):
				print("3",r)
				"""
				ser.write(b'\x00')
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				time.sleep(.01)

				if(r==b'\x00'):
					tiempoLimBill=0
					estado=4
			


def disable_coin(ser):



	while (1):
		#print("asdddd")
		"""
		ser.parity = change_parity(0x0C, 1)
		ser.write(b'\x0C')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x0C, 0)
		ser.write(b'\x0C')
		"""
		print("Deshabilitando Monedero...")
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [12, 1, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0])
		#ser.close();
		#exit(0)
		ser.write(a);
		time.sleep(.01)
		r = ser.read(1)


		print(r)

		#print ("Se llego hasta aqui _ 02")
		if(r):
			if (r[0] == 0):  # Verificar la respuesta <----------
				print("Deshabilitacion de Monedas Exitosa")
				time.sleep(.005)
				break






def enable_coin(ser):
	global mona,mond
	mona=60
	mond=60
	ba = [0x0C, mona, mond]
	ckInt = checkSum(ba)
	print("vals...>>>",mona,mond,ckInt)
	#time.sleep(1)
	while (1):
		#print("asdddd")
		"""
		ser.parity = change_parity(0x0C, 1)
		ser.write(b'\x0C')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(mona, 0)
		ser.write(bytes([int(mona)]))
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(mond, 0)
		ser.write(bytes([int(mond)]))
		ser.parity = change_parity(ckInt, 0)
		ser.write(bytes([int(ckInt)]))
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [12, 1, 0, 0, mona, 0, 0, 0, mond, 0, ckInt, 0])
		ser.write(a);
		time.sleep(.01)



		#time.sleep(.05)
		r = ser.read(1)
		print(r)

		#print ("Se llego hasta aqui _ 03")
		if(r):
			if (r[0] == 0):  # Verificar la respuesta <----------
				print("Habilitacion de Monedas Exitosa")
				time.sleep(.005)
				return r
				break

def obtenerPlazaYLocalidad():
	global nom, loc
	try:
		connection = psycopg2.connect(database='CajerOk',user='postgres',password='Postgres3UMd6', host='localhost')
		#connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
		with connection.cursor() as cursor:
			cursor.execute(
				' SELECT nombre_plaza,estado FROM plaza WHERE idplaza = 1')
			row = cursor.fetchone()
			if row is not None:
				print("columns: {}, {}".format(row[0], row[1]))
				nom = str(row[0])
				loc = str(row[1])
				connection.commit()
				connection.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		
		



def Init(ser):
	#RESET COIN CHANGER
	global rep,nivelDeCambio,NoCajero
	##print(ser.inWaiting())
	ser.limpiar()
	#ser.flushInput()
	rep=0
	#botones.prenderMonedero()
	time.sleep(5)
	infile = open("/home/cajero/Documentos/plaza.txt", 'r')
	c=infile.readline()
	arr=c.split(',', 1 )
	infile.close()
	obtenerPlazaYLocalidad()
	infile = open("/home/cajero/Documentos/NoCajero.txt", 'r')
	NoCajero=infile.readline()
	infile.close()
	


	while (1):
		#ser.limpiar()
		##ser.flushInput()
		"""
		ser.parity = change_parity(0x08, 1)
		ser.write(b'\x08')
		ser.parity = change_parity(0x08, 0)
		ser.write(b'\x08')
		"""
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [8, 1, 8, 0])
		#ser.escribir(a)
		#time.sleep(0.1)


		ser.write(a);
		time.sleep(.01)

		
		r = ser.read(1)
		print("RE,",r)
		if(r):
			if (r[0] == 0):
				break
		
	while (1):
		"""
		ser.parity = change_parity(0x0F, 1)
		ser.write(b'\x0F')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x0F, 0)
		ser.write(b'\x0F')
		"""
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 0, 0, 15, 0])
		ser.write(a);
		time.sleep(.1)

		r = ser.read(33)  # Verificar en el simulador se ve que devuelve 34
		print(r)
		if (r):
			#print(r[0])
			if (r[0] == 77):  # Verificar la respuesta (4D = M, 45 = E, 49 = I) <----------
				"""
				ser.parity = change_parity(0x00, 0)
				ser.write(b'\x00')  # Devuelve ACK
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				time.sleep(.01)

				#print ("Se llego hasta aqui _ 01")

				break

	#ser.flushInput()
	ser.limpiar()
	disable_coin(ser)
	cont=0
	while(1):
		"""
		ser.parity = change_parity(0x0F, 1)
		ser.write(b'\x0F')
		ser.parity = change_parity(0x05, 0)
		ser.write(b'\x05')
		ser.parity = change_parity(0x14, 0)
		ser.write(b'\x14')
		"""
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 5, 0, 20, 0])
		ser.write(a);
		time.sleep(.01)


		#time.sleep(.02)
		r = ser.read(2)
		if(r):
			print("rrrrr__:",r)
			if(cont==2):
				print("LISTO!---")
				break
			else:
				cont=cont+1
				print("DESHINIBIENDO!---",cont)
				enable_coin(ser)
				time.sleep(2)
	





def calcularCambio(ser):
	global cp,cambio,total,aux_tarifa,comienzaCambio,cajeroSuspendido,registraPago,killbill,pagado,aux_cambio
	if(cp==1):
		cambio = total - aux_tarifa
		cambio = aux_tarifa+cambio
		print("-.-.-.-.-.cancelando pago")
		registraPago=1
	else:
		cambio = total - aux_tarifa

	aux_cambio = cambio

	if (cambio > 0):
		print("hay cambio")
		imprime=1
		comienzaCambio=1
		#dineroTotal=dineroTotal+aux_tarifa
		disable_sequence(ser)
		r = comunicacionJcm(INHIBIT_SETTING_DISABLE_JCM)
		#print(ser.inWaiting())
		ser.limpiar()
		#ser.flushInput()
		#ESTATUS TUBOS
		if(cajeroSuspendido==1):
			registraPago=1
			killbill = 1
			pagado=2
			
		else:

			cambioRestante = solicitarCambio(cambio)
			cambio = cambioRestante
			print("Cambio Restante: ",cambioRestante,cambio)
			#count(ser,0)
			#killbill = 1
			#pagado=2
			



	if(cambio==0): # if(total==aux_tarifa):
		imprime=1
		killbill = 1
		comienzaCambio=1
		time.sleep(.05)
		pagado=2
		if(cp==1):
			print("Pago cancelado")
			#cp=0
		else:
			registraPago=1
		disable_coin(ser)
		disable_sequence(ser)
		r = comunicacionJcm(INHIBIT_SETTING_DISABLE_JCM)



def solicitarCambio(cambioSolicitado):
	global PAY_OUT_JCM,SECUENCIA_COBRO
	#cambioSolicitado = 177
	
	
	#cambio5 = int(cambioSolicitado/5)
	#cambio1 = int(cambioSolicitado/1)
	cambioEntregado10 = 0
	cambioEntregado5 = 0
	cambioEntregado1 = 0
	monedasDispensadas = 0
	estatus = 0
	
	HOPPER_MONEDAS_SOLICITADAS = {10:0,5:0,1:0}
	HOPPER_MONEDAS_DISPENSADAS = {10:0,5:0,1:0}
	MONEDAS = [10,5,1]
	BILLETES = [100,50]
	cambioRestante = cambioSolicitado
	#MONEDAS = HOPPER_MONEDAS_HABILITADAS.keys()
	i = 0
	print("------------- Cambio Solicitado: ",cambioSolicitado,"-------------------")

	for billete in BILLETES:
		repeticiones = BILLETES.count(billete)
		i = i +1 
		cambio = int(cambioSolicitado/billete)

		if(cambio):

			cambioSolicitado = cambioSolicitado%billete
			PAY_OUT_JCM = [252, 9, 240, 32, 74, cambio, i]
			SECUENCIA_COBRO = 2
			print('cambio en billetes de ',billete,' : ', cambio,'cambioSolicitado',cambioSolicitado)
			cambioRestante = cambioRestante - (cambio*billete)


	i = 0
	for moneda in MONEDAS:
		repeticiones = MONEDAS.count(moneda)
		i = i +1 
		#print("reps: ",repeticiones, "iteracion: ", i)
		if(repeticiones > 2):

			#count(ser)
			break
			#exit(0)
			pass
		
		
		#print("Cambio Solicitado: ",cambioSolicitado)
		#print(moneda,cambio)
		cambio = int(cambioSolicitado/moneda)
		if(cambio):
			cambioSolicitado = cambioSolicitado%moneda
			print("\nMonedas solicitadas de ",moneda,": ",cambio)
			codigoCambio = cambioHopper(cambio,HOPPER_MONEDAS_HABILITADAS[moneda])
			dispensandoCambio = 1
			#time.sleep(1)
			
			if codigoCambio == [0]:
				while(dispensandoCambio):
					time.sleep(.3)
					estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
					if estatus:
						if estatus[1]:
							#cambioRestante = (estatus[1]*moneda)+cambioSolicitado
							print("*Entrgando Cambio*",(estatus[1]*moneda)+cambioSolicitado,"Restante")
						else:
							dispensandoCambio = 0
				if estatus:
					if estatus[0]:
						monedasPorPagar = estatus[1]
						monedasDispensadas = estatus[2]
						monedasFaltantes = estatus[3]
						if monedasFaltantes:
							MONEDAS.append(moneda)
							cambioSolicitado = cambioSolicitado + (monedasFaltantes*moneda)
							#print("monedas por pagar de ",moneda,": ",monedasPorPagar)
							print("monedas enrtegadas de ",moneda,": ",monedasDispensadas)
							cambioRestante = cambioRestante - (monedasDispensadas*moneda)
							print("Cambio incompleto , faltan ",monedasFaltantes," de $",moneda, "Restante: ",cambioRestante)
							resetHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
							habilitarHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
						else:
							#print("monedas pendientes en el pago de ",moneda,": ",monedasDispensadas)
							cambioRestante = cambioRestante - (monedasDispensadas*moneda)
							print("monedas enrtegadas de ",moneda,": ",monedasDispensadas)
							print("monedas faltantes: ",monedasFaltantes," monedas",MONEDAS,"Cambio Restante:",cambioRestante)
							#HOPPER_MONEDAS_DISPENSADAS.update({})

					else: 
						print("Hopper ",HOPPER_MONEDAS_HABILITADAS[moneda],"No puede dar cambio: Deshabilitado")

				else:
					print("No se pudo obtener el status")
			else:
					resetHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
					habilitarHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
					print("No se entrego el cambio, Hopper",HOPPER_MONEDAS_HABILITADAS[moneda],"Deshabilitado,","Faltaron",cambio,"monedas de $",moneda)
					#cambioRestante = cambioRestante+(cambio*moneda)


			#-------------VERIFICACION FINAL DEL STATUSHOPPER ---------------
			

			'''
			estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
			print("ultima moneda: ",moneda,cambioSolicitado,estatus,estatus[1],cambioSolicitado)
			if estatus:
				if estatus[3]:
					cambioRestante = (estatus[3]*moneda)+cambioSolicitado
					resetHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
					habilitarHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
					print("Cambio restante...: ",cambioRestante,"Reiniciando hopper")
				else:
					if estatus[0]:

						cambioRestante = (estatus[3]*moneda)+cambioSolicitado
						print("Cambio restante...: ",cambioRestante,"est0")
						pass
					else:
						print("Cambio restante...: ",cambioRestante,"Reiniciando")
						resetHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
						habilitarHopper(HOPPER_MONEDAS_HABILITADAS[moneda])
			'''


			print("Cambio restante...: ",cambioRestante)


			
	print("Cambio restante: ",cambioRestante)
	return cambioRestante






	#exit(0)
	"""
	cambio10 = int(cambioSolicitado/10)
	if(cambio10):
		cambioSolicitado = cambioSolicitado%10
		cambioHopper(cambio10,HOPPER_MONEDAS_HABILITADAS[10])
		print("monedas solicitadas de 10:",cambio10)
		estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS[10])
		if estatus:
			monedasDispensadas = estatus[1]
			monedasFaltantes = estatus[2]
			if monedasFaltantes:
				print("Cambio incompleto , faltan ",monedasFaltantes," monedas")
			else:
				print("monedas enrtegadas de 10: ",monedasDispensadas)
		else:
			print("No se pudo obtener el status")


	cambio5 = int(cambioSolicitado/5)
	if(cambio5):
		cambioSolicitado = cambioSolicitado%5
		cambioHopper(cambio5,HOPPER_MONEDAS_HABILITADAS[5])
		print("monedas solicitadas de 5:",cambio5)
		estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS[5])
		if estatus:
			monedasDispensadas = estatus[1]
			monedasFaltantes = estatus[2]
			if monedasFaltantes:
				print("Cambio incompleto , faltan ",monedasFaltantes," monedas")
			else:
				print("monedas enrtegadas de 5: ",monedasDispensadas)
		else:
			print("No se pudo obtener el status")

	cambio1 = int(cambioSolicitado/1)
	if(cambio1):
		cambioSolicitado = cambioSolicitado%1
		cambioHopper(cambio1,HOPPER_MONEDAS_HABILITADAS[1])
		print("monedas solicitadas de 1:",cambio1)
		estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS[1])
		if estatus:
			monedasDispensadas = estatus[1]
			monedasFaltantes = estatus[2]
			if monedasFaltantes:
				print("Cambio incompleto , faltan ",monedasFaltantes," monedas")
			else:
				print("monedas enrtegadas de 1: ",monedasDispensadas)
		else:
			print("No se pudo obtener el status")
		

	
	
	statusHopper(HOPPER_MONEDAS_HABILITADAS[1])
	"""


def validarCctalk(respuesta,comando, hopperId, validacionExacta):
	lenRecepcion = len(respuesta)
	HEADER_LEN = 0
	CABAECERA_LEN = 3
	CHECKSUM_LEN = 1
	respuestaDecoded = []
	codigosValidacion = [[],[0x00],[0x00],noSeriesHoppers[hopperId],[0x00],[0x00],[0x00,0x00,0x00,0x00]]
	#print("longitud recepcion", lenRecepcion)
	if(lenRecepcion >= 2):
		numDatos = respuesta[1]
		if(numDatos >= 1):
			HEADER_LEN = 1
	else:
		print("Respuesta no valida: ", respuesta)
		return -1

	if(lenRecepcion == CABAECERA_LEN + len(codigosValidacion[comando]) + HEADER_LEN + CHECKSUM_LEN):

		respuesta = respuesta[:lenRecepcion-1]
		respuesta = respuesta[CABAECERA_LEN+HEADER_LEN:]
		#print("datos: ", respuesta)
		HEADER_LEN = 0
		for elem in respuesta:
			respuestaDecoded.append(elem)
		#print("respuestaDec / validacion ", respuestaDecoded, codigosValidacion[comando])

		if(respuestaDecoded == codigosValidacion[comando]):
			print("Datos validos: ",respuestaDecoded)
			return respuestaDecoded
		elif(not validacionExacta):
			if(len(codigosValidacion[comando]) == len(respuestaDecoded)):
				print("Datos validos CNE: ",respuestaDecoded)
				return respuestaDecoded
			else:
				print("Datos no validos CNE: ",respuestaDecoded)
				return -1
		else:
			print("Datos NO validos: ",respuestaDecoded,)
			#exit(0)
			return -1
	else:
		print("datos malformados ",lenRecepcion,CABAECERA_LEN,len(codigosValidacion[comando]),HEADER_LEN,CHECKSUM_LEN)
		return -1



def resetHopper(hopperId):
	############### RESET POLL  #################
	resetHopper = [hopperId, 0, 1, 1]
	lenresetHopper = len(resetHopper)+1
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, resetHopper)
	ser.write(a);
	time.sleep(.1)
	r = ser.read(20) #Verificar en el simulador se ven 19
	if r:
		print("resetHopper ", lenresetHopper, "HOPPER: ", hopperId, "Data:",r , len(r))
		r = r[lenresetHopper:]
		time.sleep(.01)
		validarCctalk(r,HOPPER_RESET,hopperId,VALIDACION_EXACTA)


def statusHopper(hopperId):

	############### RESET POLL  #################
	statusHopper = [hopperId, 0, 1, 166] 
	lenstatusHopper = len(statusHopper)+1
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, statusHopper)
	ser.write(a);
	time.sleep(.1)
	r = ser.read(20) #Verificar en el simulador se ven 19
	if r:
		#print("statusHopper ", lenstatusHopper, "HOPPER: ", hopperId)
		r = r[lenstatusHopper:]
		
		time.sleep(.01)
		estatus = validarCctalk(r,HOPPER_STATUS,hopperId,VALIDACION_INEXACTA)
		#print("Estatus Hopper ",hopperId,": ",estatus)
		return estatus



def habilitarHopper(hopperId):
	############### SIMPLE POLL  #################
	estado = 0
	
	if(estado == 0):
		simplePoll = [hopperId, 0, 1, 254]
		lensimplePoll = len(simplePoll)+1
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, simplePoll)
		ser.write(a);
		time.sleep(.1)
		r = ser.read(20) #Verificar en el simulador se ven 19
		print("simplePoll ", lensimplePoll, "HOPPER: ", hopperId)
		if r:
			r = r[lensimplePoll:]
			
			time.sleep(.01)
			validarCctalk(r,HOPPER_POLL,hopperId,VALIDACION_EXACTA)
			estado = 1

	############### ENABLE HOPPER  #################
	if(estado == 1):
		hopperEnable = [hopperId, 1, 1, 164, 165]
		lenhopperEnable = len(hopperEnable)+1
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, hopperEnable)
		ser.write(a);
		time.sleep(.1)
		r = ser.read(20) #Verificar en el simulador se ven 19
		if r:
			print("hopperEnable", lenhopperEnable, "HOPPER: ", hopperId)
			r = r[lenhopperEnable:]

			time.sleep(.01)
			validarCctalk(r,HOPPER_ENABLE,hopperId,VALIDACION_EXACTA)
			estado = 2

	############### SERIE HOPPER  #################
	if(estado == 2):
		serieHopper = [hopperId, 0, 1, 242]
		lenserieHopper = len(serieHopper)+1
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, serieHopper)
		ser.write(a);
		time.sleep(.1)
		r = ser.read(20) #Verificar en el simulador se ven 19
		if r:
			print("serieHopper", lenserieHopper, "HOPPER: ", hopperId)
			r = r[lenserieHopper:]
			time.sleep(.01)
			validarCctalk(r,HOPPER_SERIE,hopperId,VALIDACION_EXACTA)
			return 1


def cambioHopper(cambioSolicitado, hopperId):
	
	############### ENABLE HOPPER  #################
	#03 04 01 A7 8F BA 20 02 
	#05 04 01 A7 0A 8E 20 02
	serieHopper = noSeriesHoppers[hopperId]
	dispenseHopper = [hopperId, 4, 1, 167, serieHopper[0], serieHopper[1], serieHopper[2], cambioSolicitado]
	lendispenseHopper = len(dispenseHopper)+1
	dispenseHopper = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, dispenseHopper)
	ser.write(dispenseHopper);
	#time.sleep(.01)
	time.sleep(.1)
	r = ser.read(20) #Verificar en el simulador se ven 19
	if r:
		#print("longitud comando ", lendispenseHopper)
		r = r[lendispenseHopper:]
		#time.sleep(.01)
		validacion = validarCctalk(r,HOPPER_DISPENSE,hopperId,VALIDACION_EXACTA)
		return validacion


	#cambioSolicitado = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, [3, 0, 1, 254])
	#cambioSolicitado = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, [3, 0, 1, 254])

def cambioRecicladorMonedas(cambioSolicitado):
	cambioSolicitado = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [10, 1, 10, 0])

def cambioRecicladorBilletes(cambioSolicitado):
	cambioSolicitado = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [10, 1, 10, 0])
	


def estatusTubos(ser):
	#ESTATUS TUBOS
	global MONEDAS_POR_SW,suspenderCajero,cajeroSuspendido
	TUBOS = [0,0,0,0]
	while(1):
		time.sleep(.1) #Para completar los 500 ms
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [10, 1, 10, 0])
		ser.write(a);
		time.sleep(.01)
		r = ser.read(18) #Verificar en el simulador se ven 19
		print("estatusTubos",r)
		if(r):
			print("h", r[4],r[5],r[6],r[7],r)
			if (r[0] == 0):  # Verificar la respuesta <----------
				if(r.__sizeof__()>=30):
					if(r[4] == 0 or r[5] == 0 or r[6] == 0 or r[7] == 0):
						print("errinfo...")
						suspenderCajero=1
						if(cajeroSuspendido==1):
							suspenderCajero=0
							cs2=0
							return -1
					else:
						suspenderCajero=0
						cs2=0
						cajeroSuspendido=0
						print("Estatus de Llenado de Tubo: ", r[0], r[1]) #Verificar si se debe imprimir en Decimal o Ascii
						mm1=r[4]
						mm2=r[5]
						mm3=r[6]
						mm4=r[7]
						TUBOS[0] = r[4]
						TUBOS[1] = r[5]
						TUBOS[2] = r[6]
						TUBOS[3] = r[7]
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);
						return TUBOS

def count(ser, estadoConexion):
	global MONEDAS_POR_SW,MONEDAS_POR_HW,registraPago,comienzaCobro,comienzaCambio,Sinpago,DA,costillo,cajeroSuspendido,cs2,suspenderCajero,cp,total,bill,cambio,tarifa,aux_cambio,killbill,pagado,monedas,monedasTotal,dineroTotal,nivelDeCambio,imprime,monedasPago,billetesPago,NoCajero,tarifasAplicadas,fechaAMD,fo,pe,h,monedasCambio
	i=-1
	#DA=DA+costillo
	descripcionMonedas=""
	descripcionBilletes=""
	descripcionMonedasCambio=""
	estatus_cambio = 0
	CODIGO_ERROR = 0
	
	comienzaCobro=1
	registraPago=0
	if(cp==1):
		cambio = total - aux_tarifa
		cambio=aux_tarifa+cambio
		print("-.-.-.-.-.cancelando pago")
	else:
		cambio = total - aux_tarifa
	aDar=0
	desconteo=0
	aux_cambio = cambio
	mm1=0
	mm2=0
	mm3=0
	mm4=0
	mmc=0
	

	


	if (cambio > 0):
		cambioRestante = solicitarCambio(cambio)
		cambio = cambioRestante
		print("Cambio Restante: ",cambioRestante,cambio)

	if (cambio > 0):
		print("hay cambio")
		imprime=1
		comienzaCambio=1
		time.sleep(1)
		#dineroTotal=dineroTotal+aux_tarifa
		#disable_sequence(ser)
		'''#print(ser.inWaiting())
		ser.limpiar()
		#ser.flushInput()'''
		
		MONEDAS_TMP = estatusTubos(ser)
		#print("Monedas previo al cambio: ",MONEDAS_TMP)

		if(cajeroSuspendido==1):
			registraPago=1
			killbill = 1
			pagado=2
			
		else:
			while(1):
				if(cambio<=20):
					#pagado=1
					if(cambio!=0):
						darCambio(ser,cambio)
					killbill = 1
					pagado=2
					break
				else:
					darCambio(ser,20)
					cambio=cambio-20
			
			MONEDAS_POR_HW = estatusTubos(ser)
			MONEDAS_TMP[0] = MONEDAS_TMP[0] - MONEDAS_POR_HW[0]
			MONEDAS_TMP[1] = MONEDAS_TMP[1] - MONEDAS_POR_HW[1]
			MONEDAS_TMP[2] = MONEDAS_TMP[2] - MONEDAS_POR_HW[2]
			MONEDAS_TMP[3] = MONEDAS_TMP[3] - MONEDAS_POR_HW[3]
			
			#print("Monedas dispensadas como cambio: ",MONEDAS_TMP)
			monedasCambio = MONEDAS_TMP
			
			MONEDAS_POR_SW[0] = MONEDAS_POR_SW[0] - MONEDAS_TMP[0]
			MONEDAS_POR_SW[1] = MONEDAS_POR_SW[1] - MONEDAS_TMP[1]
			MONEDAS_POR_SW[2] = MONEDAS_POR_SW[2] - MONEDAS_TMP[2]
			MONEDAS_POR_SW[3] = MONEDAS_POR_SW[3] - MONEDAS_TMP[3]
			
			
			
			
			
		if(cp==1):
			print("Pago canceladoA")
			#cp=0
		else:
			registraPago=1
	#print("1111cp",cp," registrapago-",registraPago,"CAMBIO...",cambio)
	if(cambio==0): # if(total==aux_tarifa):
		imprime=1
		killbill = 1
		comienzaCambio=1
		time.sleep(.05)
		pagado=2
		if(cp==1):
			print("Pago cancelado")
			#cp=0
			
		else:
			registraPago=1
		disable_coin(ser)
		disable_sequence(ser)
		comunicacionJcm(INHIBIT_SETTING_DISABLE_JCM)

	"""
	Se obtiene los datos de la operacion para su registro
	"""
	datosOperacion=str(fo) + "," + str(pe) + "," + fechaAMD +" "+h
	datosOperacionBD=str(fo) + "," + str(pe) + "," + "'"+str(fechaAMD)+" "+str(h)
	descripcionMonedas = obtenerDescripcion(monedasPago)
	descripcionBilletes = obtenerDescripcion(billetesPago)
	descripcionMonedasCambio = obtenerDescripcion(monedasCambio)
	cambio_faltante = compararCambio(monedasCambio,aux_cambio)
	print("Datos Operacion: ",datosOperacion)
	print("Monto cobrado: ",aux_tarifa)
	print("Monedas recibidas: ",descripcionMonedas)
	print("Billetes recibidos: ",descripcionBilletes)
	print("Cambio solicitado: ",aux_cambio)
	print("Cambio entregado (Monedas): ",descripcionMonedasCambio)
	print("Cambio entregado (Billetes): ","0:0")
	if(cambio_faltante):
		print("Cambio incompleto, falto: ",cambio_faltante)
		print("Intentando dispensar faltante: ","0:0")
		CODIGO_ERROR = 1
	else:
		print("Operacion exitosa.",cambio_faltante)
		CODIGO_ERROR = 0
		

	if registraPago:
		if not cambio_faltante :
			if not cajeroSuspendido:
				CODIGO_ERROR = OP_EXITOSA
			else:
				CODIGO_ERROR = OP_EXITOSA_SUSPENDIDO
		else:
			if not cajeroSuspendido:
				CODIGO_ERROR = OP_CAMBIO_INCOMPLETO
			else:
				CODIGO_ERROR = OP_CAMBIO_INCOMPLETO_SUSPENDIDO
		
		#REGISTRAR PAGO EN SERVIDOR
		#idcaj,mediopago,monto, descripcion de las monedas pagadas, descripcion de los billetes pagados, tarifas implementadas
		registrarPagoActual(cp, NoCajero, aux_cambio, aux_tarifa, costillo, datosOperacionBD, estadoConexion, descripcionMonedas, descripcionBilletes, descripcionMonedasCambio, 0, CODIGO_ERROR)

		
	else:
		if not cambio_faltante :
			if not cajeroSuspendido:
				CODIGO_ERROR = OP_CANCELADA
			else:
				CODIGO_ERROR = OP__CANCELADA_SUSPENDIDO
		else:
			if not cajeroSuspendido:
				CODIGO_ERROR = OP_CANCELADA_CAMBIO_INCOMPLETO
			else:
				CODIGO_ERROR = OP_CANCELADA_CAMBIO_INCOMPLETO_SUSPENDIDO
				
				
		
		print("ids: ",aux_tarifa,aux_cambio)
		registrarPagoActual(cp, NoCajero, aux_cambio, aux_tarifa, costillo, datosOperacionBD, estadoConexion, descripcionMonedas, descripcionBilletes, descripcionMonedasCambio, 0, CODIGO_ERROR)
	
	monedasPago[0]=0
	monedasPago[1]=0
	monedasPago[2]=0
	monedasPago[3]=0
	billetesPago[0]=0
	billetesPago[1]=0
	billetesPago[2]=0
	billetesPago[3]=0
	monedasCambio[0]=0
	monedasCambio[1]=0
	monedasCambio[2]=0
	monedasCambio[3]=0
	tarifasAplicadas=""
	print("",DA,"cp",cp," registrapago-",registraPago)
	

def registrarBoleto(NoCajero, aux_cambio, aux_tarifa, costillo, datosOperacionBD, estadoConexion, descripcionMonedas, descripcionBilletes, descripcionMonedasCambio, tipo):
	if(estadoConexion):
		#REGISTRA PAGO EN BD SERVIDOR
		print("******SOLICITANDO PAGO AL SERVIDOR*******      ",datosOperacion)
		#mensaje=str(NoCajero)+";"+"1"+";"+str(aux_tarifa)+";"+descripcionMonedas+";"+descripcionBilletes+";"+tarifasAplicadas
		if(tarifasAplicadas==""):
			tarifasAplicadas="13"
			
def registrarPagoActual(cp, NoCajero, aux_cambio, aux_tarifa, costillo, datosOperacionBD, estadoConexion, descripcionMonedas, descripcionBilletes, descripcionMonedasCambio, tipo, CODIGO_ERROR):
	print("Solocitando registro del pago",datosOperacionBD)
	respuestaServidor = 0
	if(estadoConexion):
		#REGISTRA PAGO EN BD SERVIDOR
		#mensaje=str(NoCajero)+";"+"1"+";"+str(aux_tarifa)+";"+descripcionMonedas+";"+descripcionBilletes+";"+tarifasAplicadas
		tarifasAplicadas="13"			
		#mensaje=str(NoCajero)+";"+"1"+";"+str(costillo)+";"+str(DA)+";"+descripcionBilletes+";"+descripcionMonedasCambio+";"+str(tarifasAplicadas)
		mensaje=str(NoCajero)+";"+"1"+";"+str(costillo)+";"+str(descripcionMonedas)+";"+descripcionBilletes+";"+descripcionMonedasCambio+";"+str(tarifasAplicadas)
		print("Mensaje pago: ,tarifasAplicadas ",mensaje,tarifasAplicadas)
		if(cp):
			print("Pago cancelado")
		else:
			respuestaServidor=Servidor.configSocket("pago boleto", datosOperacionBD+"*"+mensaje)
			if(respuestaServidor==-1):
				Sinpago=Sinpago+1
			#s.send("1;1;20.00;2:5,1:10;0:0;2,5".encode('utf-8'))
	else:
		respuestaServidor = 0
		
	#REGISTRA PAGO EN BD INTERNA
	consu="insert into \"PAGOS\"(\"idBoleto\",expedidora,\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes, cambio_entregado, tipo) values("+datosOperacionBD+"'"+","+str(CODIGO_ERROR)+","+str(respuestaServidor)+","+str(aux_tarifa)+","+str(aux_cambio)+",'"+str(descripcionMonedas)+"','"+str(descripcionBilletes)+"','"+str(descripcionMonedasCambio)+"',"+str(0)+")"
	cur.execute(consu)
	conn.commit()
	
	
	

def compararCambio(cambioEntregado,cambioSolicitado):
	valorCambio=0
	i=-1
	if(cambioEntregado[0]==0 and cambioEntregado[1]==0 and cambioEntregado[2]==0 and cambioEntregado[3]==0):
		valorCambio=0
	else:
		for item in cambioEntregado:
			i=i+1
			if(item!=0):
				valorCambio=valorCambio+(item*valoresMonedas[i])
				
	print("comparativa cambio solicitado/entregado: ", cambioSolicitado,valorCambio)
	return cambioSolicitado - valorCambio
	
def obtenerDescripcion(lista):
	descripcion=""
	i=-1
	if(lista[0]==0 and lista[1]==0 and lista[2]==0 and lista[3]==0):
		descripcion="0:0"
	else:
		for item in lista:
			i=i+1
			if(item!=0):
				descripcion=descripcion+str(item)+":"+str(valoresMonedas[i])+","
	descripcion=descripcion.rstrip(',')
	return descripcion
def darCambioManual(ser,valor):
	while(1):
		time.sleep(.05)
		print(valor,"<--- aDar")
		ba = [0x0D, int(valor)]
		ckInt = checkSum(ba)

		"""
		ser.parity = change_parity(0x0D, 1)
		ser.write(b'\x0D')
		ser.parity = change_parity(int(valor), 0)
		ser.write(bytes([int(valor)]))
		ser.parity = change_parity(int(ckInt), 0)
		ser.write(bytes([int(ckInt)]))

		time.sleep(.05)
		ser.parity = change_parity(0x0B, 1)
		ser.write(b'\x0B')
		ser.parity = change_parity(0x0B, 0)
		ser.write(b'\x0B')
		time.sleep(.005)
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [13, 1, valor, 0, ckInt, 0])
		ser.write(a);
		time.sleep(.01)

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
		ser.write(a);
		time.sleep(.01)



		k = ser.read(4)
		if(k):
			print(k)
			if(k.__sizeof__()==18):
				if(k[0]==2):
					print("insistir",k)
					break
			if(k.__sizeof__()==19):
				if(k[0]==2 or k[1]==2):
					print("insistir",k)
					break
			if(k.__sizeof__()==20):
				if(k[0]==2 or k[1]==2 or k[2]==2):
					print("insistir",k)
					break
	while(1):
		"""
		ser.parity = change_parity(0x0B, 1)
		ser.write(b'\x0B')
		ser.parity = change_parity(0x0B, 0)
		ser.write(b'\x0B')
		time.sleep(.005)
		"""
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
		ser.write(a);
		time.sleep(.01)


		k = ser.read(3)
		print("poll",k)
		if(k):
			if(k[0]==0):
				print("roto")
				time.sleep(.005)
				break


def darCambio(ser,monto):
	while(1):
		print("NO")
		global total,cambio
		#print(monto)
		dar=monto/factorDeEscala
		print(dar)
		ba = [0x0F, 0x02, int(dar)]
		ckInt = checkSum(ba)
		#print("cambio->", cambio, "check->", ckInt)


		"""
		ser.parity = change_parity(0x0F, 1)
		ser.write(b'\x0F')
		ser.parity = change_parity(0x02, 0)
		ser.write(b'\x02')
		ser.parity = change_parity(int(dar), 0)
		ser.write(bytes([int(dar)]))
		ser.parity = change_parity(int(ckInt), 0)
		ser.write(bytes([int(ckInt)]))
		time.sleep(.009)
		ser.parity = change_parity(0x0B, 1)
		ser.write(b'\x0B')
		ser.parity = change_parity(0x0B, 0)
		ser.write(b'\x0B')
		time.sleep(.005)
		"""
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 2, 0, int(dar), 0, int(ckInt), 0])
		ser.write(a);
		time.sleep(.01)

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
		ser.write(a);
		time.sleep(.01)




		k = ser.read(3)

		if(k):

			print(k)
			if(k.__sizeof__()>18):

				if(k[0]==2 or k[1]==2):
					print("Comenzando pago..",k)

					break
	while(1):
		"""
		ser.parity = change_parity(0x0B, 1)
		ser.write(b'\x0B')
		ser.parity = change_parity(0x0B, 0)
		ser.write(b'\x0B')
		time.sleep(.005)
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
		ser.write(a);
		time.sleep(.01)

		k = ser.read(6)
		print("poLL",k)
		if(k):
			if(k[0]!=2):
				palPoll(ser,k[0], k)
				if(k[0]==0):
					print("roto")
					time.sleep(.005)
					break
				else:
					ser.SECUNCIA_COBRO = 2()
					#ser.flushInput()
					print("Error al finalizar el pago...")

					"""
					ser.parity = change_parity(0x00, 0)
					ser.write(b'\x00')
					"""
					a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
					ser.write(a);
					time.sleep(.01)





			#if(k[0]==0):
			#	break;


def change_parity(comando,paridad):
	b=128
	cont=0
	while b!=0 :
		if b&comando!=0:
			cont=+cont+1
		b=b>>1
	if paridad == 1:
		if cont % 2 == 0:
			return serial.PARITY_ODD
		else:
			return serial.PARITY_EVEN
	elif paridad == 0:
		if cont % 2 == 0:
			return serial.PARITY_EVEN
		else:
			return serial.PARITY_ODD

def checkSum(arr):
	j=0
	sum=0
	tam=arr.__len__()
	while(j<tam):
		#print(j, tam)
		sum=sum+arr[j]
		print(sum)
		j=j+1	
	return 255&sum



def clicks():
	#Leyendo stream de video...
	time.sleep(5)
	time.sleep(10)
	print("Click 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
	os.system("xdotool click 1")
	time.sleep(3)


def streaming():
	#Leyendo stream de video...
	time.sleep(5)
	time.sleep(3)
	print("Click 0000000000000000000000000000000000000000000000000000000000000000000000000000000000")
	os.system("xdotool click 1")
	time.sleep(3)
	try:
		os.system("vlc http://192.168.1.129:8080 --fullscreen")
		time.sleep(15)
		os.system("xdotool click 3")
		print("Click 111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
	except:
		print("error en el stream")
	time.sleep(5)
	time.sleep(3)
	print("Click 22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
	os.system("xdotool click 1")
	time.sleep(3)



def leerCodQR2():
	global camInicial
	#time.sleep(1)
	lee2 = os.system("sudo find /dev -name 'video*' > cam.txt")
	a = open("cam.txt", "r")
	cam=(a.readline().rstrip("\n")).lstrip("\x00")
	a.close()
	a = open("cam.txt", "w")
	a.write('')
	camInicial=cam
	print('CamInicial',camInicial)
	while(1):
		time.sleep(1)
		lee2 = os.system("sudo find /dev -name 'video*' > cam.txt")
		a = open("cam.txt", "r")
		cam=(a.readline().rstrip("\n")).lstrip("\x00")
		a.close()
		a = open("cam.txt", "w")
		a.write('')
		print('Cam',cam,camInicial)
		if(cam==camInicial):

			try:
				#print('Camara Detectada')
				lee = os.system("zbarcam --raw --prescale=280x150   "+cam+" > /home/cajero/Documentos/ticket.txt")
				#lee = os.system("zbarcam --raw  --prescale=10x10 /dev/video0 > /home/cajero/Documentos/eum/app/caseta/ticket.txt")
				#lee = os.system("/home/cajero/Documentos/eum/app/caseta/dsreader -l 27 -b 14 -r 30 -s 100 -u 50  > /home/cajero/Documentos/eum/app/caseta/ticket.txt")
				#lee = os.system("cd /home/cajero/scanner/dsreader")
				#lee = os.system("./dsreader -l 27 -b 14 -r 30 -s 100 -u 50  > /home/cajero/Documentos/eum/app/caseta/ticket.txt")

			except e:
				mensajeTolerancia=1
				#print("Error al crear el socket: ",e)
		else:
			
			if(cam!=''):
				camInicial=cam
			else:
				#print('Camara desconectada')
				pass


def reiniciarComuicacion():
	global ser
	#STAKER
	print("RESET SERIAL")
	TON_02 = Temporizador("RESET ARDUINO", 4)
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.RESET)
	ser.write(a);
	while(1):
		TON_02.entrada = not TON_02.salida
		TON_02.actualizar()
		print("tiempo transcurrido: ",TON_02.tiempoActual,TON_02.salida,TON_02.tiempo)
		if TON_02.salida:
			print("FIN RESET")
			ser = abrirPuerto()
			return 1




def disable_sequence(ser):
#Bill-type-
	print("Bill-Type-disable")
	while(1):
		time.sleep(1)
		"""
		ser.parity = change_parity(0x34, 1)
		ser.write(b'\x34')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x34, 0)
		ser.write(b'\x34')
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [52, 1, 0, 0, 0, 0, 0, 0, 0, 0, 52, 0])
		ser.write(a);
		time.sleep(.01)


		ask = ser.read(1)
		print(ask)
		if (ask):
			if(ask==b'\x00'):
				time.sleep(.25)
		break


def iniciarTemporizador(TON):

	TON.entrada = not TON.salida
	TON.actualizar()
	print("tiempo transcurrido: ",TON.tiempoActual,TON.salida,TON.tiempo)
	if TON.salida:
		print("secuencia no completada: ",TON.nombre)
		return True
	else:
		return False
			
		

def abrirPuerto():
	global ser
	ser = serial.Serial(obtenerNombreDelPuerto(dispositivo = Botones.PUERTO_ARDUINO_MICRO))  # Open named port
	ser.baudrate = 9600  # Set baud rate
	ser.parity = serial.PARITY_NONE
	ser.stopbits = serial.STOPBITS_ONE
	ser.bytesize = serial.EIGHTBITS
	#ser.timeout = 0
	#ser.timeout = .005
	#ser.timeout = .005 tiempo raspberry
	ser.timeout = .005
	return ser



def limpiar():
	serJCM.flushOutput()
	serJCM.flushInput()



def comunicacionJcm(comandoJcm):
	limpiar()
	#print(comandoJcm)
	comandoCRC = CRC(comandoJcm)
	comandoJcm.append(comandoCRC.crc_l())
	comandoJcm.append(comandoCRC.crc_h())
	
	lencomando = len(comandoJcm)+1
	#a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, comandoJcm)
	#ser.write(a);
	serJCM.write(comandoJcm)
	comandoJcm.pop()
	comandoJcm.pop()
	time.sleep(.1)
	r = serJCM.read(20) #Verificar en el simulador se ven 19
	trama = ''
	for data in r:
		trama = trama + hex(data)+ ' '
	print("comandoJcm ",comandoJcm, "Res:",r)
	print(trama)
	print('')
	#exit(0)
	#r = r[lencomando:]
	
	#time.sleep(.01)
	return r


def secuenciaJCMAcceptor():

	comunicacionJcm(STATUS_REQUEST_JCM)
	comunicacionJcm(STATUS_REQUEST_JCM)
	comunicacionJcm(RECYCLER_SOFTWARE_VERSION_REQUEST_JCM)
	
	#comunicacionJcm(UNIT_INFORMATION_REQUEST_JCM)
	
	comunicacionJcm(RESET_JCM)
	comunicacionJcm(STATUS_REQUEST_JCM)
	#comunicacionJcm(COMUNICATION_MODE_SETTING_JCM)

	comunicacionJcm(REQUEST_STATUS_ENABLE)
	comunicacionJcm(ENABLE_SETTING_JCM)
	comunicacionJcm(SECURITY_SETTING_JCM)
	comunicacionJcm(OPTIONAL_FUNCTION_SETTING_JCM)
	comunicacionJcm(INHIBIT_SETTING_JCM)

	#comunicacionJcm(RECYCLE_CURRENCY_REQUEST_JCM)
	#comunicacionJcm(STATUS_REQUEST_JCM)


	#comunicacionJcm(RECYCLE_CURRENCY_SETTING_JCM)
	#comunicacionJcm(RECYCLE_COUNT_SETTING_JCM)
	comunicacionJcm(STATUS_REQUEST_JCM)
	comunicacionJcm(STATUS_REQUEST_JCM)
	#exit(0)
	operacionesControl()

def secuenciaJCMRecyclerManual():
	comunicacionJcm(STATUS_REQUEST_JCM)
	comunicacionJcm(STATUS_REQUEST_JCM)
	comunicacionJcm(RECYCLER_SOFTWARE_VERSION_REQUEST_JCM)
	
	#comunicacionJcm(UNIT_INFORMATION_REQUEST_JCM)
	
	comunicacionJcm(RESET_JCM)
	comunicacionJcm(STATUS_REQUEST_JCM)
	#comunicacionJcm(COMUNICATION_MODE_SETTING_JCM)
	comunicacionJcm(ENABLE_SETTING_JCM)
	#comunicacionJcm(SECURITY_SETTING_JCM)
	#comunicacionJcm(OPTIONAL_FUNCTION_SETTING_JCM)
	comunicacionJcm(INHIBIT_SETTING_JCM)

	#comunicacionJcm(RECYCLE_CURRENCY_REQUEST_JCM)
	#comunicacionJcm(STATUS_REQUEST_JCM)


	#comunicacionJcm(RECYCLE_CURRENCY_SETTING_JCM)
	comunicacionJcm(RECYCLE_COUNT_SETTING_JCM_1)
	comunicacionJcm(STATUS_REQUEST_JCM)
	comunicacionJcm(STATUS_REQUEST_JCM)
	comunicacionJcm(RECYCLE_COUNT_SETTING_JCM_2)
	comunicacionJcm(STATUS_REQUEST_JCM)
	comunicacionJcm(STATUS_REQUEST_JCM)

	#exit(0)
	#operacionesControl()

	#exit(0)
	#operacionesControl()
def operacionesControl():
	global total,SECUENCIA_COBRO
	contador = 0
	ct_max = 3

	INSTRUCCIONES = ["A_MON","A_BIL","CAMBIO","CHECK_SENSOR"]

	
	#0000 0000

	SECUENCIA_INICIO = 1  
	SECUENCIA_TICKET = 2
	SECUENCIA_PAGO = 4
	SECUENCIA_CAMBIO = 8
	ESTADO_ACEPTACION = 0
	TON_01 = Temporizador("TON_01",.2)
	while(True):
		TON_01.entrada = not TON_01.salida
		TON_01.actualizar()
		if TON_01.salida:
			contador+=1
			if( contador >= ct_max):
				contador = 0 
			serJCM.flushOutput()
			serJCM.flushInput()
			#print("-----------------contador: ---------------",contador,SECUENCIA_COBRO)
			
			
			#if contador == 1:
			if contador == 1 and SECUENCIA_COBRO == 0:
				#pass

				data = comunicacionJcm(STATUS_REQUEST_JCM)
				if len(data) > 4:
					print('ESTADO_ACEPTACION',ESTADO_ACEPTACION,data[2])
					if data[2] == 19 and ESTADO_ACEPTACION == 0: # Esperando ESCROW (Deteccion de Billete) 16/19
						ESTADO_ACEPTACION = 1
						if data[3] == 98:
							total = total + 20
						if data[3] == 99:
							total = total + 50
						if data[3] == 100: 
							total = total + 100
						if data[3] == 101:
							total = total + 200
						if data[3] == 102:
							total = total + 500


						r = comunicacionJcm(STACK_2_JCM)
						print('STACK_2')
						if len(r) > 4:
							if r[2] == 80 and ESTADO_ACEPTACION == 1: # Esperando ACK
								print('ACK RECIVED')
								ESTADO_ACEPTACION = 2
					#elif data[2] == 80 and ESTADO_ACEPTACION == 0: # Esperando ACK
					#	print('ACK RECIVED')
					#	ESTADO_ACEPTACION = 2

					#NOTA: EN RECYCLER SI MANDA STATUS "STACKING" (20)
					elif data[2] == 20 and ESTADO_ACEPTACION == 2: # Esperando STACKING  20
						print('STACKING RECIVED')
						ESTADO_ACEPTACION = 3
					elif data[2] == 21 and ESTADO_ACEPTACION == 2: # Esperando VEND VALID  16/21
						ESTADO_ACEPTACION = 4
						print('VEND VALID')
						#r = comunicacionJcm(ACK_JCM)
						r = comunicacionJcm(ACK_JCM2)
						print('ACK',r)
						
						
						#r = comunicacionJcm(ACK_JCM)

					elif data[2] == 22 and ESTADO_ACEPTACION == 4: # Esperando STACKED  22
						ESTADO_ACEPTACION = 0
						print('-----------------------secuencia de aceptacion completada------')

			if contador == 2 and SECUENCIA_COBRO == 2:
				print('-----------------------iniciando secuencia de pago------')
				if ESTADO_ACEPTACION == 2:
					data = comunicacionJcm(STARUS_REQUEST_EXTENSION_JCM)
				else: 
					data = comunicacionJcm(STATUS_REQUEST_JCM)
				if len(data) > 4:
					print('ESTADO_PAGO',ESTADO_ACEPTACION)
					if ESTADO_ACEPTACION == 0: # Esperando ESCROW (Deteccion de Billete) 19
						ESTADO_ACEPTACION = 1
						r = comunicacionJcm(INHIBIT_SETTING_DISABLE_JCM)
						#r = comunicacionJcm(INHIBIT_SETTING_JCM)
						print('INHIBING...', r)
					elif ESTADO_ACEPTACION == 1: # Esperando ACK
						ESTADO_ACEPTACION = 2
					elif data[4] == 16 and ESTADO_ACEPTACION == 2: # Esperando Estatus Normal  data[4]  16 !!!
						print('PAY OUT')
						r = comunicacionJcm(PAY_OUT_JCM)
						if r[2] == 80: # Esperando ACK
							print('ACK RECIVED')
							ESTADO_ACEPTACION = 3
						

					 #elif data[2] == 80 and ESTADO_ACEPTACION == 3: # Esperando ACK
					#	ESTADO_ACEPTACION = 4


					elif data[2] == 32 and ESTADO_ACEPTACION == 3: # Dispensando billete(s)
						print('Dispensando billete(s)')

					elif data[2] == 36 and ESTADO_ACEPTACION == 3: # Billete esperando a ser retirado
						print('Billete esperando a ser retirado')

					elif data[2] == 35 and ESTADO_ACEPTACION == 3: # Esperando PAY VALID  
						ESTADO_ACEPTACION = 4
						
						r = comunicacionJcm(ACK_JCM2)
						print('ACK',r)

					elif data[2] == 32 and ESTADO_ACEPTACION == 4: #  Esperando PAYING (Buscando mas biletes por pagar)
						ESTADO_ACEPTACION = 3
						print('Dispensando billete(s)')

					elif data[2] == 26 and ESTADO_ACEPTACION == 4: # Esperando DISABLE(INHIBIT)  22
						ESTADO_ACEPTACION = 0
						SECUENCIA_COBRO = 0
						print('Secuencia de pago completada')

#MAIN
if __name__ == "__main__":
	#global ser
	os.system("echo eum | sudo -S chmod 777 /dev/ttyUSB*")
	time.sleep(3)

	ba = [0x04,0x04,0x01,0xA7,0x00,0x8E,0x20,0x02]
	ckInt = checkSum(ba)
	print("checksum: ",256-(ckInt%256))

	comunicacion = Comunicacion ()
	"""
	ser = PuertoSerie ("PuertoSerie")
	ser.modificarConfiguracion (dispositivo = PuertoSerie.PUERTO_ARDUINO_MICRO, baudrate = 9600)
	ser.start()
	ser.abrirPuerto()
	"""




	#ser = abrirPuerto()
	ser = PuertoSerie ("PuertoSerie",dispositivo = PuertoSerie.ARDUINO_MICRO)
	ser.abrirPuerto()

	serJCM = serial.Serial("/dev/ttyUSB0")  # Open named port
	serJCM .baudrate = 9600  # Set baud rate
	serJCM .parity = serial.PARITY_EVEN
	serJCM .stopbits = serial.STOPBITS_ONE
	serJCM .bytesize = serial.EIGHTBITS
	serJCM .timeout = .005
	
	#reiniciarComuicacion()
	SECUENCIA_COBRO = 0

	RESET_JCM = [252, 5, 64]
	ACK_JCM = [252, 5, 80]
	ACK_JCM2 = [252, 5, 80, 170, 5, 0, 252, 5, 11, 39, 86]
	STACK_1_JCM = [252, 5, 65]
	STACK_2_JCM = [252, 5, 66]
	STACK_3_JCM = [252, 5, 73]
	ENABLE_SETTING_JCM = [252, 7, 192, 81, 255]
	#ENABLE_SETTING_JCM = [252, 7, 192, 63, 0]
	REQUEST_STATUS_ENABLE = [252, 5, 128]

	SECURITY_SETTING_JCM = [252, 7, 193, 255, 0]
	COMUNICATION_MODE_SETTING_JCM = [252, 6, 194, 0]
	OPTIONAL_FUNCTION_SETTING_JCM = [252, 7, 197, 255, 0]

	INHIBIT_SETTING_JCM = [252, 6, 195, 0]
	INHIBIT_SETTING_DISABLE_JCM = [252, 6, 195, 63]
	STATUS_REQUEST_JCM = [252, 5, 17]


	PAY_OUT_JCM = [252, 9, 240, 32, 74, 1, 1] # 1 Bill to dispense DATA 1: No. Bills  | Data 2: Denom


	#-----------------SETTING STATUS REQUEST (Extension)-------------
	STARUS_REQUEST_EXTENSION_JCM = [252, 7, 240, 32, 26]
	UNIT_INFORMATION_REQUEST_JCM =  [252, 5, 146]
	RECYCLE_CURRENCY_REQUEST_JCM = [252, 7, 240, 32, 144]
	RECYCLE_KEY_REQUEST_JCM = [252, 7, 240, 32, 145]
	RECYCLE_COUNT_REQUEST_JCM = [252, 7, 240, 32, 146]
	RECYCLER_SOFTWARE_VERSION_REQUEST_JCM = [252, 7, 240, 32, 147]

	#-----------------SETTING COMAND (Extension)-------------

	#RECYCLE_CURRENCY_SETTING_JCM = [252, 11, 240, 32, 208, 8, 0, 4, 0]
	RECYCLE_CURRENCY_SETTING_JCM = [252, 13, 240, 32, 208, 8, 0, 1, 4, 0, 2]
	#RECYCLE_CURRENCY_SETTING_JCM = [252, 13, 240, 32, 208, 8, 0, 1, 4, 0, 1]
	#FC 0B F0 20 90 08 00 04 00 

	#RECYCLE_COUNT_SETTING_JCM = [252, 11, 240, 32, 210, 0, 0, 0, 0]
	#FC 0B F0 20 92 00 00 00 00

	RECYCLE_COUNT_SETTING_JCM_1 = [252, 10, 240, 32, 210, 80, 0, 1]
	RECYCLE_COUNT_SETTING_JCM_2 = [252, 10, 240, 32, 210, 80, 0, 2]
	

	

	print("FIN RESET2")
	


	leerArch = open("/home/cajero/Documentos/ticket.txt", "w")
	leerArch.write('')
	leerArch.close()
	#pulsos = Botones("/dev/ttyUSB1", 3, 2)
	#pulsos = Botones("/dev/ttyUSB1", 3, 3, dispositivo = Botones.PUERTO_ARDUINO)
	conexion = Conexiones()
	cola = Pila()
	

	HOPPER_3 = 3
	HOPPER_4 = 4
	HOPPER_5 = 5
	HOPPER_6 = 6


	HOPPER_POLL = 1
	HOPPER_ENABLE = 2
	HOPPER_SERIE = 3
	HOPPER_DISPENSE = 4
	HOPPER_RESET = 5
	HOPPER_STATUS = 6


	HOPPER_MONEDAS_HABILITADAS = {10 : HOPPER_5, 5 : HOPPER_4, 1 : HOPPER_3 }

	
	noSeriesHoppers = [[],[],[],[0x8F,0xBA,0x20],[0x00,0x8E,0x20],[0x0A,0x8E,0x20]]

	
	VALIDACION_INEXACTA = 0
	VALIDACION_EXACTA = 1
	
	#time.sleep(20)

	secuenciaJCMRecyclerManual()
	resetHopper(int(HOPPER_3))
	resetHopper(int(HOPPER_4))
	resetHopper(int(HOPPER_5))

	habilitarHopper(int(HOPPER_3))
	habilitarHopper(int(HOPPER_4))
	habilitarHopper(int(HOPPER_5))
	
	#solicitarCambio(3)
	

	
	
	test = 1
	while(test != 0):
		test = int(input("Cambio a dispensar: "))
		#print("...Dispensando: ",test)
		solicitarCambio(test)
	
	'''
	cambioHopper(0,int(HOPPER_3))
	cambioHopper(2,int(HOPPER_4))
	cambioHopper(0,int(HOPPER_5))
	'''

	Init(ser)
	#enable_coin(ser)
	disable_sequence(ser)
	r = comunicacionJcm(INHIBIT_SETTING_DISABLE_JCM)

	#INICIALIZAMOS EL HILO DE LA INTERFAZ

	
	'''test = 1
	while(test != 0):
		test = int(input("Cambio a dispensar: "))
		#print("...Dispensando: ",test)
		solicitarCambio(test)
	'''

	

	thread1 = Thread(target=interface,args=())
	#time.sleep(5)
	thread3 = Thread(target=streaming, args = ())
	thread5 = Thread(target=clicks, args=())
	thread4 = Thread(target=leerArchivo, args=())
	control = Thread(target=operacionesControl, args=())
	
	#os.system("sudo nice -n -19 python3 archimp.py")
	try:

		#thread3.start()
		time.sleep(4)
		#thread5.start()
		control.start()
		time.sleep(.4)
		thread1.start()
		thread4.start()
		time.sleep(5)
		os.system("xprop -f _MOTIF_WM_HINTS 32c -set _MOTIF_WM_HINTS '0x2, 0x0, 0x0, 0x0, 0x0'")
		time.sleep(3)
		os.system("xdotool click 1")
		print("Click 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")


	except Exception as e:
		pass

	while(thread1.is_alive()):
		kill = 0
	kill = 1
	if(ser.is_open):
		ser.close()
	else:
		print("termine")
		exit(0)
	

