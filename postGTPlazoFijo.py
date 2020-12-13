# *-* coding: utf-8 *-*
# Postea fondos que rinde mas que un PF
# {"info.diaria.rendimientos.month.tna": {$gte:"37"}, "model.fondo.tipoRentaId":{ $in:["3","4"] }}

from pymongo import MongoClient
from datetime import datetime, timedelta

mongo_db = MongoClient()
db = mongo_db.fciar
db_rendimientos = db.rendimientos

def getTop3(tipo_rentaParam):
    #Obtengo el top 3 de los fondos Mercado de Dinero id=3
    fecha_hasta=datetime.today()- timedelta(days=1)

    #Por defecto es -2, si es lunes hago -4
    day_Diff=2
    if datetime.today().weekday() == 0:
        day_Diff=4

    fecha_desde=fecha_hasta.today()- timedelta(days=day_Diff)
    curs = db_rendimientos.find({"moneda":"ARS", "tipo_renta.id":tipo_rentaParam, "fecha":{"$gte" : fecha_desde, "$lt": fecha_hasta } }).sort([("rendimientos.day.rendimiento", -1)]).limit(15)
    # curs = db_rendimientos.find({"moneda":"ARS", "tipo_renta.id":"4", "fecha":{ "$max": fecha_hasta } }).sort([("rendimientos.day.rendimiento", -1)]).limit(3)

    fecha_publish=str(curs[0]["fecha"].strftime("%d/%m/%Y"))
    tipo_renta=curs[0]["tipo_renta"]["nombre"]
    message_post="TOP 3 FCIs "+tipo_renta+" del "+ fecha_publish+"\n\n"
    i=0
    arrayPosted=[]
    for item in curs:
        diario= item["rendimientos"]["day"]
        mensual= item["rendimientos"]["monthYear"]
        fondo_id= item["fondo_id"]

        if fondo_id not in arrayPosted:
            if diario["rendimiento"] < "30":
                message_post += item["nombre"] + "\nDiario: " + str(diario["rendimiento"]) + "% | Mes: " +mensual["rendimiento"] + "% | TNA: "+ diario["tna"] + "\n"
                i+=1
                arrayPosted.append(fondo_id)

        if i==3:
            break

    print(message_post)
    return message_post

def getFCIBilleteras():
    #Obtengo el top 3 de los fondos Mercado de Dinero id=3
    fecha_hasta=datetime.today()- timedelta(days=1)

    #Por defecto es -2, si es lunes hago -4
    day_Diff=2
    if datetime.today().weekday() == 0:
        day_Diff=4

    fecha_desde=fecha_hasta.today()- timedelta(days=day_Diff)
    curs = db_rendimientos.find({"fondo_id":{"$in":["798", "443"]}, "fecha":{"$gte" : fecha_desde, "$lt": fecha_hasta } }).sort([("rendimientos.day.rendimiento", -1)]).limit(15)

    fecha_publish=str(curs[0]["fecha"].strftime("%d/%m/%Y"))
    message_post_wallet="Rendimiento FCIs Billeteras del "+ fecha_publish+"\n\n"
    i=0
    for item in curs:
        diario= item["rendimientos"]["day"]
        mensual= item["rendimientos"]["monthYear"]
        fondo_id= item["fondo_id"]

        message_post_wallet += item["nombre"] + "\nDiario: " + str(diario["rendimiento"]) + "% | Mes: " +mensual["rendimiento"] + "% | TNA: "+ diario["tna"] + "\n"
        
        
        if fondo_id=="443":
            message_post_wallet += "@uala_arg @GRUPOSBSOK\n\n"
        else:
            message_post_wallet += "@mercadopago @BINDInversiones"
        i+=1
        if i==2:
            break

    print(message_post_wallet)
    return message_post_wallet

def Twittea(message, tweet_id_parent):
    #Twittea
    import tweepy
    # personal details 
    my_consumer_key ="wh1bOA5mnfbDsjtUFfAw01Q59"
    my_consumer_secret ="4k9z39AHyyPMhznSI1EDyr9JVqFZm3do2ZenrQ9dYqKVChlWK9"
    my_access_token ="1328507402593980416-XqnVH4jmEKRM3wwGL1qrqnTlTHMuGE"
    my_access_token_secret ="NfohErteVPbl7U1M4NKKEDmhG7zWIfrCOIwICFxiCDbA3"
    # authentication of consumer key and secret 
    my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
    # Authentication of access token and secret 
    my_auth.set_access_token(my_access_token, my_access_token_secret) 
    my_api = tweepy.API(my_auth)

    if tweet_id_parent is None :
        status=my_api.update_status(status=message,auto_populate_reply_metadata=True)
    else:
        status = my_api.update_status(status=message, 
                                 in_reply_to_status_id=tweet_id_parent, 
                                 auto_populate_reply_metadata=True)
    return status


#Fondos de Billeteras
message_post_Wallet=getFCIBilleteras()
#tweet_id=Twittea(message_post_Wallet,None).id

#For por cada id de tipo de renta
for i in ["2","3","4","5","6","7","8"]:
    message_post = getTop3(i)
    #tweet_id=Twittea(message_post,tweet_id).id