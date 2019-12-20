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
        #here choice create rsi table or brute rsi treshold strategy
        analysis = 'RSI'
        type = '\\Compiled_Data'
        ss.select_data(type, analysis)
