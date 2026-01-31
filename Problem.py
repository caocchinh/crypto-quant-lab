import pprint

portfolio = {"RNDR": 20,
        "MINA": 30,
        "HBAR": 40,
        "ETH": 10}

leverage = {"RNDR": 5,
        "MINA": 3,
        "HBAR": 23,
        "ETH": 6}

buyAmount = {}
allowance = 100

for symbol in portfolio.keys():
        multiplier = leverage[symbol]
        buyAmount[symbol] = {'normal': allowance / 100 * portfolio[symbol]}
        buyAmount[symbol]["borrow"] = ((allowance / 100 * portfolio[symbol]) * multiplier) - \
                                                   buyAmount[symbol]["normal"]

newAllowance = sum(sum(inner_dict.values()) for inner_dict in buyAmount.values())

for pSYMBOL in buyAmount.keys():
        buyAmount[pSYMBOL]["order"] = newAllowance / 100 * portfolio[pSYMBOL]

pprint.pprint(buyAmount)
print("\n")

deleveragedBuyAmount = {}
for symbol in portfolio.keys():
        deleveragedBuyAmount[symbol] = buyAmount[symbol]["order"] / 100 * (portfolio[symbol]* leverage[symbol])


pprint.pprint(deleveragedBuyAmount)
print(sum(list(deleveragedBuyAmount.values())))