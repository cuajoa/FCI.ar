# *-* coding: utf-8 *-*
# Consulta fondos que más rindieron
from common.postTwitter import PostTwitter
from datetime import datetime, timedelta
from common.general import general
from common.connection import MongoDB

db_rendimientos = MongoDB.getCollection(collection_name='rendimientos')

def getMessageToPost(item):
    diario= item["rendimientos"]["day"]
    mensual= item["rendimientos"]["month"]
    YTY= item["rendimientos"]["oneYear"]
    YTD= item["rendimientos"]["year"]
    message= str(item["nombre"]).replace("Infraestructura", "") + "\nDiario: " + str(diario["rendimiento"]) + "% | Mes: " +mensual["rendimiento"] + "% | YTD: "+ YTD["rendimiento"] + "\n"
    
    return message

def getTop3(tipo_rentaParam):
    #Obtengo el top 3 de los fondos Mercado de Dinero id=3
    fecha_hasta=datetime.today()- timedelta(days=1)

    fecha_desde=general.getFechaDesde(fecha_hasta)
    curs = db_rendimientos.find({"moneda":"ARS", "tipo_renta.id":tipo_rentaParam, "fecha":{"$gte" : fecha_desde, "$lt": fecha_hasta } }).sort([("rendimientos.day.rendimiento", -1)]).limit(15)

    fecha_publish=str(curs[0]["fecha"].strftime("%d/%m/%Y"))
    tipo_renta=curs[0]["tipo_renta"]["nombre"]
    message_post="TOP 3 FCIs "+tipo_renta+" del "+ fecha_publish+"\n\n"
    i=0
    arrayPosted=[]
    for item in curs:
        diario= item["rendimientos"]["day"]
        fondo_id= item["fondo_id"]

        if fondo_id not in arrayPosted:
            if diario["rendimiento"] < "30":
                message_post += getMessageToPost(item) 
                i+=1
                arrayPosted.append(fondo_id)

        if i==3:
            break
    message_post=PostTwitter.etiquetar(message_post)

    print(message_post)
    return message_post

def getFCIBilleteras():
    fecha_hasta=datetime.today()- timedelta(days=1)

    print(fecha_hasta)

    fecha_desde=general.getFechaDesde(fecha_hasta)
    print(fecha_desde)
    curs = db_rendimientos.find({"fondo_id":{"$in":["798", "443"]}, "fecha":{"$gte" : fecha_desde, "$lt": fecha_hasta } }).sort([("rendimientos.day.rendimiento", -1)]).limit(15)

    fecha_publish=str(curs[0]["fecha"].strftime("%d/%m/%Y"))
    message_post_wallet="Rendimiento FCIs Billeteras del "+ fecha_publish+"\n\n"
    i=0
    arrayPosted=[]

    for item in curs:
        fondo_id= item["fondo_id"]
       
        if(fondo_id not in arrayPosted):
            message_post_wallet += getMessageToPost(item)
            arrayPosted.append(fondo_id)    

            if fondo_id=="443":
                message_post_wallet += "@uala_arg @GRUPOSBSOK\n\n"
            else:
                message_post_wallet += "@mercadopago @BINDInversiones"

        i+=1
        if i==3:
            break

    print(message_post_wallet)
    return message_post_wallet

# tw=PostTwitter()
#Fondos de Billeteras
getFCIBilleteras()
# tweet_id=tw.post(message_post_Wallet,None).id

# #For por cada id de tipo de renta
# for i in ["4","2","3","5","6","7"]:
#     message_post = getTop3(i)
#     try:
#         tweet_id=tw.post(message_post,tweet_id).id
#     except:
#         print("An exception occurred")

#  message_at="@Santander_Ar @MarivaFondos @allarialedesma @bullmarketbrok @Inverti_enBolsa @BINDInversiones @BalanzCapital @argenfunds @CohenArgentina @Inverti_enBolsa"
#  tweet_id=tw.post(message_at,tweet_id).id

