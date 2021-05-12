# *-* coding: utf-8 *-*
''' 
    Calcula los fondos que mas rindieron y los publica en Twitter
'''
from common.postTwitter import PostTwitter
from datetime import datetime, timedelta
from common.general import general
from common.connection import MongoDB

db_rendimientos = MongoDB.getCollection(collection_name='rendimientos')

# :::::::::::::::::::::::::
# Parametros de la consulta
postea = True
top = 15
delta = 1
# :::::::::::::::::::::::::

def getMessageToPost(item):
    diario = item["rendimientos"]["day"]
    mensual = item["rendimientos"]["month"]
    # YTY= item["rendimientos"]["oneYear"]
    YTD = item["rendimientos"]["year"]
    message = f'{str(item["nombre"]).replace("Infraestructura", "")} \nDiario: {str(diario["rendimiento"])}% | Mes: {mensual["rendimiento"]}% | YTD: {YTD["rendimiento"]} \n'
    
    return message


def getTop3(tipo_rentaParam):
    # Obtengo el top 3 de los fondos por tipo de renta
    fecha_hasta=datetime.today() - timedelta(days = delta)

    fecha_desde = general.getFechaDesde(fecha_hasta)
    curs = db_rendimientos.find({"moneda": "ARS", "tipo_renta.id": tipo_rentaParam, "fecha": {"$gte": fecha_desde, "$lt": fecha_hasta}}).sort([("rendimientos.day.rendimiento", -1), ("rendimientos.year.rendimiento", -1)]).limit(top)

    fecha_publish = str(curs[0]["fecha"].strftime("%d/%m/%Y"))
    tipo_renta = curs[0]["tipo_renta"]["nombre"]
    message_post = f"TOP 3 FCIs {tipo_renta} del {fecha_publish}\n\n"
    i = 0
    arrayPosted = []
    for item in curs:
        diario = item["rendimientos"]["day"]
        fondo_id = item["fondo_id"]

        if fondo_id not in arrayPosted:
            if diario["rendimiento"] < "30":
                message_post += getMessageToPost(item) 
                i += 1
                arrayPosted.append(fondo_id)

        if i == 3:
            break
    message_post = PostTwitter.etiquetar(message_post)

    print(message_post)
    return message_post


def getFCIBilleteras():
    fecha_hasta = datetime.today() - timedelta(days = delta)

    print(fecha_hasta)

    fecha_desde = general.getFechaDesde(fecha_hasta)
    print(fecha_desde)
    curs = db_rendimientos.find({"fondo_id": {"$in": ["798", "443"]}, "fecha": {"$gte" : fecha_desde, "$lt": fecha_hasta}}).sort([("rendimientos.day.rendimiento", -1)]).limit(top)

    fecha_publish = str(curs[0]["fecha"].strftime("%d/%m/%Y"))
    message_post_wallet = f"Rendimiento FCIs Billeteras del {fecha_publish}\n\n"
    i = 0
    arrayPosted = []

    for item in curs:
        fondo_id= item["fondo_id"]
       
        if(fondo_id not in arrayPosted):
            message_post_wallet += getMessageToPost(item)
            arrayPosted.append(fondo_id)    

            if fondo_id == "443":
                message_post_wallet += "@uala_arg @GRUPOSBSOK\n\n"
            else:
                message_post_wallet += "@mercadopago @BINDInversiones\n\n"

        i += 1
        if i == 3:
            break

        print(message_post_wallet)
        
    return message_post_wallet


tw=PostTwitter()
# Fondos de Billeteras
message_post_Wallet = getFCIBilleteras()
if postea:
    tweet_id = tw.post(message_post_Wallet,None).id

# For por cada id de tipo de renta
for i in ["4","2","3","5","6","7"]:
    message_post = getTop3(i)
    try:
        if postea:
            tweet_id = tw.post(message_post,tweet_id).id
    except:
       print("An exception occurred")

