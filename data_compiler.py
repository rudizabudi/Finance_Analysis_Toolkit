import os
import pandas as pd
import sys
from datetime import datetime as dt
import numpy as np

def merge_data():

    master_found = False
    while not master_found:
        master = str(input('Enter path to Master Dataset: '))
        if os.path.exists(master):
            master_found = True
        else:
            print('--> ERROR Master Dataset not found!')

    master_df = pd.read_csv(master)
    master_df.set_index('Date', inplace=True)
    print('-->  Master Dataset loaded!')

    slave_number = 0
    while slave_number not in range(1, 100):
        slave_number = int(input('Enter number of Slave Datasets: '))

    for i in range(slave_number):
        slave_found = False
        while not slave_found:
            slave = str(input('Enter path to Slave Dataset #' + str(i + 1) + ': '))
            if os.path.exists(slave):
                slave_found = True
            else:
                print('--> ERROR Slave Dataset No. ' + str(i) + ' not found!')

        slave_df = pd.read_csv(slave)
        slave_df.set_index('Date', inplace=True)

        double_column_names = []
        for j, slave_column in enumerate(slave_df.columns):
            print('--> ' + str(j) + ' : ' + slave_column)
            if slave_column in master_df.columns:
                double_column_names.append(slave_column)

        column_choice = input('Enter index for columns to use (eg. 1,2,3 or 2-6): ')

        column_choice.replace(' ', '')

        column_choice_list = []
        if ',' in column_choice:
            column_choice = column_choice.split(',')
        elif '-' in column_choice:
            column_choice = column_choice.split('-')

        try:
            for column in range(int(column_choice[0]), int(column_choice[1]) + 1):
                column_choice_list.append(slave_df.columns[column])
        except IndexError:

            column_choice_list.append(slave_df.columns[int(column_choice)])

        for slave_add_column in column_choice_list:

            if slave_add_column in double_column_names:
                print('--> WARNING Column name ' + str(slave_add_column) + ' in both datasets.')
                new_column_name = str(input('Enter new name for slave column: '))
                master_df[new_column_name] = slave_df[slave_add_column]
            else:
                master_df[slave_add_column] = slave_df[slave_add_column]

    master = master.replace('.csv', '_merged.csv')
    master_df.to_csv(master)
    print(' --> New merged master .csv created.')
    print('--> Path: ' + str(master))


def select_data():

    trigger_one = ''
    print('--> 1 : Compile single dataset.')
    print('--> 2 : Compile list of datasets jointly.')
    print('--> 3 : Compile list of datasets individually.')
    print('--> 4 : Merge datasets.')

    while trigger_one not in [1, 2, 3, 4]:
        trigger_one = int(input('Select how to compile by index: '))

    if trigger_one in [1, 2, 3]:
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
        while trigger_two not in range(1, 4):
            trigger_two = int(input('Select which data to use by index: '))

        path_found = False
        selection = ''

        if trigger_two == 1:
            path = '\\Price_Data\\intraday\\'
        elif trigger_two == 2:
            path = '\\Price_Data\\historic\\'
        elif trigger_two == 3:
            while path_found == False:
                path = input('Enter full path to folder or single .csv file: ')
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
                    if trigger_two == 2:
                        selection = contents[trigger_three-1]
                    path = path + contents[trigger_three-1] + '\\'

            path = os.getcwd() + path

        return compile_type, path, selection

    elif trigger_one == 4:
        merge_data()

    return '', '', ''

