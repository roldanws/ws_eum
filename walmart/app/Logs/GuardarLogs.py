
import time
from datetime import date
from datetime import datetime



import os
import sys
import platform
sistema = platform.system()
plataforma = platform.uname()
version = ""

caracterDirectorio = ""
if sistema == "Windows":
	caracterDirectorio = '\\'
elif  sistema == "Linux":
    caracterDirectorio = '/'
    if plataforma.node == "raspberrypi":
        version = plataforma.node

ruta =  os.path.dirname(os.path.abspath(__file__)) + caracterDirectorio
rutaUsuario = os.path.expanduser('~') + caracterDirectorio

# Detectar si tiene instalada la tarjeta de arduino por el puerto serie

sys.path.append(os.path.join(ruta, ".."))
sys.path.append(os.path.join(ruta, ".." + caracterDirectorio + ".."))

print("\nEstamos en {} {}".format(sistema, version))
print("La ruta actual es {}".format(ruta))
print("La ruta de usuario es {}".format(rutaUsuario))





class GuardarLogs ():
    def __init__(self, nombreDelArchivo = None):


        self.nombreDelArchivo = nombreDelArchivo
        self.numeroConsecutivo = 0
        self.archivo = None
        self.diaActual = date.today()
        self.abrir ()

        print ("GuardarLogs inicializada")

    def abrir(self, archivoActual = 0):
        # Verifica que el archivo exista
        aux_0 = 1 

        while(aux_0):
            try:
                self.archivo = open (ruta + self.nombreDelArchivo + "_" + str(self.numeroConsecutivo), "r", encoding='ISO-8859-1')
                aux = True
                #print ("El archivo existe")
                self.archivo.close()
                self.numeroConsecutivo +=1

                if (self.numeroConsecutivo > 100):  # evita que se creen mas de 100 archivos
                    aux_0 = 0 
                #self.separarNombreNumero()
            except IOError:
                #print ("El archivo no existe", file = sys.stderr)
                aux_0 = 0 
  
        self.archivo = open (ruta + self.nombreDelArchivo + "_" + str(self.numeroConsecutivo), "w", encoding='ISO-8859-1')
        print ("Se abrio el archivo", self.nombreDelArchivo + "_" + str(self.numeroConsecutivo))

        self.archivo.write("["+str(date.today())+"]\n")
        self.archivo.close()

    """
    def cerrar(self):
        self.archivo.close()
    """     
    def actualizarDia(self):
        if date.today() > self.diaActual:
            self.archivo.write("\n[" + str(date.today())+"]\n")

    def print (self, *args, **kwargs):


        texto = ""
        for i, arg in enumerate(args):
            texto += str(arg)
            
            if i>0 and arg!="\n":
                texto += " "

        self.actualizarDia()


        self.archivo = open (ruta + self.nombreDelArchivo + "_" + str(self.numeroConsecutivo), "a", encoding='ISO-8859-1')
        self.archivo.write(str(datetime.now().time()) + " " + texto + "\n")
        self.archivo.close()

def main ():
    guardar = GuardarLogs("Prueba")

    guardar.print("Texto de prueba1", "otro texto")
    guardar.print("Texto de prueba2", "\n", "mas")
    time.sleep(20)
    guardar.print("Texto de prueba3")
    


if __name__ == "__main__":
    main()