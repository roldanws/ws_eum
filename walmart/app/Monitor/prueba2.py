import zlib
data = "hola mundo" * 10

data = data.encode('latin')
checksum = zlib.crc32(data)& 0xffffffff

print (hex(checksum), checksum)


import qrcode
img = qrcode.make(data)
img.save("prueba.jpg")
print (img)