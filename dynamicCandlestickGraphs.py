import dash  # version 1.13.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from Dataframefiltering import getAllRecordsFromDB
from App import app


df=getAllRecordsFromDB()
list_companies=[]
for company in df['symbol'].unique():
    list_companies.append(company)

layout = html.Div([
    html.Div(children=[
        html.Button('Add Chart', id='add-chart', n_clicks=0),
    ]),
    html.Div(id='container', children=[])
])
@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width':'90%','height':'500','display' : 'inline-block' , 'outline' : 'thin lightgrey solid' , 'padding' : 10 } ,
        children=[
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type' : 'dynamic-choice' ,
                    'index' : n_clicks
                } ,
                options=[{ 'label' : 'Candlestick Chart' , 'value' : 'candlestick' } ,
                         { 'label' : 'Bar Chart' , 'value' : 'bar' }] ,
                value='candlestick'
            ) ,
            dcc.Dropdown(id={
                            'type':'dynamic-dp-company',
                            'index':n_clicks
                            },
                         options=[{ 'label' : i , 'value' : i } for i in list_companies] ,
                         value=list_companies[0]),
            html.Button(
                "Update Graph",
                id={
                    'type':'dynamic-btn-update',
                    'index':n_clicks
                },
                value='update_graph'),
        ]
    )
    div_children.append(new_child)
    return div_children

@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dp-company', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-btn-update', 'index': MATCH},component_property='n_clicks'),
     Input({ 'type' : 'dynamic-choice' , 'index' : MATCH } , 'value')]
)
def update_graph(symbol_value,update_clk,choice):
    if choice =='candlestick':
        fig=arrange_candlestick_figure(selected_company=symbol_value)
        return fig
    elif choice == 'bar':
        fig=update_figure_volume(selected_company=symbol_value)
        return fig


def update_figure_volume(selected_company) :
    stocks_df = getAllRecordsFromDB()
    filtered_df = stocks_df[stocks_df['symbol'] == selected_company]
    filtered_df = filtered_df.iloc[-50 :]
    traces = []

    traces.append(
        go.Bar(
            x=filtered_df['date'] ,
            y=filtered_df['volume'] ,
            text=filtered_df['volume']

        )
    )

    return {
        'data' : traces ,
        'layout' : go.Layout(
            xaxis={ 'title' : 'Time' } ,
            yaxis={ 'title' : 'Volume' } ,
            hovermode='closest' ,
            margin=dict(l=50 , r=20 , t=30 , b=50) ,
            paper_bgcolor="LightSteelBlue" ,
            title=selected_company+" : Volume of stock traded" ,
            height=400) }


def arrange_candlestick_figure(selected_company):
    stocks_df=getAllRecordsFromDB()
    filtered_df = stocks_df[stocks_df['symbol'] == selected_company]
    filtered_df = filtered_df.iloc[-50:]
    traces = []
    traces.append(
        go.Candlestick(x=filtered_df['date'],
                       open=filtered_df['open'],
                       high=filtered_df['high'] ,
                       low=filtered_df['low'] ,
                       close=filtered_df['close'] ,
                       name='candlestick'))
    avg_5 = filtered_df.close.rolling(window=5 , min_periods=3).mean()
    avg_8 = filtered_df.close.rolling(window=8 , min_periods=3).mean()
    traces.append(
        go.Scatter(
            x=filtered_df['date'] ,
            y=avg_5 ,
            mode='lines+markers' ,
            name='MA-5' ,
            marker={ 'size' : 5 ,
                     'opacity' : 0.5 ,
                     'line' : { 'width' : 0.5 , 'color' : 'black' } }))
    traces.append(
        go.Scatter(
            x=filtered_df['date'] ,
            y=avg_8 ,
            mode='lines+markers' ,
            name='MA-8' ,
            marker={ 'size' : 5 ,
                     'opacity' : 0.5 ,
                     'line' : { 'width' : 0.5 , 'color' : 'black' } }))
    return {
        'data' : traces ,
        'layout' : go.Layout(
            # xaxis={'title': 'Date'},
            yaxis={ 'title' : 'Price' } ,
            hovermode='closest' ,
            xaxis_rangeslider_visible=False ,
            margin=dict(l=50 , r=20 , t=30 , b=50) ,
            paper_bgcolor="LightSteelBlue" ,
            title=selected_company+" Intraday Stock Data(1min)",
            height=400 ) }
