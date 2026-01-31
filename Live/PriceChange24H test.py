from PriceChange24H import PriceChange24H

a = PriceChange24H(coins=["BTC","BNB","ETH"],pairAsset="USDT").topLoser(10)
print(a)