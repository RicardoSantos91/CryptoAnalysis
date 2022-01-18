# TODO Build Visualization module

# TODO Understand price vs supply

# Todo plot inverse exponential over the 100 top coins price

# Todo Investigate Correlation between coins

import pandas as pd
import matplotlib.pyplot as plt
import os

def open_csv(file, path=os.getcwd()):
    full_path = os.path.join(path, file)
    data = pd.read_csv(full_path)

    return data

df_coindata = open_csv('coindata.csv')

def filter_data(data, *args):
    names = list(args)
    data = data[names]

    return data

df_coindata_filtered = filter_data(df_coindata, 'slug', 'USD.price',
                                   'max_supply', 'circulating_supply', 'total_supply')


def vizualize_price_coin(x, *args, title, yscale, scatter_size):

    for i in range(len(args)):
        plt.scatter(x, args[i], s=scatter_size)

    plt.title(title)
    plt.xlabel('Price ($)')
    plt.xticks(x, rotation=-90)
    plt.yscale(yscale)
    plt.savefig('plot_' + title + '.png')

    plt.ioff()


vizualize_price_coin(df_coindata_filtered['slug'], df_coindata_filtered['USD.price'],
                     title='USD coin price', yscale='linear', scatter_size=2.5)


vizualize_price_coin(df_coindata_filtered['slug'], df_coindata_filtered['max_supply'],
                    df_coindata_filtered['circulating_supply'],
                     title='Coin supply', yscale='linear', scatter_size=2.5)

