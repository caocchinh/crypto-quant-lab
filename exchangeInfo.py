import requests

url = 'https://api.binance.com/api/v3/exchangeInfo'
params = {'symbols': '["BTCUSDT","BNBBTC"]'}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    for symbol in data['symbols']:
        if symbol['symbol'] in ["BTCUSDT", "BNBBTC"]:
            print("Symbol:", symbol['symbol'])
            print("Exchange Info:")
            print(symbol)
            print("\n")
else:
    print("Failed to fetch exchange info. Status code:", response.status_code)
