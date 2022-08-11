
from pathlib import Path
import environ
import os
import ccxt


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

env = environ.Env()


env.read_env(str(ROOT_DIR / ".envs/.local/.django"))
API_KEY = env('API_KEY')
SEC_KEY = env('SEC_KEY')


class Exchange():
    '''
    Instantiates any exchange
    '''
    # pylint: disable=too-many-instance-attributes
    # Eleven is reasonable in this case.

    def __init__(self, exchange_name, api_Key, secret, identifier=None):
        self.identifier = identifier
        self.exchange_name = exchange_name
        self.api_Key = api_Key
        self.secret = secret

        exchange = getattr(ccxt, self.exchange_name)

        self.exchange = exchange({
            'api_key': self.api_Key,
            'secret': self.secret
        })

    def __repr__(self):
        return self.exchange_name

    def get_all_coins(self):
        '''
        Fetches all coins owned by the user
        '''
        coin = []
        all_coins = self.exchange.fetch_balance()

        for key, value in all_coins['free'].items():
            if value > 0:
                coin.append(key)
        return coin

    def get_all_coin_balances(self):
        '''
        Fetches all coins with their amount owned by the user
        '''
        all_balance = self.exchange.fetch_balance()
        balance = {}
        for key, value in all_balance['free'].items():
            if value > 0:
                balance[key] = value
        return balance

    def get_coin_balance(self, coin_ticker):
        '''
        Takes in a coin ticker as input and fetches the balance
        '''
        coin = self.exchange.fetch_balance()
        return coin['free'][coin_ticker]

    def withdraw_to_multiple_beneficiaries(self, addresses):
        '''
        Takes in a dictionary of beneficiary addresses for a user
        and withdraws the percentage equivalent to them
        '''
        # TODO: Work on this later
        self.addresses = {}
        count = 0
        for address in addresses:
            self.addresses
        for coin, balance in self.get_all_coin_balances():
            self.exchange.withdraw( coin, balance, self.addresses[count])
            count += 1
        return self.success

    def withdraw_coin(self, address):
        '''
        Takes in a USDT(TRC20) Address of users beneficiary and withdraw funds to any designated wallet
        '''
        self.success = False
        self.address = str(address)
        for coin, balance in self.get_all_coin_balances():
            self.exchange.withdraw( coin, balance, self.address)
        return self.success

    def transfer(self):
        '''
        An helper function for singularizing assets
        It handles sending all assets in Main/Funding wallet to Spot wallet
        for the purpose of exchanging it to a singular coin
        to be used by singularize_assets()
        '''
        self.success = False
        self.fromAccount = 'funding'
        self.toAccount = 'spot'

        try:
            for coin, balance in self.get_all_coin_balances():
                self.exchange.transfer(coin,  balance, self.fromAccount, self.toAccount)
        except ccxt.NetworkError as e:
                print(self.exchange.id, 'Network Error:', str(e))
        except ccxt.ExchangeError as e:
                print(self.exchange.id,'exchange error, which translates that there no funds in the funding wallet', str(e))
        except Exception as e:
                print(self.exchange.id, 'Failed with', str(e))



    def singularize_assets(self):
        '''
        Converts all users coins into a singular coin
        '''

        self.success = False
        self.coins = self.get_all_coin_balances()
        for coin, amount in self.coins.items():
            try:
                self.exchange.createMarketSellOrder(f'{coin}/USDT', amount)
                self.success = True
            except ccxt.NetworkError as e:
                print(self.exchange.id, 'Network Error:', str(e))
            except ccxt.ExchangeError as e:
                print(self.exchange.id,'Exchange Error', str(e))
            except Exception as e:
                print(self.exchange.id, 'Failed with', str(e))
        
        return self.success

    def singularize_and_withdraw(self):
        self.singularize_assets()
        self.withdraw_coin()
