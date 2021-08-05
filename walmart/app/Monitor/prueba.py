"""
class CheckSum3():
    def __init__(self):
        self.numeroInicial = 0
        
    def sumar(self,numero):
        #print (numero, self.numeroInicial>>1 )
        for i in range (8):
            bit =  (numero>>i)&1^self.numeroInicial&1
            #print (bit, end=" ")
            self.numeroInicial = (self.numeroInicial>>1)^bit<<15^bit<<10^bit<<3

    def imprimirNumero(self):
        print ("{0:b}".format(self.numeroInicial).rjust( 16 ), hex(self.numeroInicial) )
  
def main ():
    prueba = CheckSum3()
    prueba.sumar(252)
    prueba.sumar(5)
    prueba.sumar(17)
    prueba.imprimirNumero()
    
if __name__ == "__main__":
    main()
"""

"""
from PyQt5.QtWidgets import QApplication, QLabel
app = QApplication([])
label = QLabel ('Hello World!')
label.show()
app.exec_()
"""

"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QThread
import sys


class MyTask(QThread):
    done_signal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        # Do some work here
        self.done_signal.emit('some string')


def process_done_signal(result):
        print(result)
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    task = MyTask()
    task.done_signal.connect(process_done_signal)
    task.start()

    # This will continue to run forever, except we are killing the app
    # in the process_done_signal() function.
    sys.exit(app.exec_())
    
"""

"""
lista = ['a', 'b', 'c']

for indice, elemento in enumerate(lista):
    print (indice, elemento)
    
"""

"""
import sys
import os
from PyQt5 import QtGui
from PyQt5 import *

class SmallGUI(QtGui.QMainWindow):
    def __init__(self):
        super(SmallGUI,self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('Sample')

        #One input
        self.MyInput = QtGui.QLineEdit(self)
        self.MyInput.setGeometry(88,25,110,20)
        ###############

        QtCore.QObject.connect(self.MyInput,QtCore.SIGNAL("textChanged(bool)"),self.doSomething)

        #Add Text
        self.MyButton = QtGui.QPushButton(self)
        self.MyButton.setGeometry(QtCore.QRect(88,65,110,20))
        self.MyButton.setText('Add Text')
        ###############

        QtCore.QObject.connect(self.MyButton,QtCore.SIGNAL("clicked(bool)"),self.addText)

        self.show()

    def addText(self):
        self.MyInput.setText('write something')
"""
"""
import sys
from PyQt5 import QtWidgets, QtGui

def basicWindow():
    app = QtWidgets.QApplication(sys.argv)
    windowExample = QtWidgets.QWidget()
    labelA = QtWidgets.QLabel(windowExample)
    labelB = QtWidgets.QLabel(windowExample)
    labelA.setText('Label Example')
    labelB.setPixmap(QtGui.QPixmap('python.jpg'))
    windowExample.setWindowTitle('Label Example')
    windowExample.setGeometry(100, 100, 300, 200)
    labelA.move(100, 40)
    labelB.move(120, 120)
    windowExample.show()
    sys.exit(app.exec_())

basicWindow()"""
"""
from tkinter import *

def create_win():
    def close(): win1.destroy();win2.destroy()
    
    win1 = Toplevel()
    win1.geometry('%dx%d%+d+%d'%(sw,sh,-sw,0))
    win1.overrideredirect(1)
    win1.state('zoomed')
    win1.update()
    
    
    print ("win1", win1.geometry(), win1.sizefrom())
    
    
    Button(win1,text="Exit1",command=close).pack()
    
    
    win2 = Toplevel()
    win2.geometry('%dx%d%+d+%d'%(sw,sh,sw,0))
    win2.overrideredirect(1)
    win2.state('zoomed')
    win2.update()
    
    print ("win2", win2.geometry())
    Button(win2,text="Exit2",command=close).pack()

root=Tk()
sw,sh = root.winfo_screenwidth(),root.winfo_screenheight()
print ("screen1:",sw,sh)
w,h = 800,600 
a,b = (sw-w)/2,(sh-h)/2 

Button(root,text="Exit",command=lambda r=root:r.destroy()).pack()
Button(root,text="Create win2",command=create_win).pack()

root.geometry('%sx%s+%d+%d'%(w,h,a,b))
root.mainloop()"""
"""
import pytz
for tz in pytz.all_timezones:
    print (tz)
"""
"""
import datetime
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

print (LOCAL_TIMEZONE, datetime.date())
"""

"""
import requests

url = "http://127.0.0.1:8000"

headers = {
    'Authorization': "Token 389e47467dd94595a3212d8762742be9adfd5a44",
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "be1551ae-23c1-43dc-95e5-8923fef974e9,48ce801d-14ae-48ef-8845-48e91c030393",
    'Host': "127.0.0.1:8000",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)    
"""

"""
import zlib
data = "Hello, World!" * 100
checksum = zlib.crc32(data)

compressed = zlib.compress(data)
decompressed = zlib.decompress(compressed)

print ("data")
"""

import time
from prtg import prtg_api

prtg = prtg_api('192.168.1.1','prtgadmin','0000000000')

for device in prtg.alldevices:
  if device.id == "1234":
    deviceobj = device

deviceobj.pause()
deviceobj.clone(newname="cloned device",newplaceid="2468")

time.sleep(10)

prtg.refresh()

for device in prtg.alldevices:
  if device.name == "cloned device":
    device.resume()