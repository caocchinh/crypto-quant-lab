import pprint

from DataGetter import DataGetter

if __name__ == "__main__":
    test = DataGetter(["BTC", "ETH", "PEPE", "ADA"], "USDT", klineInterval="1m")


    def prints(aa):
        pprint.pprint(aa)


    print(test.getLiveData(prints, column=["Open", "High", "Low", "Close", "Volume"], stackUp=False))
