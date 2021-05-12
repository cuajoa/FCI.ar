# *-* coding: utf-8 *-*
'''
Se conecta diariamente y toma la información de todos los fondos y los guarda en la DB en la collection "patrimonio".

URL que consulta: https://api.cafci.org.ar/interfaz/semanal/resumen/cartera/{interfaz}
Ejemplo Primero del 30/12/2020: https://api.cafci.org.ar/interfaz/semanal/resumen/cartera/1270332
 
Si detecta este error: {"error":"inexistent-interfaz"} detiene la ejecución. Identifica que es la última interfaz existente.
Aproximadamente hay 460 fondos diarios

Esta información que recolecta la utiliza para calcular los fondos que más patrimonio poseen en postPatrimonio

'''

import requests
from bson import Decimal128 as Decimal
from datetime import datetime
from common.connection import MongoDB
from common.general import general

counter=1270332 #30-12-2020

#Obtengo el último ID hasta el momento en la DB y le sumo 1
collection = MongoDB.getCollection(collection_name='patrimonio')

curs = collection.find().limit(1).sort([("_id", -1)])
for item in curs:
  counter = item["_id"]

counter = counter + 1

# Comienzo a recolectar la info
mongo_db = MongoDB(collection_name='patrimonio')

while True:
    url = 'https://api.cafci.org.ar/interfaz/semanal/resumen/cartera/'+str(counter)
    response = requests.get(url)
    data = response.json()
    
    if "error" in data:
        break

    if response.status_code != 200:
        print('Failed to get data:', response.status_code)
    else:

        data_converted=data['data'][0]["dataXML"]

        cabecera=data_converted["Cabecera"]
        fecha=datetime.strptime(data_converted["Cabecera"]["FechaReporte"], '%d-%m-%Y').strftime('%m-%d-%Y')
        patrimonio=data_converted["Pie"]["PieValor"].replace(',','')

        esEsco=general.IsEsco(cabecera["SGNombre"])
        
        posted_id = mongo_db.insert({"_id":counter, "data":cabecera, "fecha":datetime.strptime(fecha,'%m-%d-%Y'), "patrimonio":Decimal(patrimonio), "esESCO":esEsco})

    counter = counter + 1
    print(counter)
    
    response.close()

# Fin de insert
