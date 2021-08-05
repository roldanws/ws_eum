# -*- coding: utf-8 -*-
"""
Estacionamientos unicos de México
Este archivo es para remplaar a acceso4.py
Funcion: 		Funcion de fecha
Descripcion:	Imprime la fecha con o sin formato (dia mes año)
				Imprime la hora  con o sin formato (hora:min:seg)
Funciones que se pueden usar:
	1)mostrarFechayHora()		muestra a fecha y hora
	2)mostrarHoraSinFormato()
	3)mostrarHoraConFormato
	4)mostrarFechaSinFormato
	5)mostrarFechaConFormato


"""

import time

horas_sin_formato		="%H"
minutos_sin_formato		="%M"
segundos_sin_formato	="%S"

dia_sin_formato			="%d "
mes_sin_formato			="%B"
mes_sin_formato_numero			="%m"
anio_sin_formato		="%Y"

def Tiempohoras():
	return time.strftime(horas_sin_formato)
	pass
	
def Tiempomin():
	return time.strftime(minutos_sin_formato)
	pass
	
def Tiemposeg():
	return time.strftime(segundos_sin_formato)
	pass

def FechaDia():
	return time.strftime(dia_sin_formato)
	pass
def FechaMes():
	return time.strftime(mes_sin_formato)
	pass
def FechaAnio():
	return time.strftime(anio_sin_formato)
	pass

def fechaConFormato():
	return time.strftime("%d/%m/%Y")
	pass

def tiempoConFormato():
	return time.strftime("%H:%M:%S")
	pass


def mostrarHoraSinFormato():
	""" horas sin formato"""
	h=[Tiempohoras(),Tiempomin(),Tiemposeg()]
	return h
	

def mostrarFechaConFormato():
	""" Fecha con formato dia/mes/año """
	fechaFormato=fechaConFormato()
	print ("La Fecha es: "+fechaFormato)
	return fechaFormato
	pass

def mostrarFechaSinFormato():
	""" Fecha sin formato"""
	dia=FechaDia()
	mes=FechaMes()
	anio=FechaAnio()
	print ("Dia:"+dia)
	print ("Mes:"+mes)
	print ("Año:"+anio)
	pass

	
def mostrarHoraConFormato():
	""" horas con formato hora:min:seg """
	tiempoFormato=tiempoConFormato()
	print ("La hora es : "+tiempoFormato)
	return tiempoFormato
	pass

def mostrarHoraSinFormato():
	""" horas sin formato"""
	h=[Tiempohoras(),Tiempomin(),Tiemposeg()]
	return h
	

def mostrarFechayHora():
	return time.strftime("%d/%m/%Y")+" "+time.strftime("%H:%M:%S")
	pass

#print mostrarFechayHora()
