import os
import Indicators.moving_average as ima


def select_data(indicator_name, argument_list):
# takes indicator name as string and argument list (ma: periods)
    # Just single .csv possible
    trigger_one = ''
    print('--> 1 : Use intraday data.')
    print('--> 2 : Use historic data.')

    while trigger_one not in [1, 2, 3]:
        trigger_one = int(input('Select which data type to use by index: '))

    type = '\\Compiled_Data'
    if trigger_one == 1:
        path = type + '\\intraday\\'

    if trigger_one == 2:
        path = type + '\\historic\\'

    selection_finished = False
    while not selection_finished:
        contents = os.listdir(os.getcwd() + path)
        for i, file in enumerate(contents):
            print('--> ' + str(i) + ' : ' + file)
            if i == len(contents)-1:
                trigger_loop = ''
                while trigger_loop not in range(0, i + 1):
                    trigger_loop = int(input('Select which data to use by index: '))
                if '.csv' in contents[trigger_loop]:
                    selection = contents[trigger_loop]
                    selection_finished = True
                else:
                    path = path + contents[trigger_loop] + '\\'

    # next function needs to check if single .csv or compiled .csv

    if indicator_name == 'Simple Moving Average':
        ima.simple_moving_average(indicator_name, argument_list, selection)
    elif indicator_name == 'Exponential Moving Average':
        ima.exponential_moving_average(indicator_name, argument_list, selection)





