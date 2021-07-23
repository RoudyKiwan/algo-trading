import MetaTrader5 as mt5
from orders_management import open_order
import pandas as pd
from datetime import datetime, date, timedelta, time
import time as tm
import pytz


timezone = pytz.timezone("America/Montreal")
RISK = 0.02

class trade:
    def __init__(self, action = None, symbol = "", volume = None, type= None, entryPrice = None, stopLoss = None, takeProfit= None, type_time = None, type_filling = None, deviation = 100, magic = 1, comment = "python script"):
        self.action = action
        self.symbol = symbol
        self.volume = volume
        self.type = type 
        self.entryPrice = entryPrice
        self.deviation = deviation
        self.magic = magic
        self.comment = comment
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
        self.type_time = type_time
        self.type_filling = type_filling

    def set_deviation(self, spread):
        self.deviation += spread
        
    
#takes two dimensional array with symbol and second row to be filled with moving average 200 days
def get_moving_average(list_of_symbols, number_of_bars):
    """this function gets the number_of_bars ma for a list of symbols"""
    today = datetime.today()
    yesterday = date.today() - timedelta(days=1)
    date_from = datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo = timezone)

    symbol = 0
    counter = 0
    
    for symbol in range(len(list_of_symbols)):

        price_avg = 0
        rates = mt5.copy_rates_from(list_of_symbols[symbol][0], mt5.TIMEFRAME_D1, date_from, number_of_bars)
        counter = 0
        
        if rates != None:
            for counter in range(len(rates)):
                price_avg += rates[counter][4]

            list_of_symbols[symbol][1] = price_avg/number_of_bars
        else:
            list_of_symbols[symbol][1] = 0
        
       
            
       


def strategy(list_of_symbols, account_balance):

    symbol = 0
    todays_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, tzinfo = timezone)
    yesterday = todays_date - timedelta(days = 1)

    for symbol in range(len(list_of_symbols)):

        symbol_info = mt5.symbol_info(list_of_symbols[symbol][0])

        print(list_of_symbols[symbol][0])

        digits = symbol_info.digits


        if not symbol_info.visible:
            print(list_of_symbols[symbol][0], "is not visible, trying to switch on")
            if not mt5.symbol_select(list_of_symbols[symbol][0],True):
                print("symbol_select({}}) failed, exit",symbol)
                
        if datetime.now(timezone).time() < time(hour = 17):
        
            rates = mt5.copy_rates_from(list_of_symbols[symbol][0], mt5.TIMEFRAME_D1, yesterday, 2)
        else:
            rates = mt5.copy_rates_from(list_of_symbols[symbol][0], mt5.TIMEFRAME_D1, todays_date, 2)


        two_candles_ago_close = rates[0][4]
        last_close = rates[1][4]
        moving_average = list_of_symbols[symbol][1]


        print(moving_average, "moving average")
        print(two_candles_ago_close, "previous close")
        print(last_close, "today's close")
        
        #order buy
        
        if (two_candles_ago_close < moving_average):
            if (last_close > moving_average):
            
                risk_in_dollars = account_balance * RISK

                risk_in_pips = (rates[1][4] - rates[1][3]) * 10**(digits - 1)
            
                risk_d_per_pips = round(risk_in_dollars/risk_in_pips, 2)

                lots = max(round(risk_d_per_pips/10, 2), 0.01)

                position_to_open = trade()
                

                if lots >= 0.01 and lots < 100:

                    position_to_open.volume = lots

                    position_to_open.action = mt5.TRADE_ACTION_DEAL

                    position_to_open.symbol = list_of_symbols[symbol][0]

                    position_to_open.type = mt5.ORDER_TYPE_BUY

                    position_to_open.entryPrice = mt5.symbol_info_tick(list_of_symbols[symbol][0]).ask

                    position_to_open.takeProfit = round(rates[1][3] + (rates[1][4] - rates[1][1])*3, digits) 

                    position_to_open.stopLoss = round(rates[1][3], digits)

                    position_to_open.type_time = mt5.ORDER_TIME_GTC

                    position_to_open.type_filling = mt5.ORDER_FILLING_FOK

                    open_order(position_to_open)

                    tm.sleep(2)

        #order sell
        elif two_candles_ago_close > moving_average:
            
            if last_close < moving_average:

                risk_in_dollars = account_balance * 0.01

                risk_in_pips = (rates[1][2] - rates[1][4])* 10**(digits - 1)

                risk_d_per_pips = round(risk_in_dollars/risk_in_pips, 2)

                lots = max(round(risk_d_per_pips/10, 2), 0.01)

                position_to_open = trade()


                if lots >= 0.01 and lots < 100:
                    
                    position_to_open.volume = lots

                    position_to_open.action = mt5.TRADE_ACTION_DEAL

                    position_to_open.symbol = list_of_symbols[symbol][0]

                    position_to_open.type = mt5.ORDER_TYPE_SELL

                    position_to_open.entryPrice = mt5.symbol_info_tick(list_of_symbols[symbol][0]).bid

                    position_to_open.takeProfit = round(rates[1][3] - (rates[1][1] - rates[1][4])*3, digits)

                    position_to_open.stopLoss = round(rates[1][2], digits)

                    position_to_open.type_time = mt5.ORDER_TIME_GTC

                    position_to_open.type_filling = mt5.ORDER_FILLING_FOK

                    open_order(position_to_open)

                    tm.sleep(2)      

        else:
            print("No crosses found for {}".format(list_of_symbols[symbol][0]))

        

    
