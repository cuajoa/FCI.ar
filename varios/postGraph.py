# *-* coding: utf-8 *-*
''' 
    Calcula los fondos que mas rindieron y los publica en Twitter
'''
from common.postTwitter import PostTwitter
from datetime import date, datetime, timedelta
from common.general import general
from common.connection import MongoDB
from common.graph import graph


db_rendimientos = MongoDB.getCollection(collection_name='rendimientos')

# :::::::::::::::::::::::::
# Parametros de la consulta
__postea = False
__top = 50
__delta = 20
# :::::::::::::::::::::::::

def getFCIBilleteras():
    fecha_hasta=datetime.today() - timedelta(days = 1)
    fecha_desde = datetime.today() - timedelta(days = __delta)
    
    # Clase 1982 Mercado Fondos Clase A
    # Clase 839 SBS Ahorro Clase A
    curs = db_rendimientos.find({"clase_id": {"$in": ["1982", "839"]}, "fecha": {"$gte" : fecha_desde, "$lt": fecha_hasta}}).sort([("fecha", 1)]).limit(__top)

    arrayGraph1982 = []
    arrayGraph839 = []
    arrayX=[]

    for item in curs:
        _nombre = item["nombre"]
        _clase_id = item["clase_id"]

        _fecha=item["rendimientos"]["day"]["fecha"]
       
        _diario = float(item["rendimientos"]["day"]["rendimiento"])
        _diarioFinde=0
        _fechaFinde=date.today
        
       
        if _diario > 0.099:
            for i in [1,2,3]:
                _diarioFinde = round(_diario/3,4)
                _fechaConvert = datetime.strptime(_fecha, '%d/%m/%Y')
                _fechaFinde =  _fechaConvert + timedelta(days = i)
                
                if _clase_id == "839":
                    arrayGraph839.append(_diarioFinde)
                    arrayX.append(str(datetime.strftime(_fechaFinde, '%d/%m/%Y')))
                else:
                    arrayGraph1982.append(_diarioFinde)

                # print(_nombre + '\t ' + str(_fechaFinde) + '\t ' + str(_diarioFinde))
            else:
                if _clase_id == "839":
                    arrayGraph839.append(_diarioFinde)
                    _fechaConvert = datetime.strptime(_fecha, '%d/%m/%Y')
                    arrayX.append(str(_fecha))
                else:
                    arrayGraph1982.append(_diario)
                    
        _fechaConvert = datetime.strptime(_fecha, '%d/%m/%Y')

        # print(_nombre + '\t ' + str(_fechaConvert) + '\t ' + str(_diario))
    
    print(arrayGraph1982)
    print(len(arrayGraph839))
    print(arrayX)
    graph.graficar(arrayX,arrayGraph839, arrayGraph1982)


getFCIBilleteras()

