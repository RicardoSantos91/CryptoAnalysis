import os
import pandas as pd
import seaborn as sns


def open_csv(file, path=os.getcwd()):
    full_path = os.path.join(path, file)
    data = pd.read_csv(full_path)

    return data


df_coindata = open_csv('coindata.csv')


def check_duplicates(data):
    duplicated = sum(data.duplicated())

    if duplicated > 0:
        data = data[-duplicated]

    return data, duplicated


df_coindata, number_of_duplicates  = check_duplicates(df_coindata)


def convert_timezones_to_datetime(data):
    date_columns = ['date_added', 'last_updated']

    for name in date_columns:
        data[name] = pd.to_datetime(data[name])

    formated_columns = sum(df_coindata.dtypes == 'datetime64[ns, UTC]')

    return data, formated_columns


df_coindata, formated_columns = convert_timezones_to_datetime(df_coindata)





