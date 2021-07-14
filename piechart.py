
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from Investment_algorithm_final import list_cmp, linearregression,df_pie,df_rank


layout=html.Div([
            dcc.Graph(id='pie-graph',
              figure=px.pie(df_pie, values=df_pie['PercentageAllocation'].head(12),
                            names=df_pie['Company'].head(12),
                            title='Company stocks percentage allocation'))
])