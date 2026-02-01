from GetFile import GetFile
from matplotlib import pyplot as plt
import pandas as pd

plt.style.use("fivethirtyeight")

symbol1 = "BCHUSDT"
symbol2 = "DOTUSDT"
symbols = f"{symbol1}-{symbol2}"
year = 2023
file = GetFile([symbol1,symbol2],[year]).getColumn(["Close"],merge=True)[year]["Close"]
# file = pd.read_csv(r"C:\Users\Chinh\Downloads\BTC 2020-2023 Historical data.csv", index_col=0)
# plt.hist(file["Close"], bins=100, edgecolor="b",log=True)
# print(file["Close"])
# plt.plot(file.index, file["Close"], color="b")
plt.xscale("log")
plt.xscale("log")
plt.scatter(file[f"{symbol1}_{str(year)}"],file[f"{symbol2}_{str(year)}"],cmap="summer",s=100,edgecolors="b")
title = f"{symbols} {year} correlation"
plt.title(title)
plt.tight_layout()
# plt.savefig(title, dpi=360)
plt.show()
# later use
