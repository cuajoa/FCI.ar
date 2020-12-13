# *-* coding: utf-8 *-*
# consulta los fondos y trae la ficha diaria
# URL https://api.cafci.org.ar/fondo/:idFondo/clase/:idCase/ficha 

import requests
from bson import Decimal128 as Decimal
from pymongo import MongoClient
from datetime import date, datetime

class MongoDB(object):
    def __init__(self, host='localhost', port=27017, database_name='fciar', collection_name=None):
        try:
            self._connection = MongoClient(host=host, port=port, maxPoolSize=200)
        except Exception as error:
            raise Exception(error)
        self._database = None
        self._collection = None
        if database_name:
            self._database = self._connection[database_name]
        if collection_name:
            self._collection = self._database[collection_name]

    def insert(self, post):
        # add/append/new single record
        post_id = self._collection.insert_one(post).inserted_id
        return post_id

# Consulto los fondos para traer la ficha
mongo_db = MongoClient()
db = mongo_db.fciar
db_clases = db.clases

print("start @ " + str(date.now().strftime("%Y-%m-%d %H:%M:%S")))
for item in db_clases.find():
    fondo_id=item["fondo_id"]
    clase_id=item["clase_id"]

    # url = 'https://api.cafci.org.ar/fondo/428/clase/2750/ficha' 
    url = 'https://api.cafci.org.ar/fondo/'+str(fondo_id)+'/clase/'+str(clase_id)+'/ficha' 
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "error" in data:
        print('Failed to get data:', response.status_code)
    else:
        data_converted=data['data']
        mongo_db_insert = MongoDB(collection_name='rendimientos')

        print(fondo_id + "_" + clase_id)

        vcp=0
        patrimonio=0

        #Recolecto info y la acomodo como quiero que quede        
        if "diaria" in data_converted["info"] :
            diaria=data_converted["info"]["diaria"]

            rendimientos=diaria["rendimientos"]
            fecha_data=diaria["referenceDay"]

            patrimonio=diaria["actual"]["patrimonio"]
            if patrimonio!="":
                patrimonio=Decimal(patrimonio)

            vcp=diaria["actual"]["vcpUnitario"]
            if vcp !="":
                vcp=Decimal(vcp)

            #print(fecha_data)
            fecha=datetime.strptime(fecha_data, '%d/%m/%Y')
            _id=fecha.strftime('%Y%m%d')+"_"+fondo_id + "_" +clase_id
            
            db_rendimientos = db.rendimientos
            #Chequeo si ya existe, si no existe lo inserto
            if db_rendimientos.count_documents({'_id': _id}, limit=1) == 0:
                moneda=data_converted["model"]["fondo"]["moneda"]["codigoCafci"]

                tpr=data_converted["model"]["fondo"]["tipoRenta"]
                tipo_renta={"id":tpr["id"], "nombre":tpr["nombre"], "codigoCafci":tpr["codigoCafci"]}
                # tipo_clase=data_converted["model"]["tipoClaseId"]
                nombre=data_converted["model"]["fondo"]["nombre"]
                tickerBloomberg=data_converted["model"]["tickerBloomberg"]
                gerente=data_converted["model"]["fondo"]["gerente"]["nombreCorto"]

                # print(fecha)
                # print(_id)
                # print(moneda)
                # print(rendimientos)
                # print(patrimonio)
                # print(vcp)

                try:
                    posted_id = mongo_db_insert.insert({"_id":_id, "fondo_id":fondo_id, "clase_id":clase_id, 
                    "tickerBloomberg":tickerBloomberg, "fecha":fecha, "nombre":nombre, "gerente":gerente,
                    "moneda":moneda, "vcp": vcp, "patrimonio":patrimonio,"tipo_renta":tipo_renta, 
                    "rendimientos":rendimientos})   
                except:
                    print("Error " + _id)

                print(_id)
                response.close()
        

mongo_db.close()
print("end @ " + str(date.now().strftime("%Y-%m-%d %H:%M:%S")))
