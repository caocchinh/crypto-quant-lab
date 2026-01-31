import talib,numpy, json, websocket, pprint
import tradingview_ta
from binance.client import Client
from binance.enums import *
from tradingview_ta import *
import functools
import sys
import br

SOCKET = "wss://stream.binance.com:9443/ws/btcbusd@kline_1m"

inLongOrder1 = False

inShortOrder1 = False






TRADE_SYMBOL = "BTCUSDT"
TRADE_QUANTITY = 0.001

Bitcoin = TA_Handler(
    symbol="BTCUSDT",
    screener="Crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

api_key = "8bXhl5epOF0ArJj2ftZTExZFUobiZxOGpEz14Gcp4n1DOKZjQd6BRaZMx4Qm25yd"
secret_api_key ="oNEv4zJoyHJZV19HkLbIQrAM5ClBG1HfSzkI96pxdghTO8J6CP5MZiKJoqzFsEkx"
client = Client(api_key,secret_api_key)



def order(side, quantity,symbol, leverage,order_type="MARKET"):
    try:
        print("Sending order")
        order = client.futures_create_order(symbol=symbol,side=side,type=order_type,leverage=leverage,quantity=quantity)
        print(order)

    except Exception as e:
        print(e)
    return True

def LONG(entry_price,quantity,symbol,TAKE_PROFIT_PERCENT, STOP_LOSS_PERCENT,LEVERAGE):
    order(side="BUY", quantity=quantity,symbol=symbol,leverage=LEVERAGE)
    LONG_TAKE_PROFIT = round(entry_price + ((entry_price * TAKE_PROFIT_PERCENT / 100) / LEVERAGE))
    LONG_STOP_LOSS = round(entry_price - ((entry_price * STOP_LOSS_PERCENT / 100) / LEVERAGE))
    take_profit = client.futures_create_order(symbol=symbol, side='SELL', type='TAKE_PROFIT_MARKET', stopPrice=LONG_TAKE_PROFIT, closePosition='true' )
    stop_loss = client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET', stopPrice=LONG_STOP_LOSS, closePosition='true')


def SHORT(entry_price,quantity,symbol,TAKE_PROFIT_PERCENT, STOP_LOSS_PERCENT,LEVERAGE):
    order(side="SELL", quantity=quantity,symbol=symbol,leverage=LEVERAGE)
    SHORT_TAKE_PROFIT = round(entry_price - ((entry_price * TAKE_PROFIT_PERCENT / 100) / LEVERAGE))
    SHORT_STOP_LOSS = round( entry_price + ((entry_price * STOP_LOSS_PERCENT / 100) / LEVERAGE))
    take_profit = client.futures_create_order(symbol=symbol, side='BUY', type='TAKE_PROFIT_MARKET', stopPrice=SHORT_TAKE_PROFIT, closePosition='true' )
    stop_loss = client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET',stopPrice=SHORT_STOP_LOSS, closePosition='true')


def on_open(ws):
    print("Opened conncetion")
def on_close(ws):
    print("Closed conncetion")


def on_message(ws,message):

    json_message = json.loads(message)
    candle = json_message["k"]
    is_candle_closed = candle["x"]
    if is_candle_closed:

        if EXECUTION < -1000:
            SHORT(entry_price=round(TA_DATA["close"]), quantity=TRADE_QUANTITY, symbol=TRADE_SYMBOL,
                  TAKE_PROFIT_PERCENT=41, STOP_LOSS_PERCENT=20, LEVERAGE=125)
        elif EXECUTION > 1000:
            LONG(entry_price=round(TA_DATA["close"]), quantity=TRADE_QUANTITY, symbol=TRADE_SYMBOL,
                  TAKE_PROFIT_PERCENT=41, STOP_LOSS_PERCENT=20, LEVERAGE=125)


ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()

import functools
import time
from tradingview_ta import  *



Bitcoin = TA_Handler(
    symbol="BTCUSDT",
    screener="Crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

BULLISH = 3
VERY_BULLISH = 5
MEGA_BULLISH = 7

BEARISH = -3
VERY_BEARISH = -5
MEGA_BEARISH = -7

LEAST_IMPORTANT_INDICATOR = 1.1
NORMAL_INDICATOR = 1.3
IMPORTANT_INDICATOR = 1.5

WEAK_MOMENTUM = 0.7
NORMAL_MOMENTUM = 1.1
STRONG_MOMENTUM = 1.7

total = []
MOMENTUM = []
def incrementEXECUTION (importance, momentum,direction,indicator_name):
    global totaL
    global MOMENTUM

    if momentum != None:
     MOMENTUM.append(momentum)
    if direction!=None:
     total.append(direction * importance)


def mySum(n1,n2):
 return n1+n2




def checkEXECUTION():
 TA_DATA = (Bitcoin.get_analysis().indicators)
 AOS = TA_DATA["AO"] and TA_DATA["AO[1]"] and TA_DATA["AO[2]"]
 ADX = TA_DATA["ADX"]
 BBWIDTH = round(round(TA_DATA["BB.upper"] / TA_DATA["BB.lower"], 2) - 1, 2)
 THRESHOLD = {'ADX':  incrementEXECUTION(LEAST_IMPORTANT_INDICATOR,STRONG_MOMENTUM,None,"ADX") if (ADX > 26) else incrementEXECUTION(LEAST_IMPORTANT_INDICATOR,NORMAL_MOMENTUM,None,"ADX")  if (ADX >= 20) else incrementEXECUTION(NORMAL_INDICATOR,WEAK_MOMENTUM,None,"ADXx") ,
  'ADX_Signal_Line': incrementEXECUTION(NORMAL_INDICATOR,NORMAL_MOMENTUM,VERY_BULLISH,"ADX_Signal_Line") if ((mySum(TA_DATA["ADX+DI"],TA_DATA["ADX+DI[1]"]))-(mySum(TA_DATA["ADX-DI"],TA_DATA["ADX-DI[1]"])) > 10 ) else incrementEXECUTION(NORMAL_INDICATOR,NORMAL_MOMENTUM,VERY_BEARISH,"ADX_Signal_Line") if ((mySum(TA_DATA["ADX+DI"],TA_DATA["ADX+DI[1]"]))-(mySum(TA_DATA["ADX-DI"],TA_DATA["ADX-DI[1]"])) < -10 ) else incrementEXECUTION(NORMAL_INDICATOR,WEAK_MOMENTUM,None,"ADX_Signal_Line"),
  'AWESOME_OSCILLATORS': incrementEXECUTION(LEAST_IMPORTANT_INDICATOR,STRONG_MOMENTUM,VERY_BULLISH,"AWESOME_OSCILLATORS") if AOS >150 else incrementEXECUTION(LEAST_IMPORTANT_INDICATOR,STRONG_MOMENTUM,BULLISH,"AWESOME_OSCILLATORS") if AOS >100 else incrementEXECUTION(LEAST_IMPORTANT_INDICATOR,STRONG_MOMENTUM,VERY_BEARISH,"AWESOME_OSCILLATORS") if AOS <-150 else incrementEXECUTION(LEAST_IMPORTANT_INDICATOR,STRONG_MOMENTUM,BEARISH,"AWESOME_OSCILLATORS") if AOS < -100 else incrementEXECUTION(NORMAL_INDICATOR,WEAK_MOMENTUM,None,"AWESOME_OSCILLATORS"),
  "Exponential moving averages": incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,MEGA_BULLISH,"Exponential moving averages") if (TA_DATA["EMA100"]<TA_DATA["EMA50"] and TA_DATA["EMA50"] < TA_DATA["EMA30"] and TA_DATA["EMA30"]<TA_DATA["EMA20"] and TA_DATA["EMA20"]<TA_DATA["EMA10"] and TA_DATA["close"] > TA_DATA["EMA200"]+50) else  incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,MEGA_BEARISH,"Exponential moving averages") if (TA_DATA["EMA100"]>TA_DATA["EMA50"] and TA_DATA["EMA50"] > TA_DATA["EMA30"] and TA_DATA["EMA30"]>TA_DATA["EMA20"] and TA_DATA["EMA20"]>TA_DATA["EMA10"] and TA_DATA["close"] < TA_DATA["EMA200"]-50) else incrementEXECUTION(IMPORTANT_INDICATOR,NORMAL_MOMENTUM,VERY_BULLISH,"Exponential moving averages") if (TA_DATA["close"] > (TA_DATA["EMA200"]+100)) else incrementEXECUTION(IMPORTANT_INDICATOR,NORMAL_MOMENTUM,VERY_BEARISH,"Exponential moving averages") if (TA_DATA["close"] < (TA_DATA["EMA200"]-100)) else incrementEXECUTION(IMPORTANT_INDICATOR,WEAK_MOMENTUM,None,"Exponential moving averages"),
  "Simple moving averages": incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,VERY_BULLISH,"Simple moving averages") if  (TA_DATA["SMA100"]<TA_DATA["SMA50"] and TA_DATA["SMA50"] < TA_DATA["SMA30"] and TA_DATA["SMA30"]<TA_DATA["SMA20"] and TA_DATA["SMA20"]<TA_DATA["SMA10"] and TA_DATA["close"] > TA_DATA["SMA200"]+50) else  incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,MEGA_BEARISH,"Simple moving averages") if (TA_DATA["SMA100"]>TA_DATA["SMA50"] and TA_DATA["SMA50"] > TA_DATA["SMA30"] and TA_DATA["SMA30"]>TA_DATA["SMA20"] and TA_DATA["SMA20"]>TA_DATA["SMA10"] and TA_DATA["close"] < TA_DATA["SMA200"]-50) else incrementEXECUTION(IMPORTANT_INDICATOR,NORMAL_MOMENTUM,BULLISH,"Simple moving averages") if (TA_DATA["close"] > (TA_DATA["SMA200"]+100)) else incrementEXECUTION(IMPORTANT_INDICATOR,NORMAL_MOMENTUM,BEARISH,"Simple moving averages") if (TA_DATA["close"] < (TA_DATA["SMA200"]-100)) else incrementEXECUTION(IMPORTANT_INDICATOR,WEAK_MOMENTUM,None,"Simple moving averages"),
  'RSI': incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,BEARISH,"RSI") if TA_DATA["RSI"] >= 75 else incrementEXECUTION(NORMAL_INDICATOR,WEAK_MOMENTUM,None,"RSI") if (TA_DATA["RSI"] > 35 and TA_DATA["RSI"] < 60) else incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,BULLISH,"RSI") if TA_DATA["RSI"] <25 else None,
  'VWMA': incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,VERY_BULLISH,"VWMA") if TA_DATA["close"] > TA_DATA["VWMA"]+69 else incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,VERY_BEARISH,"VWMA") if TA_DATA["close"] < TA_DATA["VWMA"]-69 else incrementEXECUTION(IMPORTANT_INDICATOR,WEAK_MOMENTUM,None,"VWMA"),
  'MACD': incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,VERY_BULLISH,"MACD") if (TA_DATA["MACD.macd"] and TA_DATA["MACD.signal"] > 5)  and (TA_DATA["MACD.macd"] > TA_DATA["MACD.signal"]+1 ) else incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,VERY_BEARISH,"MACD") if (TA_DATA["MACD.macd"] and TA_DATA["MACD.signal"] < -5)  and (TA_DATA["MACD.macd"] < TA_DATA["MACD.signal"]-1 ) else incrementEXECUTION(NORMAL_INDICATOR,WEAK_MOMENTUM,None,"MACD"),
  'Momemtum oscillator':incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,MEGA_BEARISH,"Momemtum oscillator") if (TA_DATA["Mom"] and TA_DATA["Mom[1]"]) > 300 else incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,VERY_BULLISH,"Momemtum oscillator") if (TA_DATA["Mom"] and TA_DATA["Mom[1]"]) > 200 else incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,BULLISH,"Momemtum oscillator") if (TA_DATA["Mom"] and TA_DATA["Mom[1]"]) > 100 else incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,MEGA_BEARISH,"Momemtum oscillator") if (TA_DATA["Mom"] and TA_DATA["Mom[1]"]) < -300 else incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,VERY_BEARISH,"Momemtum oscillator") if (TA_DATA["Mom"] and TA_DATA["Mom[1]"]) < -200 else incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,BEARISH,"Momemtum oscillator") if (TA_DATA["Mom"] and TA_DATA["Mom[1]"]) < -100 else incrementEXECUTION(NORMAL_INDICATOR,WEAK_MOMENTUM,None,"Momemtum oscillator"),
  'Commodity channel index': incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,BULLISH,"Commodity channel index") if (TA_DATA["CCI20"] < -200) else incrementEXECUTION(NORMAL_INDICATOR,NORMAL_MOMENTUM,BULLISH,"Commodity channel index") if (TA_DATA["CCI20"] < -100) else  incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,BEARISH,"Commodity channel index") if (TA_DATA["CCI20"] > 200) else incrementEXECUTION(NORMAL_INDICATOR,NORMAL_MOMENTUM,BEARISH,"Commodity channel index") if (TA_DATA["CCI20"] > 100) else incrementEXECUTION(NORMAL_INDICATOR,WEAK_MOMENTUM,None,"Commodity channel index") if (TA_DATA["CCI20"] >-90 and TA_DATA["CCI20"] < 90) else None,
  'P.SAR': incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,BULLISH,"Parabolic SAR") if (TA_DATA["close"] > TA_DATA["P.SAR"]+100) else incrementEXECUTION(NORMAL_INDICATOR,NORMAL_MOMENTUM,BULLISH,"Parabolic SAR") if (TA_DATA["close"] > TA_DATA["P.SAR"]+30) else incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,BEARISH,"Parabolic SAR") if (TA_DATA["close"] < TA_DATA["P.SAR"]-100) else incrementEXECUTION(NORMAL_INDICATOR,NORMAL_MOMENTUM,BEARISH,"Parabolic SAR") if (TA_DATA["close"] < TA_DATA["P.SAR"]-30) else None,
  'Ultimate oscillator':incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,BULLISH,"Ultimate oscillator") if TA_DATA["UO"] >= 75 else incrementEXECUTION(NORMAL_INDICATOR,WEAK_MOMENTUM,None,"Ultimate oscillator") if (TA_DATA["UO"] > 35 and TA_DATA["UO"] < 60) else incrementEXECUTION(NORMAL_INDICATOR,STRONG_MOMENTUM,BEARISH,"Ultimate oscillator") if TA_DATA["RSI"] >= 75 else None,
  'Stochastic': incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,MEGA_BULLISH,"Stochastic") if ((TA_DATA["Stoch.D"] and TA_DATA["Stoch.D[1]"] or TA_DATA["Stoch.RSI.K"] < 20) and (TA_DATA["close"] > TA_DATA["EMA50"]+10 or TA_DATA["EMA20"] > TA_DATA["EMA50"]+30)) else incrementEXECUTION(IMPORTANT_INDICATOR,STRONG_MOMENTUM,MEGA_BEARISH,"Stochastic") if ((TA_DATA["Stoch.D"] and TA_DATA["Stoch.D[1]"] or TA_DATA["Stoch.RSI.K"] > 90) and (TA_DATA["close"] < TA_DATA["EMA50"]-10 or TA_DATA["EMA20"] - TA_DATA["EMA50"]-30)) else incrementEXECUTION(IMPORTANT_INDICATOR,NORMAL_MOMENTUM,BULLISH,"Stochastic") if ((TA_DATA["Stoch.D"] and TA_DATA["Stoch.D[1]"] or TA_DATA["Stoch.RSI.K"] < 20)) else incrementEXECUTION(IMPORTANT_INDICATOR,NORMAL_MOMENTUM,BEARISH,"Stochastic") if ((TA_DATA["Stoch.D"] and TA_DATA["Stoch.D[1]"] or TA_DATA["Stoch.RSI.K"] > 90)) else None }

 bruh = functools.reduce(lambda a,b:a*b,MOMENTUM)
 EXECUTION = round(bruh*sum(total))
 return EXECUTION