import time

from TradeExecutor import TradeExecutor


def main():
    capital_asset = "USDT"
    portfolio = {
        "L_VTHO_1.5X": 4.35,
        "L_SKL_1X": 4.35,
        "L_SEI_1X": 4.35,
        'S_DOGE_3X': 2.18,
        "L_AVAX_1X": 4.35,
        "L_GLMR_1X": 48,
        'S_IMX_2X': 3.75,
        'S_INJ_2X': 3.75,
        "L_COTI_1X": 0,
        'S_BEAMX_9X': 2.06,
        "L_ARB_1X": 0,
        "L_BTC_1X":10,
        'S_MINA_9X': 2.06,
        'S_FTM_3X': 2.99,
        'L_IMX_3X': 4.75,
        "L_FET_10X":30,
        "L_FIL_10X": 30,
    }

    static_order = TradeExecutor(capital_asset, list(portfolio.keys()), 100, margin_type="cross",
                                 margin=True, confirmation=True
                                 , vip=0, global_leverage=2,
                                 global_order_side="long", delay=5)

    # static_order.redeem_flexible(everything=True)
    # static_order.lock_to_flexible(everything=True)
    # static_order.sell(everything=True, convert=False, amount="100%")
    # static_order.repay(everything=True)
    # time.sleep(5)
    static_order.internal_transfer(specific_symbols=["USDT"], from_place="cross", to_place="spot", isolated_transfer_asset="base")
    # static_order.buy()


if __name__ == "__main__":
    main()
