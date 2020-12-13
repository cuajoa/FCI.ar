# *-* coding: utf-8 *-*

# Ultimo del 13/11 https://api.cafci.org.ar/interfaz/semanal/resumen/cartera/1250331
# Primero del 16/11 https://api.cafci.org.ar/interfaz/semanal/resumen/cartera/1250332 
# Ultimo del 16/11 https://api.cafci.org.ar/interfaz/semanal/resumen/cartera/1250800
# stop: {"error":"inexistent-interfaz"}
# Aproximadamente 468 fondos diarios

#Se conecta

import requests
from pymongo import MongoClient
from bson import Decimal128 as Decimal
from datetime import datetime
from common.connection import MongoDB

counter=1250332

#Obtengo el último ID
mongo_db = MongoClient()
db = mongo_db.fciar
collection = db.patrimonio

curs = collection.find().limit(1).sort([("_id", -1)])
for item in curs:
  counter = item["_id"]

counter = counter + 1
#print(counter)

# Comienzo a recolectar la info
while True:
    url = 'https://api.cafci.org.ar/interfaz/semanal/resumen/cartera/'+str(counter)
    response = requests.get(url)
    data = response.json()
    
    if "error" in data:
        break

    if response.status_code != 200:
        print('Failed to get data:', response.status_code)
    else:
        mongo_db = MongoDB(database_name='fciar', collection_name='patrimonio')

        data_converted=data['data'][0]["dataXML"]

        cabecera=data_converted["Cabecera"]
        fecha=datetime.strptime(data_converted["Cabecera"]["FechaReporte"], '%d-%m-%Y').strftime('%m-%d-%Y')
        patrimonio=data_converted["Pie"]["PieValor"].replace(',','')

        #print(fecha)
        posted_id = mongo_db.insert({"_id":counter, "data":cabecera, "fecha":datetime.strptime(fecha,'%m-%d-%Y'), "patrimonio":Decimal(patrimonio)})

    counter = counter + 1
    print(counter)
    
    response.close()

# Fin de insert

