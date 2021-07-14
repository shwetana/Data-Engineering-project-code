import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.offline as plotly
from dash.dependencies import Output , Input
import pandas as pd
from Investment_algorithm_final import list_cmp , linearregression , df_pie , df_rank

layout = html.Div([
    dcc.Graph(id='bar-graph',
              figure=px.bar(df_rank.head(20), y=df_rank['AdjustedSlope'].head(20),
                            x=df_rank['Company'].head(20),
                            hover_data=['CurrentPrice', 'ATR'],
                            labels={'color': 'criteria', 'y': 'AdjustedSlope', 'x': 'Company'},
                            height=500,
                            color=df_rank['Eligibility'].head(20) , title='Top 20 Ranked Companies')\
              .update_traces(dict(marker_line_width=1, marker_line_color="rgb(8,48,107)" , opacity=0.6)))
])
