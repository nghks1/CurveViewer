import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import os
import time
import utility as ul

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'Data/UScurve.csv'),parse_dates=['Date'])
df=df.dropna()
df['Date']= df['Date'].astype(np.int64)
col_names = df.drop('Date',axis=1).columns.values
col_names= np.insert(col_names,0," ",axis=0)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label = 'outright', children = [

            html.Div([
                dcc.Graph(
                    id='curve-graph',

                )
            ], style={'display': 'inline-block'}),
            html.Div(dcc.Slider(
                id='year-slider',
                min=df['Date'].min(),
                max=df['Date'].max(),
                value=df['Date'].max(),
                marks={str(year): str(year) for year in df['Date'].unique()},
                step=None
            ),
            ),
            html.H4(children='Choose tenor to view historical timeseries:'),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-yaxis-column',
                    options=[{'label': i, 'value': i} for i in df.drop('Date', axis=1).columns],
                    value='1y'
                ),
            ], ),

            html.Div([
                dcc.Graph(id='x-time-series'),
            ], )

        ]),

        dcc.Tab(label = 'curve',children = [
            html.H1(children='US Curve Spread (Bps)'),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in col_names],
                data=ul.generate_table(df)
            ),
            html.Div([
                dcc.Dropdown(
                    id='1st-tenor',
                    options=[{'label': i, 'value': i} for i in df.drop('Date', axis=1).columns],
                    value='1y'
                ),

            ],
                style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='2nd-tenor',
                    options=[{'label': i, 'value': i} for i in df.drop('Date', axis=1).columns],
                    value='2y'
                ),

            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='curve-graph',

                )
            ], style={'display': 'inline-block'}),

        ])
    ])



])



@app.callback(
    dash.dependencies.Output('curve-graph', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])

def update_graph(date_value):
    dff = df[df['Date'] == date_value]
    return {
        'data': [dict(
            x= ["1y", "2y","3y","4y","5y","6y","7y","8y","9y","10y","12y","15y","20y","25y","30y"],
            y=dff.drop('Date',axis=1).values[0],
            mode='lines',

            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            title='US Swap Curve ( ' + time.strftime('%Y-%m-%d', time.localtime(date_value//10**9))+ " )",
            xaxis={
                'title': 'Tenor',
            },
            yaxis={
                'title': "Rate (%)",
            },
            margin={'l': 50, 'b': 30, 't': 30, 'r': 10},
            height=500,
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('curve-graph', 'figure'),
    [dash.dependencies.Input('1st-tenor', 'value'),
     dash.dependencies.Input('2nd-tenor', 'value')])

def update_curve_graph(front,back):
    dff = (df[back]-df[front])*100
    dff=dff.round(1)
    return {
        'data': [dict(
            x= pd.to_datetime(df['Date'],unit='ns'),
            y=dff,
            mode='lines',

            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            title= back + " - " + front,
            xaxis={
                'title': 'Year',
            },
            yaxis={
                'title': "Rate (%)",
            },
            margin={'l': 50, 'b': 30, 't': 30, 'r': 10},
            height=500,
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
def update_y_timeseries(tenor):
    return {
        'data': [dict(
            x=pd.to_datetime(df['Date'],unit='ns'),
            y=df[tenor],
            mode='lines'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 40, 'b': 30, 'r': 30, 't': 40},
            'title': "Timeseries of US " + tenor,
        }
    }



if __name__ == '__main__':
    app.run_server(debug=True)