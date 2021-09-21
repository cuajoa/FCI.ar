
import urllib3
import json
from urllib.request import Request, urlopen

# :::::::::::::::::::::::::
# Parametros de la consulta
__url = 'https://apids-test.primary.com.ar/crypto/v1/ticker/price?symbol=BTCUSDT'
# :::::::::::::::::::::::::


req = Request(__url)
req.add_header('Cache-Control',
               'no-cache')
req.add_header('Ocp-Apim-Subscription-Key',
               '8Z0Hj8hEMW0acQOTtKuDcuynO0xpIRLQNHv84OOmsuNKrckz2T3XOv89m')
content = urlopen(req).read()
print(content)
