import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

data = pd.read_csv(
    'coindata_derivate_metrics.csv')

app = dash.Dash(__name__)



fig1 = px.scatter(data, x='slug', y='csomd',
                 size='validation', title='USD Price per coin',
                 log_y=True)

fig2 = px.scatter(data, x='slug', y=['total_supply', 'circulating_supply'],
                 size='validation', title='Supply per coin',
                 log_y=True)

app.layout = html.Div(
    children=[
        html.H1(children='Crypto Analytics'),
        html.P(
            children='USD Price per coin'
        ),
        dcc.Graph(
                    figure=fig1
        ),
        html.P(
            children='Supply per coin'
        ),
        dcc.Graph(
                    figure=fig2
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)