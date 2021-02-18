# *-* coding: utf-8 *-*

from datetime import datetime, timedelta
from common.general import general
from decimal import Decimal
from common.connection import MongoDB
import matplotlib.pyplot as plt

mongo_db = MongoDB.getCollection(collection_name='patrimonio')

cotizacion_usd=93.75

fecha_hasta=datetime.today()- timedelta(days=1)
fecha_desde=datetime.today()- timedelta(days=2)

resultado = mongo_db.aggregate(
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
PN_Esco=(patrimonio_esco/total)*100
PN_ot=(patrimonio_restante/total)*100


labels = 'Esco', 'No Esco'
sizes = [PN_Esco, PN_ot]
explode = (0.1, 0)  

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

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