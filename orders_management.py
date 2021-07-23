import MetaTrader5 as mt5
from datetime import datetime, time
import pytz

timezone = pytz.timezone("America/Montreal")


todays_date = datetime.now(timezone)
market_close = time(hour = 17)

class TradingDay:
    """UTC-5 trading days are between 17h00 first day to next day from sunday to friday. This class changes the days of the week considering the market opening and closing time"""
    def __init__(self, market_day = None):
      self.market_day = market_day

    def get_trading_day(self):
       
        if (todays_date.isoweekday() == 7 and todays_date.time() >= market_close  or (todays_date.isoweekday() == 1 and todays_date.time() < market_close)):
             self.market_day = 1
        elif (todays_date.isoweekday() == 1 and todays_date.time() >= market_close  or (todays_date.isoweekday() == 2 and todays_date.time() < market_close)):
            self.market_day = 2
        elif (todays_date.isoweekday() == 2 and todays_date.time() >= market_close  or (todays_date.isoweekday() == 3 and todays_date.time() < market_close)):
            self.market_day = 3
        elif (todays_date.isoweekday() == 3 and todays_date.time() >= market_close  or (todays_date.isoweekday() == 4 and todays_date.time() < market_close)):
            self.market_day = 4
        elif (todays_date.isoweekday() == 4 and todays_date.time() >= market_close  or (todays_date.isoweekday() == 5 and todays_date.time() < market_close)):
            self.market_day = 5

    def change_trading_day(self, new_num):
        self.market_day = new_num

def is_market_open():
    """This function will check if the market is opened. It returns a boolean"""
    
    market_open_closing_hour = time(hour = 17)

    #if it's friday after 17:00 then the market is close
    if todays_date.isoweekday() == 5 and todays_date.time() > market_open_closing_hour:
        return False
    #if it's saturday, then the market is closed
    elif (todays_date.isoweekday() == 6):
        return False
    #if it's sunday before 17:00, then the market is closed
    elif (todays_date.isoweekday() == 7 and todays_date.time() < market_open_closing_hour):
         return False
    else:
        return True

def open_order(trading_position):
    
    request = {
        "action": trading_position.action,
        "symbol": trading_position.symbol,
        "volume": trading_position.volume,
        "type": trading_position.type,
        "price": trading_position.entryPrice,
        "sl" : trading_position.stopLoss,
        "tp" : trading_position.takeProfit,
        "deviation": trading_position.deviation,
        "magic" : trading_position.magic,
        "comment" : trading_position.comment,
        "type_time" : trading_position.type_time,
        "type_filling" : trading_position.type_filling,

        }
    
    print(request)

    result = mt5.order_send(request)

    print("1. {} :  sending order at {} lot".format(trading_position.symbol, trading_position.volume))

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. Order failed to send, retcode = {}".format(result.retcode))


def is_new_trading_day(x):

    temp_day = TradingDay()
    temp_day.get_trading_day()

    if temp_day.market_day == x.market_day:
        return False

    elif temp_day.market_day != x.market_day:
        day.change_trading_day(temp_day)
        return True

