
from django.shortcuts import render
from transaccion.models import Transaccion, Tienda
from equipo.models import Equipo, Tarifa
from datetime import datetime, timedelta
from django.db.models import Sum, Q, Count
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.views.generic.list import ListView


class Calculador:
    """
    Clase utulizada para administrar el cajero
    """
    
    def __init__(self):
        self.tarifa = ""
        self.descuento = ""
        
    def calcular_tarifa(self,fecha_ingreso,hora_ingreso, descuento):
        #-------------------- Seleccionar tarifa y extraer datos --------------------#

        tarifa = Tarifa.objects.filter(descuento=descuento)
        print("Tarifa encontrada: ",tarifa)
        if tarifa:
            indice = 0
            descuento = tarifa[0].descuento
            tiempo_base = tarifa[0].tiempo_base
            monto_base = tarifa[0].monto_base
            fraccion_tiempo = tarifa[0].fraccion_tiempo
            incremental = tarifa[0].incremental
            tarifa_seleccionada = tarifa[0].id
            # ( monto_base representa el descuento tipo 1 por el tiempo : tiempo_base )
            self.descuento = monto_base

            #-------------------- Calcular tiempo estacionado en minutos --------------------#
            resta = self.restar_hora(hora_ingreso,fecha_ingreso)
            dias = resta[0]
            segundos = resta[1]
            tiempo_estacionado = int(segundos/60)
            print("#-------------------- Informacion Boleto --------------------# ")
            print("tiempo_estacionado: {} dias con {} minutos".format(dias,tiempo_estacionado))
            if dias:
                tiempo_estacionado += dias*1440
            self.tiempo_estacionado = tiempo_estacionado
            print("minutos totales: {}".format(tiempo_estacionado))
            #-------------------- Calcular monto total en base a tiempo estacionado --------------------#
            monto_total = 0
            if tiempo_base > tiempo_estacionado:
                monto_total = monto_base
                self.monto_ingresar = monto_total
                return monto_total
            else:
                monto_total += monto_base
                tiempo_restante = tiempo_estacionado - tiempo_base
                fracciones_de_tiempo =  int(tiempo_restante/fraccion_tiempo)
                monto_total += fracciones_de_tiempo * incremental
                self.monto_ingresar = monto_total
                print("Fracciones: ",fracciones_de_tiempo)
                print("Monto a ingresar: ",self.monto_ingresar)
                return monto_total

    def restar_hora(self,horab,fechab):
        horab = horab.split(':',2)
        fechab = fechab.split('-')
        fechaBoleto = datetime.strptime(str(fechab[0]) + str(fechab[1]) + str(fechab[2]), '%Y%m%d').date()
        horaBoleto = datetime.strptime(str(horab[0]) +':'+str(horab[1]) +':'+ str(horab[2]), '%H:%M:%S').time()
        fechaActual=datetime.now().date()
        horaActual=datetime.now().time()
        horayFechaBoleto = datetime.now().combine(fechaBoleto, horaBoleto)
        horayFechaActual = datetime.now().combine(fechaActual, horaActual)
        restaFechas = horayFechaActual - horayFechaBoleto
        aux_dif=(str(restaFechas).split('.',1))[0]
        dias = int(restaFechas.days)
        segundos = restaFechas.seconds 
        return dias,segundos,aux_dif