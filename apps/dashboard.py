import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sqlite3 as sql
from app import app, DATABASE
from sql_functions import *

layout = html.Div(id="dashboard", children=[
    html.Div(className="container", children=[
        dbc.Row(children=[
            dbc.Col(children=[
                html.H1("DASHBOARD", className="title text-center text-white fs-bold"),
                html.A([html.I(className="fas fa-sync-alt text-white subtitle p-4")], href="/apps/clients"),
            ], className="my-5 text-center", xs=12)
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card(
                            dbc.CardBody([
                                html.Div(
                                    html.H3("Most Sold Product", className="text-white text-center fw-bold py-2"),
                                    className="bg-danger rounded-20"
                                ),
                                dbc.Row([
                                    dbc.Col(children=[
                                        html.H4(id="most-sold-product-name", className="text-uppercase text-dark fw-bold"),
                                        html.H1(id="most-sold-product-quantity", className="text-danger text-center fw-bold"),
                                        html.H5("Units", className="text-dark text-center fw-bold")
                                    ], xs=6),
                                    dbc.Col(children=[
                                        html.Img(id="most-sold-product-image", className="rounded text-center img-fluid")
                                    ], xs=6),
                                ], className="py-3")
                            ]), className="rounded-20"
                        )
                    ], xs=12, md=4),
                    dbc.Col(children=[
                        dbc.Card(children=[
                            dbc.CardBody(children=[
                                html.Div(
                                    html.H3("Best Client", className="text-white text-center fw-bold py-2"),
                                    className="bg-danger rounded-20"
                                ),
                                dbc.Row(children=[
                                    dbc.Col(children=[
                                        html.I(className="fas fa-user text-dark profile")
                                    ], className="text-center", xs=6),
                                    dbc.Col(children=[
                                        html.H4("Name:", className="fw-bold text-dark"),
                                        html.H4(id="best-client-name"),
                                        html.H4("Instagram:", className="fw-bold text-dark"),
                                        html.H4(id="best-client-instagram"),
                                        html.H4("Age:", className="fw-bold text-dark"),
                                        html.H4(id="best-client-age"),
                                        html.H4("Address:", className="fw-bold text-dark"),
                                        html.H4(id="best-client-address"),
                                        html.H4("Spent:", className="fw-bold text-dark"),
                                        html.H4(id="best-client-spent"),
                                    ], className="text-start", xs=6)
                                ])
                            ])
                        ], className="rounded-20")
                    ], xs=12, md=8)
                ]),
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card(
                            dbc.CardBody([
                                html.Div(
                                    html.H3("Best Sales Month", className="text-white text-center fw-bold py-2"),
                                    className="bg-danger rounded-20"
                                ),
                                html.Div(
                                    html.H1(id="best-sales-month-name", className="text-center text-dark")
                                )
                            ]), className="rounded-20"
                        )
                    ], xs=12, md=4),
                    dbc.Col(children=[
                        dbc.Card(
                            dbc.CardBody([
                                html.Div(
                                    html.H3("Total Revenue", className="text-white text-center fw-bold py-2"),
                                    className="bg-danger rounded-20"
                                ),
                                html.Div(
                                    html.H1(id="total-revenue-number", className="text-center text-dark")
                                )
                            ]), className="rounded-20"
                        )
                    ], xs=12, md=4),
                    dbc.Col(children=[
                        dbc.Card(
                            dbc.CardBody([
                                html.Div(
                                    html.H3("Most Sold category", className="text-white text-center fw-bold py-2"),
                                    className="bg-danger rounded-20"
                                ),
                                html.Div(
                                    html.H1(id="most-sold-category-name", className="text-center text-dark")
                                )
                            ]), className="rounded-20"
                        )
                    ], xs=12, md=4),
                ], className="py-4"),
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card(
                            dbc.CardBody([
                                html.Div(
                                    html.H3("Product Sales Per Month", className="text-white text-center fw-bold py-2"),
                                    className="bg-danger rounded-20"
                                ),
                                html.Div(id="product-sales-per-month-graph")
                            ]),
                            className="rounded-20"
                        )
                    ])
                ], className="py-4")
            ])
        ])
    ]),
    dcc.Interval(id='update-dashboard', interval=1000 * 1000, n_intervals=0)
])


# CALLBACK FUNCTIONS TO LOAD THE DATA
@app.callback(Output("most-sold-product-name", "children"), Output("most-sold-product-quantity", "children"),
              Output("most-sold-product-image", "src"),
              [Input("update-dashboard", "n_intervals")])
def populate_most_sold_product(_):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()

    product_name, product_quantity, product_image = get_most_sold_product(cursor)
    return product_name[0], product_quantity, "../{}".format(product_image[0])