import MetaTrader5 as mt5
import pandas as pd


#PATH = "C:\Program Files\MetaTrader 5"
LOGIN = "38970565"
PASSWORD = "rokm6xks"

print("coucou")

class account_info:

    def client_info(self, data):
      self.login = data.iloc[0]['value']
      self.trade_mode = data.iloc[1]['value']
      self.leverage = data.iloc[2]['value']
      self.limit_orders = data.iloc[3]['value']
      self.margin_so_mode = data.iloc[4]['value']
      self.trade_allowed = data.iloc[5]['value']
      self.trade_expert = data.iloc[6]['value']
      self.margin_mode = data.iloc[7]['value']
      self.currency_digits =  data.iloc[8]['value']
      self.fifo_close = data.iloc[9]['value']
      self.balance = data.iloc[10]['value']
      self.credit = data.iloc[11]['value']
      self.profit = data.iloc[12]['value']
      self.equity = data.iloc[13]['value']
      self.margin = data.iloc[14]['value']
      self.margin_free = data.iloc[15]['value']
      self.margin_level = data.iloc[16]['value']
      self.margin_so_call = data.iloc[17]['value']
      self.margin_so_so = data.iloc[18]['value']
      self.margin_initial = data.iloc[19]['value']
      self.margin_maintenance = data.iloc[20]['value']
      self.assets = data.iloc[21]['value']
      self.liabilities = data.iloc[22]['value']
      self.commission_blocked = data.iloc[23]['value']
      self.name = data.iloc[24]['value']
      self.server = data.iloc[25]['value']
      self.currency = data.iloc[26]['value']
      self.company = data.iloc[27]['value']



def get_account_info():

    if mt5.account_info() == None:
        print("we cannot get the account information.")
    else:
        
        df = pd.DataFrame(list(mt5.account_info()._asdict().items()), columns = ['property', 'value'])

        client_account = account_info()
        client_account.client_info(df)
        return client_account
 

def forex_symbols():

    a_list = list()

    filtered_GROUP = "*AUD*, *NZD*, *EUR*, *USD*, *CHF*, *CAD*, *JPY*, *GBP*"
    all_symbols = mt5.symbols_get(group = filtered_GROUP)

    all_symbols_list = [s.name for s in all_symbols]

    removed_group = ["BTC", "DSH", "ETC", "EMC", "XMR", "ZEC" ,"ETH", "LTC", "EOS", "XRP", "XAG", "XPT", "XPD", "MBT", "XTI", "XNG", "XBR", "MXN", "SGD"]

    custom_remove = ["XAUUSD","XAUEUR", "XAUAUD"]

    custom_remove_2 = ["CZK", "DKK", "MXN", "PLN", "ARS", "COP", "GEL", "CLP", "NOK", "RUB", "SEK", "SGD", "NOK", "TRY", "ZAR", "HUF", "RUR", "HUF", "NOK"]

    first_symbols_list = list(filter(lambda x : x[:3] not in removed_group, all_symbols_list))
    
    filtered_symbols_list = list(filter(lambda x : x not in custom_remove, first_symbols_list))

    filtered_symbols_list_1 = list(filter(lambda x : x[-3:] not in custom_remove_2, filtered_symbols_list))

    print(filtered_symbols_list_1)

    for s in filtered_symbols_list_1:
        a_list.append([s, 0])

    return a_list
    

def open_metatrader(connection):
    if not mt5.initialize():
        #we will send an email later on the say that we have a connection problem
        print("error connecting, the error code is ", mt5.last_error())
        connection = False

    else:
        
        mt5.login(login = LOGIN, password= PASSWORD)
        connection = True
