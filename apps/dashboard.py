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
                html.A([html.I(className="fas fa-sync-alt text-white subtitle p-4")], href="/apps/dashboard"),
            ], className="my-5 text-center", xs=12)
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card(                           # MOST SOLD PRODUCT
                            dbc.CardBody([
                                html.Div(
                                    html.H3("Most Sold Product", className="text-white text-center fw-bold py-2"),
                                    className="bg-danger rounded-20"
                                ),
                                dbc.Row([
                                    dbc.Col(children=[
                                        html.H4(id="most-sold-product-name", className="text-uppercase text-dark text-center fw-bold"),
                                        html.H1(id="most-sold-product-quantity", className="text-danger text-center fw-bold"),
                                        html.H5("Units", className="text-dark text-center fw-bold")
                                    ], xs=12),
                                ], className="py-2")
                            ]), className="rounded-20"
                        )
                    ], xs=12, md=4),
                    dbc.Col(children=[
                        dbc.Card(children=[                 # BEST CLIENT
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
                                        html.Span("Name: ", className="h4 fw-bold text-dark"),
                                        html.Span(id="best-client-name", className="h4"),
                                        html.Br(),
                                        html.Span("Instagram: ", className="h4 fw-bold text-dark"),
                                        html.Span(id="best-client-instagram", className="h4"),
                                        html.Br(),
                                        html.Span("Age: ", className="h4 fw-bold text-dark"),
                                        html.Span(id="best-client-age", className="h4"),
                                        html.Br(),
                                        html.Span("Address: ", className="h4 fw-bold text-dark"),
                                        html.Span(id="best-client-address", className="h4"),
                                        html.Br(),
                                        html.Span("Spent: ", className="h4 fw-bold text-dark"),
                                        html.Span(id="best-client-spent", className="h4"),
                                    ], className="text-start", xs=6)
                                ], className="pt-2")
                            ])
                        ], className="rounded-20")
                    ], xs=12, md=8)
                ]),
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card(                       # BEST SALES MONTH
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
                        dbc.Card(                       # TOTAL REVENUE
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
                        dbc.Card(                       # MOST SOLD CATEGORY
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
                        dbc.Card(                       # PRODUCT SALES PER MONTH GRAPH
                            dbc.CardBody([
                                html.Div(
                                    html.H3("Product Sales Per Month", className="text-white text-center fw-bold py-2"),
                                    className="bg-danger rounded-20"
                                ),
                                html.Div(children=[dcc.Graph(id='products-sale-per-month-graph')])
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
              [Input("update-dashboard", "n_intervals")])
def populate_most_sold_product(_):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()

    product_name, product_quantity, _ = get_most_sold_product(cursor)
    return product_name[0], product_quantity


@app.callback(Output("best-client-name", "children"), Output("best-client-instagram", "children"),
              Output("best-client-age", "children"), Output("best-client-address", "children"),
              Output("best-client-spent", "children"),
              [Input("update-dashboard", "n_intervals")])
def populate_best_client(_):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    name, insta, age, address, spent = get_best_client(cursor)
    return name, "@{}".format(insta), age, address, "{} €".format(spent)


@app.callback(Output("best-sales-month-name", "children"),
              [Input("update-dashboard", "n_intervals")])
def populate_best_sales_month(_):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    data = get_best_sales_month(cursor)
    month = get_month_name(data[0][5:])
    return month


@app.callback(Output("total-revenue-number", "children"), [Input("update-dashboard", "n_intervals")])
def populate_total_revenue(_):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    return "{} €".format(get_total_revenue(cursor)[0])


@app.callback(Output("most-sold-category-name", "children"), [Input("update-dashboard", "n_intervals")])
def populate_most_sold_category(_):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    category = get_most_sold_category(cursor)
    return category


@app.callback(Output("products-sale-per-month-graph", "figure"), [Input("update-dashboard", "n_intervals")])
def populate_products_sale_per_month(_):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    product_sales_data = get_product_sales_per_month(cursor)

    data = []
    products = []
    for info in product_sales_data:
        base = {'x': [], 'y': [], 'type': 'bar', 'name': ''}
        if info[0] not in products:
            products.append(info[0])
            base['x'].append(info[1])
            base['y'].append(info[2])
            base['name'] = info[0]
            data.append(base)
        else:
            for a in data:
                if a['name'] == info[0]:
                    a['x'].append(info[1])
                    a['y'].append[info[2]]

    figure = {'data': data}
    return figure

def get_month_name(number):
    switcher = {
        '01': "January",
        '02': "February",
        '03': "March",
        '04': "April",
        '05': "May",
        '06': "June",
        '07': "July",
        '08': "August",
        '09': "September",
        '10': "October",
        '11': "November",
        '12': "December"
    }
    return switcher.get(number, "Invalid Month")

