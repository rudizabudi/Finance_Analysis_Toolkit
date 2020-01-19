#custom
import handle_tickers as ht
import get_data as gd
import data_compiler as dc
import Analysis.analysis_selector as ans
import Indicators.indicator_selector as ins

while True:
    trigger_one = ''
    print('--> 1 : Create/update ticker list.')
    print('--> 2 : Create/update stock prices.')
    print('--> 3 : Create/update compiled dataset.')
    print('--> 4 : Create Indicators.')
    print('--> 5 : Analyse data.')
    while trigger_one not in [1, 2, 3, 4, 5]:
        trigger_one = int(input('Select action by index: '))

    if trigger_one == 1:
        ht.save_tickers()
    elif trigger_one == 2:
        symbols = ht.select_tickers()
        gd.get_data(symbols)
    elif trigger_one == 3:
        compile_type, path, selection = dc.select_data()
        if compile_type and path and selection:
            dc.compile_data(compile_type, path, selection)
    elif trigger_one == 4:
        ins.select_indicator()
    elif trigger_one == 5:
        ans.select_analysis()

    print('- - - - - - - - - - - - - - - - - - \n')


