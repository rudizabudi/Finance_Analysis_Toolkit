import time
#custom
import handle_tickers as ht
import get_data as gd
import data_compiler as dc
import Analysis.analysis_selector as ans

while True:
    trigger_one = ''
    print('--> 1 : Create/update ticker list.')
    print('--> 2 : Create/update stock prices.')
    print('--> 3 : Create/update compiled dataset.')
    print('--> 4 : Analyse data.')

    while trigger_one != 1 and trigger_one != 2 and trigger_one != 3 and trigger_one != 4:
        trigger_one = int(input('Select action by index: '))

    if trigger_one == 1:
        ht.save_tickers()

    if trigger_one == 2:
        symbols = ht.select_tickers()
        gd.get_data(symbols)

    if trigger_one == 3:
        compile_type, path, selection = dc.select_data()
        dc.compile_data(compile_type, path, selection)

    if trigger_one == 4:
        ans.select_analysis()
    print('- - - - - - - - - - - - - - - - - - \n')


