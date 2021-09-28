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
__postea = True
__top = 15
__delta = 1
# :::::::::::::::::::::::::


def getMessageToPost(item):
    diario = item["rendimientos"]["day"]
    mensual = item["rendimientos"]["month"]
    # YTY= item["rendimientos"]["oneYear"]
    YTD = getYTD(item["fondo_id"])  # item["rendimientos"]["year"]
    message = f'{str(item["nombre"]).replace("Infraestructura", "")} \nDiario: {str(diario["rendimiento"])}% | Mes: {mensual["rendimiento"]}% | YTD: {YTD["rendimiento"]} \n'

    return message


def getYTD(fondo_id):
    fecha_hasta = datetime.today() - timedelta(days=__delta)

    fecha_desde = general.getFechaDesde(fecha_hasta)
    curs = db_rendimientos.find({"fondo_id": fondo_id, "fecha": {"$gte": fecha_desde, "$lt": fecha_hasta}, "rendimientos.day.rendimiento": {
                                "$ne": '0.0000'}}).sort([("rendimientos.year.rendimiento", -1)]).limit(1)

    for item in curs:
        YTD = item["rendimientos"]["year"]
        fondo_id = item["fondo_id"]

        # print( f"fondo_id {fondo_id} YTD {YTD}")

    return YTD


def getTop3(tipo_rentaParam, moneda):
    # Obtengo el top 3 de los fondos por tipo de renta
    fecha_hasta = datetime.today() - timedelta(days=__delta)

    fecha_desde = general.getFechaDesde(fecha_hasta)
    curs = db_rendimientos.find({"moneda": moneda, "tipo_renta.id": tipo_rentaParam, "fecha": {"$gte": fecha_desde, "$lt": fecha_hasta}, "rendimientos.day.rendimiento": {
                                "$ne": '0.0000'}}).sort([("rendimientos.day.rendimiento", -1), ("rendimientos.year.rendimiento", -1)]).limit(__top)

    fecha_publish = str(curs[0]["fecha"].strftime("%d/%m/%Y"))
    tipo_renta = curs[0]["tipo_renta"]["nombre"]

    message_post = f"TOP 3 FCIs ${moneda} {tipo_renta} del {fecha_publish}\n\n"

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
    fecha_hasta = datetime.today() - timedelta(days=__delta)
    fecha_desde = general.getFechaDesde(fecha_hasta)

    curs = db_rendimientos.find({"fondo_id": {"$in": ["798", "443"]}, "fecha": {"$gte": fecha_desde, "$lt": fecha_hasta}, "rendimientos.day.rendimiento": {
                                "$ne": '0.0000'}}).sort([("rendimientos.day.rendimiento", -1)]).limit(__top)

    if curs.count() > 0:
        _fecha_publish = str(curs[0]["fecha"].strftime("%d/%m/%Y"))
        _message_post_wallet = f"Rendimiento FCIs Billeteras del {_fecha_publish}\n\n"

    i = 0
    arrayPosted = []

    for item in curs:
        fondo_id = item["fondo_id"]

        if(fondo_id not in arrayPosted):
            _message_post_wallet += getMessageToPost(item)
            arrayPosted.append(fondo_id)

            if fondo_id == "443":
                _message_post_wallet += "@uala_arg @GRUPOSBSOK\n\n"
            else:
                _message_post_wallet += "@mercadopago @BINDInversiones\n\n"

        i += 1
        if i == 3:
            break

        print(_message_post_wallet)

    return _message_post_wallet


tw = PostTwitter()
# Fondos de Billeteras
message_post_Wallet = getFCIBilleteras()
if __postea:
    tweet_id = tw.post(message_post_Wallet, None).id

# For por cada id de tipo de renta ARS
for idRenta in ["4", "2", "3", "5", "6", "7"]:
    # Excluyo el tipo de renta 6 para USD
    message_post = getTop3(idRenta, "ARS")
    print(len(message_post))
    try:
        if __postea:
            tweet_id = tw.post(message_post, tweet_id).id
    except:
        print("An exception occurred")

twUSD = PostTwitter()
tweet_idUSD = None
# For por cada id de tipo de renta USD
for idRenta in ["4", "2", "3", "5", "7"]:
    message_post = getTop3(idRenta, "USD")
    print(len(message_post))
    try:
        if __postea:
            tweet_idUSD = twUSD.post(message_post, tweet_idUSD).id
    except:
        print("An exception occurred")
