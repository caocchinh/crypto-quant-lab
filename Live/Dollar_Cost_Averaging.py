class DCA:
    def __int__(self, client, testing: bool, portfolio: dict, scope: int, slippage: int, amount: int):
        self.client = client
        self.testing = testing
        self.portfolio = {'ADAUSDT': {'COIN_Value': 70.3, 'USDT_Value': 25.766567856842396},
                          'ATOMUSDT': {'COIN_Value': 2.38, 'USDT_Value': 25.766567856842396},
                          'AVAXUSDT': {'COIN_Value': 1.74, 'USDT_Value': 25.766567856842396},
                          'BTCUSDT': {'COIN_Value': 0.00113, 'USDT_Value': 30.060995832982798},
                          'DOGEUSDT': {'COIN_Value': 355.0, 'USDT_Value': 25.766567856842396},
                          'DOTUSDT': {'COIN_Value': 4.06, 'USDT_Value': 21.472139880702},
                          'ETHUSDT': {'COIN_Value': 0.0119, 'USDT_Value': 21.472139880702},
                          'FILUSDT': {'COIN_Value': 4.87, 'USDT_Value': 21.472139880702},
                          'HBARUSDT': {'COIN_Value': 498.0, 'USDT_Value': 25.766567856842396},
                          'IMXUSDT': {'COIN_Value': 34.59, 'USDT_Value': 25.766567856842396},
                          'LINKUSDT': {'COIN_Value': 3.91, 'USDT_Value': 25.766567856842396},
                          'MATICUSDT': {'COIN_Value': 25.3, 'USDT_Value': 21.472139880702},
                          'MINAUSDT': {'COIN_Value': 38.1, 'USDT_Value': 21.472139880702},
                          'RNDRUSDT': {'COIN_Value': 13.22, 'USDT_Value': 25.766567856842396},
                          'SNXUSDT': {'COIN_Value': 7.8, 'USDT_Value': 17.177711904561598},
                          'SOLUSDT': {'COIN_Value': 1.05, 'USDT_Value': 21.472139880702},
                          'VETUSDT': {'COIN_Value': 1322.8, 'USDT_Value': 25.766567856842396},
                          'XRPUSDT': {'COIN_Value': 49.0, 'USDT_Value': 21.472139880702}}
        self.scope = scope
        self.slippage = slippage
        self.amount = amount
        self.threshold = 10.1

    def computeGrid(self):
        pass
