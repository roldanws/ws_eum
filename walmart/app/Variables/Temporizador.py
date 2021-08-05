import time
import threading

class Temporizador():

    def __init__(self, nombre, tiempo, descripcion = ""):
            self.nombre = nombre
            self.descripcion = descripcion

            self.entrada = False
            self.salida = False
            self.reset = False

            self.tiempo = tiempo
            self.tiempoActual = 0

            self.bandera = False
            self.tiempo_Aux1 = 0
            self.tiempo_Aux2 = 0


            """
            self.hiloFuncionando = False
            hilo1 = threading.Thread(target=self.actualizarHilo)
            print ("Iniciado hilo TON")
            hilo1.start()""" 

    def actualizar (self):
        if self.entrada:
            if self.reset:
                self.salida = False
                self.bandera = False
                self.reset = False
                    
            if not self.bandera:
                self.bandera = True
                self.tiempo_Aux1 = time.time()
                            
            self.tiempo_Aux2 = time.time()
            self.tiempoActual = self.tiempo_Aux2 - self.tiempo_Aux1

            if self.tiempoActual > self.tiempo:
                            self.salida = True
        else:
            self.salida = False
            self.bandera = False
                        
    def iniciar (self, energizar):
        self.energizar = energizar
        #self.hiloFuncionando = False
        hilo1 = threading.Thread(target=self.actualizarHilo)
        print ("Iniciado hilo TON")
        hilo1.start()

    def actualizarHilo (self):
        self.hiloFuncionando = True
        while self.hiloFuncionando:
            self.actualizar()
            time.sleep (0.001)

            if not self.energizar.energizar:
                self.hiloFuncionando = False
            print ("TON ", self.entrada, self.tiempo, self.tiempoActual, self.salida)
        print ("Hilo terminado ", self.nombre)
        #print ("TON ", self.salida, self.tiempoActual)

    def stop (self):
        self.self.hiloFuncionando = False
                
    def __str__(self):
            return "%s->%s    %f %s %f %s" %(self.nombre, self.descripcion, self.tiempo, self.entrada, self.tiempoActual, self.salida)


def main ():
    
    TON_01 = Temporizador("TON_01", 16, "Tiempo de Prueba")
    TON_02 = Temporizador("TON_02", 6)
    TON_03 = Temporizador("TON_03", 2)

    while True:
        TON_01.entrada = True
        TON_01.actualizar()
        
        TON_02.entrada = not TON_02.salida
        TON_02.actualizar()
        
        if TON_02.salida:
            TON_01.reset = True

        print (TON_01)

if __name__ == "__main__":
    main ()
