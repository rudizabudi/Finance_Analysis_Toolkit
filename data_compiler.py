import os
import pickle
import pandas as pd
import sys
from datetime import datetime

def select_data():

    trigger_one = ''
    print('--> 1 : Use intraday data.')
    print('--> 2 : Use historic data.')
    while trigger_one != 1 and trigger_one != 2 :
        trigger_one = int(input('Select which data type to use by index: '))

    if trigger_one == 1:
        path = 'intraday\\'
        contents = os.listdir(os.getcwd() + '\\Price_Data\\intraday')
        i = 0
        for file in contents:
                print('--> ' + str(i) + ' : ' + file)
                i += 1

        trigger_two = ''
        while trigger_two not in range(0,i):
            trigger_two = int(input('Select which interval to use by index: '))

        path = 'intraday\\' + contents[trigger_two] + '\\'

        contents = os.listdir(os.getcwd() + '\\Price_Data\\intraday\\' + contents[trigger_two])
        i = 0
        for file in contents:
            print('--> ' + str(i) + ' : ' + file)
            i += 1

        trigger_three = ''
        while trigger_three not in range(0, i):
            trigger_three = int(input('Select which data to use by index: '))

        selection = contents[trigger_three]
        return selection, path


    if trigger_one == 2:
        path = 'historic\\'

        contents = os.listdir(os.getcwd() + '\\Price_Data\\historic')
        i = 0
        for file in contents:
                print('--> ' + str(i) + ' : ' + file)
                i += 1

        trigger_two = ''
        while trigger_two not in range(0, i):
            trigger_two = int(input('Select which data to use by index: '))

        selection = contents[trigger_two]

    return selection, path

def compile_data(selection, path):

    trigger_one = -1
    datasets = ['Open', 'Close', 'High', 'Low', 'Volume']
    for i, set in enumerate(datasets):
        print('--> ' + str(i) + ' : ' + str(set) + '.')

    while trigger_one not in range(1,5):
        trigger_one = int(input('Select dataset for dataframe: '))

    selected_set = datasets[trigger_one]
    datasets.remove(selected_set)

    with open(os.getcwd() + '\\Stock_Symbol_List\\' + selection +'.pickle',"rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame

    i = 0
    for count, ticker in enumerate(tickers):
        if ticker.count('.') == 2:
            ticker = ticker.replace('.', '-', 1)
            print(ticker)

        if os.path.isfile(os.getcwd() + '\\Price_Data\\' + path + selection + '\\' + ticker + '.csv'):
            df = pd.read_csv(os.getcwd() + '\\Price_Data\\' + path + selection + '\\' + ticker + '.csv')
            if 'date' in df:
                df.rename(columns={'date': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'}, inplace=True)
            elif 'Date' in df:
                df.drop('Close', 1, inplace=True)
                df.rename(columns= {'Adj Close': 'Close'}, inplace = True)

            df.set_index('Date', inplace=True)

            for set in datasets:
                df.drop(set, 1, inplace = True)
            df.rename(columns={selected_set: ticker}, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')
        else:
            print('Error: ' + ticker + ' not found')

        sys.stdout.write('\r')
        ticks = int(round(count / (int(len(tickers)) / 20), 0))
        sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, (count + 1) * (100 / (int(len(tickers))))))
        sys.stdout.flush()

    entries = count - i + 1
    print('\n--> ' + str(entries) +' / ' + str(len(tickers)) + ' entries loaded.')


    if not os.path.exists(os.getcwd() + '\\Compiled_Data\\' + path + '\\' + selection):
        os.makedirs(os.getcwd() + '\\Compiled_Data\\' + path + '\\' + selection)


    main_df.to_csv(os.getcwd() + '\\Compiled_Data\\' + path + '\\' + selection + '\\' + 'Dataset_Joined' + selected_set + '_' + datetime.now().strftime("%d.%m.%Y") + '.csv')
    print('--> Compiled dataframe created!')
    print('--> Path: '+ os.getcwd() + '\\Compiled_Data\\' + path + '\\' + selection + '\\' + 'Dataset_Joined' + selected_set + datetime.now().strftime("%d.%m.%Y") + '.csv')