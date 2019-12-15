import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import nan
import datetime as dt
import os
import operator
from datetime import datetime
import sys

def GB_Cross(path, selection):
    df = pd.read_csv(os.getcwd() + path + selection)

    #single stock
    if 'Price_Data' in path:
        if 'date' in df:
            df.rename(
                columns={'date': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close',
                         '5. volume': 'Volume'}, inplace = True)
        elif 'Date' in df:
            df.drop('Close', 1, inplace = True)
            df.rename(columns={'Adj Close': 'Close'}, inplace = True)

        df.set_index('Date', inplace=True)

        dropcolumns = ['High', 'Low', 'Open', 'Volume']
        for column in dropcolumns:
            df.drop(column, 1, inplace = True)

        df = pd.DataFrame(df)

        analyses = ['Golden Cross', 'Black Cross']
        for i, analysis in enumerate(analyses):
            print('--> ' + str(i) + ' : ' + analysis)

        trigger_one = ''
        while trigger_one != 0 and trigger_one != 1:
            trigger_one = int(input('Select which analysis type to use: '))

        analysis = analyses[trigger_one]

        faster_ma = int(input('Choose periods for faster Moving Average: '))
        slower_ma = int(input('Choose periods for slower Moving Average: '))

        df['MA_' +str(faster_ma)] = df['Close'].rolling(faster_ma).mean()
        df['MA_' + str(slower_ma)] = df['Close'].rolling(slower_ma).mean()

        percentage_list = []
        absolute_list = []
        duration_list = []
        index_old = 0

        ops = {
            "==": operator.eq,
            "!=": operator.ne,
            "<>": operator.ne,
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">": operator.ge
        }

        if analysis == 'Golden Cross':
            oplt = '<'
            opgt = '>'

        if analysis == 'Black Cross':
            oplt = '>'
            opgt = '<'

        filename = selection + '_' + analysis + '_' + str(slower_ma) +'-' + str(faster_ma) + '_' + datetime.now().strftime("%d.%m.%Y")
        results = open(os.getcwd() + '\\Analysis_Results\\' + filename + '.txt', 'a')

        print('- - - - - - - - - - - - - - - - - - ')
        for i, (index, row) in enumerate(df[slower_ma:].iterrows(), start=slower_ma):
            if i != slower_ma:
                #golden Crossing
                if ops[oplt](old_ma_1, old_ma_2) and ops[opgt](row['MA_' + str(faster_ma)], row['MA_' + str(slower_ma)]):
                    index_old = index
                    start_price = row['Close']
                #black Crossing
                if ops[opgt](old_ma_1, old_ma_2) and ops[oplt](row['MA_' +str(faster_ma)], row['MA_' + str(slower_ma)]) and index_old != 0:
                    time = dt.datetime.strptime(index, '%Y-%m-%d') - dt.datetime.strptime(index_old, '%Y-%m-%d')
                    duration_list.append(int(time.days))
                    end_price = row['Close']
                    percentage_gain = round(((end_price - start_price) / start_price) * 100, 2)
                    absolute_gain = round(end_price - start_price, 2)
                    if analysis == 'Black Cross':
                        percentage_gain = -1 * percentage_gain
                        absolute_gain = -1 * absolute_gain
                    percentage_list.append(percentage_gain)
                    absolute_list.append(absolute_gain)
                    message = '-->' + analysis + ' on ' + str(index_old) + '. It lasted for ' + str(time.days) + ' days. It gained ' + str(absolute_gain) + ' or ' + str(percentage_gain) + ' %.'
                    results.write(message + '\n')
                    print(message)

            old_ma_1 = row['MA_' + str(faster_ma)]
            old_ma_2 = row['MA_' + str(slower_ma)]


        print('- - - - - - - - - - - - - - - - - - ')
        results.write('- - - - - - - - - - - - - - - - - - ' + '\n')
        print('--> ' + analysis + ' Occurrences: ' + str(len(absolute_list)))
        results.write('--> ' + analysis + ' Occurrences: ' + str(len(absolute_list)) + '\n')
        print('--> Total gains: ' + str(round(np.sum(absolute_list),0)) + ' MU ')
        results.write('--> Total gains: ' + str(round(np.sum(absolute_list),0)) + ' MU ' + '\n')
        print('--> Average gain: ' + str(round(np.average(absolute_list),2)) + ' MU | StdDev: ' + str(round(np.std(absolute_list),2)))
        results.write('--> Average gain: ' + str(round(np.average(absolute_list),2)) + ' MU | StdDev: ' + str(round(np.std(absolute_list),2)) + '\n')
        print('--> Average gain in percent: ' + str(round(np.average(percentage_list),2)) + ' % | StdDev: ' + str(round(np.std(percentage_list),2)))
        results.write('--> Average gain in percent: ' + str(round(np.average(percentage_list),2)) + ' % | StdDev: ' + str(round(np.std(percentage_list),2)) + '\n')
        print('--> Average duration: ' + str(round(np.average(duration_list))) + ' days | StdDev: ' + str(round(np.std(duration_list),0)))
        results.write('--> Average duration: ' + str(round(np.average(duration_list))) + ' days | StdDev: ' + str(round(np.std(duration_list))) + '\n')

        results.close()
        print('-->  Results saved as ' + os.getcwd() + '\\Analysis_Results\\' + filename + '.txt')

        choice = input('Show graph? (y/n) ')
        if choice == 'y':
            df.plot()
            plt.show()

    elif 'Compiled_Data' in path:
        df.set_index('Date', inplace=True)

        df = pd.DataFrame(df)

        analyses = ['Golden Cross', 'Black Cross']
        for i, analysis in enumerate(analyses):
            print('--> ' + str(i) + ' : ' + analysis)

        trigger_one = ''
        while trigger_one != 0 and trigger_one != 1:
            trigger_one = int(input('Select which analysis type to use: '))

        analysis = analyses[trigger_one]

        faster_ma = int(input('Choose periods for faster Moving Average: '))
        slower_ma = int(input('Choose periods for slower Moving Average: '))

        name1 = '_MA_' + str(faster_ma)
        name2 = '_MA_' + str(slower_ma)

        for i in range(0, 3 * len(df.columns.values)):
            if name1 not in df.columns[i] and name2 not in df.columns[i]:
                df.insert(i + 1, df.columns[i] + name1, '')
                df[str(df.columns[i]) + name1] = df[str(df.columns[i])].rolling(faster_ma).mean()
                df.insert(i + 2, df.columns[i] + name2, '')
                df[str(df.columns[i]) + name2] = df[str(df.columns[i])].rolling(slower_ma).mean()

        df.fillna(0, inplace=True)

        percentage_list = []
        total_percentage_list = []
        absolute_list = []
        total_absolute_list = []
        duration_list = []
        total_duration_list =[]
        index_old = 0

        ops = {
            "==": operator.eq,
            "!=": operator.ne,
            "<>": operator.ne,
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">": operator.ge
        }

        if analysis == 'Golden Cross':
            oplt = '<'
            opgt = '>'

        if analysis == 'Black Cross':
            oplt = '>'
            opgt = '<'

        absolute_path = os.getcwd() + path + selection
        index = absolute_path[:absolute_path.rindex('\\')][absolute_path[:absolute_path.rindex('\\')].rindex('\\') + 1:]
        filename = index + '_Joined' + '_' + analysis + '_' + str(slower_ma) +'-' + str(faster_ma) + '_' + datetime.now().strftime("%d.%m.%Y")
        results = open(os.getcwd() + '\\Analysis_Results\\' + filename + '.txt', 'w')

        for j, column in enumerate(df.columns):
            if name2 in column:
                for i, row in enumerate(df[column].values):
                    print(column)
                    if df[column][i] != 0:
                        if ops[oplt](df[old_column][i - 1], df[column][i - 1]) and ops[opgt](df[old_column][i], df[column][i]):
                            index_old = df.index[i]
                            basename = column[:column.index('_')]
                            start_price = df[basename][i]
                        if ops[opgt](df[old_column][i - 1], df[column][i - 1]) and ops[oplt](df[old_column][i], df[column][i]) and index_old != 0:
                            time = dt.datetime.strptime(df.index[i], '%Y-%m-%d') - dt.datetime.strptime(index_old, '%Y-%m-%d')
                            duration_list.append(int(time.days))
                            end_price = df[basename][i]
                            percentage_gain = ((end_price - start_price) / start_price) * 100
                            absolute_gain = end_price - start_price
                            if analysis == 'Black Cross':
                                percentage_gain = -1 * percentage_gain
                                absolute_gain = -1 * absolute_gain
                            percentage_list.append(percentage_gain)
                            absolute_list.append(absolute_gain)
                            message = '--> ' + column[:column.index('_')] + ' did a ' + analysis + ' on ' + str(index_old) + '. It lasted for ' + str(time.days) + ' days. It gained ' + str(round(
                                absolute_gain,2)) + ' or ' + str(round(percentage_gain,2)) + ' %.'
                            results.write(message + '\n')
                            #print(message)

                if absolute_list != []:

                    total_absolute_list.append(absolute_list)
                    total_duration_list.append(duration_list)
                    total_percentage_list.append(percentage_list)

                    results.write('- - - - - - - - - - - - - - - - - - ' + '\n')
                    results.write('--> ' + column[:column.index('_')] + analysis + ' Occurrences: ' + str(len(absolute_list)) + '\n')
                    results.write('--> ' + column[:column.index('_')] + ' Total gains: ' + str(round(np.sum(absolute_list),2)) + ' MU ' + '\n')
                    results.write('--> ' + column[:column.index('_')] + ' Average gain: ' + str(round(np.average(absolute_list),2)) + ' MU | StdDev: ' + str(round(np.std(absolute_list), 2)) + '\n')
                    results.write('--> ' + column[:column.index('_')] + ' Average gain in percent: ' + str(round(np.average(percentage_list),2)) + ' % | StdDev: ' + str(round(np.std(percentage_list), 2)) + '\n')
                    results.write('--> ' + column[:column.index('_')] + ' Average duration: ' + str(round(np.average(duration_list),2)) + ' days | StdDev: ' + str(round(np.std(duration_list),2)) + '\n')
                    results.write('- - - - - - - - - - - - - - - - - - ' + '\n')
                    results.write('- - - - - - - - - - - - - - - - - - ' + '\n')
                    results.write('- - - - - - - - - - - - - - - - - - ' + '\n')

                    absolute_list = []
                    duration_list = []
                    percentage_list = []

            sys.stdout.write('\r')
            ticks = int(round(j / (int(len(df.columns)) / 20), 0))
            # print('ticks: ' + str(ticks) + "; i: " + str(i))
            sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, (j+1) * (100 / (int(len(df.columns))))))
            sys.stdout.flush()

            old_column = column

        results.close()
        results = open(os.getcwd() + '\\Analysis_Results\\' + filename + '.txt', 'r')
        single_results = results.read()
        results.close()

        total_absolute_list = [val for sublist in total_absolute_list for val in sublist]
        total_percentage_list = [val for sublist in total_percentage_list for val in sublist]
        total_duration_list = [val for sublist in total_duration_list for val in sublist]

        results = open(os.getcwd() + '\\Analysis_Results\\' + filename + '.txt', 'w')
        results.write('--> Total' + analysis + ' Occurrences: ' + str(np.sum(total_absolute_list)) + '\n')
        results.write('--> Total gains: ' + str(round(np.sum(total_absolute_list),2)) + ' MU ' + '\n')
        results.write('--> Average gain: ' + str(round(np.average(total_absolute_list),2)) + ' MU | StdDev: ' + str(round(np.std(total_absolute_list),2)) + '\n')
        results.write('--> Average gain in percent: ' + str(round(np.average(total_percentage_list),2)) + ' % | StdDev: ' + str(round(np.std(total_percentage_list),2)) + '\n')
        results.write('--> Average duration: ' + str(round(np.average(total_duration_list),2)) + ' days | StdDev: ' + str(round(np.std(total_duration_list),2)) + '\n')
        results.write('\n')
        results.write('* * * * * * * * * * * * * * * * * * ' + '\n')
        results.write('- - - - - - - - - - - - - - - - - - ' + '\n')
        results.write('* * * * * * * * * * * * * * * * * * ' + '\n')
        results.write(single_results)
        results.close()

        print('\n--> Analysis successfully finished!')
        print('--> Results saved in ' + os.getcwd() + '\\Analysis_Results\\' + filename + '.txt')

