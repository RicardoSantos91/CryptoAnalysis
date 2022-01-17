# TODO Build Visualization module

# TODO Understand price vs supply

# Todo Investigate Correlation between coins

import pandas as pd
import os

def open_csv(file, path=os.getcwd()):
    full_path = os.path.join(path, file)
    data = pd.read_csv(full_path)

    return data

df_coindata = open_csv('coindata.csv')

def filter_data(data, *arg):
    names = list(arg)
    data = data[names]

    return data

df_coindata_filtered = filter_data(df_coindata, 'slug', 'USD.price')

def vizualize_price_coin(data):