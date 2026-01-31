import vectorbt as vbt
from GetFile import GetFile
import pandas_ta as ta
import pandas as pd

if __name__ == "__main__":
    year = 2022
    DATA = GetFile("LTCUSDT", [year])
    DATA_COL = DATA.getColumn(["High", "Low", "Close"])
    ICHIMOKU = vbt.IndicatorFactory.from_pandas_ta("ICHIMOKU")
    RSI = vbt.IndicatorFactory.from_pandas_ta("RSI")
    low = DATA_COL[year]["Low"]
    close = DATA_COL[year]["Close"]
    high = DATA_COL[year]["High"]

    ema20 = RSI.run(close,21,return_raw=True,to_2d=False,keep_pd=True,pass_col=True)
    ichimoku = ICHIMOKU.run(high,low,close,tenkan=9,kijun=26,to_2d =False,keep_pd =True, per_column=True)
    print(ichimoku)
    # conversion_line = pd.DataFrame(index=ichimoku.config.wrapper.config.index,data=ichimoku.config.output_list[0].real,columns=DATA.SYMBOL)
    # baseline_line = pd.DataFrame(index=ichimoku.config.wrapper.config.index,data=ichimoku.config.output_list[1].real,columns=DATA.SYMBOL)
    # fig = close.vbt.plot(trace_kwargs=dict(name="Price"))
    # fig = conversion_line.vbt.plot(trace_kwargs=dict(name="Conversion line",line=dict(color="red")),fig=fig)
    # fig = baseline_line.vbt.plot(trace_kwargs=dict(name="Baseline line",line=dict(color="blue")),fig=fig)
    #
    # fig.show()
