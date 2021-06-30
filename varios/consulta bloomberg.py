# *-* coding: utf-8 *-*
# Postea fondos que rinde mas que un PF
# {"rendimientos.day.tna": { $gte:"37"}, "tipo_renta.id":{ $in:["3","4"] }}

from common.general import general
from datetime import datetime, timedelta
from common.general import general
from common.connection import MongoDB

mongo_db = MongoDB.getCollection(collection_name='clases')

tasa_PF = 37

def getBLOOMBERG():
    fecha_hasta = datetime.today()- timedelta(days=1)

    fecha_desde = general.getFechaDesde(fecha_hasta)- timedelta(days=7)
    curs = mongo_db.find({"gerente":"StoneX Asset"})

    i = 0
    for item in curs:
        bloomberg = str(item["tickerBloomberg"])
        fondo = str(item["nombre"])
        print(fondo + ' ticker: ' + bloomberg)
    


getBLOOMBERG()