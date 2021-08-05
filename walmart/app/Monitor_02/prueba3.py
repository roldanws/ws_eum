"""

import platform
system = ""
release = ""
version = ""





print (platform.system(), platform.release(),platform.version())

res = platform.system_alias(
            platform.system(),
            platform.release(),
            platform.version(),)
            

            
print (res, platform.machine(), platform.node(), platform.processor(), platform.python_implementation(), platform.uname(), platform.linux_distribution())

"""

"""
sudo apt-get --purge remove postgresql-11 postgresql-client-11 postgresql-client-common postgresql-common postgresql-contrib postgresql-contrib




sudo apt-get --purge remove postgresql postgresql-11 postgresql-client-11 postgresql-client-common postgresql-common postgresql-contrib  





sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'Postgres3UMd6';"



superset db upgrade


sudo apt-get --purge remove  postgresql-11 postgresql-client-11 postgresql-client-common postgresql-common 
"""

"""

import serial

puerto = serial.Serial("/dev/ttyS0", baudrate=9600)

for i in range (100):
    puerto.write("\n\tPruebasssssssssssssssssssssssssssssssssssssssssss".encode())

print ("Fin de la prueba")


"""
def intercalarLista(datos, intercalar=1):
    lista = []
    for i, dato in enumerate (datos):
        if (i%intercalar) == 0:
            lista.append(dato)
    return lista

    
a=[1, 2, 3, 4, 5, 6, 7, 8]


b =  intercalarLista(a,2)

print (b)