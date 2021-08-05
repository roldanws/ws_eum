# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Sigfrido"
__date__ = "$23-jul-2019 13:39:03$"

class VariableTiempo ():
   
    def __init__(self):
        self.hora = 0
        self.minuto = 0
        self.segundo = 0
        self.dia = 0
        self.mes = 0
        self.anio = 0
        
    def obtenerTiempoActual ():
        c = datetime.now()
        
    def __str__(self):
        return ("")
        