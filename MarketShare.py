# *-* coding: utf-8 *-*

import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime, timedelta
from common.general import general
from decimal import Decimal

mongo_db = MongoClient()
db = mongo_db.fciar
db_patrimonio = db.patrimonio

cotizacion_usd=93.50

fecha_hasta=datetime.today()- timedelta(days=1)
fecha_desde=general.getFechaDesde(fecha_hasta)

resultado = db_patrimonio.aggregate(
    [{
        "$match":{
            "$and": [
                    { "fecha": { "$gte": fecha_desde } },
                    { "fecha": { "$lt":  fecha_hasta } }
                ]
        }
    },
    {
        "$group": {
            "_id":["$esESCO","$data.Moneda"],
            "patrimonio": { "$sum": "$patrimonio" }
        }
    }]
    )

patrimonio_esco=0
patrimonio_restante=0

for i in resultado:
    # print(i["_id"][0])
    if i["_id"][0]:
        if i["_id"][1] == 'Peso Argentina':
            patrimonio_esco=i["patrimonio"].to_decimal()
        else:
            patrimonio_esco=+ (i["patrimonio"].to_decimal() *Decimal(cotizacion_usd))
    else:
        if i["_id"][1] == 'Peso Argentina':
            patrimonio_restante=i["patrimonio"].to_decimal()
        else:
            patrimonio_restante=+ (i["patrimonio"].to_decimal() *Decimal(cotizacion_usd))

total=patrimonio_esco+patrimonio_restante

print(patrimonio_esco)
print((patrimonio_esco/total)*100)
print((patrimonio_restante/total)*100)


#  "$group": {
#             "_id":["$esESCO","$data.Moneda"],
#             "patrimonio": {
#                 "$cond" : [
#                     {"$eq":["$data.Moneda","Dolar Estadounidense"]},
#                     {"$multiply": [cotizacion_usd, {"$sum": "$patrimonio" }]},
#                     {"$sum": "$patrimonio" }
#                  ]
#              }
#          }
#      }]