def adjust_time(target, df, selected_set, selected_type):
    if selected_set == '':
        selected = False
        readjust_high, readjust_low, readjust_open, readjust_close, readjust_volume, new_date, new_high, new_low, new_open, new_close, new_volume = ([] for i in range(11))
    elif selected_set != '':
        selected = True
        readjust, new_date, new = ([] for i in range(3))

    df.reset_index(inplace=True)

    min_target = False
    if 'min' in target:
        target = int(target[:target.index('min')])
        min_target = True
    try:
        date_format = dt.strptime(df['Date'].iloc[0], '%Y-%m-%d')
        origin_time_format = '%Y-%m-%d'
    except ValueError:
        origin_time_format = '%Y-%m-%d %H:%M:%S'

    for i, row in enumerate(df.iterrows()):
        if i < df.shape[0] - 1:
            if min_target:
                target_time_format = '%Y-%m-%d %H:%M:%S'
                date_row = dt.strptime(df['Date'].iloc[i], origin_time_format).minute
                if date_row % target != 0:
                    end = False
                else:
                    end = True
            elif target == 'daily':
                target_time_format = '%Y-%m-%d'
                day_row = dt.strptime(df['Date'].iloc[i], origin_time_format).day
                day_next = dt.strptime(df['Date'].iloc[i + 1], origin_time_format).day
                if day_row == day_next:
                    end = False
                else:
                    end = True
            elif target == 'weekly':
                target_time_format = '%Y-%m-%d'
                weekday_row = dt.strptime(df['Date'].iloc[i], origin_time_format).weekday()
                weekday_next = dt.strptime(df['Date'].iloc[i + 1], origin_time_format).weekday()
                if weekday_row < weekday_next:
                    end = False
                else:
                    end = True
            elif target == 'monthly':
                target_time_format = '%Y-%m'
                month_row = dt.strptime(df['Date'].iloc[i], origin_time_format).month
                month_next = dt.strptime(df['Date'].iloc[i + 1], origin_time_format).month
                if month_row == month_next:
                    end = False
                else:
                    end = True
            elif target == 'yearly':
                target_time_format = '%Y'
                year_row = dt.strptime(df['Date'].iloc[i], origin_time_format).year
                year_next = dt.strptime(df['Date'].iloc[i + 1], origin_time_format).year
                if year_row == year_next:
                    end = False
                else:
                    end = True

            if not end:
                if not selected:
                    readjust_high.append(df['High'].iloc[i])
                    readjust_low.append(df['Low'].iloc[i])
                    readjust_open.append(df['Open'].iloc[i])
                    readjust_close.append(df['Close'].iloc[i])
                    readjust_volume.append(df['Volume'].iloc[i])
                elif selected:
                    readjust.append(df[selected_set].iloc[i])

            elif end:
                if not selected:
                    new_date.append(dt.strftime(dt.strptime(df['Date'].iloc[i], origin_time_format), target_time_format))
                    new_high.append(np.max(readjust_high))
                    new_low.append(np.min(readjust_low))
                    new_open.append(readjust_open[0])
                    new_close.append(readjust_close[-1])
                    new_volume.append(np.sum(readjust_volume))

                    readjust_high, readjust_low, readjust_open, readjust_close, readjust_volume = ([] for i in range(5))

                elif selected:
                    new_date.append(dt.strftime(dt.strptime(df['Date'].iloc[i], origin_time_format), target_time_format))
                    if selected_type == 'High':
                        new.append(np.max(readjust))
                    elif selected_type == 'Low':
                        new.append(np.min(readjust))
                    elif selected_type == 'Open':
                        new.append(readjust[0])
                    elif selected_type == 'Close':
                        new.append(readjust[-1])
                    elif selected_type == 'Volume':
                        new.append(np.sum(readjust))
                    readjust = []

    if not selected:
        new_df = pd.DataFrame()
        new_df['Date'] = new_date
        new_df['High'] = new_high
        new_df['Low'] = new_low
        new_df['Open'] = new_open
        new_df['Close'] = new_close
        new_df['Volume'] = new_volume
    elif selected:
        new_df = pd.DataFrame()
        new_df['Date'] = new_date
        new_df[selected_set] = new

    new_df.set_index('Date', inplace=True)

    import_df = pd.DataFrame(new_df)

    return import_df


