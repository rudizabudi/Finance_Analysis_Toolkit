import pandas as pd
import numpy as np


df = pd.read_csv('C:\\Users\\fruhd\\Desktop\\Python\\Finance_Analysis_Toolkit\\Price_Data\\historic\\DAX\\LHA.DE.csv')

df = pd.DataFrame(df)
df.set_index('Date', inplace=True)
df.drop(['High', 'Low', 'Open', 'Volume', 'Adj Close'], 1, inplace=True)
print(df)

df['ema_fast'] = df['Close'].ewm(span=50, adjust=False).mean()
df['ema_slow'] = df['Close'].ewm(span=200, adjust=False).mean()
print(df)






















ma_types = ['Simple Moving Average', 'Exponential Moving Average']
for i, ma_type in enumerate(ma_types):
    print('--> ' + str(i) + ' : ' + ma_type)

trigger_two = ''
while trigger_two not in range(0, len(ma_types) - 1):
    trigger_two = int(input('Select which Moving Average type to use for faster MA: '))

faster_ma_type = ma_types[trigger_two]
faster_ma = int(input('Choose periods for faster Moving Average: '))

for i, ma_type in enumerate(ma_types):
    print('--> ' + str(i) + ' : ' + ma_type)

trigger_three = ''
while trigger_three not in range(0, len(ma_types) - 1):
    trigger_three = int(input('Select which Moving Average type to use for faster MA: '))

slower_ma_type = ma_types[trigger_three]
slower_ma = int(input('Choose periods for slower Moving Average: '))

if faster_ma_type == 'Simple Moving Average':
    df['MA_' + str(faster_ma)] = df['Close'].rolling(faster_ma).mean()
elif faster_ma_type == 'Exponential Moving Average':
    df['MA_' + str(faster_ma)] = df['Close'].ewm(span=faster_ma, adjust=False).mean()

if slower_ma == 'Simple Moving Average':
    df['MA_' + str(slower_ma)] = df['Close'].rolling(slower_ma).mean()
elif slower_ma_type == 'Exponential Moving Average':
    print(slower_ma_type)
    df['MA_' + str(slower_ma)] = df['Close'].ewm(span=slower_ma).mean()















