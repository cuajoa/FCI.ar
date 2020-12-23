# *-* coding: utf-8 *-*
# Postea fondos que rinde mas que un PF
# {"rendimientos.day.tna": { $gte:"37"}, "tipo_renta.id":{ $in:["3","4"] }}

from common.general import general
from common.postTwitter import PostTwitter
from pymongo import MongoClient
from datetime import datetime, timedelta
from common.general import general

mongo_db = MongoClient()
db = mongo_db.fciar
db_rendimientos = db.rendimientos

tasa_PF=37

def getTop3(tipo_renta):
    #Obtengo el top 3 de los fondos Mercado de Dinero id=3 y Renta Fija id=4 que rinden mas que un PF
    fecha_hasta=datetime.today()- timedelta(days=1)

    fecha_desde=general.getFechaDesde(fecha_hasta)
    curs = db_rendimientos.find({"moneda":"ARS", "tipo_renta.id":tipo_renta,"rendimientos.day.tna": {"$gte":tasa_PF}, "fecha":{"$gte" : fecha_desde, "$lt": fecha_hasta } }).sort([("rendimientos.day.rendimiento", -1)]).limit(15)

    fecha_publish=str(curs[0]["fecha"].strftime("%d/%m/%Y"))
    tipo_renta=curs[0]["tipo_renta"]["nombre"]
    message_post="TOP 3 FCIs "+tipo_renta+" que rinden más que Plazo Fijo del "+ fecha_publish+"\n\n"
    i=0
    arrayPosted=[]
    for item in curs:
        diario= item["rendimientos"]["day"]
        fondo_id= item["fondo_id"]

        if fondo_id not in arrayPosted:
            if diario["rendimiento"] < "30":
                message_post += item["nombre"] + "\nDiario: " + str(diario["rendimiento"]) + "% | TNA: "+ diario["tna"] + "\n"
                i+=1
                arrayPosted.append(fondo_id)

        if i==5:
            break

    print(message_post)
    return message_post

tw=PostTwitter()
#Fondos de Billeteras
message_post3=getTop3(3)
#tweet_id=tw.post(message_post3,None).id

message_post4 = getTop3(4)
#tweet_id=tw.post(message_post4,tweet_id).id