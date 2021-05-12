# *-* coding: utf-8 *-*
''' 
Consulta los fondos/clase y trae la ficha diaria
URL https://api.cafci.org.ar/fondo/{idFondo}/clase/{idCase}/ficha 
Ejemplo de URL = 'https://api.cafci.org.ar/fondo/428/clase/2750/ficha' 

Esta información que recolecta la utiliza para calcular los fondos que más rindieron en postRendimiento
'''

import requests
from bson import Decimal128 as Decimal
from datetime import datetime
from common.connection import MongoDB
from common.general import general

# Consulto los fondos para traer la ficha
db_clases = MongoDB.getCollection(collection_name='clases')

print("start @ " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
mongo_db_insert = MongoDB(collection_name='rendimientos')

for item in db_clases.find():
    fondo_id=item["fondo_id"]
    clase_id=item["clase_id"]

    url = f'https://api.cafci.org.ar/fondo/{str(fondo_id)}/clase/{str(clase_id)}/ficha' 
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "error" in data:
        print('Failed to get data:', response.status_code)
    else:
        data_converted=data['data']

        print(f"{fondo_id}_{clase_id}")

        vcp=0
        patrimonio=0

        #Recolecto info y la acomodo la información a guardar        
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

            fecha=datetime.strptime(fecha_data, '%d/%m/%Y')
            _id=fecha.strftime('%Y%m%d')+"_"+fondo_id + "_" +clase_id
            
            db_rendimientos = MongoDB.getCollection(collection_name='rendimientos')
            #Chequeo si ya existe, si no existe lo inserto
            if db_rendimientos.count_documents({'_id': _id}, limit=1) == 0:
                moneda=data_converted["model"]["fondo"]["moneda"]["codigoCafci"]

                tpr=data_converted["model"]["fondo"]["tipoRenta"]
                tipo_renta={"id":tpr["id"], "nombre":tpr["nombre"], "codigoCafci":tpr["codigoCafci"]}
                nombre=data_converted["model"]["fondo"]["nombre"]
                tickerBloomberg=data_converted["model"]["tickerBloomberg"]
                gerente=data_converted["model"]["fondo"]["gerente"]["nombreCorto"]
                gerente_nom=data_converted["model"]["fondo"]["gerente"]["nombre"]
                horizonte=data_converted["model"]["fondo"]["horizonte"]["nombre"]
                duration=data_converted["model"]["fondo"]["duration"]["nombre"]

                esEsco=general.IsEsco(gerente_nom)

                try:
                    posted_id = mongo_db_insert.insert({"_id":_id, "fondo_id":fondo_id, "clase_id":clase_id, 
                    "tickerBloomberg":tickerBloomberg, "fecha":fecha, "nombre":nombre, "gerente":gerente,
                    "moneda":moneda, "vcp": vcp, "patrimonio":patrimonio,"tipo_renta":tipo_renta,
                    "horizonte":horizonte,"duration":duration, "rendimientos":rendimientos, "esESCO":esEsco})   
                except:
                    print("Error " + _id)

                print(_id)
                response.close()

print("end @ " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
