import pprint
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.test import GOOG, EURUSD
from Live.FutureOrder import ExecuteFutureOrder
import matplotlib.pyplot as plt
from backtesting.lib import crossover, plot_heatmaps
import talib
from GetFile import GetFile
import seaborn as sns


class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(talib.SMA, close, self.n1)
        self.sma2 = self.I(talib.SMA, close, self.n2)

    def next(self):
        price = self.data.Close[-1]
        size = 0.1
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy(tp=1.15*price)

        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell(tp=0.9*price)



def _read_file(filename):
    from os.path import dirname, join

    return pd.read_csv(join(dirname(__file__), filename),
                       index_col=0, parse_dates=True)


file = GetFile("DOGEUSDT", [2023]).getColumn(["Open", "High", "Low", "Close", "Volume"], merge=False)["DOGEUSDT_2023"]
# pprint.pprint(file)
file2 = _read_file(GetFile("ATOMUSDT", [2023]).PATH[0])
file3 = _read_file(r"C:\Users\Chinh\Downloads\Binance_BCHUSDT_2023_minute.csv")
# bt = Backtest(file, RSI, cash=454)


bt = Backtest(file2, SmaCross, cash=370)


def optim_func(series):
    if series["# Trades"] < 2:
        return -1
    return series["Win Rate [%]"]


stats ,heatmap = bt.optimize(n1=range(5, 50, 5),
                    n2=range(50, 100, 5),
                    maximize="# Trades",
                    constraint=lambda param: param.n2 > param.n1,
                    return_heatmap=True )
print(stats)
hm = heatmap.groupby(["n1","n2"]).mean().unstack()
sns.heatmap(hm,cmap="plasma")
# plt.show()
print(hm)
# plot_heatmaps(heatmap,agg="mean")
bt.plot(resample=False)
