import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import LRplot
import piechart
import barchart
import dynamicCandlestickGraphs
import MultipleCompanyGraphs
from dash.dependencies import Input, Output
from App import app

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div([
        html.H2("Stock Data", className="display-4"),
        html.Hr(),
        html.P(
            "Visualizations", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Dynamic Candlestick chart" , href="/page-1" , id="page-1-link") ,
                dbc.NavLink("Weekly Top Ranked Companies" , href="/page-2" , id="page-2-link") ,
                dbc.NavLink("Linear Regression Plot", href="/page-3", id="page-3-link"),
                dbc.NavLink("Percentage Allocation", href="/page-4", id="page-4-link"),
                dbc.NavLink("Candlestick chart", href="/page-5", id="page-5-link")
            ],
            vertical=True,
            pills=True, ),],
    style=SIDEBAR_STYLE,)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False , False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return dynamicCandlestickGraphs.layout
    elif pathname == "/page-2":
        return barchart.layout
    elif pathname == "/page-3":
        return LRplot.layout
    elif pathname == "/page-4":
        return piechart.layout
    elif pathname == "/page-5":
        return MultipleCompanyGraphs.layout
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)