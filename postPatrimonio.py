# *-* coding: utf-8 *-*
# Consulta fondos con mas patrimonio
from common.postTwitter import PostTwitter
from common.connection import MongoDB
from datetime import datetime, timedelta
from decimal import Decimal

mongo_db = MongoDB.getCollection(collection_name='patrimonio')

fecha_hasta=datetime.today()- timedelta(days=1)
fecha_desde=fecha_hasta.today()- timedelta(days=2)
curs = mongo_db.find({"data.Moneda":"Peso Argentina", "fecha":{"$gte" : fecha_desde, "$lt": fecha_hasta } }).sort([("patrimonio", -1)]).limit(5)

message_post="Fondos en pesos con Mayor Patrimonio al "+str(fecha_hasta.strftime("%d/%m/%Y"))+"\n \n"

for item in curs:
    pn= str(item["patrimonio"])
    dec= f'{Decimal(pn):,}'
    PatNet=dec.replace(',', ' ').replace('.', ',').replace(' ', '.')

    message_post += item["data"]["FondoNombre"] + " | " + PatNet + "\n"

message_post=PostTwitter.etiquetar(message_post)

print(message_post)

tw=PostTwitter()
tw.post(message_post,None)