import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3 as sql

# connect to main app.py file
from app import app, DATABASE, server

# connect to app pages
from apps import shop, dashboard, error, clients

# import components
from components.sidebar import sidebar

########################################################################################################################

# layout of the main page
content = html.Div(
    [
        dbc.Container(
            [
                html.H1('LXPYRO WEB APP', className="title text-center text-white pt-3"),
                html.H4('NO PYRO, NO PARTY', className="subtitle text-center text-white"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='main-sales',
                                    figure={}
                                )
                            ],
                            md=6, xs=12
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='main-products',
                                    figure={}
                                )
                            ],
                            md=6, xs=12
                        ),
                        dcc.Interval(
                            id='graph-update',
                            interval=100 * 1000,
                            n_intervals=0
                        )
                    ],
                    className="px-3 py-3"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(
                                    'AS NOSSAS REDES SOCIAIS',
                                    className="text-white text-center fw-bold"
                                ),
                            ],
                            xs=12,
                        ),
                        dbc.Col(
                            [
                                html.A(
                                    href="https://www.instagram.com/_.lx_pyro._/",
                                    target="_blank",
                                    children=[
                                        html.I(className="fab fa-instagram fa-5x text-white text-center grow")
                                    ]
                                )
                            ],
                            xs=12,
                            className="text-center pt-2 pb-3"
                        )
                    ]
                )

            ],
            fluid=True,
        )
    ],
    id='main-content'
)


########################################################################################################################
# Callbacks

# update stock graph
@app.callback(Output('main-products', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_products(_):
    con = sql.connect(DATABASE)
    # Load the data into a DataFrame
    df = pd.read_sql_query("SELECT name, in_stock from Product", con)

    barchart_products = go.Figure(
        data=[
            go.Bar(
                name='Initial Stock',
                x=df['name'],
                y=df['in_stock'],
                marker_color='#ff8100'
            ),
        ],
        layout=go.Layout(
            title='Stock',
            yaxis_title='Quantity',
        ),
    )

    barchart_products.update_layout(
        title={
            'xanchor': 'center',
            'yanchor': 'top',
            'y': 0.9,
            'x': 0.5,
            'font': {
                'family': 'Poppins',
                'size': 30,
            }
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='rgba(255,255,255,1)',
        font_family='Poppins',
        bargap=0.25
    )

    return barchart_products


# update sales graph
@app.callback(Output('main-sales', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_sales(_):
    con = sql.connect(DATABASE)
    # Load the data into a DataFrame
    df = pd.read_sql_query(
        """
            SELECT strftime('%m',time_created) as month, sum(sale_amount_paid) as total 
            FROM Sale 
            GROUP BY month
        """, con)

    barchart_sales = go.Figure(
        data=[
            go.Bar(
                name='Months',
                x=df['month'],
                y=df['total'],
                marker_color='#ff8100',
            ),
        ],
        layout=go.Layout(
            title='Sales',
            yaxis_title='Total Revenue',
            xaxis_title='Months'
        ),
    )

    barchart_sales.update_layout(
        title={
            'xanchor': 'center',
            'yanchor': 'top',
            'y': 0.9,
            'x': 0.5,
            'font': {
                'family': 'Poppins',
                'size': 30,
            }
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='rgba(255,255,255,1)',
        font_family='Poppins',
        bargap=0.25,
    )

    barchart_sales.update_traces(marker_color='#fc3512')

    return barchart_sales


########################################################################################################################
# template layout with the sidebar
app.layout = html.Div(
    className="container-fluid",
    children=[
        html.Div(
            children=[
                html.Div(
                    className="col-lg-2 left-panel bg-semi-dark",
                    children=[
                        sidebar,
                    ]
                ),

                html.Div(
                    className="col-lg-10 right-panel bg-dark",
                    children=[],
                    id='page-content'
                )
            ],
            className="row",

        ),
        dcc.Location(id="url"),
    ]
)


# functions callbacks
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/apps/shop':
        return shop.layout
    elif pathname == '/apps/dashboard':
        return dashboard.layout
    elif pathname == '/':
        return content
    elif pathname == '/apps/clients':
        return clients.layout
    else:
        return error.layout


if __name__ == '__main__':
    app.run_server(debug=False)
