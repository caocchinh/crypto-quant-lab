import pprint
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '200',
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '11399715-9a87-48e5-8379-411f6e693a1c',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    coins = []
    for data in data["data"]:
        coins.append(data["symbol"])
    stable = ["USDT", "BUSD", "USDC", "TUSD", "FDUSD", "USDD", "USDP", "USTC"]
    top200 = [e for e in coins if e not in stable]
    print(top200)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    pprint.pprint(e)
