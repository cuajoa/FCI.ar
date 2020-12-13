# *-* coding: utf-8 *-*
# Consulta fondos con mas patrimonio
from common.postTwitter import PostTwitter
from pymongo import MongoClient
from datetime import datetime, timedelta

mongo_db = MongoClient()
db = mongo_db.fciar
collection = db.patrimonio

fecha_hasta=datetime.today()- timedelta(days=1)
fecha_desde=fecha_hasta.today()- timedelta(days=2)
curs = collection.find({"data.Moneda":"Peso Argentina", "fecha":{"$gte" : fecha_desde, "$lt": fecha_hasta } }).sort([("patrimonio", -1)]).limit(5)

message_post="Fondos en pesos con Mayor Patrimonio al "+str(fecha_hasta.strftime("%d/%m/%Y"))+"\n \n"

for item in curs:
    precio= item["patrimonio"]

    #formatted_float = "${:,.2f}".format(float(precio))
    #print(formatted_float)

    message_post += item["data"]["FondoNombre"] + " " + str(precio) + "\n"

    print(message_post)

tw=PostTwitter
tw.post(message_post)