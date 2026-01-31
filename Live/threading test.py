from threading import Thread
from typing import Optional, Dict

from binance import ThreadedWebsocketManager

api_key = "6bGIW8dm1BrXD7MPNQJZ5wQsyv5yHDf2L0VoGqEw7562vGM3u44lf3d12sP45BHL"
secret_api_key = "B05gKqNJSpFu6eZuP0GVLUHLpuhsVnJJe9zTOdAvZwm6n7bhJQB0v2dM8JYye0R3"


def foo(bar):
    print(bar)


class ThreadWithReturnValue(ThreadedWebsocketManager, Thread):

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
                 requests_params: Optional[Dict[str, str]] = None, tld: str = 'com',
                 testnet: bool = False, group=None, target=None, name=None, args=(), kwargs={}):
        ThreadedWebsocketManager.__init__(self, api_key=api_key, api_secret=api_secret,
                                          requests_params=requests_params, tld=tld, testnet=testnet)
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def start_listener(self,  socket, path: str, callback):

        self._return = self.start_multiplex_socket(callback=callback, streams=["btc@kline_1s"])

    def join(self, *args):
        print("a")
        ThreadedWebsocketManager.join(self, *args)
        return self._return


twrv = ThreadWithReturnValue(api_key=api_key, api_secret=secret_api_key)
print("c")
twrv.start_multiplex_socket(callback=foo, streams=["btc@kline_1s"])
print(" b")
twrv.join()  # prints foo
