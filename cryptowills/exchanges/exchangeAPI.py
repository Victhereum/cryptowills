import time

import ccxt


class Exchange:
    """
    Instantiates any exchange
    """

    # pylint: disable=too-many-instance-attributes
    # Eleven is reasonable in this case.

    def __init__(
        self,
        exchange_name: str,
        api_Key: str,
        secret: str,
        addresses=None,
        identifier=None,
    ):
        self.identifier = identifier
        self.exchange_name = exchange_name
        self.api_Key = api_Key
        self.secret = secret
        self.addresses = addresses
        self.success = False
        self.balance = 0.00

        exchange = getattr(ccxt, self.exchange_name)

        self.exchange = exchange(
            {
                "api_key": self.api_Key,
                "secret": self.secret,
                "enableRateLimit": True,
            }
        )

    def __repr__(self):
        return self.exchange_name

    def is_valid(self):
        try:
            self.exchange.fetchBalance()
            return True
        except ccxt.AuthenticationError:
            return False

    def get_exchange_logo(self):
        return self.exchange.urls["logo"]

    def get_balance(self):
        start = time.time()
        balances = self.exchange.fetch_balance()["info"]["balances"]
        self.balance = 0.00
        for i in balances:
            if float(i["free"]) != 0 or float(i["locked"]) != 0:
                if i["asset"] != "USDT":
                    request = i["asset"] + "/USDT"
                    try:
                        # Get the SYMBOL price of the coin
                        price = float(self.exchange.fetchTicker(request)["last"])
                        # Multiply the total of this asset by it's price
                        val_usd = (float(i["free"]) + float(i["locked"])) * price
                        # Add this asset's balance to my total balance
                        self.balance += val_usd
                    except ccxt.ExchangeError:
                        try:
                            request = i["asset"] + "/BTC"
                            price = float(self.exchange.fetchTicker(request)["last"])
                            val_btc = (float(i["free"]) + float(i["locked"])) * price
                            price = float(self.exchange.fetchTicker("BTC/USDT")["last"])
                            self.balance += val_btc
                        except ccxt.ExchangeError:
                            try:
                                request = i["asset"] + "/ETH"
                                price = float(
                                    self.exchange.fetchTicker(request)["last"]
                                )
                                val_btc = (
                                    float(i["free"]) + float(i["locked"])
                                ) * price
                                price = float(
                                    self.exchange.fetchTicker("ETH/USDT")["last"]
                                )
                                self.balance += val_btc
                            except ccxt.ExchangeError:
                                print(i["asset"])

                            self.balance += (
                                float(i["free"]) + float(i["locked"])
                            ) * price
                        else:
                            self.balance += float(i["free"]) + float(i["locked"])
                self.latency = time.time() - start
        print(self.balance)
        return round(self.balance, 2)

    def get_all_coins(self):
        """
        Fetches all coins owned by the user
        """
        coin = []
        all_coins = self.exchange.fetch_balance()

        for key, value in all_coins["free"].items():
            if value > 0:
                coin.append(key)
        return coin

    def get_all_coin_balances_(self):
        """
        Fetches all coins with their amount owned by the user
        """
        all_balance = self.exchange.fetch_balance()
        balance = {}
        for key, value in all_balance["free"].items():
            if value > 0:
                balance[key] = value
        return balance

    def get_all_coin_balances(self):
        start = time.time()
        balances = self.exchange.fetch_balance()["info"]["balances"]
        self.balance = 0.00
        asset = {}
        asset_price = {}
        asset_usd_val = {}
        for i in balances:
            if float(i["free"]) != 0 or float(i["locked"]) != 0:
                if i["asset"] != "USDT":
                    request = i["asset"] + "/USDT"
                    asset[i["asset"]] = [i["asset"]]
                    try:
                        # Get the SYMBOL price of the coin
                        price = float(self.exchange.fetchTicker(request)["last"])
                        asset_price[i["asset"]] = price
                        # Multiply the total of this asset by it's price
                        val_usd = (float(i["free"]) + float(i["locked"])) * price
                        asset_usd_val[i["asset"]] = val_usd
                    except ccxt.ExchangeError:
                        # TODO: Work on exceptions later
                        try:
                            request = i["asset"] + "/BTC"
                            price = float(self.exchange.fetchTicker(request)["last"])
                            val_btc = (float(i["free"]) + float(i["locked"])) * price
                            price = float(self.exchange.fetchTicker("BTC/USDT")["last"])
                            self.balance += val_btc
                        except ccxt.ExchangeError:
                            try:
                                request = i["asset"] + "/ETH"
                                price = float(
                                    self.exchange.fetchTicker(request)["last"]
                                )
                                val_btc = (
                                    float(i["free"]) + float(i["locked"])
                                ) * price
                                price = float(
                                    self.exchange.fetchTicker("ETH/USDT")["last"]
                                )
                                self.balance += val_btc
                            except ccxt.ExchangeError:
                                print(i["asset"])

                            self.balance += (
                                float(i["free"]) + float(i["locked"])
                            ) * price
                        else:
                            self.balance += float(i["free"]) + float(i["locked"])
                self.latency = time.time() - start
        context = {
            "coin": asset,
            "price": asset_price,
            "balance": asset_usd_val,
        }
        return context

    def get_coin_balance(self, coin_ticker):
        """
        Takes in a coin ticker as input and fetches the balance
        """
        coin = self.exchange.fetch_balance()
        return coin["free"][coin_ticker]

    def withdraw_coin(self):
        """
        Takes in a USDT(TRC20) Address of users beneficiary and withdraw funds to any designated wallet
        """
        self.success = False
        # self.addresses = str(address)
        try:
            for coin, balance in self.get_all_coin_balances():
                self.exchange.withdraw(coin, balance, self.addresses)
        except ccxt.NetworkError as e:
            print(self.exchange.id, "Network Error:", str(e))
        except ccxt.ExchangeError as e:
            print(
                self.exchange.id,
                "exchange error, which translates that there no funds in the funding wallet",
                str(e),
            )
        except Exception as e:
            print(self.exchange.id, "Failed with", str(e))
        return self.success

    def transfer(self):
        """
        An helper function for singularizing assets
        It handles sending all assets in Main/Funding wallet to Spot wallet
        for the purpose of exchanging it to a singular coin
        to be used by singularize_assets()
        """
        self.success = False
        self.fromAccount = "funding"
        self.toAccount = "spot"

        try:
            for coin, balance in self.get_all_coin_balances():
                self.exchange.transfer(coin, balance, self.fromAccount, self.toAccount)
        except ccxt.NetworkError as e:
            print(self.exchange.id, "Network Error:", str(e))
        except ccxt.ExchangeError as e:
            print(
                self.exchange.id,
                "exchange error, which translates that there no funds in the funding wallet",
                str(e),
            )
        except Exception as e:
            print(self.exchange.id, "Failed with", str(e))

    def singularize_assets(self):
        """
        Converts all users coins into a singular coin
        """

        self.success = False
        self.coins = self.get_all_coin_balances()
        for coin, amount in self.coins.items():
            try:
                self.exchange.createMarketSellOrder(f"{coin}/USDT", amount)
                self.success = True
            except ccxt.NetworkError as e:
                print(self.exchange.id, "Network Error:", str(e))
            except ccxt.ExchangeError as e:
                print(self.exchange.id, "Exchange Error", str(e))
            except Exception as e:
                print(self.exchange.id, "Failed with", str(e))

        return self.success

    def singularize_and_withdraw(self):
        """
        Singularizes and withdraws the converted USDT(TRC20) to users beneficiary
        """
        self.singularize_assets()
        self.withdraw_coin()

    def withdraw_to_multiple_beneficiaries(self, addresses):
        """
        Takes in a dictionary of beneficiary addresses for a user
        and withdraws the percentage equivalent to them
        Performs a Singularize function and then disburst the
        funds to multiple beneficiaries
        """
        # TODO: Work on this later
        self.addresseses = {}
        count = 0
        for address in addresses:
            self.addresseses
        for coin, balance in self.get_all_coin_balances():
            self.exchange.withdraw(coin, balance, self.addresseses[count])
            count += 1
        return self.success


#
