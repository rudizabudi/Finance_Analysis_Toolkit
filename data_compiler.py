import os
import pickle
import pandas as pd
import sys
from datetime import datetime

def select_data():

    trigger_one = ''
    print('--> 1 : Compile single dataset.')
    print('--> 2 : Compile list of datasets jointly.')
    print('--> 3 : Compile list of datasets individually.')
    while trigger_one not in range(1,3+1):
        trigger_one = int(input('Select how to compile by index: '))

    if trigger_one == 1:
        compile_type = 'Single'
    elif trigger_one == 2:
        compile_type = 'Joined'
    elif trigger_one == 3:
        compile_type = 'Individual'

    trigger_two = ''
    print('--> 1 : Use intraday data.')
    print('--> 2 : Use historic data.')
    print('--> 3 : Use custom path to data.')
    while trigger_two not in range(1,3+1):
        trigger_two = int(input('Select which data to use by index: '))

    path_found = False
    selection = ''

    if trigger_two == 1:
        path = '\\Price_Data\\intraday\\'
    elif trigger_two == 2:
        path = '\\Price_Data\\historic\\'
    elif trigger_two == 3:
        while path_found == False:
            path = input('Enter full path to folder or single .csv: ')
            if os.path.exists(path):
                path_found = True

    if trigger_two == 1 or trigger_two == 2:
        while not path_found:
            contents = os.listdir(os.getcwd() + '\\' + path)
            j = 0
            for file in contents:
                if '.csv' in file:
                    j += 1
            if j > 0.8 * len(contents):
                if trigger_one > 1:
                    path_found = True
                elif trigger_one == 1:
                    for i, file in enumerate(contents, start=1):
                        print('--> ' + str(i) + ' : ' + file)
                    trigger_three = 0
                    while trigger_three not in range(1, len(contents)+1):
                        trigger_three = int(input('Select path by index: '))
                    selection = contents[trigger_three-1]
                    path_found = True
            else:
                trigger_three = 0
                for i, file in enumerate(contents, start=1):
                    print('--> ' + str(i) + ' : ' + file)
                while trigger_three not in range(1, len(contents) +1 ):
                    trigger_three = int(input('Select path by index: '))
                path = path + contents[trigger_three-1] + '\\'

        path = os.getcwd() + path

    return compile_type, path, selection

def compile_data(compile_type, path, selection):
    # Standard Format: Alpha Vantage
    drop_columns = True

    if compile_type == 'Single':
        decision = ''
        while decision != 'n' and decision != 'y':
            decision = input('Do you want to drop columns? (y/n) ')
        if decision == 'n':
            drop_columns = False

    if drop_columns:
        datasets = ['Open', 'Close', 'High', 'Low', 'Volume']
        for i, set in enumerate(datasets):
            print('--> ' + str(i) + ' : ' + str(set) + '.')

        trigger_one = -1
        while trigger_one not in range(1,5):
            trigger_one = int(input('Select dataset for dataframe to keep: '))

        selected_set = datasets[trigger_one]
        datasets.remove(selected_set)

    if compile_type == 'Single':
        import_df = pd.read_csv(path + selection)
        import_df = pd.DataFrame(import_df)
        for column in import_df.columns.values:
            # alpha vantage
            if column == 'date':
                import_df.rename(columns={'date': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'}, inplace=True)
            # yahoo fianance
            elif column == 'Date':
                import_df.drop('Close', 1, inplace=True)
                import_df.rename(columns={'Adj Close': 'Close'}, inplace=True)

        import_df.set_index('Date', inplace=True)

        if drop_columns == True:
            for set in datasets:
                import_df.drop(set, 1, inplace=True)

        save_path = path.replace('Price_Data', 'Compiled_Data') + compile_type + '\\'
        # if selection == '':
        #     save_path = os.getcwd() + '\\Compiled_Data\\individual\\'
        #     selection = path[path.rindex('\\')+1:]
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        print(save_path + selection)
        import_df.to_csv(save_path + selection)


    elif compile_type == 'Joined' or compile_type == 'Individual':
        contents = os.listdir(path)
        df = []
        df = pd.DataFrame(df)

        save_path = path.replace('Price_Data', 'Compiled_Data')
        if compile_type == 'Joined':
            save_path = save_path + 'Joined' + '\\'
        elif compile_type == 'Individual':
            save_path = save_path + 'Individual' + '\\'
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for i, file in enumerate(contents):
            import_df = pd.read_csv(path + file)

            for column in import_df.columns.values:

                # alpha vantage
                if column == 'date':
                    import_df.rename(columns={'date': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'}, inplace=True)
                #yahoo fianance
                elif column == 'Date':
                    import_df.drop('Close', 1, inplace=True)
                    import_df.rename(columns={'Adj Close': 'Close'}, inplace=True)

            import_df.set_index('Date', inplace=True)

            for set in datasets:
                import_df.drop(set, 1, inplace = True)

            import_df.rename(columns={selected_set: file[:file.index('.csv')]}, inplace=True)

            if compile_type == 'Individual':
                import_df.to_csv(save_path + 'Individual\\' + file + '.csv')
            if compile_type == 'Joined':
                if df.empty:
                    df = import_df
                else:
                    df = df.join(import_df, how='outer')

            sys.stdout.write('\r')
            ticks = int(round(i / (int(len(contents)) / 20), 0))
            sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, (i + 1) * (100 / (int(len(contents))))))
            sys.stdout.flush()

        if compile_type == 'Joined':
            df.fillna(0, inplace=True)
            df.to_csv(save_path + 'Joined_' + datetime.now().strftime("%d.%m.%Y") + '.csv')

    print('--> Compiled dataframe created!')
    print('--> Path: '+ str(save_path))
