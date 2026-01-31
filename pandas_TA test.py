import pandas_ta
from GetFile import GetFile

if __name__ == "__main__":
    file = GetFile(10, [2020]).getColumn(["Close","High","Volume","Low","Open"],merge=False)

    print(file)