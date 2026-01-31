import sys
import talib
import numpy as np
import pandas_ta as ta


class Indicator:
    def __init__(self,data,symbol):
        self.keys = list(data.keys())
        self.symbol = symbol
        self.dataPD = data
        self.dataNP = []
        for value in data.values():
            self.dataNP.append(value.to_numpy())

    def MACD(self, fast=14, slow=13, signal=12):
        MACD_Line = []
        Histogram = []
        Signal_Line = []
        for data in self.dataNP:
            macd = talib.MACD(data,fastperiod=fast, slowperiod=slow, signalperiod=signal)
            MACD_Line.append(macd[0])
            Histogram.append(macd[1])
            Signal_Line.append(macd[2])
        constant = len(MACD_Line[0])
        MACD_Line = np.array(MACD_Line).reshape(constant, len(self.symbol))
        Histogram = np.array(Histogram).reshape(constant, len(self.symbol))
        Signal_Line = np.array(Signal_Line).reshape(constant, len(self.symbol))
        return dict(MACD_Line=MACD_Line, Histogram=Histogram, Signal_Line=Signal_Line)

