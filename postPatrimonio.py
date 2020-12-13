# *-* coding: utf-8 *-*
# Consulta fondos con mas patrimonio
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

# for patrimonio in mongo_db._collection.find().limit(5).sort([("PieValor", 1),("FechaReporte",-1)]):
#     print(patrimonio)
#     message_post=""

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
my_api.update_status(status=message_post)