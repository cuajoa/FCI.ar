# *-* coding: utf-8 *-*
''' 
    Obtiene el ranking de los fondos
'''
from datetime import datetime, timedelta
from common.connection import MongoDB
import pandas as pd

db_rendimientos = MongoDB.getCollection(collection_name='rendimientos')

# :::::::::::::::::::::::::
# Parametros de la consulta
__delta = 2
# :::::::::::::::::::::::::


def getRanking():
    fecha_hasta = datetime.today() - timedelta(days=1)
    fecha_desde = datetime.today() - timedelta(days=__delta)

    curs = db_rendimientos.find({"fecha": {
                                "$gte": fecha_desde, "$lt": fecha_hasta}}).sort([("rendimientos.year.tna", 1)])

    df = pd.DataFrame(list(curs))

    print('Type of df:', type(df))

    # Printing the df to console
    print()
    print(df.head())


getRanking()
