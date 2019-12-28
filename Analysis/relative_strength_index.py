import numpy as np
import pandas as pd
import os
from pandas.core.common import SettingWithCopyWarning
import warnings
import sys
from datetime import datetime
import datetime as dt


def create_RSI(path, selection):

    warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

    df = pd.read_csv(os.getcwd() + path + selection)

    save_path = path.replace('Price_Data', 'Compiled_Data')

    df.sort_values(by='Date', inplace=True)
    df.set_index('Date', inplace=True)

    input_periods = input('Enter periods for Relative Strength Index (eg. 1,2,3 or 2-6): ')

    if ' ' in input_periods:
        input_periods.replace(' ', '')
    input_periods = input_periods.split(',')

    periods = []
    addlist = []
    for i, period in enumerate(input_periods):
        if '-' in period:
            for_range = period.split('-')
            start = int(for_range[0])
            end = int(for_range[1])
            for j in range(start, end + 1):
                addlist.append(j)
        else:
            try:
                periods.append(int(period))
            except:
                continue

    for item in addlist:
        periods.append(item)

    periods.sort()

    df = pd.DataFrame(df)
    gains = []
    losses = []

    skip_columns = ['Open', 'High', 'Low', 'Volume', 'Date', 'Adj Close']
    count = 0
    for column in df.columns.values:
        if column not in skip_columns and 'RSI-' not in column:
            count +=1

    tick = count * len(periods)
    count = 0

    for k, column in enumerate(df.columns.values, start=1):
        if column not in skip_columns and 'RSI-' not in column:
            column_index = df.columns.values.tolist().index(column) + 1

            add_index = 0
            for period in periods:
                if column == 'Close':
                    name = ''
                else:
                    name = column + '_'

                df.insert(column_index + add_index, name + 'RSI-' + str(period), '')
                add_index += 1

                for i, row in enumerate(df.iterrows(), start=0):
                    if i >= period:
                        relative_strength = 0
                        if i >= period and 0 not in df[column].iloc[i-period:i].tolist():
                            for j in range(i - period + 1, i + 1):
                                dif = df[column].iloc[j] - df[column].iloc[j-1]
                                if dif > 0:
                                    gains.append(dif)
                                elif dif < 0:
                                    losses.append(dif)

                            avg_gain = np.sum(gains) / period
                            avg_gain_old = avg_gain
                            avg_loss = -1 * (np.sum(losses) / period)
                            avg_loss_old = avg_loss
                            if avg_loss != 0:
                                relative_strength = avg_gain / avg_loss
                            gains.clear()
                            losses.clear()

                        elif i > period and 0 not in df[column].iloc[i-period:i].tolist():
                            dif = df[column].iloc[i] - df[column].iloc[i - 1]
                            if dif > 0:
                                gain = dif
                                loss = 0
                            elif dif < 0:
                                gain = 0
                                loss = -1 * dif
                            else:
                                gain = 0
                                loss = 0

                            avg_gain = (avg_gain_old * (period - 1) + gain) / period
                            avg_loss = (avg_loss_old * (period - 1) + loss) / period
                            if avg_loss != 0:
                                relative_strength = avg_gain / avg_loss
                            avg_gain_old = avg_gain
                            avg_loss_old = avg_loss


                        if avg_loss == 0:
                            relative_strength_index = 100
                        else:
                            relative_strength_index = 100 - (100 / (1 + relative_strength))

                    if i < period:
                        df[name + 'RSI-' + str(period)].iloc[i] = 0
                    else:
                        df[name + 'RSI-' + str(period)].iloc[i] = round(relative_strength_index,2)

                sys.stdout.write('\r')
                count += 1
                ticks = int(round(count / (int(tick) / 20), 0))
                sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, count * (100 / (int(tick)))))
                sys.stdout.flush()

    if not os.path.exists(os.getcwd() + save_path):
        os.mkdir(os.getcwd())
    df.to_csv(os.getcwd() + save_path + selection[:-4] + '_RSI' + '_' + datetime.now().strftime("%d.%m.%Y") + '.csv')

    print('\n--> Table successfully created!')
    print('--> Path: ' + str(os.getcwd() + save_path + selection[:-4] + '_RSI' + '_' + datetime.now().strftime("%d.%m.%Y") + '.csv'))


