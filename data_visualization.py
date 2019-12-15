import os
import pickle
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

def select_joined_data():

    trigger_one = ''
    print('--> 1 : Use intraday data.')
    print('--> 2 : Use historic data.')
    while trigger_one != 1 and trigger_one != 2 :
        trigger_one = int(input('Select which data type to use by index: '))

    if trigger_one == 1:
        path = 'intraday\\'
        contents = os.listdir(os.getcwd() + '\\Compiled_Data\\intraday')
        i = 0
        for file in contents:
            print('--> ' + str(i) + ' : ' + file)
            i += 1

        trigger_two = ''
        while trigger_two not in range(0,i):
            trigger_two = int(input('Select which interval to use by index: '))

        path = 'intraday\\' + contents[trigger_two] + '\\'

        contents = os.listdir(os.getcwd() + '\\Compiled_Data\\intraday\\' + contents[trigger_two])
        i = 0
        for file in contents:
            joined_files =  os.listdir(os.getcwd() + '\\Compiled_Data\\' + path )
            print('--> ' + str(i) + ' : ' + file)
            i += 1

        trigger_three = ''
        while trigger_three not in range(0, i):
            trigger_three = int(input('Select which base to use by index: '))
        base = contents[trigger_three]

        contents = os.listdir(os.getcwd() + '\\Compiled_Data\\' + path + contents[trigger_three])
        i = 0
        for file in contents:
            print('--> ' + str(i) + ' : ' + file)
            i += 1

        trigger_four = ''
        while trigger_four not in range(0, i):
            trigger_four = int(input('Select which dataset to use by index: '))

        selection = contents[trigger_four ]
        return base, selection, path

    if trigger_one == 2:
        path = 'historic\\'

        contents = os.listdir(os.getcwd() + '\\Compiled_Data\\\historic')
        i = 0
        for file in contents:
            print('--> ' + str(i) + ' : ' + file )
            i += 1

        trigger_two = ''
        while trigger_two not in range(0, i):
            trigger_two = int(input('Select which base to use by index: '))

        base = contents[trigger_two]

        contents = os.listdir(os.getcwd() + '\\Compiled_Data\\\historic\\' + base)
        i = 0
        for file in contents:
            print('--> ' + str(i) + ' : ' + file)
            i += 1

        trigger_three = ''
        while trigger_three not in range(0, i):
            trigger_three = int(input('Select which base to use by index: '))

        selection = contents[trigger_three]

    return base, selection, path


def visualize_data(base, selection, path):
    df = pd.read_csv(os.getcwd() + '\\Compiled_Data\\' + path + base + '\\' + selection)
    df['ALV.DE'].plot()

    df_corr = df.corr()
    print(df_corr.head())