def compile_data(compile_type, path, selection):
    # Standard Format: Alpha Vantage
    drop_columns = True

    if compile_type == 'Single':
        decision = ''
        while decision != 'n' and decision != 'y':
            decision = input('Do you want to drop columns? (y/n) ')
        if decision == 'n':
            drop_columns = False

    selected_set = ''
    if drop_columns:
        datasets = ['Open', 'Close', 'High', 'Low', 'Volume']
        for i, set in enumerate(datasets):
            print('--> ' + str(i) + ' : ' + str(set) + '.')

        trigger_one = -1
        while trigger_one not in range(1,5):
            trigger_one = int(input('Select dataset for dataframe to keep: '))

        selected_set = datasets[trigger_one]
        datasets.remove(selected_set)

    decision = ''
    while decision != 'n' and decision != 'y':
        decision = input('Do you want to adjust the timeframe? (y/n) ')
    if decision == 'y':
        time_adjust = True
    elif decision == 'n':
        time_adjust = False

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

        if time_adjust:
            try:
                date_format = dt.strptime(import_df['Date'].iloc[0], '%Y-%m-%d')
                origin_time_format = '%Y-%m-%d'
            except ValueError:
                origin_time_format = '%Y-%m-%d %H:%M:%S'

            import_df.sort_values('Date', 0, ascending=True, inplace=True)
            date_one = dt.strptime(import_df['Date'].iloc[0], origin_time_format)
            date_two = dt.strptime(import_df['Date'].iloc[1], origin_time_format)
            print(date_one)
            print(date_two)
            time_delta = date_two - date_one
            print(time_delta.seconds)
            minute_times = [1, 5, 15, 30, 60]
            selectable_times = []

            for minutes in minute_times:
                if time_delta.seconds / 60 < minutes and date_one.day == date_two.day:
                    selectable_times.append(str(minutes) + 'min')

            longer_times = ['daily', 'weekly', 'monthly', 'yearly']
            if date_one.day != date_two.day or date_one.month != date_two.month:
                if time_delta.days == 1:
                    longer_times = longer_times[1:]
                elif time_delta.days > 1 and time_delta.days < 5:
                    longer_times = longer_times[2:]
                elif time_delta.days > 5 and time_delta.days < 25:
                    longer_times = longer_times[3:]
                else:
                    print(' --> ERROR: Time Adjustment not possible!')

            for time in longer_times:
                selectable_times.append(time)

            for i, time in enumerate(selectable_times, start=0):
                print('--> ' + str(i) + ' : ' + str(time.capitalize()) + '.')

            time_selection = ''
            while time_selection not in range(0, len(selectable_times)):
                time_selection = int(input('Select timeframe to convert table to by index: '))

            selected_time = selectable_times[time_selection]

        import_df.set_index('Date', inplace=True)

        if drop_columns == True:
            for set in datasets:
                try:
                    import_df.drop(set, 1, inplace=True)
                except:
                    next

        save_path = path.replace('Price_Data', 'Compiled_Data') + compile_type + '\\'
        # if selection == '':
        #     save_path = os.getcwd() + '\\Compiled_Data\\individual\\'
        #     selection = path[path.rindex('\\')+1:]
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        selected_column = selected_set
        if time_adjust:
            import_df = adjust_time(selected_time, import_df, selected_column, selected_set)
            import_df.dropna(0, inplace=True)
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

        time_adjusted = False
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

            if time_adjust and not time_adjusted:
                try:
                    date_format = dt.strptime(import_df['Date'].iloc[0], '%Y-%m-%d')
                    origin_time_format = '%Y-%m-%d'
                except ValueError:
                    origin_time_format = '%Y-%m-%d %H:%M:%S'

                import_df.sort_values('Date', 0, True)
                date_one = dt.strptime(import_df['Date'].iloc[0], origin_time_format)
                date_two = dt.strptime(import_df['Date'].iloc[1], origin_time_format)
                time_delta = date_two - date_one
                minute_times = [1, 5, 15, 30, 60]
                selectable_times = []

                for minutes in minute_times:
                    if time_delta.seconds / 60 < minutes and date_one.day == date_two.day:
                        selectable_times.append(str(minutes) + 'min')

                longer_times = ['daily', 'weekly', 'monthly', 'yearly']
                if date_one.day != date_two.day or date_one.month != date_two.month:
                    if time_delta.days == 1:
                        longer_times = longer_times[1:]
                    elif time_delta.days > 1 and time_delta.days < 5:
                        longer_times = longer_times[2:]
                    elif time_delta.days > 5 and time_delta.days < 25:
                        longer_times = longer_times[3:]
                    else:
                        print(' --> ERROR: Time Adjustment not possible!')

                for time in longer_times:
                    selectable_times.append(time)

                for i, time in enumerate(selectable_times, start=0):
                    print('--> ' + str(i) + ' : ' + str(time.capitalize()) + '.')

                time_selection = ''
                while time_selection not in range(0, len(selectable_times)):
                    time_selection = int(input('Select timeframe to convert table to by index: '))

                selected_time = selectable_times[time_selection]
                time_adjusted = True

            import_df.set_index('Date', inplace=True)

            for set in datasets:
                import_df.drop(set, 1, inplace = True)
            import_df.rename(columns={selected_set: file[:file.index('.csv')]}, inplace=True)

            selected_column = file[:file.index('.csv')]

            if compile_type == 'Individual':
                if time_adjust:
                    import_df = adjust_time(selected_time, import_df, selected_column, selected_set)
                    import_df.dropna(0, inplace=True)
                import_df.to_csv(save_path + 'Individual\\' + file + '.csv')
            if compile_type == 'Joined':
                if df.empty:
                    if time_adjust:
                        import_df = adjust_time(selected_time, import_df, selected_column, selected_set)
                        import_df.dropna(0, inplace=True)
                    df = import_df
                else:
                    if time_adjust:
                        import_df = adjust_time(selected_time, import_df, selected_column, selected_set)
                        import_df.dropna(0, inplace=True)
                    df = df.join(import_df, how='outer')

            sys.stdout.write('\r')
            ticks = int(round(i / (int(len(contents)) / 20), 0))
            sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, (i + 1) * (100 / (int(len(contents))))))
            sys.stdout.flush()

        if compile_type == 'Joined':
            df.fillna(0, inplace=True)
            save_path = save_path + 'Joined_' + selection + '_' + dt.now().strftime("%d.%m.%Y") + '.csv'
            # todo adjust path to selected timeframe
            df.to_csv(save_path)

    print('--> Compiled dataframe created!')
    print('--> Path: ' + str(save_path))
