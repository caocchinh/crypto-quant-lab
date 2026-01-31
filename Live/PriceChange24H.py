import pprint
import urllib.parse
import json
from DataGetter import DataGetter

class PriceChange24H(DataGetter):
    def __int__(self,coins, pairAsset, additionalPairs):
        super().__init__(coins=coins, pairAsset=pairAsset, additionalPairs=additionalPairs)


    def topGainer(self):
        pass

    def topLoser(self,topNthPosition):
        ticker = self.client.get_ticker()
        priceChange = {}
        for i in ticker:
            if i["symbol"][-4:] == self.pairAsset and "DOWN" not in i["symbol"] and "UP" not in i["symbol"]:
                priceChange[i["symbol"]] = float(i["priceChangePercent"])
        topDict = {}
        count = 0
        for symbol, change in priceChange.items():
            if change in list(sorted(priceChange.values()))[0:topNthPosition]:
                count+=1
                topDict[f"top{count}"] = {symbol:change}
        pprint.pprint(topDict)
    def change24H(self):
        tickers = self.client.get_ticker(symbols=urllib.parse.quote(json.dumps(self.coins).replace(" ","")))
        priceChange = {}
        for i in tickers:
            priceChange[i["symbol"]] = float(i["priceChangePercent"])
        return priceChange