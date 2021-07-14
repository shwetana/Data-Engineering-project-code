
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import statsmodels.api as sm
from App import app
from dash.dependencies import Output, Input
import pandas as pd
from Investment_algorithm_final import list_cmp, linearregression,df_pie,df_rank



layout = html.Div([
    html.Div([
        dcc.Dropdown(id='company-dropdown-picker' , options=[{'label': i, 'value': i} for i in list_cmp],
                     value='AAPL')
    ], style={'width':'40%','display':'inline-block'}),
    html.Div([dcc.Graph(id='scatter-graph')])
])
@app.callback(Output('scatter-graph','figure'),
    [Input('company-dropdown-picker','value')])
def update_lr (company_name):
    x, log_y, y_fit= linearregression(company_name=company_name)
    fig = px.scatter(x=x,
                     y=log_y,
                     trendline="ols",
                     title='Company wise Linear Regression plot',
                     color=log_y,
                     height=500,
                     labels={'y': 'Log of price', 'x': 'Number Of Days'})
    return fig

    # # fig.update_xaxes(tickvals=dates)
    # # fig.update_xaxes(ticks="outside" , tickwidth=2 , tickcolor='pink' , ticklen=10)
    # # fig.update_yaxes(ticks="outside" , tickwidth=2 , tickcolor='pink' , ticklen=10 , col=1)
    # # strdates=[]
    # for d in dates:
    #     formatted=str(d).split(" ")
    #     strdates.append(formatted[0])
    #     print(formatted[0])
    # print(strdates)
    # fig.update_layout(
    #     xaxis=dict(
    #         tickmode='array' ,
    #         tickvals=x,
    #         ticktext=dates,
    #         # nticks=20,
    #         # tickangle=45 ,
    #         tickfont=dict(family='Rockwell' , color='black' , size=10),
    #         # margin=dict(
    #         #     pad=20
    #         # )
    # #     ),
    #     # xaxis_tickformat='%d %B (%a)<br>%Y'
    # )
    # fig.update_xaxes(tick0=2 , dtick=2)
    # return fig
