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


def produce_signal(ema1,ema2):
    trend = np.where((vbt.nb.crossed_above_nb(ema1, ema2)==True), 0,vbt.nb.crossed_above_nb(ema1, ema2).astype(int))
    trend = np.where((vbt.nb.crossed_above_nb(ema2, ema1)==True), -1,trend)
    return trend


def myIndicator(close, ema_length1=10, ema_length2=100):
    ema1 = EMA.run(close, ema_length1).real.to_numpy()
    ema2 = EMA.run(close, ema_length2).real.to_numpy()
    trend = produce_signal(ema1,ema2)
    return trend


name = "EMA"
param_names = ["ema_length1","ema_length2"]

indicator = vbt.IndicatorFactory(
    class_name=name,
    short_name=name,
    input_names=["close"],
    param_names=param_names,
    output_names=["value"],
).from_apply_func(myIndicator, ema_length1=10,ema_length2=50, keep_pd=True)


def runIndicator(year):
    column = "Close"
    mergedData = FILE.getColumn([column], merge=True)
    result = indicator.run(mergedData[year][column],
                           ema_length1=np.arange(2,100,step=2),
                           ema_length2=np.arange(101,200,step=2),
                           param_product=True)
    long_entries = result.value == 1
    short_entries = result.value == -1

    statistics = Utilities(mergedData, year, column, long_entries, short_entries, FILE.SYMBOL,
                           param_names, name,
                           value_type="Winrate")
    statistics.plot(trades=True,heatmap=True, volume=True)
    pprint.pprint(statistics.bestStrategies)


if __name__ == "__main__":
    process = psutil.Process(os.getpid())
    year = 2023
    FILE = GetFile("LTCUSDT", [year])
    DATA = FILE.getColumn(["Close"], merge=False)
    runIndicator(year)
    end = time.perf_counter()
    print(f"\nStrategy took {process.memory_info().rss / 1000000}mb of memory")
    print(f"Finished in {round(end - start, 2)} seconds")
