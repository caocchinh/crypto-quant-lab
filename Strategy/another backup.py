import pprint
import pandas as pd
from vbtCustomIndicator import Indicator
from numba import *
from Utilities import Utilities
import pandas_ta as ta
import warnings
import numpy as np
from GetFile import GetFile
import time
import vectorbt as vbt
import sys

start = time.perf_counter()

# Initialization
warnings.filterwarnings("ignore")
# np.set_printoptions(threshold=sys.maxsize)
EMA = vbt.IndicatorFactory.from_talib("EMA")
MACD = vbt.IndicatorFactory.from_talib("MACD")


@njit(fastmath=True)
def produce_signal(close, MACD_Line, Histogram, Signal_line, ema200):
    trend = np.where(vbt.nb.crossed_above_nb(Signal_line, MACD_Line) & (Histogram < 0) & (close > ema200), 1, 0)
    trend = np.where(vbt.nb.crossed_above_nb(MACD_Line, Signal_line) & (Histogram > 0) & (close < ema200), -1,
                     trend)
    return trend

def myIndicator(close, fast=12, slow=26, signal=9, ema_length=200):
    macd = myIndicator.MACD(fast=fast,slow=slow,signal=signal)
    ema200 = EMA.run(close, ema_length).real.to_numpy()

    trend = produce_signal(close=close.to_numpy(), MACD_Line=macd["MACD_Line"], Histogram=macd["Histogram"], Signal_line=macd["Signal_Line"],ema200=ema200)


    return trend

name = "MACD"
param_names = [ "fast", "slow", "signal", "ema_length"]

indicator = vbt.IndicatorFactory(
    class_name=name,
    short_name=name,
    input_names=["close"],
    param_names=param_names,
    output_names=["value"],
).from_apply_func(myIndicator, fast=12, slow=26, signal=9, ema_length=200, keep_pd=True)


def runIndicator(year):
    column = "Close"
    mergedData = FILE.getColumn([column], merge=True)
    result = indicator.run(mergedData[year][column],
                           fast=np.arange(3, 6, step=1),
                           slow=np.arange(3, 6, step=1),
                           signal=np.arange(3, 6, step=1),
                           ema_length=np.arange(3, 6, step=1),
                           param_product=True)
    long_entries = result.value == 1
    short_entries = result.value == -1

    statistics = Utilities(mergedData, year, column, long_entries, short_entries, FILE.SYMBOL,
                          param_names,name,value_type=
                           "Winrate")
    statistics.plotTrades()
    # statistics.plotHeatMap()
    pprint.pprint(statistics.bestStrategies)


if __name__ == "__main__":
    year = 2023
    FILE = GetFile(1, [year])
    DATA = FILE.getColumn(["Close"], merge=False)
    myIndicator = Indicator(DATA,FILE.SYMBOL)
    # print(myIndicator.MACD())
    returns = runIndicator(year)
    end = time.perf_counter()
    print(f"\nFinished in {round(end - start, 2)} seconds")
