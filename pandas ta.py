import functools
import sys
from numba import njit,jit
import pandas as pd
from GetFile import GetFile
import pandas_ta as ta
import vectorbt as vbt
import talib

def reMerge(data):
    finalData = {}
    for symbol in DATA.SYMBOL:
        for year,column in DATA_CLOSE.items():
            temp = []
            col = []
            for key,value in column.items():
                col.append(key)
                temp.append(value[symbol])
                data = functools.reduce(lambda a, b: pd.merge(a, b, left_index=True, right_index=True),
                                                temp)
            data.columns = col
            finalData[symbol] = data
    return finalData

if __name__ == "__main__":
    year = 2023
    DATA = GetFile(["DASHUSDT", "LTCUSDT"], [year])
    symbol = DATA.SYMBOL

    DATA_CLOSE = DATA.getColumn(["High","Low","Close","Volume"])
    reMergeData = reMerge(DATA_CLOSE)


    # ema20 = reMergeData[symbol[0]].ta.ema(length=20)
    # ema200 = reMergeData[symbol[0]].ta.ema(length=200)
    for i,v in enumerate(reMergeData.items()):
        ichimoku = reMergeData[symbol[i]].ta.ichimoku(include_chikou=False, tenkan=9, kijun=26, senkou=52)
        currentIchimoku = ichimoku[0]
        leadingIchimoku = ichimoku[1]
        # vwap = DATA_CLOSE[symbol].ta.vwap()
        #
        ichi_col = currentIchimoku.columns.values
        # print(ichi_col)

        fig = reMergeData[symbol[i]]["Close"].vbt.plot(trace_kwargs=dict(name="Price"))
        # fig = ema20.vbt.plot(trace_kwargs=dict(name="EMA20",line=dict(color="red")),fig=fig)
        # fig = ema200.vbt.plot(trace_kwargs=dict(name="EMA200",line=dict(color="yellow")),fig=fig)
        # # fig = vwap.vbt.plot(trace_kwargs=dict(name="VWAP",line=dict(color="orange")),fig=fig)
        #
        fig = currentIchimoku[ichi_col[0]].vbt.plot(trace_kwargs=dict(name=ichi_col[0], line=dict(color="#a5d6a7")),
                                                    fig=fig)
        fig = currentIchimoku[ichi_col[1]].vbt.plot(trace_kwargs=dict(name=ichi_col[1], line=dict(color="#faa1a4")),
                                                    fig=fig)
        fig = currentIchimoku[ichi_col[2]].vbt.plot(trace_kwargs=dict(name=ichi_col[2], line=dict(color="#2196f3")),
                                                    fig=fig)
        fig = currentIchimoku[ichi_col[3]].vbt.plot(trace_kwargs=dict(name=ichi_col[3], line=dict(color="#801922")),
                                                    fig=fig)


        fig.show()
    # #
