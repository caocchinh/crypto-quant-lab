import sys

import vectorbt as vbt
from vbtCustomIndicator import Indicator
from GetFile import GetFile
import time

start = time.perf_counter()

if __name__ == "__main__":
    FILE = GetFile("max", [2023])

    DATA = FILE.getColumn(["Close"],merge=False)
    myIndicator = Indicator(DATA,FILE.SYMBOL)
    print(sys.getsizeof(myIndicator.MACD()["MACD_Line"]))

    print(myIndicator.MACD())


    end = time.perf_counter()
    print(end-start)
#     # bb = vbt.IndicatorFactory.from_pandas_ta("ICHIMOKU").run(DATA[2023]["High"],DATA[2023]["Low"],DATA[2023]["Close"]).output_names

        # DATA[i]["Close"].vbt.plot().show()
    # rsi = vbt.RSI.run(DATA[FILE.SYMBOL[0]]["Close"],14)
    # fig = DATA[FILE.SYMBOL[0]].vbt.ohlcv.plot(make_subplots_kwargs=dict(rows=3,cols=2))

    # fig = vbt.RSI.run(DATA[FILE.SYMBOL[0]]['Close']).plot()


# if __name__ == "__main__":
#     FILE = GetFile("max",[2023])
#     DATA = FILE.getColumn(["Close"],merge=False)
#     ('macd', 'macdsignal', 'macdhist')
#     print(sys.getsizeof(vbt.IndicatorFactory.from_talib("MACD").run(DATA[FILE.SYMBOL[0]])))
#     print(sys.getsizeof( vbt.IndicatorFactory.from_talib("MACD").run(DATA[FILE.SYMBOL[0]]).macd.to_numpy()))
#     print(sys.getsizeof( vbt.IndicatorFactory.from_talib("MACD").run(DATA[FILE.SYMBOL[0]]).macdsignal.to_numpy()))
#     print(sys.getsizeof( vbt.IndicatorFactory.from_talib("MACD").run(DATA[FILE.SYMBOL[0]]).macdhist.to_numpy()))
#
#     end = time.perf_counter()
#     print(end - start)

    # bb = vbt.IndicatorFactory.from_pandas_ta("ICHIMOKU").run(DATA[2023]["High"],DATA[2023]["Low"],DATA[2023]["Close"]).output_names

        # DATA[i]["Close"].vbt.plot().show()
    # rsi = vbt.RSI.run(DATA[FILE.SYMBOL[0]]["Close"],14)
    # fig = DATA[FILE.SYMBOL[0]].vbt.ohlcv.plot(make_subplots_kwargs=dict(rows=3,cols=2))

    # fig = vbt.RSI.run(DATA[FILE.SYMBOL[0]]['Close']).plot()
