import time

from TradeExecutor import TradeExecutor


def main():
    capital_asset = "USDT"
    portfolio = {
        "L_VTHO_1.5X": 2.83,
        "L_SKL_1X": 2.83,
        "L_SEI_1X": 2.83,
        'S_DOGE_3X': 1.42,
        "L_AVAX_1X": 2.83,
        "L_GLMR_1X": 31.14,
        'S_IMX_2X': 2.44,
        'S_INJ_2X': 2.44,
        "L_COTI_1X": 0,
        'S_BEAMX_9X': 1.34,
        "L_ARB_1X": 0,
        "L_BTC_1X": 6.50,
        'S_MINA_9X': 1.34,
        'L_IMX_3X': 3.08,
        "L_FET_10X": 19.49,
        "L_FIL_10X": 19.49,
    }

    static_order = TradeExecutor(capital_asset, portfolio, 100, margin_type="cross",
                                 margin=True, confirmation=True
                                 , vip=0, global_leverage=2,
                                 global_order_side="long", delay=5)

    # static_order.redeem_flexible(everything=True)
    # static_order.lock_to_flexible(everything=True)
    # static_order.sell(everything=True, convert=False, amount="100%")
    # static_order.repay(everything=True)
    # time.sleep(5)
    # static_order.internal_transfer(specific_symbols=["USDT"], from_place="cross", to_place="spot", isolated_transfer_asset="base")
    static_order.buy(test_money=1000)


if __name__ == "__main__":
    main()
