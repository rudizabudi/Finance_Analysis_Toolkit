import Analysis.source_selector as ss

def select_analysis():
    trigger_one = ''
    print('--> 1 : Golden/Black Cross.')
    while trigger_one != 1:
        trigger_one = int(input('Select which analysis tool to run: '))

    if trigger_one == 1:
        analysis = 'GB_Cross'
        ss.select_data_type(analysis)
