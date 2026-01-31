import copy
import fnmatch
import functools
import multiprocessing
import pathlib
import warnings
import numpy as np
import pandas as pd
from FormatRegulator import FormatRegulator

warnings.filterwarnings("ignore")

hour_data_path = r"/home/caocchinh/Downloads/Bitcoin/Binance_Historical_Data/1 Hour"
minute_data_path = r"/home/caocchinh/Downloads/Bitcoin/Binance_Historical_Data/1 Minute"


def checkDictionary(i, data, dictionary, year):
    try:
        dictionary[i.parent.name] == {}
    except KeyError:
        dictionary[i.parent.name] = {}
        if i in data:
            dictionary[i.parent.name][year] = str(i.as_posix())
    else:
        if i in data:
            dictionary[i.parent.name][year] = str(i.as_posix())
    return dictionary


class GetFile(FormatRegulator):
    def __init__(self, symbol=None, year=None, sortType="ascending", dropCol=None, cryptoWatch=True,
                 checkDefault=True, checkDatetimeFormat=True, checkColumn=True, checkOrder=True, checkSymCol=True):
        self.csv = None
        self.descending = None
        self.ascending = None
        if symbol is not None or year is not None:
            self.symbol = symbol
            self.year = year
            self.PURE_SYMBOL = []
            self.hour_data = self.get_csv_file(hour_data_path)
            self.minute_data = self.get_csv_file(minute_data_path)
            self.DATA = self.getFile(symbol, year)
            self.PATH = np.array([v for i in self.DATA for x, v in i.items()])
            self.SYMBOL = np.array([x for i in self.DATA for x, v in i.items()])
            self.PATHDICT = {}
            self.pathDict()
            super().__init__(self.PATH, self.SYMBOL, sortType=sortType, dropCol=dropCol, cryptoWatch=cryptoWatch,
                             checkDefault=checkDefault, checkDatetimeFormat=checkDatetimeFormat
                             , checkColumn=checkColumn, checkOrder=checkOrder, checkSymCol=checkSymCol)

    @staticmethod
    def get_csv_file(path):
        crypto_currency_historical_data = pathlib.Path(path)
        historical_data = {}
        data = list(crypto_currency_historical_data.glob("**/*.csv"))
        file_csv = [pathlib.Path(i) for i in data]
        if path is minute_data_path:
            filtered_2019_path = np.array([i for i in file_csv if fnmatch.fnmatch(i.name, "*2019_minute.csv") is True])
            filtered_2020_path = np.array([i for i in file_csv if fnmatch.fnmatch(i.name, "*2020_minute.csv") is True])
            filtered_2021_path = np.array([i for i in file_csv if fnmatch.fnmatch(i.name, "*2021_minute.csv") is True])
            filtered_2022_path = np.array([i for i in file_csv if fnmatch.fnmatch(i.name, "*2022_minute.csv") is True])
            filtered_2023_path = np.array([i for i in file_csv if fnmatch.fnmatch(i.name, "*2023_minute.csv") is True])
            for i in file_csv:
                historical_data = checkDictionary(i, filtered_2019_path, historical_data, 2019)
                historical_data = checkDictionary(i, filtered_2020_path, historical_data, 2020)
                historical_data = checkDictionary(i, filtered_2021_path, historical_data, 2021)
                historical_data = checkDictionary(i, filtered_2022_path, historical_data, 2022)
                historical_data = checkDictionary(i, filtered_2023_path, historical_data, 2023)
        elif path is hour_data_path:
            for i in range(len(file_csv)):
                historical_data[file_csv[i].parent.name] = str(file_csv[i].as_posix())
        else:
            raise Exception("Invalid data path!")
        return historical_data

    def bruhbruh(self, symbol, year=None):
        final = []
        if year == "all":
            if type(symbol) == list:
                for x in symbol:
                    for i, v in self.minute_data[x].items():
                        temp = {f"{x}_{i}": (self.minute_data[x][i])}
                        self.PURE_SYMBOL.append(x)
                        final.append(temp)
                final_np = np.array(final)
                return final_np
            elif type(symbol) == str:
                self.PURE_SYMBOL.append(symbol)
                for i, v in self.minute_data[symbol].items():
                    temp = {f"{symbol}_{i}": (self.minute_data[symbol][i])}
                    final.append(temp)
                final_np = np.array(final)
                return final_np
            else:
                raise ValueError("Please enter a list or a string!")
        elif type(symbol) == list and all(i in (self.minute_data[x].keys()) for i in year for x in symbol):
            for i in range(len(year)):
                for x in symbol:
                    self.PURE_SYMBOL.append(x)
                    temp = {f"{x}_{year[i]}": self.minute_data[x][year[i]]}
                    final.append(temp)
            return final
        elif type(symbol) != list and all(i in (self.minute_data[symbol].keys()) for i in year):
            self.PURE_SYMBOL.append(symbol)
            for i in range(len(year)):
                temp = {f"{symbol}_{year[i]}": self.minute_data[symbol][year[i]]}
                final.append(temp)
            return final

        else:
            if type(symbol) == list:
                bruh = np.array([[i for i, v in self.minute_data[x].items()] for x in symbol])
            elif type(symbol) == str:
                bruh = np.array([i for i, v in self.minute_data[symbol].items()])
            else:
                raise Exception("Please enter data in either a 'str' or 'list'!")
            bruh2 = np.array([x for i in bruh for x in i]) if type(symbol) == list and len(symbol) > 1 else bruh
            bruh3 = np.array([i for i in bruh2 if i in bruh[0] and i in bruh[1]]) if type(symbol) == list and len(
                symbol) > 1 else bruh
            bruh4 = np.array(list(dict.fromkeys(bruh3))) if type(symbol) == list and len(symbol) > 1 else bruh
            raise ValueError(
                f"Please enter a year between 2019 and 2023 if available!\n{[i for i in symbol] if type(symbol) == list else symbol} only contains the years: {bruh4}")

    def getFile(self, symbol, year=None):
        final = []
        try:
            if all([symbol in self.minute_data] or [i in self.minute_data for i in symbol]) and not all(
                    i in self.hour_data for i in symbol):
                return self.bruhbruh(symbol, year)
        except TypeError:
            if all([i in self.minute_data for i in symbol]) and not all(i in self.hour_data for i in symbol):
                return self.bruhbruh(symbol, year)

        if symbol == "minute_data" or symbol == "max":
            if year == "all":
                for i, v in self.minute_data.items():
                    for x, y in v.items():
                        temp = {}
                        self.PURE_SYMBOL.append(i)
                        temp[f"{i}_{x}"] = y
                        final.append(temp)
            elif all(i in list(dict.fromkeys([y for i, v in self.minute_data.items() for y, x in v.items()])) for i in
                     year):
                for i, v in self.minute_data.items():
                    for x, y in v.items():
                        if x in year:
                            temp = {}
                            self.PURE_SYMBOL.append(i)
                            temp[f"{i}_{x}"] = y
                            final.append(temp)
            else:
                raise Exception(
                    f"Please enter a year between 2019 and 2023 if available!\n{symbol} only contains the years: {list(dict.fromkeys([y for i, v in self.minute_data.items() for y, x in v.items()]))}")

        elif symbol == "hour_data":
            for i, v in self.hour_data.items():
                self.PURE_SYMBOL.append(i)
                temp = {i: v}
                final.append(temp)

        elif type(symbol) == int and year is not None:
            if symbol < 1:
                raise Exception("Please enter a value larger or equal to 1")
            key_symbol = []
            count = 0
            index = 0
            while count < symbol:
                try:
                    if all(x in list(list(self.minute_data.items())[index][1].keys()) for x in year):
                        count += 1
                        key_symbol.append(list(self.minute_data.items())[index][0])
                except IndexError as error:
                    raise Exception(f"Values wanted to select is too large, the maximum value is {count}\n-->{error}")
                index += 1
            for _, k_sym in enumerate(key_symbol):
                for YEAR in year:
                    temp = {}
                    self.PURE_SYMBOL.append(key_symbol[_])
                    temp[f"{key_symbol[_]}_{YEAR}"] = self.minute_data[key_symbol[_]][YEAR]
                    final.append(temp)

        elif type(symbol) != list and not symbol == "all":
            if symbol in self.hour_data:
                self.PURE_SYMBOL.append(symbol)
                temp = {symbol: self.hour_data[symbol]}
                final.append(temp)

        elif type(symbol) == list and all(i in self.hour_data for i in symbol):
            for i in range(len(symbol)):
                temp = {}
                self.PURE_SYMBOL.append(symbol[i])
                temp[symbol[i]] = self.hour_data[symbol[i]]
                final.append(temp)

        elif symbol == "all":
            if year is None:
                for i, v in self.hour_data.items():
                    temp = {i: v}
                    final.append(temp)
                for i, v in self.minute_data.items():
                    for x, y in v.items():
                        temp = {}
                        self.PURE_SYMBOL.append(i)
                        temp[f"{i}_{x}"] = y
                        final.append(temp)

            elif all(i in [q for i, v in self.minute_data.items() for q, g in v.items()] for i in year):
                for i, v in self.minute_data.items():
                    for x, y in v.items():
                        if x in year:
                            temp = {}
                            self.PURE_SYMBOL.append(i)
                            temp[f"{i}_{x}"] = y
                            final.append(temp)
            elif year == "all":
                for i, v in self.minute_data.items():
                    for x, y in v.items():
                        temp = {}
                        self.PURE_SYMBOL.append(i)
                        temp[f"{i}_{x}"] = y
                        final.append(temp)
            else:
                raise Exception("Please enter a valid year from 2019-2022]")

        else:
            raise Exception("Symbol doesn't exists!")
        np_final = np.array(final)
        return np_final

    def unMerge(self, mergedData):
        finalData = {}
        for year, columns in mergedData.items():
            for column, data in columns.items():
                data.columns = [data.columns[i] + "_" + column for i in range(len(data.columns))]
        for symbol in self.SYMBOL:
            mergedDataReal = copy.deepcopy(mergedData)
            for year, column in mergedDataReal.items():
                temp = []
                col = []
                for key, value in column.items():
                    col.append(key)
                    temp.append(value[symbol + "_" + key])
                    mergedDataReal = functools.reduce(lambda a, b: pd.merge(a, b, left_index=True, right_index=True),
                                                      temp)
                mergedDataReal.columns = col
                finalData[symbol] = mergedDataReal
        return finalData

    def getColumn(self, columns: list, merge=False):
        for i in columns:
            if i not in np.array(["Close", "High", "Volume", "Low", "Open", "Date"]):
                raise Exception("""Please enter a valid parameter for columns!
Valid columns:  ["Close","High","Volume","Low","Open","Date"]""")
        if len(self.PATH) <= 3:
            data = self._read_file([i for i in self.PATHDICT.keys()])
        else:
            data = self._read_file("all")
        final_data = {}
        for symbol in np.array(
                [i for i in list(dict.fromkeys([y for i, v in self.minute_data.items() for y, x in v.items()])) if
                 type(self.year) == list and i in self.year or self.year == "all"]):
            vectorized = {}
            for column in columns:
                current_symbol = np.array([i for i, v in data.items() if str(symbol) in i])
                data_temp = [data.get(i) for i in current_symbol]
                current_year = []
                for temp_item in data_temp:
                    current_year.append(temp_item[column].rename(temp_item[column].name + "_" + temp_item["Symbol"][0]))
                merged_data = functools.reduce(lambda a, b: pd.merge(a, b, left_index=True, right_index=True),
                                               current_year)
                if isinstance(merged_data, pd.Series):
                    merged_data = merged_data.to_frame(current_symbol[0])
                elif isinstance(merged_data, pd.DataFrame):
                    merged_data.columns = current_symbol
                if not (len(merged_data.index) / len(self.SYMBOL)).is_integer():
                    while not (len(merged_data.index) / len(self.SYMBOL)).is_integer():
                        merged_data.drop(index=merged_data.index[-1], axis=0, inplace=True)
                vectorized[column] = merged_data
            final_data[symbol] = vectorized
        if not merge:
            final_data = self.unMerge(final_data)
        return final_data

    @staticmethod
    def read(file, symbol):
        data = {symbol: pd.read_csv(file, index_col="Date", parse_dates=True, engine="pyarrow")}

        return data

    def pathDict(self):
        for i in range(len(self.PATH)):
            self.PATHDICT[self.SYMBOL[i]] = self.PATH[i]

    def _read_file(self, position):
        from os.path import dirname, join
        data = {}
        if position == "all":
            with multiprocessing.Pool() as pool:
                args = np.array([(self.PATH[i], self.SYMBOL[i]) for i in range(len(self.PATH))])
                results = np.array(pool.starmap(self.read, args))
            for i in results:
                for x, y in i.items():
                    data[x] = y
            return data
        else:
            for i in position:
                data[i] = pd.read_csv(
                    join(dirname(__file__), self.PATHDICT[i]),
                    index_col="Date", parse_dates=True,
                    engine="pyarrow")
            return data
