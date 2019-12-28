import datetime as dt
import os
import pandas_datareader.data as web
from alpha_vantage.timeseries import TimeSeries
import sys
import time

def get_data(symbols):

    txt = open(os.getcwd() + '\\Stock_Symbol_List\\' + symbols, "r")
    tickers = txt.readlines()

    for i, ticker in enumerate(tickers, start = 0):
        if '\n' in ticker:
            tickers[i] = ticker.strip('\n')

    print('--> 1 : Get intraday data.')
    print('--> 2 : Get historic data.')

    trigger_one = ''
    while trigger_one != 1 and trigger_one != 2:
        trigger_one = int(input('Select action by index: '))

    if trigger_one == 1:
        intraday = ('1min', '5min', '30min', '60min')
        i = 0

        for interval in intraday:
            print('--> ' + str(i) + ' : ' + interval)
            i += 1

        interval_choice = -1
        while interval_choice not in range(0, len(intraday)):
            interval_choice = int(input('Select interval by index: '))

    if trigger_one == 1:
        path = '\\intraday\\' + str(intraday[interval_choice]) + '\\'
    if trigger_one == 2:
        path = '\\historic\\'

        print('--> 1 : Alpha Vantage.')
        print('--> 2 : Yahoo Finance.')
        trigger_two = ''
        while trigger_two != 1 and trigger_two != 2:
            trigger_two = int(input('Select source by index: '))

        if trigger_two == 2:
            today = dt.date.today()
            start = dt.datetime(2000, 1, 1)
            end = dt.datetime(int(today.strftime('%Y')), int(today.strftime('%m')), int(today.strftime('%d')))


    #av_keys = ('LK0LEI22RYDLKS3S', 'HQL2R9KNYW99K4BT', 'FJ485A1KCAZCODB', 'PZ2ISG9CYY379KLI', 'MCAF9B429I44328U', 'AOIAMG3WFZ8LS58W', '06VFCKNZ709V6XFG', '06VFCKNZ709V6XFG', '4BTFICZGTPWZRRQS')

    i = 1
    j = 1
    print('--> Downloading data')
    for ticker in tickers:
        if trigger_one == 1 or (trigger_one == 2 and trigger_two == 1):
            while True:
                try:
                    ts = TimeSeries(key='AOIAMG3WFZ8LS58W', output_format='pandas')
                    if trigger_one == 1:
                        data, meta = ts.get_intraday(symbol = ticker, interval= str(intraday[interval_choice]), outputsize='full')
                    elif trigger_one == 2:
                        data, meta  = ts.get_daily(symbol = ticker, outputsize='full')
                except ValueError:
                    time.sleep(5)
                    continue
                break
        elif trigger_one == 2 and trigger_two == 2:
            try:
                if j != len(tickers) and '.' in ticker:
                    for ticker_two in tickers:
                        if ticker_two.count('.') >= 1:
                            j +=1

                if j != len(tickers) and ticker.count('.') == 1:
                    ticker = ticker.replace('.','-')
                if j == len(tickers) and ticker.count('.') == 2:
                     ticker = ticker.replace('.','-', 1)

                if ticker.count('.') == 2:
                    ticker = ticker.replace('.','-', 1)
                #if ticker[:-2] == '.':
                 #   ticker = ticker.replace('.' , '-')
                data = web.DataReader(ticker, 'yahoo', start, end)
            except KeyError or pandas_datareader._utils.RemoteDataError:
                print('\nQuery broke on ' + ticker)
                print('Start time ' + str(start))
                print('End time ' + str(end))
        else:
            print('Source selection error!')

        if not os.path.exists(os.getcwd() + '\\Price_Data' + path + symbols[:-7] + '\\'):
            os.makedirs(os.getcwd() + '\\Price_Data' + path + symbols[:-7] + '\\')

        data.to_csv(os.getcwd() + '\\Price_Data' + path + symbols[:-7] + '\\' + ticker + '.csv', ',')

        sys.stdout.write('\r')
        ticks = int(round(i / (int(len(tickers))/ 20), 0))
        sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, i * (100 / (int(len(tickers))))))
        sys.stdout.flush()
        i += 1

    print('\n--> Data download successful!')






