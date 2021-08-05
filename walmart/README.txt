Descripcion:

[vista]
- Despliega las interfaces de usuario
- Contiene la base de datos (Gestionada por el ORM DJANGO)
- Se ejecuta a traves del servicio vista.service en la direccion http://[mi_ip]:8000/


[app]
- Se comunica con los dispositivos de cobro (Monedero, Billeteros, Hoppers, Validador, Reciclador) Puede usar los protocolos MDB, CCTALK , ID0003
- Extrae la configuracion de la base de datos a traves del API de [vista]
- Recibe y envia instrucciones a la aplicacion [vista] a traves de Webhooks en la url http://[mi_ip]:8000/hook/
- Controla la secuencia de operacion del equipo  



