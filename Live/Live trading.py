import decimal
import multiprocessing
import numpy as np
# import talib
# import vectorbt as vbt
import pprint
from binance import ThreadedWebsocketManager, Client
from cffi.backend_ctypes import xrange
from Live.FutureOrder import ExecuteFutureOrder

api_key = "6bGIW8dm1BrXD7MPNQJZ5wQsyv5yHDf2L0VoGqEw7562vGM3u44lf3d12sP45BHL"
secret_api_key = "B05gKqNJSpFu6eZuP0GVLUHLpuhsVnJJe9zTOdAvZwm6n7bhJQB0v2dM8JYye0R3"
client = Client(api_key, secret_api_key)
twm = ThreadedWebsocketManager(api_key=api_key, api_secret=secret_api_key)


def main(streams):
    prices = {}
    period = 26
    minutes = period * 15
    streams_symbols = [x[y]["stream"] for x in streams for y in x]
    twm.start()

    def getOldData(msg):
        if not msg["data"]["s"] in prices.keys():
            prices[msg["data"]["s"]] = dict(Open=[], High=[], Low=[], Close=[], Volume=[])

            for i in client.get_historical_klines_generator(msg["data"]["s"], Client.KLINE_INTERVAL_1MINUTE,
                                                            f"{minutes} minutes ago UTC"):
                prices[msg["data"]["s"]]["Open"].append(float(i[1]))
                prices[msg["data"]["s"]]["High"].append(float(i[2]))
                prices[msg["data"]["s"]]["Low"].append(float(i[3]))
                prices[msg["data"]["s"]]["Close"].append(float(i[4]))
                prices[msg["data"]["s"]]["Volume"].append(float(i[5]))

    def appendData(msg):
        if len(prices[msg["data"]["s"]]["Open"]) >= 2000:
            print("Restarted")
            prices[msg["data"]["s"]]["Open"] = prices[msg["data"]["s"]]["Open"][-period:]
            prices[msg["data"]["s"]]["High"] = prices[msg["data"]["s"]]["High"][-period:]
            prices[msg["data"]["s"]]["Low"] = prices[msg["data"]["s"]]["Low"][-period:]
            prices[msg["data"]["s"]]["Close"] = prices[msg["data"]["s"]]["Close"][-period:]
            prices[msg["data"]["s"]]["Volume"] = prices[msg["data"]["s"]]["Volume"][-period:]
        prices[msg["data"]["s"]]["Open"].append(float(msg["data"]["k"]["o"]))
        prices[msg["data"]["s"]]["High"].append(float(msg["data"]["k"]["h"]))
        prices[msg["data"]["s"]]["Low"].append(float(msg["data"]["k"]["h"]))
        prices[msg["data"]["s"]]["Close"].append(float(msg["data"]["k"]["c"]))
        prices[msg["data"]["s"]]["Volume"].append(float(msg["data"]["k"]["v"]))

    def calculateIndicator(msg):
        if "Signal" not in prices[msg["data"]["s"]].keys():
            prices[msg["data"]["s"]]["Signal"] = ""
        if "RSI" not in prices[msg["data"]["s"]].keys():
            prices[msg["data"]["s"]]["RSI"] = []

        def produce_signal(rsi, overbought, oversold):
            overbought = np.full(rsi.shape, overbought)
            oversold = np.full(rsi.shape, oversold)
            trend = np.where(vbt.nb.crossed_above_1d_nb(rsi, oversold), 1,
                             vbt.nb.crossed_above_1d_nb(rsi, oversold).astype(int))
            trend = np.where(vbt.nb.crossed_above_1d_nb(rsi, overbought), -1, trend)
            return trend[-1]

        def myIndicator(close, overbought=91, oversold=18):
            rsi = talib.RSI(np.array(close), period).real
            prices[msg["data"]["s"]]["RSI"].append(rsi[-1])
            trend = produce_signal(np.array(prices[msg["data"]["s"]]["RSI"]), overbought, oversold)
            return trend

        prices[msg["data"]["s"]]["Signal"] = myIndicator(prices[msg["data"]["s"]]["Close"])

    def sendOrder(msg):
        long = 1
        short = -1
        take_profit = 30
        stop_loss = 30
        try:
            if prices[msg["data"]["s"]]["Signal"] == short:
                ExecuteFutureOrder(client=client, SIDE="LONG",
                                   ENTRY_PRICE=float(msg["data"]["k"]["c"]),
                                   QUANTITY=25 / float(msg["data"]["k"]["c"]),
                                   SYMBOL=msg["data"]["s"],
                                   pricePrecision=streams[0][msg["data"]["s"]]["pricePrecision"],
                                   quantityPrecision=streams[0][msg["data"]["s"]]["quantityPrecision"],
                                   TAKE_PROFIT_PERCENT=take_profit,
                                   STOP_LOSS_PERCENT=stop_loss,
                                   LEVERAGE=streams[0][msg["data"]["s"]]["leverage"],
                                   ORDER_TYPE="MARKET").SEND_ORDER()
                print(f"Longed {msg['data']['s']} at {msg['data']['k']['c']}")
            elif prices[msg["data"]["s"]]["Signal"] == long:
                ExecuteFutureOrder(client=client, SIDE="SHORT",
                                   ENTRY_PRICE=float(msg["data"]["k"]["c"]),
                                   QUANTITY=25 / float(msg["data"]["k"]["c"]),
                                   SYMBOL=msg["data"]["s"],
                                   pricePrecision=streams[0][msg["data"]["s"]]["pricePrecision"],
                                   quantityPrecision=streams[0][msg["data"]["s"]]["quantityPrecision"],
                                   TAKE_PROFIT_PERCENT=take_profit,
                                   STOP_LOSS_PERCENT=stop_loss,
                                   LEVERAGE=streams[0][msg["data"]["s"]]["leverage"],
                                   ORDER_TYPE="MARKET").SEND_ORDER()
                print(f"Shorted {msg['data']['s']} at {msg['data']['k']['c']}")
        except Exception as error:
            print(error)

    def handle_socket_message(msg):
        try:
            getOldData(msg)
            if msg["data"]["k"]["x"]:
                appendData(msg)
                calculateIndicator(msg)
                sendOrder(msg)
        except Exception:
            pass
    print(streams_symbols)
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams_symbols)
    twm.join()


