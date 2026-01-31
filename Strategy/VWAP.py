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
# np.set_printoptions(threshold=sys.maxsize)
VWAP = vbt.IndicatorFactory.from_pandas_ta("VWAP")

@jit
def produce_signal(close,vwap,threshold):
    refactered_price = close + close*threshold
    trend = np.where((vbt.nb.crossed_above_nb(vwap, refactered_price)) == True, 1,
                     vbt.nb.crossed_above_nb(vwap,refactered_price).astype(int))
    trend = np.where((vbt.nb.crossed_above_nb(refactered_price, vwap)) == True, -1, trend)

    return trend



def myIndicator(close, data,threshold):
    vwap = VWAP.run(data["High"],data["Low"],data["Close"],data["Volume"]).vwap_d.to_numpy()
    trend = produce_signal(close.to_numpy(),vwap,threshold)
    return trend

name = "RSI"
param_names = ['data',"threshold"]

indicator = vbt.IndicatorFactory(
    class_name=name,
    short_name=name,
    input_names=["close"],
    param_names=param_names,
    output_names=["value"],
).from_apply_func(myIndicator,threshold=0.02, data=None, keep_pd=True)


def runIndicator(year):
    column = "Close"
    mergedData = FILE.getColumn(["High","Low","Close","Volume"], merge=True)
    result = indicator.run(mergedData[year][column],
                           data = mergedData[year],
                           threshold = np.arange(0.01,0.1,step=0.001),
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
    year = 2021
    FILE = GetFile("DASHUSDT", [year])
    runIndicator(year)
    end = time.perf_counter()
    print(f"\nStrategy took {process.memory_info().rss / 1000000}mb of memory")
    print(f"Finished in {round(end - start, 2)} seconds")
