import os
from binance.client import Client
import time
from binance import ThreadedWebsocketManager
from binance import ThreadedDepthCacheManager


def main():
    symbol = 'BTCUSDT'
    twm = ThreadedWebsocketManager()

    # Start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        # print(f"message type: {msg['e']}")
        # print(msg)
        return "aaa"

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    twm.join()


if __name__ == "__main__":
    main()