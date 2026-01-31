import pprint
import vectorbt as vbt
import pandas_ta as ta
import talib
from GetFile import GetFile

# year = 2023
# FILE = GetFile(["DASHUSDT"], [year])
# DATA = FILE.getColumn(["Close"], merge=False)
# ema200 = ta.ema( DATA[FILE.SYMBOL[0]])
# macd =ta.macd( DATA[FILE.SYMBOL[0]],fast=12,slow=26,signal=9)
# macd.columns = ["MACD_Line","Histogram","Signal_Line"]
# print(macd)

if __name__ == "__main__":
    year = 2023
    FILE = GetFile(1, [year])
    DATA = FILE.getColumn(["Volume","Close","High","Low"],merge=True)
    VWAP = vbt.IndicatorFactory.from_talib("CCI").run(DATA[FILE.SYMBOL[0]]
                                                           )
    print(VWAP)
    # DATA = FILE.getColumn(["Close"], merge=True)
    # pprint.pprint(DATA)
# DATA = FILE.getColumn(["Close"], merge=False)