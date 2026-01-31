import multiprocessing
import numpy as np
import pandas as pd


def modify(file, dropCol, symbol):
    printState = file if symbol is None else symbol
    try:
        df = pd.read_csv(file)
        df = df.drop(
            columns=dropCol)
        df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        df['Date'] = [pd.to_datetime(x, unit='ms').strftime('%Y-%m-%d %H:%M:%S') for x in df["Date"]]
        df = df.set_index("Date")
        df.to_csv(file)
        print(f"{printState} successfully modified!")
    except KeyError as error:
        if error != "['ignore', 'taker_buy_quote_volume', 'taker_buy_volume', " \
                    "'count', 'quote_volume', 'close_time'] not found in axis":
            print(f"{printState} already has already formatted!")


def remove(file, column, symbol):
    printState = file if symbol is None else symbol
    if column is None:
        column = "blank"
    try:
        df = pd.read_csv(file)
        if column != "blank":
            df = df.drop(columns=column)
            df.to_csv(file)
        elif column == "blank":
            blankCols = np.where(df.columns.str.match("Unnamed") is True)
            if len(blankCols[0]) > 0:
                for i in blankCols:
                    df = df.drop(df.columns[i], axis=1)
                df.to_csv(file, index=False)
                print(f"{printState} successfully remove {column} columns!")
            else:
                raise ValueError(f"No more blanks column to remove in {printState}!")
        else:
            raise ValueError("Please enter valid columns!")
    except Exception as error:
        print(error)


def sort(file, sortType, symbol):
    printState = file if symbol is None else symbol

    try:
        csv = pd.read_csv(file, parse_dates=True)
        csv.set_index("Date", inplace=True)
        descending = csv.iloc[0].name > csv.iloc[1].name
        ascending = csv.iloc[0].name < csv.iloc[1].name
        if sortType == "ascending" or sortType == "Ascending":
            if ascending:
                print(f"The file {printState} is already in ascending order!")
            elif not ascending:
                csv = csv[::-1]
                csv.to_csv(file, index=True)
                print(f"{printState} successfully modified in ascending order!")
        elif sortType == "descending" or sortType == "Descending":
            if descending:
                print(f"The file {printState} is already in descending order!")
            elif not descending:
                csv = csv[::-1]
                csv.to_csv(file, index=True)
                print(f"{printState} successfully modified in descending order!")
    except Exception as error:
        print(error)


def modifyCWD(file, symbol):
    printState = file if symbol is None else symbol
    try:
        df = pd.read_csv(file, low_memory=False)
        df = df.drop(columns="https://www.CryptoDataDownload.com")
        col = np.array([i for i in df.index])
        Date = np.array(
            ["".join(x) for x in [[i for i in col[x + 1][1]] for x in range(len([i for i in col[1:-1]]) + 1)]],
            dtype="M")
        Open = np.array(
            ["".join(x) for x in [[i for i in col[x + 1][3]] for x in range(len([i for i in col[1:-1]]) + 1)]],
            dtype="f")
        High = np.array(
            ["".join(x) for x in [[i for i in col[x + 1][4]] for x in range(len([i for i in col[1:-1]]) + 1)]],
            dtype="f")
        Low = np.array(
            ["".join(x) for x in [[i for i in col[x + 1][5]] for x in range(len([i for i in col[1:-1]]) + 1)]],
            dtype="f")
        Close = np.array(
            ["".join(x) for x in [[i for i in col[x + 1][6]] for x in range(len([i for i in col[1:-1]]) + 1)]],
            dtype="f")
        Volume = np.array(
            ["".join(x) for x in [[i for i in col[x + 1][8]] for x in range(len([i for i in col[1:-1]]) + 1)]],
            dtype="f")
        df2 = pd.DataFrame({
            "Date": Date,
            "Open": Open,
            "High": High,
            "Low": Low,
            "Close": Close,
            "Volume": Volume
        })
        df2["Date"] = pd.to_datetime(df2["Date"])
        df2.to_csv(file, index=False)
        print(f"CryptoWatchDate of file {printState} has successfully modified")

    except KeyError as error:
        print(error)
        if error != "['https://www.CryptoDataDownload.com'] not found in axis":
            print(f"{printState} has already formatted")


def date(file, symbol):
    printState = file if symbol is None else symbol
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df["Date"], infer_datetime_format=True)
    df.to_csv(file, index=False)
    print(f"Datetime format of {printState} successfully modified!")


def add(file, symbol):
    printState = file if symbol is None else symbol
    df = pd.read_csv(file)
    if "Symbol" not in df.columns:
        df["Symbol"] = pd.Series([symbol for _ in range(len(df.index))])
        df.to_csv(file, index=False)
        print(f"Column 'Symbol' has successfully added to{printState}")

    else:
        print(f"{printState} has already modified!")


