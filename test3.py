import sys
import pandas as pd
from datetime import datetime

df = pd.read_csv('C:\\Users\\fruhd\\Desktop\\Python\\Finance_Analysis_Toolkit\\schaumamoi1.csv')


# for i, column in enumerate(df.columns[1:], start = 1):
#     if df[column].iloc[0] != 'close' and df[column].iloc[2] != '':
#         df.drop(column, 1, inplace=True)
#
# for i, column in enumerate(df.columns, start=0):
#     if '.' in column:
#         df.columns.values[i] =  column[:column.rindex('.')]
#
# df.drop('Unnamed: 0', 1, inplace = True)
# df.drop('Unnamed: 0.1', 1, inplace = True)
# df = pd.DataFrame(df)

df.rename(columns= {'Unnamed: 0.1': 'Date'}, inplace = True)
# for i, row in enumerate(df['Date'], start = 2):
#     if ' ' in df['Date'].iloc[i]:
#         df['Date'].iloc[i] = df['Date'].iloc[i][:df['Date'].iloc[i].index(' ')]

datesplit = df['Date'].str.split(' ', n = 1, expand = True)
df['Date'] = datesplit[0]

df.rename(columns= {'Unnamed: 0.1': 'Date'}, inplace = True)
df.drop([0, 1 ], 0, inplace = True)
df.set_index('Date', inplace = True)
df.drop('Unnamed: 0', 1, inplace = True)
df.fillna(0, inplace = True)
print(df[0:5])



df.to_csv('schaumamoi2.csv')

