import pprint
import pandas as pd
from numba import *
from Utilities import Utilities
import pandas_ta as ta
import warnings
import numpy as np
from GetFile import GetFile
import time
import vectorbt as vbt
import sys
import os, psutil

start = time.perf_counter()

# Initialization
warnings.filterwarnings("ignore")
np.set_printoptions(threshold=sys.maxsize)
EMA = vbt.IndicatorFactory.from_talib("EMA")
MACD = vbt.IndicatorFactory.from_talib("MACD")


@njit(fastmath=True)
def produce_signal(close, MACD_Line, Histogram, Signal_line, ema200):
    trend = np.where(vbt.nb.crossed_above_nb(Signal_line, MACD_Line) & (Histogram < 0) & (close > ema200), 1, 0)
    trend = np.where(vbt.nb.crossed_above_nb(MACD_Line, Signal_line) & (Histogram > 0) & (close < ema200), -1,
                     trend)
    return trend


def myIndicator(close, fast=12, slow=26, signal=9, ema_length=200):
    macd = vbt.IndicatorFactory.from_talib("MACD").run(close, fast, slow, signal)
    ema200 = EMA.run(close, ema_length).real.to_numpy()
    trend = produce_signal(close=close.to_numpy(), MACD_Line=macd.macd.to_numpy(), Histogram=macd.macdhist.to_numpy(),
                           Signal_line=macd.macdsignal.to_numpy(), ema200=ema200)
    return trend


name = "MACD"
param_names = ["fast", "slow", "signal", "ema_length"]

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
                           fast=np.arange(3, 50, step=1),
                           slow=np.arange(3, 50, step=1),
                           param_product=True)
    long_entries = result.value == 1
    short_entries = result.value == -1

    statistics = Utilities(mergedData, year, column, long_entries, short_entries, FILE.SYMBOL,
                           param_names, name,
                           value_type="Winrate")
    statistics.plot(trades=False)
    pprint.pprint(statistics.bestStrategies)


if __name__ == "__main__":
    process = psutil.Process(os.getpid())
    year = 2023
    FILE = GetFile(1, [year])
    DATA = FILE.getColumn(["Close"], merge=False)
    # myIndicator  =Indicator(DATA,FILE.SYMBOL)
    # print(myIndicator.MACD())
    runIndicator(year)
    end = time.perf_counter()
    print(f"\nStrategy took {process.memory_info().rss / 1000000}mb of memory")
    print(f"Finished in {round(end - start, 2)} seconds")
