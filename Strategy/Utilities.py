import re
import numpy as np
import vectorbt as vbt
import pandas as pd
from itertools import combinations

vbt.settings.set_theme("light")
vbt.settings["plotting"]["layout"]["height"] = 530
vbt.settings["plotting"]["layout"]["width"] = 910
vbt.settings.portfolio["fees"] = 0.00042
vbt.settings.portfolio["slippage"] = 0.0005
vbt.settings.portfolio["sl_stop"] = 0.0025
vbt.settings.portfolio["tp_stop"] = 0.005


class Utilities:
    def __init__(self, mergedData, year, column, long_entries, short_entries, symbol, params, short_name,
                 value_type=None):
        self.mergedData = mergedData
        self.year = year
        self.column = column
        self.long_entries = long_entries
        self.short_entries = short_entries
        self.pf = vbt.Portfolio.from_signals(self.mergedData[self.year][self.column], entries=self.long_entries,
                                             short_entries=self.short_entries,
                                             upon_dir_conflict=vbt.portfolio.enums.DirectionConflictMode.Ignore,
                                             upon_opposite_entry=vbt.portfolio.enums.OppositeEntryMode.Close,
                                             sl_trail=False,
                                             freq="1m", init_cash=481.6685, size=1)
        self.SYMBOL = symbol
        self.params = params
        self.short_name = short_name
        self.value_type = value_type
        self.returns = self.pf.trades.win_rate()
        self.stats = self.pf.stats(silence_warnings=True, agg_func=None,
                                   metrics=["total_return", "total_trades", "win_rate", "profit_factor", "expectancy",
                                            "sharpe_ratio",
                                            "calmar_ratio", "omega_ratio", "sortino_ratio", "end_value"])

        if len(self.SYMBOL) > 1:
            self.stats.index = self.stats.index.rename("Symbol", level=-1)
        elif len(self.SYMBOL) == 1:
            pass
        self.bestStrategies = self.returnStrategies()

    def plot(self, trades=False, heatmap=False, volume=False):
        if trades:
            self.plotTrades()
        if heatmap:
            self.plotHeatMap()
        if volume:
            self.plotVolume()

    def plotTrades(self):
        for symbol in self.SYMBOL:
            fig = self.pf.plot(subplots=[
                "orders",
                "trade_pnl"
            ], column=self.bestStrategies[symbol]["Strategy"])

            fig.show()

    def plotHeatMap(self):
        if isinstance(self.returns, pd.Series):
            if len(self.returns.index[0]) < 2:
                for i, v in enumerate(self.returns):
                    print(f"{self.SYMBOL[i]}-{self.value_type}: {round(v * 100, 2)}%")
            elif len(self.returns.index[0]) >= 2 and len(self.SYMBOL) == 1:
                for x_level, y_level in combinations(self.params, 2):
                    try:
                        fig = self.returns.vbt.heatmap(
                            y_level=f"{self.short_name}_{x_level}",
                            x_level=f"{self.short_name}_{y_level}")
                        fig.show()
                    except ValueError as error:
                        print("Please optimize more parameters to plot heatmap!")
                        print(error)
            elif len(self.returns.index[0]) > 2 and len(self.SYMBOL) > 1:
                self.returns.index = self.returns.index.rename("Symbol", level=-1)
                for x_level, y_level in combinations(self.params, 2):
                    try:
                        fig = self.returns.vbt.heatmap(
                            y_level=f"{self.short_name}_{x_level}",
                            x_level=f"{self.short_name}_{y_level}",
                            slider_level="Symbol")
                        fig.show()
                    except ValueError as error:
                        print("Please optimize more parameters to plot heatmap! ")
                        print(error)
        elif isinstance(self.returns, np.float_):
            print(f"{self.SYMBOL[0]}-{self.value_type}: {round(self.returns * 100, 2)}%")

    def plotVolume(self):
        try:
            if isinstance(self.returns, pd.Series) or isinstance(self.returns, pd.DataFrame):
                if len(self.returns.index[0]) < 2:
                    for i, v in enumerate(self.returns):
                        print(f"{self.SYMBOL[i]}-{self.value_type}: {round(v * 100, 2)}%")
                elif len(self.returns.index[0]) >= 2 and len(self.SYMBOL) == 1:
                    for x_level, y_level, z_level in combinations(self.params, 3):
                        try:
                            fig = self.returns.vbt.volume(
                                y_level=f"{self.short_name}_{x_level}",
                                x_level=f"{self.short_name}_{y_level}",
                                z_level=f"{self.short_name}_{z_level}")
                            fig.show()
                        except ValueError as error:
                            print("Please optimize more parameters to plot heatmap! ")
                            print(error)

                elif len(self.returns.index[0]) > 2 and len(self.SYMBOL) > 1:
                    self.returns.index = self.returns.index.rename("Symbol", level=-1)
                    for x_level, y_level, z_level in combinations(self.params, 3):
                        try:
                            fig = self.returns.vbt.volume(
                                y_level=f"{self.short_name}_{x_level}",
                                x_level=f"{self.short_name}_{y_level}",
                                z_level=f"{self.short_name}_{z_level}",
                                slider_level="Symbol")
                            fig.show()
                        except ValueError as error:
                            print("Please optimize more parameters to plot heatmap! ")
                            print(error)
            elif isinstance(self.returns, np.float_):
                print(f"{self.SYMBOL[0]}-{self.value_type}: {round(self.returns * 100, 2)}%")
        except ValueError as error:
            print("Please optimize more parameters to plot volume! ")
            print(error)

    def returnStrategies(self):
        global largest, symbol
        if len(self.SYMBOL) > 1:
            averageMax_returnsDict = {}
            for index in self.SYMBOL:
                if index not in averageMax_returnsDict.keys():
                    averageMax_returnsDict[index] = {}
                    for index_value in self.stats.index:
                        strindex = "-".join(str(v) for v in index_value)
                        if index_value[-1] == index:
                            if index not in averageMax_returnsDict[index].keys():
                                averageMax_returnsDict[index][strindex] = np.array([], dtype="f")
                                for column in self.stats.columns:
                                    if index_value[-1] == index:
                                        real_index = strindex.split("-")
                                        for _, value in enumerate(real_index):
                                            try:
                                                if value.isdigit() and re.match(r'^-?\d+(?:\.\d+)$', value) is None:
                                                    real_index[_] = int(value)
                                                elif not re.match(r'^-?\d+(?:\.\d+)$',
                                                                  value) is None and not value.isdigit() and float(
                                                    value):
                                                    real_index[_] = float(value)
                                            except ValueError:
                                                pass
                                        real_index = tuple(real_index)
                                        averageMax_returnsDict[index][strindex] = np.append(
                                            averageMax_returnsDict[index][strindex], self.stats.loc[real_index][column])
            averageMax_returnsDictList = {}
            for index in self.stats.index:
                strindex = "-".join(str(v) for v in index)
                if not index[-1] in averageMax_returnsDictList.keys():
                    averageMax_returnsDictList[index[-1]] = {}
                if index not in averageMax_returnsDictList.keys():
                    averageMax_returnsDictList[index[-1]][strindex] = []
            final = {}

            for symbol in self.SYMBOL:
                if symbol not in final.keys():
                    final[symbol] = {}
                for count, key in enumerate(averageMax_returnsDictList[symbol].keys()):
                    for j in range(len(averageMax_returnsDictList[symbol].keys())):
                        averageMax_returnsDictList[symbol][key].append(
                            sum(averageMax_returnsDict[symbol][key] > list(averageMax_returnsDict[symbol].values())[j]))

                for i, v in averageMax_returnsDictList[symbol].items():
                    averageMax_returnsDictList[symbol][i] = sum(v)
                largest = None
                for i, v in averageMax_returnsDictList[symbol].items():
                    if largest is None:
                        largest = i
                    elif averageMax_returnsDictList[symbol][i] > averageMax_returnsDictList[symbol][largest]:
                        largest = i
                largest = largest.split("-")

                for index, value in enumerate(largest):
                    try:
                        if value.isdigit() and re.match(r'^-?\d+(?:\.\d+)$', value) is None:
                            largest[index] = int(value)
                        elif not re.match(r'^-?\d+(?:\.\d+)$', value) is None and not value.isdigit() and float(value):
                            largest[index] = float(value)
                    except ValueError:
                        pass
                final[symbol]["Strategy"] = tuple(largest)
                for i in self.stats:
                    final[symbol][i] = self.stats.loc[tuple(largest)][i]
            return final
        else:
            averageMax_returnsDict = {}
            for index in self.stats.index:
                if index not in averageMax_returnsDict.keys():
                    averageMax_returnsDict[index] = np.array([], dtype="f")
                    for column in self.stats.columns:
                        averageMax_returnsDict[index] = np.append(
                            averageMax_returnsDict[index], self.stats.loc[index][column])

            averageMax_returnsDictList = {}
            for index in self.stats.index:
                if index not in averageMax_returnsDictList.keys():
                    averageMax_returnsDictList[index] = []

            final = {}
            for symbol in self.SYMBOL:
                if symbol not in final.keys():
                    final[symbol] = {}
            for count, key in enumerate(averageMax_returnsDictList.keys()):
                for j in range(len(averageMax_returnsDictList.keys())):
                    averageMax_returnsDictList[key].append(sum(
                        averageMax_returnsDict[key] >
                        list(averageMax_returnsDict.values())[j]))

            for i, v in averageMax_returnsDictList.items():
                averageMax_returnsDictList[i] = sum(v)
                largest = None
            for i, v in averageMax_returnsDictList.items():
                if largest is None:
                    largest = i
                elif averageMax_returnsDictList[i] > averageMax_returnsDictList[largest]:
                    largest = i

            final[symbol]["Strategy"] = largest
            for i in self.stats:
                final[symbol][i] = self.stats.loc[largest][i]
        return final
