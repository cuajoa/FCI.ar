# *-* coding: utf-8 *-*
'''
    Calcula los fondos con mas patrimonio y los postea en Twitter
'''
from common.general import general
from common.postTwitter import PostTwitter
from common.connection import MongoDB
from datetime import datetime, timedelta

# :::::::::::::::::::::::::
# Parametros de la consulta
__postea = True
__top = 5
__delta = 1
# :::::::::::::::::::::::::

mongo_db = MongoDB.getCollection(collection_name='patrimonio')

fecha_hasta = datetime.today() - timedelta(days=__delta)
fecha_desde = fecha_hasta.today() - timedelta(days=1+__delta)
curs = mongo_db.find({"data.Moneda": "Peso Argentina", "fecha": {
                     "$gte": fecha_desde, "$lt": fecha_hasta}}).sort([("patrimonio", -1)]).limit(__top)

fecha_publish = datetime.today()

message_post = f'Fondos en pesos con Mayor Patrimonio al {str(fecha_publish.strftime("%d/%m/%Y"))}\n\n'

for item in curs:
    PatNet = general.FormatDecimal(str(item["patrimonio"]))

    message_post += f'{item["data"]["FondoNombre"]} | {PatNet} \n'

message_post = PostTwitter.etiquetar(message_post)

print(message_post)

if __postea:
    tw = PostTwitter()
    tw.post(message_post, None)
