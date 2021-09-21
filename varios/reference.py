
import urllib3
import json
from urllib.request import Request, urlopen

# :::::::::::::::::::::::::
# Parametros de la consulta
__url = 'https://apids.primary.com.ar/prd-ro/v3/api/Schemas/schema-000/Data/by-odata'
# :::::::::::::::::::::::::


# params = urllib3.urlencode({
#     '$filter': f"type eq 'MF' and currency eq 'ARS'",
#     '$select': 'symbol,underlyingSymbol,date,performanceDay,performanceMtd,performanceYtd,performanceYear,currency'
#    # 'orderby': 'performanceDay DESC'
# }).encode("utf-8")


req = Request(__url)
req.add_header('Cache-Control',
               'no-cache')
req.add_header('Ocp-Apim-Subscription-Key',
               'x5pfRfliT9MmaOJqP4YAt654RoLR5VmBbGvc2l7hcx8o2pfKpTJaxVquY2SAsJ54gFAsMSG84UWAOJ8')
content = urlopen(req).read()
print(content)
