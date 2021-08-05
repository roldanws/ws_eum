import Pila as pila
import requests
import json,os

from urllib.request import urlopen

def internet_on():
	try:
		conexionServ=os.system("ping -c 1 192.168.1.129")

		if conexionServ:
			return False
		else:
			return True
	except: 
		return False




p=pila.Pila()

payload = {
			"turno":"M",
			"boletaje": "0",
			"encargado": "1",
			}
p.incluir(payload)

payload = {
			"turno":"V",
			"boletaje": "143",
			"encargado": "33",
			}
			
p.incluir(payload)

payload = {
			"turno":"M",
			"boletaje": "111",
			"encargado": "3",
			}



print("Conectado: ",internet_on())
print(p.estaVacia())
p.incluir(payload)
print(p.inspeccionar())	
print(p.tamano())
print(p.estaVacia())
print(p.extraer())
print(p.extraer())
print(p.extraer())
print(p.tamano())
					