class FormatRegulator:
    def __init__(self, filePath: list, symbol=None, sortType="ascending", dropCol=None, cryptoWatch=False,
                 checkDefault=True, checkDatetimeFormat=True, checkColumn=True, checkOrder=True, checkSymCol=True):
        if dropCol is None:
            self.dropCol = ["ignore", "taker_buy_quote_volume", "taker_buy_volume", "count", "quote_volume",
                            "close_time"]
        elif dropCol is not None and type(dropCol) == list or dropCol == "blank":
            self.dropCol = dropCol
        else:
            raise TypeError("Please enter drop columns in a list!")
        self.filePath = filePath
        self.symbol = symbol
        if type(self.filePath) != list and not isinstance(self.filePath, np.ndarray):
            if self.symbol is None:
                raise TypeError("Please enter file paths in a list!")
            if type(self.symbol) != list and not isinstance(self.symbol, np.ndarray):
                raise TypeError("Please enter file paths in a list!")
        self.sortType = sortType
        if not (self.sortType == "ascending" or self.sortType == "Ascending"
                or self.sortType == "descending" or self.sortType == "Descending"):
            raise ValueError("Please enter either 'ascending' or 'descending'!")
        self.cryptoWatch = cryptoWatch
        self.checkDefault = checkDefault
        self.checkDatetimeFormat = checkDatetimeFormat
        self.checkColumn = checkColumn
        self.checkSymCol = checkSymCol
        self.checkOrder = checkOrder

    def defaultCheck(self):
        if self.checkDefault:
            if self.cryptoWatch:
                self.modifyCryptoWatchData()
            else:
                self.modifyDefaultFormat()
        if self.checkOrder:
            self.sortFile()
        if self.checkDatetimeFormat:
            self.reformatDate()
        if self.checkColumn:
            self.removeCol()
        if self.checkSymCol:
            self.addSymbolColumn()

    def modifyDefaultFormat(self):
        if len(self.filePath) > 5:
            with multiprocessing.Pool() as pool:
                args = [(self.filePath[i], self.dropCol, self.symbol[i] if self.symbol is not None else self.symbol) for
                        i in range(len(self.filePath))]
                pool.starmap(modify, args)
        else:
            for i in range(len(self.filePath)):
                if self.symbol is None:
                    modify(self.filePath[i], self.dropCol, self.symbol)
                else:
                    modify(self.filePath[i], self.dropCol, self.symbol[i])

    def sortFile(self):
        if len(self.filePath) > 5:
            with multiprocessing.Pool() as pool:
                args = [(self.filePath[i], self.sortType, self.symbol[i] if self.symbol is not None else self.symbol)
                        for i in range(len(self.filePath))]
                pool.starmap(sort, args)
        else:
            for i in range(len(self.filePath)):
                if self.symbol is None:
                    sort(self.filePath[i], self.sortType, self.symbol)
                else:
                    sort(self.filePath[i], self.sortType, self.symbol[i])

    def reformatDate(self):
        if len(self.filePath) > 5:
            with multiprocessing.Pool() as pool:
                args = [(self.filePath[i], self.symbol[i] if self.symbol is not None else self.symbol) for i in
                        range(len(self.filePath))]
                pool.starmap(date, args)
        else:
            for i in range(len(self.filePath)):
                if self.symbol is None:
                    date(self.filePath[i], self.symbol)
                else:
                    date(self.filePath[i], self.symbol[i])

    def modifyCryptoWatchData(self):
        if len(self.filePath) > 5:
            with multiprocessing.Pool() as pool:
                args = [(self.filePath[i], self.symbol[i] if self.symbol is not None else self.symbol) for i in
                        range(len(self.filePath))]
                pool.starmap(modifyCWD, args)
        else:
            for i in range(len(self.filePath)):
                if self.symbol is None:
                    modifyCWD(self.filePath[i], self.symbol)
                else:
                    modifyCWD(self.filePath[i], self.symbol[i])

    def removeCol(self):
        if len(self.filePath) > 5:
            with multiprocessing.Pool() as pool:
                args = [(self.filePath[i], self.dropCol, self.symbol[i] if self.symbol is not None else self.symbol) for
                        i in range(len(self.filePath))]
                pool.starmap(remove, args)
        else:
            for i in range(len(self.filePath)):
                if self.symbol is None:
                    remove(self.filePath[i], self.dropCol, self.symbol)
                else:
                    remove(self.filePath[i], self.dropCol, self.symbol[i])

    def addSymbolColumn(self):
        if len(self.filePath) > 5:
            with multiprocessing.Pool() as pool:
                args = [(self.filePath[i], self.symbol[i] if self.symbol is not None else self.symbol) for i in
                        range(len(self.filePath))]
                pool.starmap(add, args)
        else:
            for i in range(len(self.filePath)):
                if self.symbol is None:
                    remove(self.filePath[i], self.dropCol, self.symbol)
                else:
                    remove(self.filePath[i], self.dropCol, self.symbol[i])
