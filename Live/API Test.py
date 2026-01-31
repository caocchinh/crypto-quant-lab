import time
import json
import hmac
import hashlib
import requests
from urllib.parse import urljoin, urlencode


class BinanceException(Exception):
    def __init__(self, status_code, data):
        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"
        super().__init__(message)


API_KEY = '6bGIW8dm1BrXD7MPNQJZ5wQsyv5yHDf2L0VoGqEw7562vGM3u44lf3d12sP45BHL'
SECRET_KEY = 'B05gKqNJSpFu6eZuP0GVLUHLpuhsVnJJe9zTOdAvZwm6n7bhJQB0v2dM8JYye0R3'
BASE_URL = 'https://api.binance.com'
headers = {
    'X-MBX-APIKEY': API_KEY
}

PATH = '/sapi/v1/convert/orderStatus'
timestamp = int(time.time() * 1000)
params = {
    'quoteId': "702efc05c6844873bb9083aab896ff35",
    "timestamp":timestamp
}
query_string = urlencode(params)
params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
url = urljoin(BASE_URL, PATH)
r = requests.get(url, headers=headers, params=params)
if r.status_code == 200:
    data = r.json()
    print(json.dumps(data, indent=2))
else:
    raise BinanceException(status_code=r.status_code, data=r.json())
