# *-* coding: utf-8 *-*
''' 
Consulta los fondos/clase y trae la ficha diaria
URL https://api.cafci.org.ar/fondo/{idFondo}/clase/{idCase}/ficha 
Ejemplo de URL = 'https://api.cafci.org.ar/fondo/428/clase/2750/ficha' 

Esta información que recolecta la utiliza para calcular los fondos que más rindieron en postRendimiento
'''

import requests
from bson import Decimal128 as Decimal
from datetime import datetime, timedelta
from common.connection import MongoDB
from common.general import general

__today = datetime.today() - timedelta(days=1)

def notExistFicha(_fondo_id, _clase_id):
    # Consulto cuales fichas ya tengo en la DB para la fecha de hoy

    __id = f"{__today.strftime('%Y%m%d')}_{_fondo_id}_{_clase_id}"

    print(__id)
    rendimientos = MongoDB.getCollection(collection_name='rendimientos')

    return (rendimientos.count_documents({'_id': __id}, limit=1) == 0)


def getFichas():
    print(f'start @ {str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}')

    # Consulto los fondos para traer la ficha
    db_clases = MongoDB.getCollection(collection_name='clases')

    for item in db_clases.find():
        fondo_id = item["fondo_id"]
        clase_id = item["clase_id"]

        if notExistFicha(fondo_id, clase_id):
            url = f'https://api.cafci.org.ar/fondo/{str(fondo_id)}/clase/{str(clase_id)}/ficha'
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200 or "error" in data:
                print('Failed to get data:', response.status_code)
            else:
                data_converted = data['data']

                vcp = 0
                patrimonio = 0

                # Recolecto info y la acomodo la información a guardar
                if "diaria" in data_converted["info"]:
                    diaria = data_converted["info"]["diaria"]

                    rendimientos = diaria["rendimientos"]
                    fecha_data = diaria["referenceDay"]

                    patrimonio = diaria["actual"]["patrimonio"]
                    if patrimonio != "":
                        patrimonio = Decimal(patrimonio)

                    vcp = diaria["actual"]["vcpUnitario"]
                    if vcp != "":
                        vcp = Decimal(vcp)

                    fecha = datetime.strptime(fecha_data, '%d/%m/%Y')

                    if fecha == __today:
                        _id = f"{fecha.strftime('%Y%m%d')}_{fondo_id}_{clase_id}"

                        print(f'{_id} Inserted')

                        moneda = data_converted["model"]["fondo"]["moneda"]["codigoCafci"]

                        tpr = data_converted["model"]["fondo"]["tipoRenta"]
                        tipo_renta = {
                            "id": tpr["id"], "nombre": tpr["nombre"], "codigoCafci": tpr["codigoCafci"]}
                        nombre = data_converted["model"]["fondo"]["nombre"]
                        tickerBloomberg = data_converted["model"]["tickerBloomberg"]
                        gerente = data_converted["model"]["fondo"]["gerente"]["nombreCorto"]
                        gerente_nom = data_converted["model"]["fondo"]["gerente"]["nombre"]
                        horizonte = data_converted["model"]["fondo"]["horizonte"]["nombre"]
                        duration = data_converted["model"]["fondo"]["duration"]["nombre"]

                        esEsco = general.IsEsco(gerente_nom)

                        try:
                            mongo_db_insert = MongoDB(
                                collection_name='rendimientos')
                            posted_id = mongo_db_insert.insert({"_id": _id, "fondo_id": fondo_id, "clase_id": clase_id,
                                                                "tickerBloomberg": tickerBloomberg, "fecha": fecha, "nombre": nombre, "gerente": gerente,
                                                                "moneda": moneda, "vcp": vcp, "patrimonio": patrimonio, "tipo_renta": tipo_renta,
                                                                "horizonte": horizonte, "duration": duration, "rendimientos": rendimientos, "esESCO": esEsco})
                            mongo_db_insert.close()
                        except:
                            print("Error " + _id)

                    response.close()

    print(f'end @ {str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}')


getFichas()
