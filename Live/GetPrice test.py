import pprint
import pandas as pd
from GetPrice import GetPrice


def printData(liveData=None):
    pprint.pprint(liveData)
    print("\n")
    pass


if __name__ == "__main__":
    bruh = GetPrice(
        ["BTC", "ETH", "BNB"], "USDT", "1d", printData, stackUp=False,
        getChange=True, live=True, timezone=7, _format=pd.DataFrame)
    bruh.getCurrentPrice()

    # print(getPrice.getOldData(_format=pd.DataFrame, klineInterval="1d", timeSince=
    # frozendict({"timeAmountSince": 100, "timeIntervalSince": "day"}), column=("Open", "High", "Low"), timezone=7))