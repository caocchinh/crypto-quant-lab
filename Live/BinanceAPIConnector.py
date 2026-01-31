import time
import hmac
import hashlib
import requests
from urllib.parse import urljoin, urlencode
from MyClient import MyClient


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


class BinanceAPIConnector(MyClient):
    def __init__(self, ):
        super().__init__()
        self.BASE_URL = 'https://api.binance.com'
        self.headers = {
            'X-MBX-APIKEY': self.api_key
        }

    def connect(self, endpoint, requestType, otherParams=None, includeTimestamps=True, includeSignature=True):
        PATH = endpoint
        timestamp = int(time.time() * 1000)
        if includeTimestamps:
            params = {
                "timestamp": timestamp
            }
        else:
            params = {}
        if otherParams:
            params.update(otherParams)

        query_string = urlencode(params)
        if includeSignature:
            params['signature'] = hmac.new(self._secret_api_key.encode('utf-8'), query_string.encode('utf-8'),
                                           hashlib.sha256).hexdigest()
        url = urljoin(self.BASE_URL, PATH)
        r = None
        if requestType.upper() == "GET":
            r = requests.get(url, headers=self.headers, params=params)
        elif requestType.upper() == "POST":
            r = requests.post(url, headers=self.headers, params=params)
        elif requestType.upper() == "DELETE":
            r = requests.delete(url, headers=self.headers, params=params)

        if r.status_code == 200:
            return r.json()
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())


