from GetFile import GetFile
import talib
if __name__ == "__main__":
    data = GetFile(["DASHUSDT", "LTCUSDT"], [2020]).getColumn(["High", "Close"], merge=False)
    macd = talib.MACD(data["DASHUSDT_2020"]["Close"].to_numpy())
    print(len(macd))