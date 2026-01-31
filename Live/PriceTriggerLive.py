from binance import ThreadedWebsocketManager, Client

api_key = "6bGIW8dm1BrXD7MPNQJZ5wQsyv5yHDf2L0VoGqEw7562vGM3u44lf3d12sP45BHL"
secret_api_key = "B05gKqNJSpFu6eZuP0GVLUHLpuhsVnJJe9zTOdAvZwm6n7bhJQB0v2dM8JYye0R3"
client = Client(api_key, secret_api_key)
twm = ThreadedWebsocketManager(api_key=api_key, api_secret=secret_api_key)

from TradeExecutor import TradeExecutor

capital_asset = "USDT"
portfolio = {
    "SEI": 4,
    "GRT": 4,
    "ARB": 4,
    "SOL": 4,
    "AVAX": 3,
    "DOT": 4,
    "MATIC": 4,
    "IMX": 4,
    "ADA": 3,
    "XRP": 3,
    "VET": 4,
    "RNDR": 4,
    "FIL": 4,
    "MINA": 4,
    "HBAR": 4,
    "APT": 3,
    "AGIX": 3,
    "THETA": 3,
    "SKL": 3,
    "ALGO": 3,
    "FTM": 3,
    "OP": 3,
    "STX": 3,
    "TRB": 4,
    "MANA": 3,
    "NEAR": 3,

    "KDA": 1,
    "RUNE": 1,
    "IOTA": 1,
    "RVN": 1,
    "QI": 1,
    "ICP": 1,
    "CAKE": 1,
    "RAY": 1,
    "ONE": 1,
}

static_order = TradeExecutor(capital_asset, portfolio, 99.99, margin=False, vip=0, leverage=10,
                             minimumAmount=5, testing=False, confirmation=False)


def main():
    twm.start()

    def handle_socket_message(msg):
        price = float(msg["data"]["k"]["c"])
        symbol = msg["stream"]
        threshold = (symbol == "btcusdt@kline_1s" and price <= 41550) or (symbol == "trbusdt@kline_1s" and price <= 127) \
                    or (symbol == "solusdt@kline_1s" and price <= 91)
        print(price, symbol, threshold)
        if threshold:
            static_order.buy(redeemFromFlexible=False)

    twm.start_multiplex_socket(callback=handle_socket_message,
                               streams=["trbusdt@kline_1s", "btcusdt@kline_1s", "solusdt@kline_1s"])
    twm.join()


if __name__ == "__main__":
    main()
