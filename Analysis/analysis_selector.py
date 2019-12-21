import Analysis.source_selector as ss

def select_analysis():
    trigger_one = ''
    print('--> 1 : Golden/Black Cross.')
    print('--> 2 : Relative Strength Index.')

    while trigger_one != 1 and trigger_one != 2:
        trigger_one = int(input('Select which analysis tool to run: '))

    if trigger_one == 1:
        analysis = 'GB_Cross'
        ss.select_data_type(analysis)

    if trigger_one == 2:
        print('--> 1 : Create Relative Strength Index.')
        print('--> 2 : Analyse Relative Strength Index.')
        trigger_two = ''
        while trigger_two != 1 and trigger_two != 2:
            trigger_two = int(input('Select which analysis tool to run: '))

        if trigger_two == 1:
            analysis = 'RSI_Create'
            type = '\\Compiled_Data'
            ss.select_data(type, analysis)
        elif trigger_two == 2:
            analysis = 'RSI_Analyse'
            type = '\\Compiled_Data'
            ss.select_data(type, analysis)
