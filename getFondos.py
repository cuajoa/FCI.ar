# *-* coding: utf-8 *-*
'''
Obtiene y Carga todos los fondos con información para hacer estadísticas
https://api.cafci.org.ar/fondo?estado=1&include=entidad;depositaria,entidad;gerente,tipoRenta,moneda,horizonte,duration,tipo_fondo&limit=0&order=fondo.nombre
Sólo se ejecuta en el Setup del proyecto.

'''

import requests
from common.connection import MongoDB
from common.general import general

# Comienzo a recolectar la info
i=1

url = 'https://api.cafci.org.ar/fondo?estado=1&include=entidad;depositaria,entidad;gerente,tipoRenta,moneda,horizonte,duration,tipo_fondo&limit=0&order=fondo.nombre'
response = requests.get(url)
data = response.json()

if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    mongo_db = MongoDB(collection_name='fondos')
    data=data['data']

    #print(data)

    for item in data:
        gerente_nom=item["gerente"]["nombre"]

        nombre=item["nombre"]
        gerente=item["gerente"]["nombreCorto"]
        plazo=item['diasLiquidacion']
        fechaInicio=item['inicio']
        depositaria=item["depositaria"]["nombre"]
        tipoRenta=item["tipoRenta"]["nombre"]
        horizonte=item["horizonte"]["nombre"]
        tipoFondo=item["tipoFondo"]["nombre"]
        duration=item["duration"]["nombre"]
        moneda=item["moneda"]["codigoCafci"]
        
        esEsco=general.IsEsco(gerente_nom)
        
        _id = item["id"]
        posted_id = mongo_db.insert({"_id":_id,
        "nombre": nombre, "gerente":gerente, 
        "plazo": plazo, "fechaInicio": fechaInicio, "depositaria":depositaria, 
        "tipoRenta": tipoRenta, "horizonte":horizonte, "tipoFondo": tipoFondo, 
        "duration":duration, "moneda": moneda, "esESCO":esEsco} )

        print(posted_id)

response.close()
# Fin de insert

