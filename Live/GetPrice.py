from json import dumps
import pandas as pd
from frozendict import frozendict
from DataGetter import DataGetter
from Live.BinanceAPIConnector import BinanceAPIConnector


class GetPrice(DataGetter):
    def __init__(self, coins: list, klineInterval: str, *funcs, getChange=False,
                 live=False, stackUp: bool = False, timezone=7, _format: dict | pd.DataFrame = dict):
        super().__init__(coins=coins, klineInterval=klineInterval)
        self.priceChanges = None
        self.timezone = timezone
        self.getChange = getChange
        self._format = _format
        self.stackUp = stackUp
        self.live = live
        self.funcs = funcs

    def getCurrentPrice(self, specificCoins=None):
        currentPrice = {}
        if specificCoins is not None:
            currentCoins = specificCoins
        else:
            currentCoins = self.coins
        if not self.live:
            for i in currentCoins:
                if self.getChange:
                    currentPrice[i] = dict(Close=0, Change="+0.0%")
                else:
                    currentPrice[i] = dict(Close=0)
            priceList = BinanceAPIConnector().connect("/api/v3/ticker/price", "GET",
                                                      otherParams={"symbols": dumps(currentCoins).replace(" ", "")},
                                                      includeSignature=False, includeTimestamps=False)
            for i in priceList:
                currentPrice[i["symbol"]]["Close"] = float(i["price"])
            if self.getChange:
                changeTemp = self.getPriceChange(_format=pd.DataFrame,
                                                 timeSince=frozendict(
                                                     {"timeAmountSince": int(self.timeIntervalSince[0]) * 3,
                                                      "timeIntervalSince": self.intervalDict[
                                                          self.timeIntervalSince[1]]}),
                                                 column=tuple(["Close"]), timezone=self.timezone,
                                                 klineInterval=self.klineInterval, liveData=currentPrice)
                for symbol, change in changeTemp.items():
                    currentPrice[symbol]["Change"] = change
            return currentPrice
        else:
            self.getLiveData(self.getPriceChange, self.funcs,
                             getChange=self.getChange,
                             stackUp=self.stackUp, _format=self._format, timezone=self.timezone)

    def getPriceChange(self, _format: dict | pd.DataFrame = None, klineInterval=None, timeSince=None, column=None,
                       timezone=7, liveData=None):
        if liveData is None:
            liveData = self.getCurrentPrice()
        oldData = self.getOldData(_format=_format, klineInterval=klineInterval, timeSince=timeSince, column=column,
                                  timezone=timezone)
        change = {}
        if not self.live:
            for symbol in self.coins:
                last = oldData[symbol].iloc[1]["Close"]
                price = liveData[symbol]["Close"]
                difference = price - last
                temp = round((difference / last) * 100, 2)
                change[symbol] = f"{'+' + str(temp) + '%' if temp >= 0 else str(temp) + '%'}"
        else:
            for symbol, price_ in liveData.items():
                coin = symbol
                price = price_["Close"][-1]
                last = oldData[coin].iloc[1]["Close"]
                difference = price - last
                temp = round((difference / last) * 100, 3)
                change[coin] = {"Date": price_["Date"],
                                "Change": f"{'+' + str(temp) + '%' if temp >= 0 else str(temp) + '%'}"}
        return change
