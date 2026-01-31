import math


class ExecuteFutureOrder:
    inPosition = None

    def __init__(self, client, SIDE, ENTRY_PRICE, QUANTITY, SYMBOL, pricePrecision, quantityPrecision,
                 TAKE_PROFIT_PERCENT,
                 STOP_LOSS_PERCENT, LEVERAGE,
                 ORDER_TYPE):
        self.SIDE = SIDE
        self.client = client
        self.pricePrecision = pricePrecision
        self.quantityPrecision = quantityPrecision
        if self.SIDE == "LONG":
            self.ORDER_SIDE = "BUY"
        elif self.SIDE == "SHORT":
            self.ORDER_SIDE = "SELL"
        self.ENTRY_PRICE = ENTRY_PRICE
        self.QUANTITY = math.ceil(QUANTITY) if self.quantityPrecision == 0 else math.ceil(
            QUANTITY * int("1" + "0" * quantityPrecision)) / int("1" + "0" * quantityPrecision)
        self.SYMBOL = SYMBOL
        self.TAKE_PROFIT_PERCENT = TAKE_PROFIT_PERCENT
        self.STOP_LOSS_PERCENT = STOP_LOSS_PERCENT
        self.LEVERAGE = LEVERAGE
        self.ORDER_TYPE = ORDER_TYPE
        self.LONG_TAKE_PROFIT = round(
            self.ENTRY_PRICE + ((self.ENTRY_PRICE * self.TAKE_PROFIT_PERCENT / 100) / self.LEVERAGE),
            self.pricePrecision)
        self.LONG_STOP_LOSS = round(
            self.ENTRY_PRICE - ((self.ENTRY_PRICE * self.STOP_LOSS_PERCENT / 100) / self.LEVERAGE), self.pricePrecision)
        self.SHORT_TAKE_PROFIT = round(
            self.ENTRY_PRICE - ((self.ENTRY_PRICE * self.TAKE_PROFIT_PERCENT / 100) / self.LEVERAGE),
            self.pricePrecision)
        self.SHORT_STOP_LOSS = round(
            self.ENTRY_PRICE + ((self.ENTRY_PRICE * self.STOP_LOSS_PERCENT / 100) / self.LEVERAGE), self.pricePrecision)

    def SEND_ORDER(self):
        try:
            if self.SIDE == "LONG":
                self.LONG()
            elif self.SIDE == "SHORT":
                self.SHORT()
            else:
                raise Exception("""ONLY ENTER 'LONG' OR 'SHORT'!""")
        except Exception as error:
            print(error)

    def OPEN_POSITION(self):
        try:
            ExecuteFutureOrder.inPosition = True
            print("Sending order")
            self.client.futures_change_leverage(symbol=self.SYMBOL, leverage=self.LEVERAGE)
            self.client.futures_create_order(symbol=self.SYMBOL, side=self.ORDER_SIDE, type=self.ORDER_TYPE,
                                             quantity=self.QUANTITY)
        except Exception as e:
            print(f"An error occur while sending order {self.SYMBOL}: {e}\n")

    def CHECK_POSITION(self):
        openPosition = self.client.futures_position_information(symbol=self.SYMBOL)[0]["entryPrice"]
        if openPosition == '0.0':
            ExecuteFutureOrder.inPosition = False
            self.client.futures_cancel_all_open_orders(symbol=self.SYMBOL)
            return "Not in position"
        else:
            ExecuteFutureOrder.inPosition = True
            return "Already in position"

    def LONG(self):
        try:
            if self.CHECK_POSITION() == "Not in position":
                self.OPEN_POSITION()
                self.client.futures_create_order(symbol=self.SYMBOL, side='SELL', type='TAKE_PROFIT_MARKET',
                                                 stopPrice=self.LONG_TAKE_PROFIT, closePosition='true')
                self.client.futures_create_order(symbol=self.SYMBOL, side='SELL', type='STOP_MARKET',
                                                 stopPrice=self.LONG_STOP_LOSS, closePosition='true')
            else:
                raise Exception("Already in position")
        except Exception as error:
            print(error)

    def SHORT(self):
        try:
            if self.CHECK_POSITION() == "Not in position":
                self.OPEN_POSITION()
                self.client.futures_create_order(symbol=self.SYMBOL, side='BUY', type='TAKE_PROFIT_MARKET',
                                                 stopPrice=self.SHORT_TAKE_PROFIT, closePosition='true')
                self.client.futures_create_order(symbol=self.SYMBOL, side='BUY', type='STOP_MARKET',
                                                 stopPrice=self.SHORT_STOP_LOSS, closePosition='true')
            else:
                raise Exception("Already in position")
        except Exception as error:
            print(error)

    def FORCE_STOP(self):
        try:
            if self.SIDE == "LONG":
                self.client.futures_cancel_all_open_orders(symbol=self.SYMBOL)
                self.client.futures_create_order(symbol=self.SYMBOL, side='SELL', type='MARKET', quantity=self.QUANTITY)
                print("Position closed!")
            elif self.SIDE == "SHORT":
                self.client.futures_cancel_all_open_orders(symbol=self.SYMBOL)
                self.client.futures_create_order(symbol=self.SYMBOL, side='BUY', type='MARKET', quantity=self.QUANTITY)
                print("Position closed!")
        except Exception as error:
            print(error)
