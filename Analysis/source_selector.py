import os
import Analysis.golden_black_cross as gbc
import Analysis.relative_strength_index as rsi

def select_data_type(analysis):
    trigger_one = ''
    print('--> 1 : Use single data.')
    print('--> 2 : Use joined data.')
    while trigger_one != 1 and trigger_one != 2 :
        trigger_one = int(input('Select which data type to use by index: '))

    if trigger_one == 1:
        type = '\\Price_Data'
    elif trigger_one == 2:
        type = '\\Compiled_Data'

    select_data(type, analysis)

def select_data(type, analysis):

    trigger_one = ''
    print('--> 1 : Use intraday data.')
    print('--> 2 : Use historic data.')
    while trigger_one != 1 and trigger_one != 2:
        trigger_one = int(input('Select which data type to use by index: '))

    if trigger_one == 1:
        path = type + '\\intraday\\'

    if trigger_one == 2:
        path = type + '\\historic\\'

    selection_finished = False
    while selection_finished == False:
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

    if analysis == 'GB_Cross':
        gbc.GB_Cross(path, selection)
    elif analysis == 'RSI_Create':
        rsi.create_RSI(path, selection)
    elif analysis == 'RSI_Analyse':
        if '_RSI' in selection:
            rsi.analyse_RSI(path, selection)
        else:
            print('--> ERROR: No RSI Table selected!')
            select_data(type, analysis)




