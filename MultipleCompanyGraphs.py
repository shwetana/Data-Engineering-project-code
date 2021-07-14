import dash  
import dash_core_components as dcc  
import dash_html_components as html  
import plotly.graph_objs as go  
import plotly.express as px
from dash.dependencies import Output, Input
import pandas as pd  
from Dataframefiltering import getAllRecordsFromDB
from App import app

df=getAllRecordsFromDB()
list_companies=[]
for company in df['symbol'].unique():
    list_companies.append(company)

layout=html.Div([
    html.Div([
        dcc.Dropdown(id='company-picker' ,
                     options=[{ 'label' : i , 'value' : i } for i in list_companies] ,
                     value=list_companies[0])
    ], style={'width':'40%','display':'inline-block'}),
    html.Div([ dcc.Graph(id='graph-with-picker')],style={'height':'50%','width':'90%','display':'inline-block','padding': '0px 10px 10px 10px'}),
    html.Div([dcc.Graph(id='volume-with-picker')],style={'height':'30%','width':'90%','display':'inline-block','padding': '0px 10px 10px 10px'})
    
])


def arrange_candlestick_figure(selected_company):
    stocks_df=getAllRecordsFromDB()
    filtered_df = stocks_df[stocks_df['symbol'] == selected_company]
    filtered_df=filtered_df.iloc[-50:]
    traces = []
    traces.append(
        go.Candlestick(x=filtered_df['date'],
                    open=filtered_df['open'],
                    high=filtered_df['high'],
                    low=filtered_df['low'],
                    close=filtered_df['close'],
                    name='candlestick')
        
    )

    avg_5 = filtered_df.close.rolling(window=5, min_periods=3).mean()
    avg_8 = filtered_df.close.rolling(window=8, min_periods=3).mean()

    traces.append(
        go.Scatter(
            x=filtered_df['date'],
            y=avg_5,
            mode='lines+markers',
            name='MA-5',
            marker={'size':5,
            'opacity':0.5,
            'line':{'width':0.5,'color':'black'}}
        )
    )
    traces.append(
        go.Scatter(
            x=filtered_df['date'],
            y=avg_8,
            mode='lines+markers',
            name='MA-8',
            marker={'size':5,
            'opacity':0.5,
            'line':{'width':0.5,'color':'black'}}
        )
    )

    return {
    'data': traces,
    'layout': go.Layout(
    yaxis={'title': 'Price'},
    hovermode='closest',
    xaxis_rangeslider_visible=False,
    margin=dict(l=50, r=20, t=28, b=90),
    paper_bgcolor="LightSteelBlue",
    title="CandleStick Chart of intraday stock data(1min)",
    height=300,
    legend={'orientation':'h'}
    )}

@app.callback(Output(component_id='graph-with-picker',component_property='figure'),
            [Input(component_id='company-picker',component_property='value')])
def update_figure(selected_company):
    fig = arrange_candlestick_figure(selected_company=selected_company)
    return fig


@app.callback(Output(component_id='volume-with-picker',component_property='figure'),
            [Input(component_id='company-picker',component_property='value')])
def update_figure_volume(selected_company):
    stocks_df = getAllRecordsFromDB()
    filtered_df = stocks_df[stocks_df['symbol'] == selected_company]
    filtered_df=filtered_df.iloc[-50:]
    traces = []
    traces.append(
        go.Bar(
            x=filtered_df['date'],
            y=filtered_df['volume'],
            text=filtered_df['volume']
        )
    )

    return {
    'data': traces,
    'layout': go.Layout(
    xaxis={'title': 'Time'},
    yaxis={'title': 'Volume'},
    hovermode='closest',
    margin=dict(l=50, r=20, t=28, b=45),
    paper_bgcolor="LightSteelBlue",
    title="Volume of stocks traded",
    height=200)}