def run():
    leverage = client.futures_leverage_bracket()
    tradeQty = client._request_futures_api("get", "exchangeInfo")["symbols"]
    duplicatedModifiedLeverage = [i for i in leverage for x in tradeQty if
                                  i["symbol"] in x["symbol"] and "USDT" in i["symbol"][-4:]]
    duplicatedModifiedQty = [x for x in tradeQty for i in leverage if
                             x["symbol"] in i["symbol"] and "USDT" in x["symbol"][-4:]]
    unmodifiedFinalLeverage = []
    unmodifiedFinalQty = []
    for i in duplicatedModifiedQty:
        if i not in unmodifiedFinalQty:
            unmodifiedFinalQty.append(i)
    for i in duplicatedModifiedLeverage:
        if i not in unmodifiedFinalLeverage:
            unmodifiedFinalLeverage.append(i)
    final = {}
    for qty, leverage in zip(sorted(unmodifiedFinalQty, key=lambda d: d['symbol']),
                             sorted(unmodifiedFinalLeverage, key=lambda d: d['symbol'])):
        for keys in qty.keys():
            if keys == "filters":
                final[qty["symbol"]] = {"stream": qty["symbol"].lower() + "@kline_1m",
                                        "pricePrecision": abs(
                                            decimal.Decimal(qty["filters"][0]["tickSize"]).as_tuple().exponent),
                                        "quantityPrecision": qty["quantityPrecision"]}
        for values in leverage.values():
            if type(values) != str:
                final[leverage["symbol"]]["leverage"] = values[0]["initialLeverage"]
    chunks = 22
    from functools import reduce
    streams = [[reduce(lambda a, b: a | b, list({i: final[i]} for i in
                                                list(final.keys())[x:x + chunks]))] for x in
               xrange(0, len(final), chunks)]

    pprint.pprint(streams)
    # with multiprocessing.Pool() as pool:
    #     pool.map(main, streams)


if __name__ == "__main__":
    run()
