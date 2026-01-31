from GetFile import GetFile
import mplfinance as mplf

symbol = "LTCUSDT"
year = 2023
ltcusdt = GetFile([symbol], [year]).getColumn(["Open", "High", "Low", "Close", "Volume"], merge=False)[f"{symbol}_{year}"]

mplf.plot(ltcusdt,type="candle",volume=True,tight_layout=True,style="yahoo")

mplf.show()