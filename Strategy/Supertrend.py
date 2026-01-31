import pprint
import time
from ProgressBar import ProgressBar
from itertools import product
import vectorbt as vbt
from numba import *
import numpy as np
import psutil
import warnings
from GetFile import GetFile
from Utilities import Utilities

start = time.perf_counter()

# Initialization
warnings.filterwarnings("ignore")
# np.set_printoptions(threshold=sys.maxsize)
su = vbt.IndicatorFactory.from_pandas_ta("RSI")

period = np.arange(2, 50, step=20)
oversold = np.arange(2, 50, step=20)
overbought = np.arange(50, 100, step=20)
bar = ProgressBar(len(list(product(period, oversold, overbought))) - 1, "Backtesting in progress").progressBar()


@jit
def produce_signal(rsi, overbought, oversold):
    overbought = np.full(rsi.shape, overbought)
    oversold = np.full(rsi.shape, oversold)
    trend = np.where(vbt.nb.crossed_above_nb(rsi, oversold), 1,
                     vbt.nb.crossed_above_nb(rsi, oversold).astype(int))
    trend = np.where(vbt.nb.crossed_above_nb(rsi, overbought), -1, trend)
    return trend


def myIndicator(close, period=14, overbought=70, oversold=30):
    try:
        next(bar)
    except StopIteration:
        pass
    rsi = RSI.run(close, period).real.to_numpy()
    trend = produce_signal(rsi, overbought, oversold)
    return trend


name = "RSI"
param_names = ["period", "overbought", "oversold"]
indicator = vbt.IndicatorFactory(
    class_name=name,
    short_name=name,
    input_names=["close"],
    param_names=param_names,
    output_names=["value"],
).from_apply_func(myIndicator, period=14, overbought=70, oversold=30, keep_pd=True)


def runIndicator(year):
    column = "Close"
    mergedData = FILE.getColumn([column], merge=True)
    result = indicator.run(mergedData[year][column],
                           period=period,
                           oversold=oversold,
                           overbought=overbought,
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
    year = 2022
    FILE = GetFile(["ETHUSDT"], [year])
    runIndicator(year)
    end = time.perf_counter()
    print(f"\nStrategy took {process.memory_info().rss / 1000000}mb of memory")
    print(f"Finished in {round(end - start, 2)} seconds")
