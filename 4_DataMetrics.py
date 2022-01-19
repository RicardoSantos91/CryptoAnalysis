import pandas as pd
import matplotlib.pyplot as plt
import os

def open_csv(file, path=os.getcwd()):
    full_path = os.path.join(path, file)
    data = pd.read_csv(full_path)

    return data

df_coindata = open_csv('coindata.csv')


def create_metrics(data):

    data_metrics = data['slug', 'total_supply', 'circulating_supply',
                'max_supply', 'USD.price', 'USD.market_cap_dominance']

    data_metrics['csop'] = data_metrics['circulating_supply'] / data_metrics['USD.price']
    data_metrics['csomd'] = data_metrics['circulating_supply'] \
                            / data_metrics['USD.market_dominance']
    data_metrics['validation'] = data_metrics['circulating_supply'] \
                               / data_metrics['total_supply']


    return data_metrics

df_coindata_derivate_metrics = create_metrics(df_coindata)


def save_data_csv(data, filename):
    data.to_csv(str(cwd) + '/' + filename + '.csv', index=False)


save_data_csv(coindata, 'coindata_derivate_metrics')





