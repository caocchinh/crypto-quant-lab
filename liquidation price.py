# User A's information
collateral = 10000  # USDT
debt = 20000  # USDT
asset_amount = 1  # BTC
asset_price = 30000  # USDT

# Cross Margin liquidation ratio
liquidation_ratio = 1.1

# Calculating liquidation price
liquidation_price = (debt + collateral) / asset_amount / liquidation_ratio
print("The estimated liquidation price for BTC in this scenario is:", liquidation_price, "USDT")
