import MetaTrader5 as mt5
import broker
import strategy
import orders_management
from datetime import datetime, time
import time as tm
import pytz

connected = True


def main():
    
    broker.open_metatrader(connected)
    if connected == False:
        #First we check the connection to the terminal
        print("we couldn't connect to the terminal.")
        exit()
    else:
        my_account = broker.get_account_info()
       
        symbols_traded = broker.forex_symbols()

        #setting variables before intering infinite loop
        new_trading_day = True
        start = 0
        market_opened = True
        orders_to_send = list()
        trading_day = orders_management.TradingDay()
        trading_day.get_trading_day()
        

         
        while connected:

            todays_date = datetime.now(pytz.timezone("America/Montreal"))

            if todays_date.time() > time(hour = 17) and todays_date.time() < time(hour = 19):
                #do not trade because spread is too high
                pass
            else:
                #etant donne que le programme roule pour la premiere fois c'est sur c'est un new trading day
                if start != 0:
                    new_trading_day = orders_management.is_new_trading_day(trading_day)
            
                if new_trading_day == True:
                    message = False
            
                    market_opened = orders_management.is_market_open()

                    start = 1

                    if market_opened == True:
                
                        message = False

                        strategy.get_moving_average(symbols_traded, 200)
                
                        if mt5.positions_total() >= 100:
                            pass

                        elif mt5.positions_total() < 100:
                        
                            strategy.strategy(symbols_traded, my_account.balance)

                            
                    else:
                
                        if message == False:
                            print("market is currently closed")
                            message == True
                else:
                    tm.sleep(1)



           
main()