def analyse_RSI(path, selection):
    np.seterr(all='ignore')
    df = pd.read_csv(os.getcwd() + path + selection)

    df = pd.DataFrame(df)

    lower_tresholds = []
    input_lower = input('Enter Lower Treshold to brute: (eg. 8-35): ')
    #backtest single input with timeframes
    if '-' in input_lower:
        lower_range = input_lower.split('-')
        for i in range(int(lower_range[0]), int(lower_range[1]) + 1):
            lower_tresholds.append(i)
    else:
        lower_tresholds.append(int(input_lower))

    upper_tresholds = []
    input_upper = input('Enter Upper Treshold to brute: (eg. 14 or 8-35): ')
    if '-' in input_upper:
        upper_range = input_upper.split('-')
        for i in range(int(upper_range[0]), int(upper_range[1]) + 1):
            upper_tresholds.append(i)
    else:
        upper_tresholds.append(int(input_upper))

    single_tresholds = False
    if len(upper_tresholds) == 1 and len(lower_tresholds) == 1:
        single_tresholds = True

    count = 0
    single_stock = False
    for column in df.columns.values:
        if column == 'Close':
            single_stock = True
        if 'RSI-' in column:
            count += 1

    if single_stock and count > 1:
        all_rsi = []
        for column in df.columns.values:
            if 'RSI-' in column:
                all_rsi.append(column)
        print('--> 0 : Analyse all')
        for i, rsi in enumerate(all_rsi, start=1):
            print('--> ' + str(i) + ' : ' + rsi)
        choices = input('Select which RSI to use by index (eg. 1,3,5): ')
        choices = choices.split(',')
        selected_columns = []
        for choice in choices:
            selected_columns.append(all_rsi[(int(choice) - 1)])
        count = len(selected_columns)

    name = selection[:selection.index('_RSI')]

    if not single_tresholds:
        tick = count * (int(lower_range[1]) - int(lower_range[0]) + 1) * (int(upper_range[1]) - int(upper_range[0]) + 1)
    count = 0

    results = []
    trade_done = False
    msg_list = []
    best_performance = 0

    df.set_index('Date', inplace=True)
    for column in df.columns.values:
        single_multi_checker = True
        if not single_stock and column != 'Date' and 'RSI-' not in column:
            name = column
        if single_stock and column not in selected_columns:
            single_multi_checker = False

        if not single_tresholds:
            filename = name + '_RSI-Analysis_' + str(lower_tresholds[0]) + str(lower_tresholds[len(lower_tresholds) - 1]) + '-' + str(upper_tresholds[0]) + str(upper_tresholds[len(upper_tresholds) - 1]) + '_' + datetime.now().strftime("%d.%m.%Y")

        if 'RSI-' in column and single_multi_checker:
            for lower_treshold in lower_tresholds:
                for upper_treshold in upper_tresholds:
                    results.clear()
                    in_trade = False
                    for i, row in enumerate(df.iterrows()):
                        if i > int(column[column.rindex('-')+1:]):
                            old_rsi = df[column].iloc[i - 1]
                            new_rsi = df[column].iloc[i]
                            if old_rsi < lower_treshold < new_rsi and not in_trade:
                                in_trade = True
                                if single_stock:
                                    in_price = df['Close'].iloc[i]
                                elif not single_stock:
                                    reference_name = str(column[:column.index('_')])
                                    in_price = df[reference_name].iloc[i]
                                if single_tresholds:
                                    in_time = df.index[i]
                            if old_rsi < upper_treshold < new_rsi and in_trade:
                                in_trade = False
                                trade_done = True
                                if single_stock:
                                    out_price = df['Close'].iloc[i]
                                elif not single_stock:
                                    reference_name = str(column[:column.index('_')])
                                    out_price = df[reference_name].iloc[i]
                                if single_tresholds:
                                    out_time = df.index[i]
                            if old_rsi > lower_treshold > new_rsi and in_trade:
                                in_trade = False
                                trade_done = True
                                if single_stock:
                                    out_price = df['Close'].iloc[i]
                                elif not single_stock:
                                    reference_name = str(column[:column.index('_')])
                                    out_price = df[reference_name].iloc[i]
                                if single_tresholds:
                                    out_time = df.index[i]

                            if not in_trade and trade_done:
                                result = out_price - in_price
                                results.append(result)
                                trade_done = False
                                if single_tresholds:
                                    delta_time = dt.datetime.strptime(str(out_time), '%Y-%m-%d') - dt.datetime.strptime(str(in_time), '%Y-%m-%d')
                                    message = '--> ' + str(name) + ' entered the trade on ' + str(in_time) + ' and left it on ' + str(out_time) + '. Duration: ' + str(delta_time.days) + '; It gained ' + str(round(result, 2)) + '.'
                                    msg_list.append(message + '\n')

                    if len(results) != 0:
                        total_performance = np.sum(results)
                        avg_performance = np.sum(results) / len(results)
                        std_dev = np.std(results)
                    else:
                        total_performance = 0
                        avg_performance = 0
                        std_dev = 0

                    if not single_tresholds:
                        message = '--> ' + str(name) + ' did ' + str(round(len(results), 2)) + ' trades with ' + str(round(lower_treshold, 2)) + ' / ' + str(round(upper_treshold, 2)) + '. Total performance: ' + str(round(total_performance, 2)) + '; Avg. performance: ' + str(round(avg_performance, 2)) + '; StdDev: ' + str(round(std_dev , 2)) + '.'
                        msg_list.append(message + '\n')

                        if total_performance > best_performance:
                            best_performance = total_performance
                            best_avg_performance = avg_performance
                            best_std_dev = std_dev
                            best_lower = lower_treshold
                            best_upper = upper_treshold
                            best_number = len(results)

                        sys.stdout.write('\r')
                        count += 1
                        ticks = int(round(count / (int(tick) / 20), 0))
                        sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, count * (100 / (int(tick)))))
                        sys.stdout.flush()

            if single_stock:
                if len(selected_columns) == 1:
                    if single_tresholds:
                        path = os.getcwd() + '\\Analysis_Results\\'
                        filename = name + '_RSI-Analysis_' + str(lower_tresholds[0]) + '-' + str(upper_tresholds[0]) + '_' + datetime.now().strftime("%d.%m.%Y")
                        results_file = open(path + '\\' + filename + '.txt', 'a')
                    elif not single_tresholds:
                        path = os.getcwd() + '\\Analysis_Results\\' + selection[:selection.index('_RSI')]
                        if not os.path.exists(path):
                            os.makedirs(path)
                        filename = name + '_RSI-Analysis_' + str(lower_treshold) + '-' + str(upper_treshold) + '_' + datetime.now().strftime("%d.%m.%Y")
                        results_file = open(path + '\\' + filename + '.txt', 'a')
                elif len(selected_columns) > 1:
                    path = os.getcwd() + '\\Analysis_Results\\' + selection[:selection.index('_RSI')]
                    if not os.path.exists(path):
                        os.makedirs(path)
                    filename = column + '_RSI-Analysis_' + str(lower_treshold) + '-' + str(upper_treshold) + '_' + datetime.now().strftime("%d.%m.%Y")
                    results_file = open(path + '\\' + filename + '.txt', 'a')

            elif not single_stock:
                #todo choose single stock from not single_stock file
                path = os.getcwd() + '\\Analysis_Results\\' + selection
                if not os.path.exists(path):
                    os.makedirs(path)
                filename = name + '_RSI-Analysis_' + str(lower_treshold) + '-' + str(upper_treshold) + '_' + datetime.now().strftime("%d.%m.%Y")
                results_file = open(path + '\\' + filename + '.txt', 'a')

            header = []
            if not single_tresholds:
                header.append('--> BEST LOWER AND UPPER TRESHOLD: ' + str(best_lower) + ' / ' + str(best_upper) + '\n')
                header.append('--> Total Performance: ' + str(round(best_performance, 2)) + '\n')
                header.append('--> Average Performance: ' + str(round(best_avg_performance, 2)) + '\n')
                header.append('--> Standard Deviation: ' + str(round(best_std_dev, 2)) + '\n')
                header.append('--> Number of Occurences: ' + str(round(best_number, 2)) + '\n')
                header.append('- # - # - # - # - # - # - # - # - # ' + '\n')
            else:
                header.append('--> Total Performance: ' + str(round(total_performance, 2)) + '\n')
                header.append('--> Average Performance: ' + str(round(avg_performance, 2)) + '\n')
                header.append('--> Standard Deviation: ' + str(round(std_dev, 2)) + '\n')
                header.append('--> Number of Occurences: ' + str(round(len(results), 2)) + '\n')
                header.append('- # - # - # - # - # - # - # - # - # ' + '\n')

            for line in header:
                results_file.write(line)
            for line in msg_list:
                results_file.write(line)

            results_file.close()
            msg_list = []

    print('\n--> Analysis successfully finished!')
    if (single_stock and len(selected_columns) > 1) or not single_stock:
        print('--> Results saved in ' + path + '\n')
    elif single_stock and len(selected_columns) == 1:
        print('--> Result saved as ' + path + '\\' + filename + '.txt' + '\n')