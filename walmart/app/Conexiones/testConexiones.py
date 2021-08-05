from Conexiones import Conexiones
import requests
import json,os,sys,time
from datetime import datetime

from urllib.request import urlopen



def main ():
	"""
	while True:
		conexion = conexiones.activo()
		print("conexion:",conexion)
		time.sleep (0.1)
	"""
		
	while True:
		try:
			conexion = conexiones.servidorActivo()
			print("conexion:",conexion)
			time.sleep (1)
		except:
			print("ocurrio un error")
if __name__ == "__main__":
	conexiones = Conexiones()
	main ()
