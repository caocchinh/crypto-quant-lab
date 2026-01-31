import concurrent.futures
import copy
import datetime
import re
from functools import lru_cache
import numpy as np
import pandas as pd
from frozendict import frozendict
from MyClient import MyClient


class DataGetter(MyClient):
    def __init__(self, coins: list | np.ndarray,  klineInterval=None):
        super().__init__()
        self.returnData = None
        self.coins = coins
        self.klineInterval = klineInterval
        if self.klineInterval is not None:
            self.validInterval = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h"
                                                                                          "12h", "1d", "3d", "1w", "1M"]
            if type(self.klineInterval) != str or self.klineInterval not in self.validInterval:
                raise TypeError(
                    f"Please enter 'interval in string format, the valid intervals are: {self.validInterval}'")
            self.intervalDict = {"h": "hour", "d": "day", "m": "minute", "w": "week", "M": "month"}
            self.timeIntervalSince = list(filter(None, re.split(r'(\d+)', self.klineInterval)))



    def _getData(self, data):
        symbol, timeSince, column, klineInterval, timezone = data
        data = self.client.get_historical_klines_generator(symbol, klineInterval,
                                                           f"{timeSince['timeAmountSince']} "
                                                           f"{timeSince['timeIntervalSince']} ago UTC")
        temp = dict(Date=[], Open=[], High=[], Low=[], Close=[], Volume=[])
        for i in data:
            temp["Date"].append(
                pd.to_datetime(pd.to_datetime(i[0], unit='ms').strftime('%Y-%m-%d %H:%M:%S')) + datetime.timedelta(
                    hours=timezone))
            if "Open" in column:
                temp["Open"].append(float(i[1]))
            if "High" in column:
                temp["High"].append(float(i[2]))
            if "Low" in column:
                temp["Low"].append(float(i[3]))
            if "Close" in column:
                temp["Close"].append(float(i[4]))
            if "Volume" in column:
                temp["Volume"].append(int(float(i[7])))
        tempCopy = copy.deepcopy(temp)
        for k, v in tempCopy.items():
            if not v:
                del temp[k]
        return temp

    @lru_cache(maxsize=None)
    def getOldData(self, _format: dict | pd.DataFrame, klineInterval, timeSince=None, column=None, timezone=7):
        validCol = ["Open", "High", "Low", "Close", "Volume"]
        if column is None:
            column = ("Open", "High", "Low", "Close", "Volume")
        for i in column:
            if i not in validCol:
                raise ValueError(f"Please enter a valid column, the valid columns are: {validCol}")
        if timeSince is None:
            timeSince = {}
        description = ValueError("""PLease specify the time to get old data!: ERROR -> timeSince is None
            Format: {"timeAmountSince":int,"timeIntervalSince":str}""")
        validateIntervalSince = ["second", "minute", "hour", "day", "week", "month"]
        if timeSince is None or not isinstance(timeSince, frozendict):
            raise description
        if type(timeSince["timeAmountSince"]) != int or type(timeSince["timeIntervalSince"]) != str:
            raise description
        if timeSince["timeIntervalSince"] not in validateIntervalSince:
            raise ValueError(f"The valid 'timeAmountSince' are: {validateIntervalSince}")
        with concurrent.futures.ThreadPoolExecutor() as thread:
            args = [(self.coins[i], timeSince, column, klineInterval, timezone) for i in range(len(self.coins))]
            result = list(thread.map(self._getData, args))
        prices = {}
        if _format == dict:
            for count, coin in enumerate(self.coins):
                prices[coin] = result[count]
        elif type == "pandas" or pd.DataFrame:
            for count, coin in enumerate(self.coins):
                df = pd.DataFrame(result[count])
                if df.empty:
                    raise ValueError("'timeIntervalSince' range is too small, please specify a larger time range!")
                df.set_index("Date", inplace=True)
                prices[coin] = df
        return prices

    def getLiveData(self, *funcs, getChange, column: list = None, timezone: int = 7, stackUp: bool = True,
                    _format: dict | pd.DataFrame = dict):
        validCol = ["Open", "High", "Low", "Close", "Volume"]
        if column is None:
            column = ["Open", "High", "Low", "Close", "Volume"]
        for i in column:
            if i not in validCol:
                raise ValueError(f"Please enter a valid column, the valid columns are: {validCol}")

        self.twm.start()
        self.returnData = {}

        def handle_socket_message(msg):
            if msg["data"]["k"]["x"]:
                ohlcv = msg["data"]["k"]
                if msg["data"]["s"] not in self.returnData.keys():
                    if getChange:
                        self.returnData[ohlcv["s"]] = dict(Date=[], Open=[], High=[], Low=[], Close=[], Volume=[],
                                                           Change=[pd.NA])
                    else:
                        self.returnData[ohlcv["s"]] = dict(Date=[], Open=[], High=[], Low=[], Close=[], Volume=[])

                if stackUp:
                    self.returnData[ohlcv["s"]]["Date"].append(pd.to_datetime(
                        pd.to_datetime(ohlcv["t"], unit='ms').strftime('%Y-%m-%d %H:%M:%S')) + datetime.timedelta(
                        hours=timezone))
                    if "Open" in column:
                        self.returnData[ohlcv["s"]]["Open"].append(float(ohlcv["o"]))
                    if "High" in column:
                        self.returnData[ohlcv["s"]]["High"].append(float(ohlcv["h"]))
                    if "Low" in column:
                        self.returnData[ohlcv["s"]]["Low"].append(float(ohlcv["l"]))
                    if "Close" in column:
                        self.returnData[ohlcv["s"]]["Close"].append(float(ohlcv["c"]))
                    if "Volume" in column:
                        self.returnData[ohlcv["s"]]["Volume"].append(int(float(ohlcv["V"])))
                else:
                    self.returnData[ohlcv["s"]]["Date"] = [pd.to_datetime(
                        pd.to_datetime(ohlcv["t"], unit='ms').strftime('%Y-%m-%d %H:%M:%S')) + datetime.timedelta(
                        hours=timezone)]
                    if "Open" in column:
                        self.returnData[ohlcv["s"]]["Open"] = [float(ohlcv["o"])]
                    if "High" in column:
                        self.returnData[ohlcv["s"]]["High"] = [float(ohlcv["h"])]
                    if "Low" in column:
                        self.returnData[ohlcv["s"]]["Low"] = [float(ohlcv["l"])]
                    if "Close" in column:
                        self.returnData[ohlcv["s"]]["Close"] = [float(ohlcv["c"])]
                    if "Volume" in column:
                        self.returnData[ohlcv["s"]]["Volume"] = [int(float(ohlcv["V"]))]
                realFuncs = []
                defaultFuncs = []
                for func in funcs:
                    if type(func) != tuple:
                        if func.__name__ == "getPriceChange":
                            defaultFuncs.append(func)
                        else:
                            realFuncs.append(func)
                    else:
                        for x in func:
                            if x.__name__ != "getPriceChange":
                                realFuncs.append(x)
                changeData = defaultFuncs[0](_format=pd.DataFrame,
                                             timeSince=frozendict(
                                                 {"timeAmountSince": int(self.timeIntervalSince[0]) * 3,
                                                  "timeIntervalSince": self.intervalDict[
                                                      self.timeIntervalSince[1]]}),
                                             column=tuple(["Close"]), timezone=timezone,
                                             klineInterval=self.klineInterval, liveData=self.returnData)
                if stackUp:
                    if self.returnData[msg["data"]["s"]]["Change"][0] is pd.NA:
                        self.returnData[msg["data"]["s"]]["Change"] = [changeData[msg["data"]["s"]]["Change"]]
                    else:
                        self.returnData[msg["data"]["s"]]["Change"].append(changeData[msg["data"]["s"]]["Change"])
                else:
                    self.returnData[msg["data"]["s"]]["Change"] = [changeData[msg["data"]["s"]]["Change"]]

                if _format == dict:
                    checkList = [[_[column[0]]] for _ in self.returnData.values()]
                    checkLength = all(x == checkList[0] for x in checkList)
                    for func in realFuncs:
                        if len(self.coins) == len(list(self.returnData.keys())) and checkLength:
                            func(liveData=self.returnData)
                else:
                    tempDict = {}
                    for coin, data in self.returnData.items():
                        tempDf = pd.DataFrame(data)
                        tempDf.set_index("Date", inplace=True)
                        tempDict[coin] = tempDf
                    checkList = [[_[column[0]].size] for _ in tempDict.values()]
                    checkLength = all(x == checkList[0] for x in checkList)
                    for func in realFuncs:
                        if len(self.coins) == len(list(tempDict.keys())) and checkLength:
                            func(liveData=tempDict)

        self.twm.start_multiplex_socket(callback=handle_socket_message,
                                        streams=[coin.lower() + f"@kline_{self.klineInterval}" for coin in self.coins])
        self.twm.join()
