import json
import re
from copy import copy
from decimal import Decimal
from json import dumps
from math import floor
from pprint import PrettyPrinter
from time import sleep
from colorama import Fore, Style
from BinanceAPIConnector import BinanceAPIConnector, BinanceException

class TradeExecutor:
    def __init__(self, capital: str, portfolio: dict | list, quantity: float, margin: bool, borrowing=False,
                 margin_type=None, global_leverage=None, vip=None, confirmation=True, global_order_side=None, delay=3):
        self.margin = margin
        self.marginType = margin_type
        self.pp = PrettyPrinter(width=100)
        self.borrowing = borrowing
        self.BinanceAPIConnector = BinanceAPIConnector()
        if self.margin and self.marginType == "isolated":
            self.isolatedAccountLimit = self.BinanceAPIConnector.connect("/sapi/v1/margin/isolated/accountLimit", "GET")
            if len(portfolio) > self.isolatedAccountLimit["maxAccount"]:
                raise ValueError(f"Please reduce the number of coins in portfolio, maximum number of coins for "
                                 f"current isolated VIP level: {self.isolatedAccountLimit['maxAccount']} coins\n"
                                 f"            Your current coins count: {len(portfolio)}")
        if isinstance(global_leverage, str):
            self.globalLeverage = global_leverage.lower()
            if self.globalLeverage != "max":
                raise TypeError("Please enter either 'max' or a float or an integer for 'globalLeverage'")
        elif isinstance(global_leverage, (int, float)) or global_leverage is None:
            self.globalLeverage = global_leverage
        else:
            raise TypeError("Please enter either 'max' or a float or an integer for 'globalLeverage'")
        if global_leverage != "max":
            if global_leverage is not None and global_leverage < 1:
                raise ValueError("'globalLeverage' can't be smaller than 1!")
        if self.margin and self.marginType not in ["cross", "isolated"]:
            raise ValueError("Please enter either 'cross' or 'isolated' for 'marginType'!")
        if isinstance(quantity, bool) or isinstance(quantity, str) or quantity > 100 or quantity <= 0:
            raise ValueError("Please enter a valid integer or float for percentage between 0 and 100!")
        self.capitalAsset = capital.upper()
        if isinstance(portfolio, list):
            portfolio = {coin: 100 / len(portfolio) for coin in portfolio}
        if round(sum(portfolio.values())) < 100:
            raise ValueError(f"Ratios does not add up to 100%, current ratio: {sum(portfolio.values())}%")
        elif round(sum(portfolio.values())) > 100:
            raise ValueError(f"Ratios exceed 100%, current ratio: {sum(portfolio.values())}%")
        self.shortSellingSymbols = []
        self.longBuyingSymbols = []
        self.shortSymbol = []
        self.longSymbol = []
        self.portfolio = {}
        invalid_coins = []
        self.userLeverage = {}
        self.globalOrderSide = global_order_side
        regex_format = r'^(L|S)_[A-Z]+_\d+(\.\d+)?X$'
        for i in portfolio.keys():
            num = re.search(regex_format, i.upper())
            if num:
                leverage_regex = r'_(\d+(\.\d+)?)X$'
                leverage = re.search(leverage_regex, i.upper())
                length = len(leverage.group(1)) + 2
                _symbol = i.upper()[:-length].replace(" ", "")
                if not self.globalLeverage and self.margin:
                    self.userLeverage[_symbol[2:] + self.capitalAsset] = float(
                        leverage.group(1))
                if not self.globalOrderSide and self.margin:
                    if _symbol[0] == "L":
                        self.longBuyingSymbols.append(_symbol[2:] + self.capitalAsset)
                    elif _symbol[0] == "S":
                        self.shortSellingSymbols.append(_symbol[2:] + self.capitalAsset)
                self.longSymbol.append(_symbol[2:] + self.capitalAsset)
                self.shortSymbol.append(_symbol[2:])
                self.portfolio[(_symbol[2:] + self.capitalAsset).upper()] = portfolio[i]
            else:
                invalid_coins.append(i)
        if invalid_coins:
            raise ValueError(
                f"Please enter the leverage and position side for each coin at the end of the string with the correct format: "
                f"L_COIN_2x, S_COIN_3.141x, L_COIN_10.0x, etc ...\nINVALID COINS FORMAT-> {invalid_coins}\nNote: Leverage can't have negative number!")
        if self.margin:
            if self.globalOrderSide is not None and self.globalOrderSide not in ["long", "short"]:
                raise ValueError("Please enter either 'long' or 'short' for parameter 'globalOrderSide' "
                                 "for order calculations!")
            if self.globalOrderSide:
                self.warn("USER WARNING! Any specific order side will overwritten by 'globalOrderSide'")
                if self.globalOrderSide == "long":
                    self.longBuyingSymbols = list(self.portfolio.keys())
                elif self.globalOrderSide == "short":
                    self.shortSellingSymbols = list(self.portfolio.keys())
        if vip > 9 or vip < 0:
            raise ValueError("VIP levels can only between 0 and 9 inclusive")
        self.vipLevel = vip
        self.capitalInterestRates = {}

        if self.marginType == "cross" or not self.margin:
            self.crossMarginData = self.BinanceAPIConnector.connect("/sapi/v1/margin/crossMarginData", "GET",
                                                                    otherParams={"vipLevel": self.vipLevel})
            if self.margin:
                self.maxLeverage = 10
                for i in self.crossMarginData:
                    if i["coin"] == self.capitalAsset:
                        self.capitalInterestRates[i["coin"]] = {"dailyInterest": float(i["dailyInterest"]),
                                                                "yearlyInterest": float(i["yearlyInterest"])}
                        break
            self.valid_asset = [i["coin"] for i in self.crossMarginData]
            self.valid_pair = [x for i in self.crossMarginData for x in i["marginablePairs"]]
        if self.margin:
            if not self.vipLevel and not self.vipLevel == 0:
                raise ValueError("Please specify your VIP level!")

            if self.globalLeverage is None and not self.userLeverage:
                raise ValueError("Please specify your global leverages for both cross and isolated margin! Or specify "
                                 "specify leverages for each coins at the end of the string with the correct format: "
                                 f"COIN_2x, COIN_3.141x, COIN_10.0x, etc ...")
            if self.globalLeverage:
                if isinstance(self.globalLeverage, (int, float)):
                    if 1 > self.globalLeverage > 10:
                        raise ValueError(
                            "Leverage can only be between 1 and 10 inclusive (depends on coins), or 'maximum'!")
                if isinstance(self.globalLeverage, str) and self.globalLeverage != 'max':
                    raise ValueError(
                        "Leverage can only be between 1 and 10 inclusive (depends on coins),o r 'maximum'!")
                if self.globalLeverage != "max":
                    self.userLeverage = self.globalLeverage
                    self.warn(
                        "USER WARNING: Any specific leverages will be overwritten by 'globalLeverage!")
                else:
                    if self.marginType == "cross":
                        self.BinanceAPIConnector.connect("/sapi/v1/margin/max-leverage", "POST",
                                                         otherParams={"maxLeverage": 10})
                        self.userLeverage = 10
                    self.warn("USER WARNING: Any specific leverages will be overwritten and set to maximum leverage for each coins!")

            if self.marginType == "isolated":
                valid_asset = set()
                self.valid_pair = []
                self.marginData = BinanceAPIConnector().connect("/sapi/v1/margin/isolatedMarginData", "GET",
                                                                otherParams={"vipLevel": vip})
                self.maxLeverage = {}
                for i in self.marginData:
                    valid_asset.add(i["data"][0]["coin"])
                    self.valid_pair.append(i["symbol"])
                    if i["symbol"] in self.longSymbol:
                        self.maxLeverage[i["symbol"]] = int(i["leverage"])
                        if self.globalLeverage == "max":
                            self.userLeverage[i["symbol"]] = int(i["leverage"])
                    if not self.capitalInterestRates and i["data"][1]["coin"] == self.capitalAsset:
                        daily_interest = float(i["data"][1]["dailyInterest"])
                        self.capitalInterestRates[self.capitalAsset] = {"dailyInterest": daily_interest,
                                                                        "yearlyInterest": (
                                                                                (1 + daily_interest) ** 365 - 1)}
                self.valid_asset = list(valid_asset)
            self.check_asset_validity([i[:-len(self.capitalAsset)] for i in self.portfolio.keys()], "asset")
            self.check_asset_validity(list(self.portfolio.keys()), "pair")
            if self.globalLeverage != "max" or self.globalLeverage is None or isinstance(self.globalLeverage, int):
                invalid_coins = []
                for i in portfolio.keys():
                    leverage_regex = r'_(\d+(\.\d+)?)X$'
                    leverage = re.search(leverage_regex, i)
                    length = len(leverage.group(1)) + 2

                    symbol = (i.upper()[:-length].replace(" ", ""))[2:] + self.capitalAsset

                    max_leverage = self.maxLeverage[symbol] if self.marginType == "isolated" else self.maxLeverage

                    if not self.globalLeverage:
                        if float(leverage.group(1)) > max_leverage:
                            invalid_coins.append({symbol: max_leverage})
                    else:
                        if self.marginType == "cross":
                            if self.userLeverage > 10:
                                invalid_coins.append({symbol: max_leverage})
                        elif self.userLeverage > self.maxLeverage[symbol]:
                            invalid_coins.append({symbol: max_leverage})

                if invalid_coins:
                    raise ValueError(f"Leverage exceeded maximum. Valid leverage amount: {invalid_coins}")
        self.check_asset_validity(self.longSymbol, coin_type="pair")
        self.allowance = None
        self.capital = None
        self.buyAmount = None
        self.currentPrice = None
        self.quantityPrecision = {}
        self._order = None
        self.quantity = quantity
        self.confirmation = confirmation
        self.stableCoins = ["USDT", "USDC", "FDUSD", "DAI", "TUSDT", "USDP", "BUSD"]
        self.delay = delay

    def check_asset_validity(self, asset_list: list, coin_type: str):
        valid_format = isinstance(asset_list, list)
        if not valid_format:
            raise TypeError("Please enter values in a list format or numpy.ndarray!")
        if coin_type == "asset":
            for i in asset_list:
                if i not in self.valid_asset:
                    raise ValueError(f"{i} is not a valid asset!")
        elif coin_type == "pair":
            for i in asset_list:
                if i not in self.valid_pair:
                    raise ValueError(f"{i} is not a valid pair!")
        else:
            raise ValueError("Please check either assets or pairs!")

    @classmethod
    def warn(cls, string):
        print(Fore.RED + string + Style.RESET_ALL)

    @classmethod
    def notice(cls, string):
        print(Fore.LIGHTYELLOW_EX + string + Style.RESET_ALL)

    @classmethod
    def success(cls, string):
        print(Fore.GREEN + string + Style.RESET_ALL)

    def _select_assets(self, additional_symbols=None, specific_symbols=None, exclude_symbols=None, everything=False):
        valid_asset = self.shortSymbol + additional_symbols if additional_symbols is not None else specific_symbols \
            if specific_symbols is not None else self.valid_asset if everything else self.shortSymbol

        if exclude_symbols is not None:
            check_asset = copy(valid_asset)
            for i in exclude_symbols:
                if i in check_asset:
                    check_asset.remove(i)
            return check_asset
        else:
            return valid_asset

    def lock_to_flexible(self, additional_symbols=None, specific_symbols=None, exclude_symbols=None, everything=False,
                         recheck_validity=True, lock_capital=True, amount="100%", specific_amount=None):
        if everything and not lock_capital:
            raise ValueError(f"If you don't want to lock capital asset -> {self.capitalAsset} then use excludeSymbols"
                             f" instead of everything!")
        else:
            lock_capital = True

        self._validate_parameter(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                 everything=everything, recheck_validity=recheck_validity,
                                 remove_capital=not lock_capital)

        coin_list = self._select_assets(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                        exclude_symbols=exclude_symbols, everything=everything)

        if lock_capital:
            coin_list.append(self.capitalAsset)

        updated_portfolio = self.current_portfolio(check_asset_validity=False, check_precision=False, pair=False,
                                                   redeem_from_flexible=False, specific_symbols=coin_list,
                                                   ignore_zero_balance=True, recheck_validity=False,
                                                   redeem_capital=False)
        coin_list = self._compute_amount(coin_list, amount, specific_amount)
        invalid_locks = []
        for SYMBOL in \
                self.BinanceAPIConnector.connect("/sapi/v1/simple-earn/flexible/list", "GET",
                                                 otherParams={"size": 100})[
                    "rows"]:
            if SYMBOL['asset'] in list(updated_portfolio.keys()):
                current_balance = updated_portfolio[SYMBOL["asset"]][f"{SYMBOL['asset']}_Value"]
                lock_amount = self._round(current_balance * float(coin_list[SYMBOL["asset"]][:-1]) / 100 if isinstance(
                    coin_list[SYMBOL["asset"]], str) else coin_list[SYMBOL["asset"]], 8)
                if lock_amount <= current_balance:
                    if updated_portfolio[SYMBOL["asset"]][f"{SYMBOL['asset']}_Value"] > float(
                            SYMBOL["minPurchaseAmount"]):
                        if everything:
                            self.BinanceAPIConnector.connect("/sapi/v1/simple-earn/flexible/subscribe", "POST",
                                                             otherParams={"productId": SYMBOL["productId"],
                                                                          "amount": lock_amount,
                                                                          'autoSubscribe': 'true'})
                            self.success(f"{lock_amount} of {SYMBOL['asset']} has been locked to flexible earn")
                        elif SYMBOL['asset'] in coin_list:
                            if specific_symbols is None:
                                self.BinanceAPIConnector.connect("/sapi/v1/simple-earn/flexible/subscribe", "POST",
                                                                 otherParams={"productId": SYMBOL["productId"],
                                                                              "amount": lock_amount,
                                                                              "autoSubscribe": 'true'})

                                self.success(f"{lock_amount} of {SYMBOL['asset']} has been locked to flexible earn")
                            elif additional_symbols is None:
                                if SYMBOL["asset"] in specific_symbols:
                                    self.BinanceAPIConnector.connect("/sapi/v1/simple-earn/flexible/subscribe", "POST",
                                                                     otherParams={"productId": SYMBOL["productId"],
                                                                                  "amount": lock_amount,
                                                                                  "autoSubscribe": 'true'})
                                    self.success(f"{lock_amount} of {SYMBOL['asset']} has been locked to flexible earn")
                else:
                    invalid_locks.append({SYMBOL["asset"]: current_balance})
        if invalid_locks:
            raise ValueError(
                f"Unable to unlock those coin, amount exceed available balances. Max balances: {invalid_locks}")
        self.success("All assets in spot account has been locked to flexible earn!\n")

    def _compute_amount(self, coin_list, amount, specific_amount, pair=False):
        percentage_regex = r'^(0*(?:[1-9]\d?|100)(\.\d+)?)%$'
        if re.match(percentage_regex, amount) is None or not isinstance(amount, str):
            raise ValueError(
                "Please enter a valid string percentage (eg. '35%', '69%', ...) larger than 0% and smaller than or equal to 100% for 'amount', default value is '100%'\nWarning, too small amount would not get redeemed!")
        temp = copy(coin_list)
        coin_list = {}
        for i in temp:
            coin_list[i + self.capitalAsset if pair else i] = amount
        if pair and specific_amount:
            for k in copy(list(specific_amount.keys())):
                specific_amount[k + self.capitalAsset] = specific_amount[k]
                del specific_amount[k]
        if specific_amount:
            if not isinstance(specific_amount, dict):
                raise ValueError("Please enter amount in dictionary format {'COIN': 100}'")
            invalid_coin = []
            invalid_amount = []
            for key in specific_amount.keys():
                if key not in coin_list.keys():
                    invalid_coin.append(key)
                else:
                    if key in coin_list.keys():
                        if (isinstance(specific_amount[key], str) and (
                                re.match(percentage_regex, specific_amount[key]) is None)) or (
                                isinstance(specific_amount[key], (float, int)) and specific_amount[key] <= 0):
                            invalid_amount.append(key)
                        else:
                            coin_list[key] = specific_amount[key]
            if invalid_coin:
                TradeExecutor.warn(
                    f"USER WARNING: {invalid_coin} coins are not included in your coin selection, it will be ignored.")
            if invalid_amount:
                raise ValueError(
                    f"Please enter a valid string percentage (eg. '35%', '69%', ...) larger than 0% and smaller than or equal to 100% for specific {invalid_amount} coins amount\nWarning, too small amount would not get redeemed!")
        return coin_list

    def redeem_flexible(self, additional_symbols=None, specific_symbols=None, exclude_symbols=None, everything=False,
                        recheck_validity=True, redeem_capital=True, amount="100%", specific_amount=None):
        global redeem_amount
        if everything and not redeem_capital:
            raise ValueError(f"If you don't want to lock capital asset -> {self.capitalAsset} then use "
                             f"excludeSymbols instead of everything!")

        else:
            redeem_capital = True

        self._validate_parameter(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                 everything=everything, recheck_validity=recheck_validity,
                                 remove_capital=not redeem_capital)

        coin_list = self._select_assets(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                        exclude_symbols=exclude_symbols, everything=everything)
        if redeem_capital:
            coin_list.append(self.capitalAsset)
        coin_list = self._compute_amount(coin_list, amount, specific_amount)
        portfolio = \
            self.BinanceAPIConnector.connect("/sapi/v1/simple-earn/flexible/position", "GET",
                                             otherParams={"size": 100})[
                "rows"]
        invalid_redeems = []
        for SYMBOL in portfolio:
            try:
                if SYMBOL["asset"] in coin_list.keys():
                    redeem_amount = self._round(
                        float(SYMBOL["totalAmount"]) * float(coin_list[SYMBOL["asset"]][:-1]) / 100 if isinstance(
                            coin_list[SYMBOL["asset"]], str) else coin_list[SYMBOL["asset"]], 8)
                    if float(SYMBOL["totalAmount"]) >= redeem_amount:
                        if everything:
                            self.BinanceAPIConnector.connect("/sapi/v1/simple-earn/flexible/redeem", "POST",
                                                             otherParams={"productId": SYMBOL["productId"],
                                                                          "amount": redeem_amount})
                            self.success(f"{redeem_amount} of {SYMBOL['asset']} has been unlocked from flexible earn")

                        else:
                            if SYMBOL["asset"] in coin_list.keys() and SYMBOL["canRedeem"]:
                                if specific_symbols is None:
                                    self.BinanceAPIConnector.connect("/sapi/v1/simple-earn/flexible/redeem", "POST",
                                                                     otherParams={"productId": SYMBOL["productId"],
                                                                                  "amount": redeem_amount})
                                    self.success(
                                        f"{redeem_amount} of {SYMBOL['asset']} has been unlocked from flexible earn")
                                elif additional_symbols is None:
                                    if SYMBOL["asset"] in coin_list.keys():
                                        self.BinanceAPIConnector.connect("/sapi/v1/simple-earn/flexible/redeem", "POST",
                                                                         otherParams={"productId": SYMBOL["productId"],
                                                                                      "amount": redeem_amount})
                                        self.success(
                                            f"{redeem_amount} of {SYMBOL['asset']} has been unlocked from flexible "
                                            f"earn")
                    else:
                        invalid_redeems.append({SYMBOL["asset"]: float(SYMBOL["totalAmount"])})
            except BinanceException:
                self.warn(f"Unable to redeem {redeem_amount} {SYMBOL['asset']}, please manually redeem it!")

        self.success("All assets in portfolio has been redeemed from flexible earn!\n")
        if invalid_redeems:
            raise ValueError(
                f"Unable to redeem those coin, amount exceed available balances. Max balances: {invalid_redeems}")

    def current_portfolio(self, check_precision, check_asset_validity=True, redeem_from_flexible=True, everything=False,
                          additional_symbols=None, specific_symbols=None, exclude_symbols=None,
                          ignore_zero_balance=False,
                          recheck_validity=True, output=False, redeem_capital=True, pair=True, convert_precision=False,
                          account_type="spot", remove_capital=True, selling=False):
        self._validate_parameter(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                 recheck_validity=recheck_validity, remove_capital=remove_capital,
                                 everything=everything)
        valid_account_type = ["spot", "isolated", "cross"]
        if account_type not in valid_account_type:
            raise ValueError(f"'accountType' parameter only can either be: {valid_account_type}")
        coin_list = self._select_assets(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                        exclude_symbols=exclude_symbols, everything=everything)
        if check_asset_validity:
            self.check_asset_validity(coin_list, coin_type="asset")
        if redeem_capital and not redeem_from_flexible:
            self.redeem_flexible(specific_symbols=[self.capitalAsset], redeem_capital=redeem_capital)
        if redeem_from_flexible:
            self.redeem_flexible(specific_symbols=coin_list, recheck_validity=False, redeem_capital=redeem_capital)

        def find_precision(asset_list, is_pair):
            check = []
            if not is_pair:
                select2 = [i__ + self.capitalAsset for i__ in asset_list]
            else:
                select2 = asset_list

            for i_ in select2:
                if i_[:len(self.capitalAsset)] != self.capitalAsset and i_ not in self.quantityPrecision.keys():
                    check.append(i_)

            if check:
                try:
                    exchange_info = self.BinanceAPIConnector.connect("/api/v3/exchangeInfo", "GET", otherParams={
                        'symbols': json.dumps(list(set(check))).replace(" ", "")}, includeSignature=False, includeTimestamps=False)
                    for i in exchange_info['symbols']:
                        raw = float(i["filters"][1]["stepSize"])
                        precision___ = Decimal(str(raw))
                        decimal_place = abs(precision___.as_tuple().exponent)
                        if str(raw)[2] == "0" and precision___ == 1.0:
                            decimal_place = 0
                        self.quantityPrecision[i["symbol"]] = decimal_place
                except BinanceException as error:
                    raise ConnectionRefusedError(f"Request frequency to the API is too high, consider turning "
                                                 f"ignoreZeroBalance=True while checkPrecision=True\nError code: {error}")

        current_portfolio = {}

        account = [i for i in self.BinanceAPIConnector.connect("/api/v3/account", "GET")["balances"] if
                   i["asset"] in coin_list] if account_type == "spot" else \
            [i for i in self.BinanceAPIConnector.connect("/sapi/v1/margin/account", "GET")["userAssets"] if
             i["asset"] in coin_list + [self.capitalAsset]] if account_type == "cross" \
                else [[{"baseAsset": i["baseAsset"]["asset"], "free": float(i["baseAsset"]["free"]),
                        "borrowed": float(i["baseAsset"]["borrowed"])},
                       {"quoteAsset": i["quoteAsset"]["asset"], "free": float(i["quoteAsset"]["free"]),
                        "borrowed": float(i["quoteAsset"]["borrowed"])},
                       {"baseAssetIndexPrice": float(i["indexPrice"])}] for i in
                      self.BinanceAPIConnector.connect("/sapi/v1/margin/isolated/account", "GET")["assets"] if
                      i["baseAsset"]["asset"] in coin_list]
        if account_type == "isolated":
            for i in account:
                coin_value = i[0]['free']
                coin_name = i[0]['baseAsset']
                coin_borrow = i[0]['borrowed']
                quote_value = i[1]['free']
                quote_name = i[1]['quoteAsset']
                quote_borrow = i[1]['borrowed']

                if (
                        coin_value > 0 or quote_value > 0 or coin_borrow > 0 or quote_borrow > 0) or not ignore_zero_balance:
                    if pair and coin_name != self.capitalAsset or account_type == "isolated":
                        current_portfolio[coin_name + quote_name] = {f"{coin_name}_Base_Value": coin_value,
                                                                     f"{coin_name}_Base_Borrow": coin_borrow,
                                                                     f"{self.capitalAsset}_Quote_Value": quote_value,
                                                                     f"{self.capitalAsset}_Quote_Borrow": quote_borrow, }
        elif account_type == "cross":
            for i in account:
                if float(i["free"]) > 0 or float(i["borrowed"]) > 0 or not ignore_zero_balance:
                    if pair:
                        if i["asset"] != self.capitalAsset:
                            current_portfolio[i["asset"] + self.capitalAsset] = {
                                f"{i['asset']}_Value": float(i["free"]),
                                "borrowed": float(i["borrowed"])}
                        else:
                            current_portfolio[i["asset"]] = {f"{i['asset']}_Value": float(i["free"]),
                                                             "borrowed": float(i["borrowed"])}
                    elif not pair:
                        current_portfolio[i["asset"]] = {f"{i['asset']}_Value": float(i["free"]),
                                                         "borrowed": float(i["borrowed"])}
        else:
            for i in account:
                if float(i["free"]) > 0 or not ignore_zero_balance:
                    if pair and i["asset"] != self.capitalAsset:
                        current_portfolio[i["asset"] + self.capitalAsset] = {f"{i['asset']}_Value": float(i["free"])}
                    elif not pair:
                        current_portfolio[i["asset"]] = {f"{i['asset']}_Value": float(i["free"])}
        if self.quantityPrecision == {} or (all(
                [(i + self.capitalAsset if not pair else i) not in self.quantityPrecision.keys() for i in
                 coin_list]) and not selling) \
                or (all(
            [(i + self.capitalAsset if not pair else i) not in self.quantityPrecision.keys() for i in
             current_portfolio.keys()]) and not selling):
            if check_precision and not convert_precision:
                if selling:
                    temp = [i for i in current_portfolio.keys() if i not in self.quantityPrecision.keys()]
                else:
                    temp = [i + self.capitalAsset for i in coin_list if i not in self.quantityPrecision.keys()]
                if self.capitalAsset in temp:
                    temp.remove(self.capitalAsset)
                find_precision(temp, pair)
            elif check_precision and convert_precision:
                precision_list = self.BinanceAPIConnector.connect("/sapi/v1/convert/assetInfo", "GET")
                for i in precision_list:
                    if i["asset"] + self.capitalAsset not in self.quantityPrecision.keys() and \
                            i["asset"] + self.capitalAsset in list(current_portfolio.keys()):
                        self.quantityPrecision[i["asset"] + self.capitalAsset] = int(i["fraction"])
            elif not check_precision:
                for i in current_portfolio.keys():
                    self.quantityPrecision[i] = 8
        for symbol, data in current_portfolio.items():
            if check_precision:
                try:
                    precision = self.quantityPrecision[symbol if pair else symbol + self.capitalAsset]
                except KeyError:
                    precision = 8
            else:
                precision = 8

            if account_type == "isolated":
                current_portfolio[symbol][f"{symbol[:-len(self.capitalAsset)]}_Base_Value"] = self._round(
                    current_portfolio[symbol][f"{symbol[:-len(self.capitalAsset)]}_Base_Value"], precision)
            else:
                if symbol == self.capitalAsset:
                    current_portfolio[symbol][f"{self.capitalAsset}_Value"] = self._round(
                        current_portfolio[symbol][f"{self.capitalAsset}_Value"], 8)
                else:
                    _symbol = symbol[:-len(self.capitalAsset)] if pair else symbol
                    current_portfolio[symbol][f"{_symbol}_Value"] = self._round(
                        current_portfolio[symbol][f"{_symbol}_Value"], precision)

        if ignore_zero_balance:
            temp = copy(current_portfolio)

            if account_type == "isolated":
                for k, v in temp.items():
                    if temp[k][f"{k[:-len(self.capitalAsset)]}_Base_Value"] <= 0 and \
                            temp[k][f"{k[:-len(self.capitalAsset)]}_Base_Borrow"] <= 0 and \
                            temp[k][f"{self.capitalAsset}_Quote_Value"] <= 0 and \
                            temp[k][f"{self.capitalAsset}_Quote_Borrow"] <= 0:
                        del current_portfolio[k]
            else:
                if account_type == "cross":
                    for k, v in temp.items():
                        if k == self.capitalAsset:
                            _k = self.capitalAsset
                        else:
                            _k = k[:-len(self.capitalAsset)] if pair else k
                        if (not (temp[k][f"{_k}_Value"] > 0)) and (not temp[k]["borrowed"] > 0):
                            del current_portfolio[k]
                else:
                    for k, v in temp.items():
                        _k = k[:-len(self.capitalAsset)] if pair else k
                        if not temp[k][f"{_k}_Value"] > 0:
                            del current_portfolio[k]
        if current_portfolio == {}:
            self.warn("USER WARNING: There are currently no assets that has coin value > 0")
            return current_portfolio

        if account_type == "isolated":
            for i in account:
                if i[0]['baseAsset'] + i[1]['quoteAsset'] in current_portfolio.keys():
                    current_portfolio[i[0]['baseAsset'] + i[1]['quoteAsset']][
                        f"{i[0]['baseAsset']}_Base_Quote_Value"] = self._round(
                        i[2]['baseAssetIndexPrice'] * i[0]['free'], 8)

                    current_portfolio[i[0]['baseAsset'] + i[1]['quoteAsset']][f"{i[1]['quoteAsset']}_Total_Value"] = \
                        current_portfolio[i[0]['baseAsset'] + i[1]['quoteAsset']][
                            f"{i[0]['baseAsset']}_Base_Quote_Value"] + \
                        current_portfolio[i[0]['baseAsset'] + i[1]['quoteAsset']][f"{i[1]['quoteAsset']}_Quote_Value"]
            self.currentPrice = {}
            for i in account:
                self.currentPrice[i[0]["baseAsset"] + self.capitalAsset] = dict(Close=0)
                self.currentPrice[i[0]["baseAsset"] + self.capitalAsset]["Close"] = float(i[2]['baseAssetIndexPrice'])
        else:
            if not pair:
                select = [i__ + self.capitalAsset for i__ in list(current_portfolio.keys())]
            else:
                if account_type == "cross":
                    temp = list(current_portfolio.keys())
                    if self.capitalAsset in temp:
                        temp.remove(self.capitalAsset)
                    select = temp
                else:
                    select = list(current_portfolio.keys())
            self.currentPrice = {}
            for i in copy(select):
                self.currentPrice[i] = dict(Close=0)
                if i == self.capitalAsset * 2:
                    select.remove(i)

            if select and account_type != "isolated":
                price_list = self.BinanceAPIConnector.connect("/api/v3/ticker/price", "GET",
                                                              otherParams={"symbols": dumps(select).replace(" ", "")},
                                                              includeSignature=False, includeTimestamps=False)
                for i in price_list:
                    self.currentPrice[i["symbol"]]["Close"] = float(i["price"])
            for i in self.stableCoins:
                if not pair and i in current_portfolio.keys():
                    self.currentPrice[i + self.capitalAsset] = {"Close": 1}

            for symboL, price in self.currentPrice.items():
                current_portfolio[symboL if pair else symboL[:-len(self.capitalAsset)]][f"{self.capitalAsset}_Value"] = \
                    float(price["Close"]) * float(
                        current_portfolio[symboL if pair else symboL[:-len(self.capitalAsset)]][
                            f"{symboL[:-len(self.capitalAsset)]}_Value"])
                if account_type == "cross":
                    current_portfolio[symboL if pair else symboL[:-len(self.capitalAsset)]][
                        f"{self.capitalAsset}_Borrow_Value"] = \
                        float(price["Close"]) * float(
                            current_portfolio[symboL if pair else symboL[:-len(self.capitalAsset)]][
                                "borrowed"])
        if account_type == "cross" and self.capitalAsset in current_portfolio.keys() and self.capitalAsset in self.stableCoins:
            current_portfolio[self.capitalAsset][f"{self.capitalAsset}_Borrow_Value"] = \
                current_portfolio[self.capitalAsset]["borrowed"]

        if pair and account_type == "spot":
            sum_portfolio = sum([v[f"{self.capitalAsset}_Value"] for v in list(current_portfolio.values())])
            for k, v in current_portfolio.items():
                if k in self.longSymbol:
                    try:
                        current_portfolio[k]["Ratio"] = v[f"{self.capitalAsset}_Value"] / \
                                                        sum_portfolio * (100 * self.portfolio[k]) / 100
                    except ZeroDivisionError:
                        current_portfolio[k]["Ratio"] = 0
        if output:
            self._output_portfolio(current_portfolio, account_type, check_precision)
        return current_portfolio

    def _output_portfolio(self, portfolio, account_type, check_precision):
        self.pp.pprint(portfolio)
        total = self._round(sum(
            [portfolio[i][f'{self.capitalAsset}_Value'] + portfolio[i][
                f'{self.capitalAsset}_Borrow_Value'] for i in
             portfolio.keys() if i != self.capitalAsset]) if account_type == "cross" else
                            sum([i[f'{self.capitalAsset}_Total_Value'] for i in
                                 portfolio.values()]) if account_type == "isolated" else sum(
                                [i[f'{self.capitalAsset}_Value'] for i in portfolio.values()]), 8)
        if check_precision:
            print(f"Total computed value, with checking precision: {total} {self.capitalAsset}")
        else:
            print(f"Total computed value, without checking precision: {total} {self.capitalAsset}")

    @staticmethod
    def _round(item, precision):
        return floor(item * int(
            "1" + "0" * precision)) / int(
            "1" + "0" * precision)

    def _check_other_asset_validity(self, additional_symbols, specific_symbols):
        if additional_symbols:
            temp = copy(additional_symbols)
            if self.capitalAsset in temp:
                temp.remove(self.capitalAsset)
            self.check_asset_validity(temp, coin_type="asset")
            self.check_asset_validity([i.upper() + self.capitalAsset for i in temp], coin_type="pair")
        elif specific_symbols:
            temp = copy(specific_symbols)
            if self.capitalAsset in temp:
                temp.remove(self.capitalAsset)
            self.check_asset_validity(temp, coin_type="asset")
            self.check_asset_validity([i.upper() + self.capitalAsset for i in temp],
                                      coin_type="pair")

    def internal_transfer(self, from_place, to_place, additional_symbols=None, specific_symbols=None,
                          exclude_symbols=None,
                          everything=False, recheck_validity=True, portfolio=None,
                          isolated_transfer_asset=None):

        global base_amount, base_asset
        valid_place = ["spot", "isolated", "cross"]
        if from_place not in valid_place or to_place not in valid_place or from_place == to_place:
            raise ValueError(f"Please enter a valid destination to transfer asset, either parameter 'fromPlace' and "
                             f"'toPlace' must be: {valid_place}")
        if from_place == "isolated":
            valid_type = ["quote", "base", "both"]
            if isolated_transfer_asset not in valid_type:
                raise ValueError(
                    f"Please enter a valid asset type to transfer from isolated margin ('isolatedTransferAsset'), "
                    f"either parameter 'quote', 'base', or 'both'")
        if not portfolio:
            self._validate_parameter(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                     everything=everything, recheck_validity=recheck_validity,
                                     remove_capital=False)

            coin_list = self._select_assets(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                            exclude_symbols=exclude_symbols, everything=everything)
            if from_place == "spot":
                self.redeem_flexible(specific_symbols=coin_list, recheck_validity=False)
            portfolio = self.current_portfolio(check_asset_validity=False, check_precision=False,
                                               pair=True if to_place == "isolated" else False,
                                               redeem_from_flexible=False, specific_symbols=coin_list,
                                               ignore_zero_balance=True, recheck_validity=False, redeem_capital=False,
                                               account_type=from_place, remove_capital=False, selling=True)

            if not portfolio:
                self.success("All asset has been transferred!")
                return
        if from_place == "spot" and to_place == "cross":
            for k in portfolio.keys():
                self.BinanceAPIConnector.connect("/sapi/v1/asset/transfer", "POST",
                                                 otherParams={"type": "MAIN_MARGIN", "asset": k,
                                                              "amount": portfolio[k][f"{k}_Value"]})
                self.success(
                    f"{portfolio[k][f'{k}_Value']} {k} from spot has been transferred to cross margin account!")
            self.success("All asset has been transferred from spot to cross margin!\n")

        elif from_place == "cross" and to_place == "spot":
            for k in portfolio.keys():
                try:
                    if portfolio[k][f"{k}_Value"] > 0:
                        self.BinanceAPIConnector.connect("/sapi/v1/asset/transfer", "POST",
                                                         otherParams={"type": "MARGIN_MAIN", "asset": k,
                                                                      "amount": portfolio[k][f"{k}_Value"]})
                        self.success(
                            f"{portfolio[k][f'{k}_Value']} {k} from cross margin has been transferred to spot account!")
                except BinanceException as e:
                    self.warn(
                        f"Unable to transfer {portfolio[k][f'{k}_Value']} {k} to spot account, please manually repay all debts! Error code: {str(e)}")
            self.success("All asset has been transferred from cross margin to spot!")

        elif from_place == "spot" and to_place == "isolated":
            account = self.BinanceAPIConnector.connect("/sapi/v1/margin/isolated/account", "GET")['assets']
            activated_symbols = []
            for i in account:
                activated_symbols.append(i["symbol"])
            for i in copy(activated_symbols):
                if i not in self.portfolio.keys() and len(set(list(portfolio.keys()) + activated_symbols)) > \
                        self.isolatedAccountLimit["maxAccount"]:
                    try:
                        self.BinanceAPIConnector.connect("/sapi/v1/margin/isolated/account", "DELETE",
                                                         otherParams={"symbol": i})
                        activated_symbols.remove(i)
                        self.notice(f"Disabling {i} isolated pair account, pair not in portfolio! Waiting {self.delay} second!")
                        sleep(self.delay)
                    except BinanceException:
                        raise ValueError(f"Cannot disable {i} isolated margin pair, as there are still assets or debts of this pair. Please manually transfer/repay.")
            for k in portfolio.keys():
                if k not in activated_symbols:
                    self.notice(f"Enabling {k} isolated pair account, pair has not been activated. Waiting {self.delay} second!")
                    if portfolio[k][f"{self.capitalAsset}_Value"] > 0:
                        self.BinanceAPIConnector.connect("/sapi/v1/asset/transfer", "POST",
                                                         otherParams={"type": "MAIN_ISOLATED_MARGIN",
                                                                      "asset": self.capitalAsset, "ToSymbol": k,
                                                                      "amount": portfolio[k][
                                                                          f"{self.capitalAsset}_Value"]})
                        sleep(self.delay)
                        self.success(
                            f"{portfolio[k][f'{self.capitalAsset}_Value']} {self.capitalAsset} from spot has been enabled and transferred to {k} isolated margin! pair!")
                else:
                    if portfolio[k][f"{self.capitalAsset}_Value"] > 0:
                        self.BinanceAPIConnector.connect("/sapi/v1/asset/transfer", "POST",
                                                         otherParams={"type": "MAIN_ISOLATED_MARGIN",
                                                                      "asset": self.capitalAsset, "ToSymbol": k,
                                                                      "amount": portfolio[k][
                                                                          f"{self.capitalAsset}_Value"]})
                        self.success(
                            f"{portfolio[k][f'{self.capitalAsset}_Value']} {self.capitalAsset} from spot has been transferred to {k} isolated margin pair!")
            self.success("All asset has been transferred from spot to isolated margin!\n")

        elif from_place == "isolated" and to_place == "spot":
            account = self.BinanceAPIConnector.connect("/sapi/v1/margin/isolated/account", "GET")['assets']
            activated_symbols = []
            for i in account:
                if i["symbol"] in list(portfolio.keys()):
                    activated_symbols.append(i["symbol"])
            amount = {key: {"quote": {k.split('_')[0]: v for k, v in value.items() if k.endswith('_Quote_Value')},
                            "base": {k.split('_')[0]: v for k, v in value.items() if k.endswith('_Base_Value')}}
                      for key, value in portfolio.items()}
            for i in activated_symbols:
                try:
                    quote_asset = list(amount[i]["quote"].keys())[0]
                    quote_amount = list(amount[i]["quote"].values())[0]
                    base_asset = list(amount[i]["base"].keys())[0]
                    base_amount = list(amount[i]["base"].values())[0]

                    if isolated_transfer_asset == "quote" or isolated_transfer_asset == "both":
                        if quote_amount > 0:
                            self.BinanceAPIConnector.connect("/sapi/v1/asset/transfer", "POST",
                                                             otherParams={"type": "ISOLATED_MARGIN_MAIN",
                                                                          "asset": quote_asset,
                                                                          "amount": quote_amount, "FromSymbol": i})
                            self.success(
                                f"{quote_amount} {quote_asset} has been transferred out from isolated margin pair {i} to spot!")
                    elif isolated_transfer_asset == "base" or isolated_transfer_asset == "both":
                        if base_amount > 0:
                            self.BinanceAPIConnector.connect("/sapi/v1/asset/transfer", "POST",
                                                             otherParams={"type": "ISOLATED_MARGIN_MAIN",
                                                                          "asset": base_asset,
                                                                          "amount": base_amount, "FromSymbol": i})
                            self.success(
                                f"{base_amount} {base_asset} has been transferred out from isolated margin pair {i} to spot!")
                except BinanceException as e:
                    self.warn(
                        f"Unable to transfer {base_amount} {base_asset} to spot account, please manually repay all debts! Error code: {str(e)}")
            self.success("All asset has been transferred from isolated margin to spot!")

    def buy(self, lock_up_to_flexible=True, additional_symbols=None, specific_symbols=None,
            test_money=None, real_money=None, testing=False, minimum_amount=5.1, margin_collateral_ratio=0.0,
            order_type="market", order_mode="concentrated", order_activation_price=0,
            order_spread_amount=10, order_spread_deviation=0.1, slippage=0,
            take_profit_activation_price=5, stop_loss_activation_price=5,
            take_profit_mode="concentrated", take_profit_spread_amount=10, take_profit_spread_deviation=0.1,
            stop_loss_mode="concentrated", stop_loss_spread_amount=1, stop_loss_spread_deviation=5,
            ) -> None:
        """  marginCollateralRatio >0-1<
             Leveraged order (has been borrowed) margin buy amount
             {'BTCUSDT': {'borrow': 44.82848250000004,
                          'collateral': 0.0,
                          'normal': 4.980942500000005}} --> Collateral ratio: 0
             {'BTCUSDT': {'borrow': 22.41424125000002,
                          'collateral': 22.41424125000002,
                          'normal': 4.980942500000005}} --> Collateral ratio: 0.5
             {'BTCUSDT': {'borrow': 11.20712062500001,
                          'collateral': 33.621361875000034,
                          'normal': 4.980942500000005}} --> Collateral ratio: 0.75"""
        global margin_buy_amount, leveraged_buy_order
        if margin_collateral_ratio >= 1 or margin_collateral_ratio < 0:
            raise ValueError("'marginCollateralRatio' must be smaller than 1 and greater than or equal 0")
        self._validate_parameter(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                 everything=None)
        if order_type not in ["limit", "market"]:
            raise ValueError("Please enter either 'limit' or 'market' for order type!")
        if slippage < 0 or slippage > 0.2:
            raise ValueError("Slippage is too large, consider between 0.01 and 0.2")
        invalid_param1 = []
        _____ = {
            "orderMode": order_mode,
            "takeProfitMode": take_profit_mode,
            "stopLossMode": stop_loss_mode
        }
        for name, value in _____.items():
            if value not in ["spread", "concentrated"]:
                invalid_param1.append(name)
        if invalid_param1:
            raise ValueError(f"Please enter either 'spread' or 'concentrated' for these parameter: {invalid_param1}")

        def check_negative_values(**kwargs):
            invalid_params = []
            for NAME, VALUE in kwargs.items():
                if isinstance(VALUE, list):
                    if any(isinstance(val, (int, float)) and val < 0 for val in VALUE):
                        invalid_params.append(NAME)
                elif isinstance(VALUE, dict):
                    if any(isinstance(val, (int, float)) and val < 0 for val in VALUE.values()):
                        invalid_params.append(NAME)
                elif isinstance(VALUE, (int, float)):
                    if VALUE < 0:
                        invalid_params.append(NAME)
            return invalid_params

        invalid_param2 = check_negative_values(
            orderActivationPrice=order_activation_price,
            orderSpreadAmount=order_spread_amount,
            orderSpreadDeviation=order_spread_deviation,
            takeProfitActivationPrice=take_profit_activation_price,
            stopLossActivationPrice=stop_loss_activation_price,
            takeProfitSpreadAmount=take_profit_spread_amount,
            takeProfitSpreadDeviation=take_profit_spread_deviation,
            stopLossSpreadAmount=stop_loss_spread_amount,
            stopLossSpreadDeviation=stop_loss_spread_deviation,
            testMoney=test_money, realMoney=real_money, minimumAmount=minimum_amount
        )
        if invalid_param2:
            raise ValueError(f"Please enter a positive integer values for these parameter: {invalid_param2}")

        self.buyAmount = {}
        if test_money and real_money:
            raise ValueError("Can't have both 'testMoney' and 'realMoney' at the same time!")

        if test_money:
            self.allowance = self._round(float(test_money) / 100 * self.quantity, 8)

        else:
            self.capital = [i for i in self.BinanceAPIConnector.connect("/api/v3/account", "GET")["balances"] if
                            i["asset"] == self.capitalAsset][0]["free"]
            money = float(self.capital)
            if real_money:
                if money < real_money:
                    self.redeem_flexible(specific_symbols=[self.capitalAsset],
                                         specific_amount={self.capitalAsset: self._round(real_money - money, 8)})
            else:
                self.redeem_flexible(specific_symbols=[self.capitalAsset])
            self.capital = [i for i in self.BinanceAPIConnector.connect("/api/v3/account", "GET")["balances"] if
                            i["asset"] == self.capitalAsset][0]["free"]
            if real_money:
                if real_money > float(self.capital):
                    raise ValueError(
                        f"You don't have enough capital, your maximum allowance is {float(self.capital['free'])} {self.capitalAsset}")
                self.allowance = self._round(real_money / 100 * self.quantity, 8)
            else:
                self.allowance = self._round(float(self.capital) / 100 * self.quantity, 8)

        self.current_portfolio(check_precision=True, redeem_from_flexible=False, redeem_capital=False)

        if minimum_amount < 1:
            minimum_amount *= self.allowance

        if self.margin:
            leverage = sum(self.userLeverage.values()) / len(self.userLeverage) \
                if not self.globalLeverage or (
                    self.globalLeverage == "max" and self.marginType != "cross") else self.userLeverage
            upper_bound_borrow = self.allowance * leverage
            interest = (upper_bound_borrow * (
                    1 + self.capitalInterestRates[self.capitalAsset]["dailyInterest"])) - upper_bound_borrow
            self.allowance -= interest

        if self.allowance < minimum_amount and not self.margin:
            raise ValueError(
                f"Not enough capital to purchase! Please have at least {minimum_amount} dollars!\nCurrent "
                f"capital: "
                f" {self.allowance} {self.capitalAsset}\nUse convert instead!")
        for symbol in copy(list(self.portfolio.keys())):
            if self.portfolio[symbol] <= 0:
                del self.portfolio[symbol]
        sum_portfolio = sum(self.portfolio.values())
        for symbol in copy(list(self.portfolio.keys())):
            self.portfolio[symbol] = self.portfolio[symbol] / sum_portfolio * 100

        def _compute_portfolio(recompute_c=False):
            for symbol__ in self.portfolio.keys():
                position_multiplier = 0.9 if symbol__ in self.shortSellingSymbols and self.margin and self.marginType != "isolated" else 1
                multiplier = 1 if not self.margin else self.userLeverage if (
                                                                                    self.globalLeverage and self.globalLeverage != "max") or (
                                                                                    self.globalLeverage == "max" and self.marginType == "cross") else \
                    self.userLeverage[symbol__]
                max_multiplier = 1 if not self.margin else self.maxLeverage[
                    symbol__] if self.marginType == "isolated" else self.maxLeverage
                if symbol__ in self.shortSellingSymbols:
                    slippage_ = (1 + slippage)
                else:
                    slippage_ = (1 - slippage)
                capital__ = self.allowance * slippage_
                self.buyAmount[symbol__] = {'normal': capital__ / 100 * self.portfolio[symbol__]}
                self.buyAmount[symbol__]["borrow"] = ((capital__ / 100 * self.portfolio[symbol__]) * multiplier) - \
                                                     self.buyAmount[symbol__]["normal"]
                self.buyAmount[symbol__]["normal"] *= position_multiplier
                self.buyAmount[symbol__]["borrow"] *= position_multiplier
                if symbol__ in self.shortSellingSymbols and self.margin and self.marginType == "isolated":
                    self.buyAmount[symbol__]["normal"] = 0
                self.buyAmount[symbol__]["collateral"] = self.buyAmount[symbol__][
                                                             "borrow"] * margin_collateral_ratio + (
                                                                 (capital__ / 100 * self.portfolio[
                                                                     symbol__]) * max_multiplier * position_multiplier) - \
                                                         self.buyAmount[symbol__]["borrow"]
                self.buyAmount[symbol__]["borrow"] *= 1 - margin_collateral_ratio
                if recompute_c:
                    self.buyAmount[symbol__]["collateral"] = self.buyAmount[symbol__]["borrow"] * margin_collateral_ratio + ((capital__ / 100 * self.portfolio[symbol__]) * max_multiplier * position_multiplier) - self.buyAmount[symbol__]["borrow"]

        _compute_portfolio()

        def _rebalance():
            def _remove_item():
                try:
                    remove_asset = min(self.buyAmount,
                                       key=lambda _k: self.buyAmount[_k]['normal'] + self.buyAmount[_k]['borrow'])
                except ValueError:
                    available_allowance = f"Current allowance: {self.allowance} {self.capitalAsset}"
                    if self.margin:
                        raise ValueError(
                            f"Please use leverage greater than 1 for isolated short positions! Or reduce your 'marginCollateralRatio', or increase your investment beyond minimum amount!\n{available_allowance}")
                    else:
                        raise ValueError(f"Please increase your investment beyond minimum amount!\n{available_allowance}")
                try:
                    del_percent = self.portfolio[remove_asset]
                    del self.buyAmount[remove_asset]
                    del self.portfolio[remove_asset]

                    for KEY in self.portfolio.keys():
                        self.portfolio[KEY] += del_percent / (len(self.portfolio.keys()))

                    _compute_portfolio(True)

                except Exception:
                    raise ValueError(
                        f"Not enough capital to purchase! Please have at least {minimum_amount} dollars!"
                        f"\nCurrent capital: "
                        f" {self.allowance} {self.capitalAsset}\n{'Use convert instead!' if not self.margin else ''}")

            try:

                while (not sum(sum(inner_dict.values()) for inner_dict in self.buyAmount.values()) > len(
                        self.buyAmount) * minimum_amount or not sum(
                    sum(inner_dict.values()) for inner_dict in self.buyAmount.values()) / len(
                    self.buyAmount) > minimum_amount):
                    _remove_item()

            except ZeroDivisionError:
                raise ValueError(
                    f"Not enough capital to purchase! Please have more than {minimum_amount} dollars --> "
                    f"{'margin' if self.margin else 'spot'} notional order limit!\nCurrent capital: "
                    f" {self.allowance} {self.capitalAsset}\n{'Use convert instead!' if not self.margin else ''}")

            if any(value_['borrow'] + value_['normal'] < minimum_amount for value_ in self.buyAmount.values()):
                _remove_item()
                _rebalance()

        _rebalance()

        for _symbol in self.buyAmount.keys():
            if _symbol in self.shortSellingSymbols and self.margin and self.marginType == "isolated":
                self.buyAmount[_symbol]['normal'] = self.allowance / 100 * self.portfolio[_symbol]

        if self.margin:
            leveraged_buy_order = copy(self.buyAmount)
        for SYMBOL, AMOUNT in self.buyAmount.items():

            price = self.currentPrice[SYMBOL]["Close"]
            coin_value = self._round((AMOUNT["normal"] + AMOUNT["borrow"]) / price, self.quantityPrecision[SYMBOL])
            self.buyAmount[SYMBOL] = {
                f"{self.capitalAsset}_Value": self._round((AMOUNT["normal"] + AMOUNT["borrow"]), 8),
                f"{SYMBOL[:-len(self.capitalAsset)]}_Value": coin_value,
                f"{self.capitalAsset}_Collateral": self._round(AMOUNT["collateral"], 8)}
            if self.margin:
                if SYMBOL in self.shortSellingSymbols and self.margin and self.marginType != "isolated":
                    leveraged_unrounded = (AMOUNT["normal"] / 90 * 100) / price
                else:
                    leveraged_unrounded = AMOUNT["normal"] / price

                leveraged_coin_value = self._round(leveraged_unrounded, self.quantityPrecision[SYMBOL])
                if SYMBOL in self.shortSellingSymbols and self.margin and self.marginType != "isolated":
                    coin_value = self._round(AMOUNT["normal"] / 90 * 100, 8)
                else:
                    coin_value = self._round(AMOUNT["normal"], 8)
                leveraged_buy_order[SYMBOL] = {f"{self.capitalAsset}_Value": coin_value,
                                               f"{SYMBOL[:-len(self.capitalAsset)]}_Value": leveraged_coin_value}

        if self.margin and self.marginType == "isolated":
            for k in self.buyAmount.keys():
                if k in self.shortSellingSymbols:
                    _SYMBOL = k[:-len(self.capitalAsset)]
                    self.buyAmount[k][f"{_SYMBOL}_Value"] = self._round(
                        self.buyAmount[k][f"{_SYMBOL}_Value"] - leveraged_buy_order[k][f"{_SYMBOL}_Value"],
                        self.quantityPrecision[k])
                    self.buyAmount[k][f"{self.capitalAsset}_Value"] = self._round(
                        self.buyAmount[k][f"{self.capitalAsset}_Value"] - leveraged_buy_order[k][
                            f"{self.capitalAsset}_Value"], 8)

        def _spread_order(order):
            pass

        if order_type == "market" and order_mode == "spread":
            _spread_order(leveraged_buy_order, "order")
            _spread_order(self.buyAmount, "order")
        if take_profit_activation_price and take_profit_mode == "spread":
            _spread_order(leveraged_buy_order, "takeProfit")
            _spread_order(self.buyAmount, "takeProfit")
        if stop_loss_activation_price and stop_loss_mode == "spread":
            _spread_order(leveraged_buy_order, "stopLoss")
            _spread_order(self.buyAmount, "stopLoss")

        if self.margin:
            if self.longBuyingSymbols:
                long_order_data = {key: value for key, value in self.buyAmount.items() if key in self.longBuyingSymbols}
                if long_order_data:
                    print(f"Leveraged order (has been borrowed) margin buy amount")
                    self.pp.pprint(long_order_data)
            print("\n")
            if self.shortSellingSymbols:
                short_order_data = {key: value for key, value in self.buyAmount.items() if
                                    key in self.shortSellingSymbols}
                if short_order_data:
                    print(f"Leveraged order (has been borrowed) margin sell amount")
                    self.pp.pprint(short_order_data)

        capital = f"{self.capital}/{self.capitalAsset}" if not test_money else f"{test_money}/{self.capitalAsset}"
        sum_buy_amount = sum(
            [i[f"{self.capitalAsset}_Value"] for i in self.buyAmount.values()]) if self.margin else sum(
            [i[f"{self.capitalAsset}_Value"] for i in self.buyAmount.values()])
        if self.margin:
            sum_collateral = sum(i[f"{self.capitalAsset}_Collateral"] for i in self.buyAmount.values())
            print("\n")
            if self.longBuyingSymbols:
                long_order_data = {key: value for key, value in leveraged_buy_order.items() if
                                   key in self.longBuyingSymbols}
                if long_order_data:
                    print(f"Margin order buy amount")
                    self.pp.pprint(long_order_data)
            print("\n")
            if self.shortSellingSymbols:
                short_order_data = {key: value for key, value in leveraged_buy_order.items() if
                                    key in self.shortSellingSymbols}
                if short_order_data:
                    print(f"Margin order sell amount")
                    self.pp.pprint(short_order_data)
                    if self.marginType == "isolated":
                        self.warn("USER WARNING: Isolated short positions leverage will be offset by 1!")
            print("\n")
            margin_buy_amount = sum(item[f'{self.capitalAsset}_Value'] for item in leveraged_buy_order.values())

            borrow_amount = self._round(sum(
                self.buyAmount[i][f'{self.capitalAsset}_Value'] for i in self.buyAmount.keys() if
                i in self.shortSellingSymbols) + (sum(
                self.buyAmount[i][f'{self.capitalAsset}_Value'] for i in self.buyAmount.keys() if
                i in self.longBuyingSymbols) - sum(
                leveraged_buy_order[i][f'{self.capitalAsset}_Value'] for i in leveraged_buy_order.keys() if
                i in self.longBuyingSymbols)), 8)
            c_ratio = 1 - (borrow_amount / (margin_buy_amount + borrow_amount))
            available_margin = self._round(margin_buy_amount * c_ratio * 0.9, 8)

            print(
                f"Allowance: {self._round(self.allowance, 8)}, Transfer (to order) amount: {margin_buy_amount}, Order amount: {sum_buy_amount}, Collateral (to debt): {round(sum_collateral, 8)},\nBorrow amount: "
                f"{borrow_amount}, Available margin: {available_margin}, Number of coins: {len(self.buyAmount)}, Average leverage: {round(sum_buy_amount / margin_buy_amount, 4)}X, Capital: {capital}")
        else:
            self.pp.pprint(self.buyAmount)
            print(
                f"Allowance: {self.allowance}, Buy amount: {sum_buy_amount}, {capital}, Nums of coins: {len(self.buyAmount)}")

        if not testing and not test_money and not self.margin:
            if self._order_verification("buy"):
                failed_stack = []
                for SYMBOL, AMOUNT in self.buyAmount.items():
                    try:
                        self.BinanceAPIConnector.connect("/api/v3/order", "POST",
                                                         otherParams={"symbol": SYMBOL, "side": "BUY", "type": "MARKET",
                                                                      "quantity": AMOUNT[
                                                                          f"{SYMBOL[:-len(self.capitalAsset)]}_Value"]})
                        self.success(f"Bought: {AMOUNT[f'{SYMBOL[:-len(self.capitalAsset)]}_Value']} {SYMBOL}")
                    except BinanceException as e:
                        self.warn(
                            f"Something went wrong during purchasing, maybe {SYMBOL} already got purchased or "
                            f"insufficient order amount! Coin has been added to the failed stack!\n Error code: {e}\n")
                        failed_stack.append(
                            {"fromAsset": self.capitalAsset, "toAsset": SYMBOL.replace(self.capitalAsset, ""),
                             "toAmount": AMOUNT[f"{SYMBOL[:-len(self.capitalAsset)]}_Value"], "fromAmount": None})
                self.convert(portfolio=failed_stack, check_validity=False)
                if lock_up_to_flexible:
                    self.notice(f"Waiting for Binance to realize purchase.")
                    sleep(self.delay)
                    self.lock_to_flexible(additional_symbols, recheck_validity=False)
                    self.notice("Locking to flexible again to making sure!")
                    self.lock_to_flexible(additional_symbols, recheck_validity=False)
                    self.notice("Locking to flexible again to making sure!")
                    self.lock_to_flexible(additional_symbols, recheck_validity=False)
                    self.success("Finished! Happy investing!")

        elif not testing and not test_money and self.margin:
            if self._order_verification("margin"):
                print("\n")
                failed_orders = []
                if self.marginType == "cross":
                    self.internal_transfer(from_place="spot", to_place="cross", portfolio={
                        self.capitalAsset: {f"{self.capitalAsset}_Value": self._round(margin_buy_amount, 8)}})

                    self.notice("Waiting for Binance to realize transfers!\n")
                    sleep(self.delay)
                    if any(i in self.buyAmount.keys() for i in self.longBuyingSymbols):
                        leveraged_order_amount = sum(
                            self.buyAmount[key][f'{self.capitalAsset}_Value'] for key in self.longBuyingSymbols if
                            key in self.buyAmount.keys())
                        margin_order_amount = sum(
                            leveraged_buy_order[key][f'{self.capitalAsset}_Value'] for key in self.longBuyingSymbols if
                            key in leveraged_buy_order.keys())
                        borrow = self._round(leveraged_order_amount - margin_order_amount, 8)
                        if borrow > 0:
                            self.BinanceAPIConnector.connect("/sapi/v1/margin/borrow-repay", "POST",
                                                             otherParams={"asset": self.capitalAsset, "amount": borrow,
                                                                          "type": "BORROW"})
                        self.success(f"Borrowed {borrow} {self.capitalAsset}")
                    if any(i in self.buyAmount.keys() for i in self.shortSellingSymbols):
                        if any(i in self.buyAmount.keys() for i in self.longBuyingSymbols):
                            self.notice("Waiting for Binance to realize margin buy borrow!")
                            sleep(self.delay)
                        for i in self.shortSellingSymbols:
                            if i in self.buyAmount:
                                _coin = i[:-len(self.capitalAsset)]
                                _amount = self.buyAmount[i][f"{_coin}_Value"]
                                self.BinanceAPIConnector.connect("/sapi/v1/margin/borrow-repay", "POST",
                                                                 otherParams={"asset": _coin,
                                                                              "amount": _amount, "type": "BORROW"})
                                print(f"Borrowed {_amount} {_coin}")

                    self.notice("\nWaiting for Binance to realize borrows!\n")
                    sleep(self.delay)
                    for SYMBOL, AMOUNT in self.buyAmount.items():
                        order = {"symbol": SYMBOL, "side": "BUY" if SYMBOL in self.longBuyingSymbols else "SELL",
                                  "type": "MARKET", "quantity": AMOUNT[f"{SYMBOL[:-len(self.capitalAsset)]}_Value"]}
                        try:
                            self.BinanceAPIConnector.connect("/sapi/v1/margin/order", "POST",
                                                             otherParams=order)
                            self.success(
                                f"{'Longed' if SYMBOL in self.longBuyingSymbols else 'Shorted'}: {order['quantity']} {SYMBOL}")
                        except BinanceException as e:
                            self.warn(f"Unable to open position on {SYMBOL} pair. Retrying after finish. Error code: {str(e)}")
                            failed_orders.append(order)

                elif self.marginType == "isolated":
                    self.internal_transfer(from_place="spot", to_place="isolated", portfolio=leveraged_buy_order)
                    self.notice("Waiting for Binance to realize transfers!\n")
                    sleep(self.delay)
                    if any(i in self.buyAmount.keys() for i in self.longBuyingSymbols):
                        for i in self.longBuyingSymbols:
                            if i in self.buyAmount.keys():
                                _AMOUNT = self._round(
                                    self.buyAmount[i][f"{self.capitalAsset}_Value"] - leveraged_buy_order[i][
                                        f"{self.capitalAsset}_Value"], 8)
                                if _AMOUNT > 0:
                                    self.BinanceAPIConnector.connect("/sapi/v1/margin/borrow-repay", "POST",
                                                                     otherParams={"asset": self.capitalAsset,
                                                                                  "amount": _AMOUNT,
                                                                                  "isIsolated": "TRUE",
                                                                                  "symbol": i, "type": "BORROW"})
                                self.success(f"Borrowed {_AMOUNT} {self.capitalAsset} in pair {i}")
                    if any(i in self.buyAmount.keys() for i in self.shortSellingSymbols):
                        for i in self.shortSellingSymbols:
                            if i in self.buyAmount.keys():
                                _SYMBOL = i[:-len(self.capitalAsset)]
                                _AMOUNT = self.buyAmount[i][f"{_SYMBOL}_Value"]
                                self.BinanceAPIConnector.connect("/sapi/v1/margin/borrow-repay", "POST",
                                                                 otherParams={"asset": _SYMBOL,
                                                                              "amount": _AMOUNT,
                                                                              "isIsolated": "TRUE",
                                                                              "symbol": i, "type": "BORROW"})
                                self.success(f"Borrowed {_AMOUNT} {_SYMBOL} in pair {i}")
                    self.notice("\nWaiting for Binance to realize borrow!\n")
                    sleep(self.delay)
                    for SYMBOL, AMOUNT in self.buyAmount.items():
                        _SYMBOL = SYMBOL[:-len(self.capitalAsset)]
                        order = {
                            "side": "BUY" if SYMBOL in self.longBuyingSymbols else "SELL",
                            "type": "MARKET",
                            "symbol": SYMBOL,
                            "quantity": AMOUNT[f"{_SYMBOL}_Value"],
                            "isIsolated": "TRUE"}
                        try:

                            self.BinanceAPIConnector.connect("/sapi/v1/margin/order", "POST",
                                                             otherParams=order)
                            self.success(
                                f"{'Longed' if SYMBOL in self.longBuyingSymbols else 'Shorted'}: {order['quantity']} {SYMBOL}")
                        except BinanceException as e:
                            self.warn(f"Unable to open position on {SYMBOL} pair. Retrying after finish. Error code: {str(e)}")
                            failed_orders.append(order)
                if failed_orders:
                    self.notice(f"Retrying to order failed orders. Waiting {self.delay} seconds!")
                    sleep(self.delay)
                    for i in failed_orders:
                        try:
                            self.BinanceAPIConnector.connect("/sapi/v1/margin/order", "POST", otherParams=i)
                        except BinanceException:
                            self.warn(f"Unable to open position on {i['symbol']} pair. Retry failed, please manually order it.")
                self.lock_to_flexible(specific_symbols=["USDT"])

        elif testing or test_money:
            self.notice(
                "Please examine each order carefully, and turn 'testing=False' and 'testMoney=None' to execute a real "
                "order!")

    def _order_verification(self, type_order: str):
        if not self.confirmation:
            return True
        if type_order.lower() == "buy":
            self._order = "buy"
        elif type_order.lower() == "sell":
            self._order = "sell"
        elif type_order.lower() == "replace":
            self._order = "replace"
        elif type_order.lower() == "convert":
            self._order = "convert"
        elif type_order.lower() == "margin":
            self._order = "execute these orders using leveraged margin with"
        elif type_order.lower() == "long":
            self._order = "margin buy"
        elif type_order.lower() == "margin-close":
            self._order = "close these margin positions and repay all debts for"
        else:
            raise ValueError("Please enter `buy` or `sell` parameters correctly!")
        while True:
            verification = input(f"Are you sure you want to {self._order} the following assets (y | n): ")
            if verification.lower() == "n" or verification.lower() == "no":
                return False
            elif verification.lower() == "y" or verification.lower() == "yes":
                return True

    def _validate_parameter(self, additional_symbols, specific_symbols, everything, recheck_validity=True,
                            remove_capital=True):
        s_count = bool(additional_symbols) + bool(specific_symbols) + bool(everything)
        if s_count > 1:
            raise ValueError("Can't not have additionalSymbols, specificSymbols, and everything at the same time!")

        if additional_symbols:
            if self.capitalAsset in additional_symbols and remove_capital:
                additional_symbols.remove(self.capitalAsset)
            if recheck_validity:
                self._check_other_asset_validity(additional_symbols, None)

        elif specific_symbols:
            if self.capitalAsset in specific_symbols and remove_capital:
                specific_symbols.remove(self.capitalAsset)
            if recheck_validity:
                self._check_other_asset_validity(None, specific_symbols)

    def convert(self, portfolio, wallet="SPOT", check_validity=True):
        if wallet.upper() not in ["SPOT", "FUNDING"]:
            raise ValueError("Please enter either SPOT or FUNDING wallet type correctly!")
        if check_validity:
            coins = set([])
            for i in portfolio:
                if i["fromAsset"] != self.capitalAsset:
                    coins.add(i["fromAsset"])
                if i["toAsset"] != self.capitalAsset:
                    coins.add(i["toAsset"])
            self._check_other_asset_validity(specific_symbols=list(coins), additional_symbols=None)
        converted = []
        print("\n")

        for i in portfolio:
            try:
                quote = None
                if i["fromAmount"] is not None:
                    quote = self.BinanceAPIConnector.connect("/sapi/v1/convert/getQuote", "POST",
                                                             otherParams={"fromAsset": i["fromAsset"],
                                                                          "toAsset": i["toAsset"],
                                                                          "fromAmount": i["fromAmount"],
                                                                          "validTime": "2m",
                                                                          "walletType": wallet})
                elif i["toAmount"] is not None:
                    quote = self.BinanceAPIConnector.connect("/sapi/v1/convert/getQuote", "POST",
                                                             otherParams={"fromAsset": i["fromAsset"],
                                                                          "toAsset": i["toAsset"],
                                                                          "toAmount": i["toAmount"], "validTime": "2m",
                                                                          "walletType": wallet})

                self.BinanceAPIConnector.connect("/sapi/v1/convert/acceptQuote", "POST",
                                                 otherParams={"quoteId": quote["quoteId"]})
                converted.append(quote["quoteId"])
                self.notice(f"Converting from {i['fromAmount']} {i['fromAsset']} to {i['toAsset']}")
            except (BinanceException, KeyError):
                self.warn(
                    f"Failed to convert from {i['fromAmount']}  {i['fromAsset']} to {i['toAsset']}. Insufficient "
                    f"{i['fromAsset']} balance to be converted")
        if converted:
            self.notice(f"\nWaiting for Binance to realize transactions")
            sleep(self.delay)
            for i in converted:
                load = self.BinanceAPIConnector.connect(endpoint="/sapi/v1/convert/orderStatus", requestType="GET",
                                                        otherParams={"quoteId": i})
                if load["orderStatus"] == "SUCCESS":
                    self.success(
                        f"{load['fromAmount']} {load['fromAsset']} successfully converted to {load['toAmount']}"
                        f" {load['toAsset']} --- quoteId: {i} ")
                else:
                    self.warn(
                        f"{load['fromAmount']} {load['fromAsset']} failed converted to {load['toAmount']}"
                        f" {load['toAsset']} --- quoteId: {i} ")

    def sell(self, additional_symbols=None, specific_symbols=None, everything=False, exclude_symbols=None,
             convert=False, repay=True,
             order_side=None, amount="100%", specific_amount=None):
        global closed_long, closed_short

        def execute_sell(coin_):
            try:
                _coin = coin_[:-len(self.capitalAsset)]
                if self.margin:
                    if self.marginType == "cross":
                        if order_side is None or order_side == "long":
                            if available_asset[i][f"{_coin}_Value"]:
                                self.BinanceAPIConnector.connect("/sapi/v1/margin/order", "POST",
                                                                 otherParams={"symbol": coin_,
                                                                              "side": "SELL",
                                                                              "type": "MARKET",
                                                                              "quantity": available_asset[coin_][
                                                                                  f"{_coin}_Value"]})
                                closed_long.append(_coin)
                                self.success(f"Sold: {available_asset[coin_][f'{_coin}_Value']} {_coin}")
                        if order_side is None or order_side == "short":
                            if available_asset[i]["borrowed"]:
                                self.BinanceAPIConnector.connect("/sapi/v1/margin/order", "POST",
                                                                 otherParams={"symbol": coin_,
                                                                              "side": "BUY",
                                                                              "type": "MARKET",
                                                                              "quantity": available_asset[coin_][
                                                                                  f"{_coin}_Value"]})
                                closed_short.append(_coin)
                                self.success(f"Bought: {available_asset[coin_]['borrowed']} {_coin}")
                    elif self.marginType == "isolated":
                        if order_side is None or order_side == "long":
                            if available_asset[i][f"{_coin}_Base_Value"]:
                                self.BinanceAPIConnector.connect("/sapi/v1/margin/order", "POST",
                                                                 otherParams={"symbol": coin_,
                                                                              "side": "SELL",
                                                                              "type": "MARKET",
                                                                              "quantity": available_asset[i][
                                                                                  f"{_coin}_Base_Value"],
                                                                              "isIsolated": "TRUE"})
                                closed_long.append(_coin)
                                self.success(f"Sold: {available_asset[i][f'{_coin}_Base_Value']} {_coin}")
                        if order_side is None or order_side == "short":
                            if available_asset[i][f"{_coin}_Base_Borrow"]:
                                self.BinanceAPIConnector.connect("/sapi/v1/margin/order", "POST",
                                                                 otherParams={"symbol": coin_,
                                                                              "side": "BUY",
                                                                              "type": "MARKET",
                                                                              "quantity": available_asset[i][
                                                                                  f"{_coin}_Base_Value"],
                                                                              "isIsolated": "TRUE"})
                                closed_short.append(_coin)
                                self.success(f"Bought: {available_asset[i][f'{_coin}_Base_Borrow']} {_coin}")

                else:
                    self.BinanceAPIConnector.connect("/api/v3/order", "POST",
                                                     otherParams={"symbol": coin_, "side": "SELL", "type": "MARKET",
                                                                  "quantity": available_asset[coin_][f"{_coin}_Value"]})

                    self.success(f"Sold: {available_asset[coin_][f'{_coin}_Value']} {_coin}")

            except BinanceException as e_:
                if not self.margin:
                    failed_stack.append(
                        {"fromAsset": coin_.replace(self.capitalAsset, ""), "toAsset": self.capitalAsset,
                         "fromAmount": available_asset[coin_][
                             f"{coin_[:-len(self.capitalAsset)]}_Value"],
                         "toAmount": None})
                self.warn(
                    f"Cannot sell {coin_} because its market value < the limit of Binance's current notional size "
                    f"5 USDT, the coin has been added to the failed stack! Error: {e_}")

        if convert and self.margin:
            raise ValueError("Cannot use convert while margin mode is turned on!")
        if self.margin and (order_side is not None and order_side not in ["long", "short"]):
            raise ValueError("Please enter the valid side that you want to close position: 'long', 'short'")
        self._validate_parameter(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                 everything=None)
        failed_stack = []

        available_asset = None
        coin_list = self._select_assets(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                        exclude_symbols=exclude_symbols, everything=everything)
        if not self.margin:
            self.redeem_flexible(specific_symbols=coin_list, recheck_validity=False,
                                 exclude_symbols=[self.capitalAsset], amount=amount, specific_amount=specific_amount)
        account_type = "isolated" if self.margin and self.marginType == "isolated" \
            else "cross" if self.margin and self.marginType == "cross" else "spot"
        available_asset = self.current_portfolio(check_precision=True, check_asset_validity=False,
                                                 redeem_from_flexible=False, specific_symbols=coin_list,
                                                 ignore_zero_balance=True, recheck_validity=False,
                                                 convert_precision=False if self.margin else convert, output=False,
                                                 redeem_capital=False, selling=True, remove_capital=True,
                                                 account_type=account_type)
        if available_asset != {}:
            self.warn(
                "USER WARNING: Your portfolio has been simplified to hide asset that has coin value == 0.0!")
            print("\n")
            sell_amount = self._compute_amount(copy(available_asset), amount, specific_amount)
            for k in copy(list(available_asset.keys())):
                if k != self.capitalAsset:
                    precision = self.quantityPrecision[k]
                    coin = k[:-len(self.capitalAsset)]
                    if not self.margin or (self.marginType == "cross" and (order_side is None or order_side == "long")):
                        available_asset[k][f"{coin}_Value"] = self._round(
                            available_asset[k][f"{coin}_Value"] * float(sell_amount[k][:-1]) / 100 if isinstance(
                                sell_amount[k], str) else sell_amount[k], precision)
                        available_asset[k][f"{self.capitalAsset}_Value"] = self._round(
                            available_asset[k][f"{coin}_Value"] * self.currentPrice[k]["Close"], 8)
                        if available_asset[k][f"{coin}_Value"] == 0:
                            del available_asset[k]
                    if self.margin and self.marginType == "isolated":
                        available_asset[k][f"{coin}_Base_Value"] = self._round(
                            available_asset[k][f"{coin}_Base_Value"] * float(sell_amount[k][:-1]) / 100 if isinstance(
                                sell_amount[k], str) else sell_amount[k], precision)
                        available_asset[k][f"{self.capitalAsset}_Total_Value"] = self._round(
                            available_asset[k][f"{coin}_Base_Value"] * self.currentPrice[k]["Close"], 8)
                        del available_asset[k][f"{self.capitalAsset}_Quote_Value"]
                        del available_asset[k][f"{coin}_Base_Quote_Value"]
                        if available_asset[k][f"{self.capitalAsset}_Total_Value"] == 0:
                            del available_asset[k]
            self._output_portfolio(available_asset, account_type, True)

            if self._order_verification("margin-close" if self.margin else "sell" if not convert else "convert"):
                print("\n")
                if convert and not self.margin:
                    for COIN in list(available_asset.keys()):
                        failed_stack.append({"fromAsset": COIN.replace(self.capitalAsset, ""),
                                             "toAsset": self.capitalAsset,
                                             "fromAmount": available_asset[COIN][
                                                 f"{COIN[:-len(self.capitalAsset)]}_Value"], "toAmount": None})
                else:
                    if self.margin:
                        closed_long = []
                        closed_short = []
                    for i in available_asset.keys():
                        if i != self.capitalAsset:
                            execute_sell(i)
                    if self.margin and (closed_long or closed_short) and repay:
                        self.notice("\nWaiting for Binance to realize transactions!")
                        sleep(self.delay)
                        self.repay(specific_symbols=closed_long + closed_short)
                        self.repay(specific_symbols=closed_long + closed_short)

            self.convert(portfolio=failed_stack, check_validity=False)

    def repay(self, additional_symbols=None, specific_symbols=None, everything=False, exclude_symbols=None,
              amount="100%", specific_amount=None):
        if self.margin:
            self._validate_parameter(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                     everything=None)
            coin_list = self._select_assets(additional_symbols=additional_symbols, specific_symbols=specific_symbols,
                                            exclude_symbols=exclude_symbols, everything=everything)
            updated_balance = self.current_portfolio(check_precision=False, check_asset_validity=False,
                                                     redeem_from_flexible=False, specific_symbols=coin_list,
                                                     ignore_zero_balance=True, recheck_validity=False,
                                                     redeem_capital=False,
                                                     account_type="isolated" if self.margin and self.marginType == "isolated"
                                                     else "cross" if self.margin and self.marginType == "cross" else "spot")
            if self.marginType == "cross":
                coin_list.append(self.capitalAsset)
            coin_list = self._compute_amount(coin_list, amount, specific_amount, pair=True if self.margin == "isolated" else False)
            invalid_borrows = []
            for i in updated_balance.keys():
                try:
                    coin = self.capitalAsset if i == self.capitalAsset else i[:-len(self.capitalAsset)]
                    if self.marginType == "cross":
                        if updated_balance[i]["borrowed"]:
                            borrow = self._round(
                                float(updated_balance[i]["borrowed"] * float(coin_list[i][:-1]) / 100 if isinstance(
                                    coin_list[i], str) else coin_list[i]), 8)
                            if borrow > updated_balance[i]["borrowed"]:
                                invalid_borrows.append(i)
                                continue
                            amount = updated_balance[i][f"{coin}_Value"] if updated_balance[i][
                                                                                f"{coin}_Value"] < borrow else borrow

                            if coin == self.capitalAsset:
                                if updated_balance[i][f"{self.capitalAsset}_Value"]:
                                    self.BinanceAPIConnector.connect("/sapi/v1/margin/borrow-repay", "POST",
                                                                     otherParams={
                                                                         "asset": coin,
                                                                         "amount": amount,
                                                                         "type": "REPAY"})
                                    self.success(f"Repayed: {amount} {coin}")
                            else:
                                if updated_balance[i][f"{coin}_Value"]:
                                    self.BinanceAPIConnector.connect("/sapi/v1/margin/borrow-repay", "POST",
                                                                     otherParams={
                                                                         "asset": coin,
                                                                         "amount": amount,
                                                                         "type": "REPAY"})
                                    self.success(f"Repayed: {amount} {coin}")
                    elif self.marginType == "isolated":
                        if updated_balance[i][f"{self.capitalAsset}_Quote_Borrow"] and updated_balance[i][
                            f"{self.capitalAsset}_Quote_Value"]:
                            borrow = self._round(float(updated_balance[i][
                                                           f'{self.capitalAsset}_Quote_Borrow'] * float(
                                coin_list[i][:-1]) / 100 if isinstance(
                                coin_list[i], str) else coin_list[i]), 8)
                            if borrow > updated_balance[i][f'{self.capitalAsset}_Quote_Borrow']:
                                invalid_borrows.append(i)
                                continue
                            amount = updated_balance[i][f"{self.capitalAsset}_Quote_Value"] if updated_balance[i][
                                                                                                   f"{self.capitalAsset}_Quote_Value"] < borrow else borrow
                            self.BinanceAPIConnector.connect("/sapi/v1/margin/borrow-repay", "POST",
                                                             otherParams={"asset": self.capitalAsset,
                                                                          "amount": amount,
                                                                          "isIsolated": "TRUE",
                                                                          "symbol": i,
                                                                          "type": "REPAY"})
                            self.success(
                                f"Repayed:  {amount} {self.capitalAsset} in {i} pair")
                        else:
                            if updated_balance[i][f"{coin}_Base_Borrow"] and updated_balance[i][f"{coin}_Base_Value"]:
                                borrow = self._round(float(updated_balance[i][
                                                               f'{self.capitalAsset}_Base_Borrow'] * float(
                                    coin_list[i][:-1]) / 100 if isinstance(
                                    coin_list[i], str) else coin_list[i]), 8)
                                if borrow > updated_balance[i][f'{self.capitalAsset}_Base_Borrow']:
                                    invalid_borrows.append(i)
                                    continue
                                amount = updated_balance[i][f"{self.capitalAsset}_Base_Value"] if updated_balance[i][
                                                                                                      f"{self.capitalAsset}_Base_Value"] < borrow else borrow
                                self.BinanceAPIConnector.connect("/sapi/v1/margin/borrow-repay", "POST",
                                                                 otherParams={"asset": coin,
                                                                              "amount": amount,
                                                                              "isIsolated": "TRUE",
                                                                              "symbol": i,
                                                                              "type": "REPAY"})
                                self.success(
                                    f"Repayed: {amount} {coin} in {i} pair")
                except BinanceException:
                    pass
            if invalid_borrows:
                raise ValueError(
                    f"Unable to repay those coin, amount exceed debt. Max debts: {invalid_borrows}")
            self.success("All (partially) debts has been repayed!")
            self.warn(
                "USER WARNING: Please manually repay all remaining debts if there's small remains!")
        else:
            self.warn("USER WARNING: Use margin mode to repay debts!")
