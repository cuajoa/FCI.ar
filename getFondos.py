# *-* coding: utf-8 *-*

# Obtiene y Carga todos los fondos 
# https://api.cafci.org.ar/fondo?estado=1&include=entidad;depositaria,entidad;gerente,tipoRenta,region,benchmark,clase_fondo&limit=0

#Se conecta

import requests
from common.connection import MongoDB

# Comienzo a recolectar la info
url = 'https://api.cafci.org.ar/fondo?estado=1&include=clase_fondo&limit=0'
response = requests.get(url)
data = response.json()

if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    mongo_db = MongoDB(collection_name='clases')
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

