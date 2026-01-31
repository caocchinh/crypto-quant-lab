import json
import urllib.parse

array = ["BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT","BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT","BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT","BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT","BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT","BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT", "BTCUSDT", "BNBUSDT"]
jsonString = json.dumps(array)
urlEncodedString = urllib.parse.quote(jsonString)
print(urlEncodedString)