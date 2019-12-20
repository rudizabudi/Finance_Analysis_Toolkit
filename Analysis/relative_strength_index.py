import numpy as np
import pandas as pd
import os
from pandas.core.common import SettingWithCopyWarning
import warnings
import sys


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

    for column in df.columns.values:
        if column not in skip_columns and 'RSI-' not in column:
            for period in periods:
                if column == 'Close':
                    name = ''
                else:
                    name = column + '_'

                df[name + 'RSI-' + str(period)] = ''

                for i, row in enumerate(df.iterrows(), start=0):
                    if i >= period:
                        relative_strength = 0
                        if i == period:
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
                            relative_strength = avg_gain / avg_loss
                            gains.clear()
                            losses.clear()

                        elif i > period:
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
    df.to_csv(os.getcwd() + save_path + selection[:-4] + '_RSI' + '.csv')

    print('\n--> Table successfully created!')
    print('--> Path: ' + str(os.getcwd() + save_path + selection[:-4] + '_RSI' + '.csv'))
