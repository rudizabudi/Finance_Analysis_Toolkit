import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

df = pd.read_csv('C:\\Users\\fruhd\\Desktop\\Python\\DAX-Stocks\\New Code\\Compiled_Data\\historic\\DAX\\Dataset_JoinedClose_09.12.2019.csv')
ticker = input('Choose ticker: ')

df.set_index('Date', inplace = True)

calc_df = pd.DataFrame(df[ticker])

###### GOLDEN CROSS
calc_df['MA_50'] = calc_df[ticker].rolling(50).mean()
calc_df['MA_200'] = calc_df[ticker].rolling(200).mean()

percentage_list = []
absolute_list = []
duration_list = []
index_old = 0
for i, (index, row) in enumerate(calc_df[200:].iterrows(), start=200):
    if i != 200:
        if old_ma_50 < old_ma_200 and row['MA_200'] < row['MA_50']:
            index_old = index
            start_price = row[ticker]
        if old_ma_50 > old_ma_200 and row['MA_200'] > row['MA_50'] and index_old != 0:
            time = dt.datetime.strptime(index, '%Y-%m-%d') - dt.datetime.strptime(index_old, '%Y-%m-%d')
            duration_list.append(int(time.days))
            end_price = row[ticker]
            percentage_gain = round(((end_price - start_price) / start_price) * 100)
            percentage_list.append(percentage_gain)
            absolute_gain = round(end_price - start_price, 2)
            absolute_list.append(absolute_gain)
            print('--> Golden cross on ' + str(index_old) + ' and it lasted for ' + str(time.days) + ' days. It gained ' + str(absolute_gain) + ' or ' + str(percentage_gain) + ' %.')

    old_ma_50 = row['MA_50']
    old_ma_200 = row['MA_200']
print('- - - - - - - - - - - - - - - - - - ')

print('--> Occurences: ' + str(len(absolute_list)))
print('--> Average total gain: ' + str(round(np.average(absolute_list),0)) + ' MU | σ: ' + str(round(np.std(absolute_list),2)))
print('--> Average gain in percent ' + str(round(np.average(percentage_list),2)) + ' % | σ: ' + str(round(np.std(percentage_list),2)))
print('--> Average duration: ' + str(round(np.average(duration_list))) + ' days | σ: ' + str(round(np.std(duration_list),0)))


calc_df.plot()
plt.show()














import sys
import pandas as pd

df = pd.read_csv('C:\\Users\\fruhd\\Desktop\\Python\\DAX-Stocks\\New Code\\Price_Data\\intraday\\1min\\S&P500\\dataset.csv')

for i, column in enumerate(df.columns[1:], start = 1)
     if df[column].iloc[0] != 'close' and df[column].iloc[0] != '':
         df.drop(column, 1, inplace=True)

    sys.stdout.write('\r')
    ticks = int(round(i / (int(df.columns[1:]) / 20), 0))
    sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, i * (100 / (int(len(df.columns[1:]))))))
    sys.stdout.flush()

for i, column in enumerate(df.columns, start=0):
    if '.' in column:
        df.columns.values[i] =  column[:column.rindex('.')]

    sys.stdout.write('\r')
    ticks = int(round(i / (int(df.columns) / 20), 0))
    sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, i * (100 / (int(len(df.columns))))))
    sys.stdout.flush()




df.to_csv('schaumamoi1.csv')







