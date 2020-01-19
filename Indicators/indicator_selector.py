import Indicators.source_selector as ss

def select_indicator():
    trigger_one = ''
    print('--> 1 : Moving Average.')
    # print('--> 2 : Relative Strength Index.')
    # TODO move RSI creation out of analysis script and test it

    while trigger_one not in [1]:
        trigger_one = int(input('Select which indicator to create: '))

    if trigger_one == 1:

        ma_indicators = ['Simple Moving Average', 'Exponential Moving Average']

        for i, ma_indicator in enumerate(ma_indicators):
            print('--> ' + str(i + 1) + ' : ' + str(ma_indicators[i]))

        trigger_two = ''
        while trigger_two not in [1]:
            trigger_two = int(input('Select which Moving Average type to use by index: '))

        indicator_name = ma_indicators[trigger_two]

        correct_input = False

        input_periods = input('Enter periods for ' + str(indicator_name) + ' (eg. 1,2,3 or 2-6): ')

        input_periods.replace(' ', '')

        argument_list = []
        if ',' in input_periods:
            argument_list = input_periods.split(',')
        elif '-' in input_periods:
            input_periods = input_periods.split('-')
            for input_period in range(int(input_periods[0]), int(input_periods[1]) + 1):
                argument_list.append(input_period)
        else:
            argument_list.append(input_periods)

        ss.select_data_type(indicator_name, argument_list)






























    #
    # if trigger_one == 2:
    #     print('--> 1 : Create Relative Strength Index.')
    #     print('--> 2 : Analyse Relative Strength Index.')
    #     trigger_two = ''
    #     while trigger_two != 1 and trigger_two != 2:
    #         trigger_two = int(input('Select which analysis tool to run: '))
    #
    #     if trigger_two == 1:
    #         analysis = 'RSI_Create'
    #         type = '\\Compiled_Data'
    #         ss.select_data(type, analysis)
    #     elif trigger_two == 2:
    #         analysis = 'RSI_Analyse'
    #         type = '\\Compiled_Data'
    #         ss.select_data(type, analysis)