# *-* coding: utf-8 *-*

# Obtiene y Carga todos los fondos 
# https://api.cafci.org.ar/fondo?estado=1&include=entidad;depositaria,entidad;gerente,tipoRenta,region,benchmark,clase_fondo&limit=0

#Se conecta

import requests
from pymongo import MongoClient

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

# Comienzo a recolectar la info

url = 'https://api.cafci.org.ar/fondo?estado=1&include=clase_fondo&limit=0'
response = requests.get(url)
data = response.json()

if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    mongo_db = MongoDB(database_name='fciar', collection_name='clases')
    data=data['data']

    #print(data)

    for item in data:
        clases=item['clase_fondos']

        for clase in clases:
            _id = clase["fondoId"] + "_" + clase["id"]
            posted_id = mongo_db.insert({"_id":_id, "fondo_id":clase["fondoId"], "clase_id":clase["id"], "tickerBloomberg" : clase["tickerBloomberg"]} )

            print(posted_id)

response.close()
# Fin de insert

