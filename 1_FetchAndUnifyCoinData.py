from requests import request, session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import config
import os


cwd = os.getcwd()


# API parameters

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}


# API data retrieval

def api_data_fetching(session, url=url,
                      parameters=parameters, headers=headers):
    session = session

    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return data


data = api_data_fetching(session(), url, parameters, headers)

# DataFrame creation from json


def data_unification(data):

    coindata = pd.DataFrame(data['data'])
    coindata_names = list(coindata.columns)

    coindata_quote = coindata['quote']
    coindata_quote = pd.json_normalize(coindata_quote)
    coindata_quote_names = list(coindata_quote.columns)

    coindata_platform = coindata['platform']
    coindata_platform = pd.json_normalize(coindata_platform)
    coindata_platform_names = list(coindata_platform.columns)

    coindata_tags = pd.DataFrame(coindata['tags'].to_list())
    coindata_tags_names = list(coindata_tags.columns)

    # Unifying the dataframe

    coindata = pd.concat([coindata, coindata_quote], axis=1, ignore_index=True)
    coindata = pd.concat([coindata, coindata_platform], axis=1, ignore_index=True)
    coindata = pd.concat([coindata, coindata_tags], axis=1, ignore_index=True)

    return coindata, coindata_names, \
           coindata_quote_names, coindata_platform_names, coindata_tags_names


coindata, general_names, quote_names, platform_names, tags_names = data_unification(data)


def columns_renaming(data, general, quote, platform, tags):

    for i in range(len(tags_names)):
        tags[i] = 'VCtag_' + str(i)

    names = general + quote + platform + tags
    names[0] = 'coin_id'
    data.columns = names

    return data


coindata = columns_renaming(coindata, general_names, quote_names, platform_names, tags_names)


def drop_irrelevant_columns(data):
    data.drop(columns=['tags', 'platform', 'quote'], axis=1, inplace=True)

    return data


coindata = drop_irrelevant_columns(coindata)


def save_data_csv(data):
     data.to_csv(str(cwd) + '/' + 'coindata.csv',index=False)


save_data_csv(coindata)


# TODO Count API credits
