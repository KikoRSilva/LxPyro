from datetime import datetime, date
import os
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_uploader as du
import dash_table as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from components.searchbar import search_bar
from sql_functions import *

add_new_item_button = dbc.Button(
    id="add_new_item_btn",
    type="button",
    className="btn btn-danger m-5",
    children=[
        html.I(className="fas fa-plus text-white"),
        " New Item",

    ]
)

# MODAL FORM INPUT
name_input = dbc.FormGroup(
    [
        dbc.Label("Name", html_for="name-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="name-row", placeholder="Enter name"
            ),
            width=10
        )
    ],
    row=True,
)

description_input = dbc.FormGroup(
    [
        dbc.Label("Description", html_for="description-row", width=3),
        dbc.Col(
            dbc.Textarea(
                id="description-row", placeholder="Enter description"
            ),
            width=9
        )
    ],
    row=True,
)

price_input = dbc.FormGroup(
    [
        dbc.Label("Price per Unit", html_for="price-row", width=4),
        dbc.Col(
            dbc.Input(
                type="number", id="price-row", placeholder="Enter price"
            ),
            width=8
        )
    ],
    row=True,
)

unit_input = dbc.FormGroup(
    [
        dbc.Label("Basic Unit", html_for="unit-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="unit-row", placeholder="Enter unit"
            ),
            width=10
        )
    ],
    row=True,
)

limited_input = dbc.FormGroup(
    [
        dbc.Label("Limited", html_for="limited-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="limited-row", placeholder="Enter 'yes' or 'no'"
            ),
            width=10
        )
    ],
    row=True,
)

stock_input = dbc.FormGroup(
    [
        dbc.Label("In stock", html_for="stock-row", width=3),
        dbc.Col(
            dbc.Input(
                type="number", id="stock-row", placeholder="Enter stock"
            ),
            width=9
        )
    ],
    row=True,
)

active_input = dbc.FormGroup(
    [
        dbc.Label("Active for sale", html_for="active-row", width=3),
        dbc.Col(
            dbc.Input(
                type="text", id="active-row", placeholder="Enter 'yes' or 'no'"
            ),
            width=9
        )
    ]
)

image_upload = du.Upload(id='new_item_uploader', filetypes=['png', 'jpg', 'jpeg', 'gif'])

save_button = dbc.Button("Add", id="save_new_item_button", className="btn btn-danger", type="button")

close_button_add_new = dbc.Button("Close", id="close_modal_add_new", className="btn btn-outline-danger")

add_new_item_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            "ADD NEW ITEM TO THE STORE",
        ),
        dbc.ModalBody(
            [
                name_input, description_input, price_input, unit_input,
                limited_input, stock_input, active_input, image_upload
            ],
        ),
        dbc.ModalFooter(
            [
                html.P(id="add-new-status", className="text-danger"),
                save_button,
                close_button_add_new,

            ]
        )
    ],
    backdrop="static",
    scrollable=True,
    id="modal_add_new"
)

########################################################################################################################
modify_item_button = dbc.Button(
    id="modify_item_btn",
    type="button",
    className="btn btn-danger m-5",
    children=[
        html.I(className="fas fa-tools text-white"),
        " Modify Item",
    ]
)
close_button_modify = dbc.Button("Close", id="close_modal_modify", className="btn btn-outline-danger")

modify_item_modal = dbc.Modal(
    [
        dbc.ModalHeader("MODIFY ITEM FROM THE STORE"),
        dbc.ModalBody(),
        dbc.ModalFooter([close_button_modify])
    ],
    backdrop="static",
    scrollable=True,
    id="modal_modify"
)
######################################################################################################

new_sale_button = dbc.Button(children=[html.I(className="fas fa-plus text-white"), " NEW SALE", ], id="new_sale_button",
                             className="btn btn-danger m-5", type="button")
new_sale_save = dbc.Button("Register", id="new_sale_save", className="btn btn-danger", type="button")
new_sale_close = dbc.Button("Close", id="new_sale_close", className="btn btn-outline-danger", type="button")
new_sale_modal = dbc.Modal(
    [
        dbc.ModalHeader("REGISTER NEW SALE"),
        dbc.ModalBody(children=[
            dcc.Dropdown(id="customers_dropdown", className="py-2", searchable=True, placeholder="Select a customer..."),
            dcc.Dropdown(id="products_dropdown", className="py-2", searchable=True, placeholder="Select a product..."),
            dbc.InputGroup([
                dbc.Input(type="number", id="product_quantity", placeholder="Quantity"),
                dbc.Button("Show Price", id="calc_price", color="danger")
            ], className="py-2"),
            html.Div(
                [html.H4("Price: ", className="py-2 fw-bold fs-4", ),
                 html.H4(id="price_of_sale", className="py-2 fw-bold fs-4")]
            ),
            dcc.DatePickerSingle(id='date-to-deliver', date=datetime.now(), className="py-2",
                                 min_date_allowed=datetime.now(), display_format="DD\/MM\/YYYY"),
            dbc.InputGroup([
                dbc.InputGroupAddon(html.I(className="fas fa-map-marker-alt fa-2x text-danger"), addon_type="prepend",
                                    className="pt-3 pr-1"),
                dbc.Input(placeholder="Address", id="address")
            ], className="py-2"),


        ]),
        dbc.ModalFooter(children=[html.P(id="new-sale-status", className="text-danger"), new_sale_save, new_sale_close])
    ],
    backdrop="static",
    scrollable=True,
    id="modal_new_sale"
)

layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                add_new_item_button,
                                add_new_item_modal,
                            ],
                            className="text-center",
                            xs=4,
                        ),
                        dbc.Col(
                            [
                                modify_item_button,
                                modify_item_modal,
                            ],
                            className="text-center",
                            xs=4,
                        ),
                        dbc.Col(
                            [
                                new_sale_button,
                                new_sale_modal,
                            ],
                            className="text-center",
                            xs=4,
                        ),
                        dbc.Col(html.H1("Products", className="text-white text-center"), xs=12),
                        search_bar
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Row(className="px-3", id="card-group-area", justify="between"),
                        dcc.Interval(id='cards-update', interval=10 * 1000, n_intervals=0)
                    ],
                    className="my-4"
                ),
                dbc.Row([
                    dbc.Col(html.H1("Sales", className="text-white text-center"), xs=12),
                    dbc.Col([
                            dt.DataTable(
                                id="sales-datatable",
                                columns=[
                                    {'name':'ID', 'id':'id'},
                                    {'name':'Customer ID', 'id':'customer_id'},
                                    {'name':'Address', 'id':'address'},
                                    {'name':'Time registered', 'id':'time_created'},
                                    {'name': 'Date to Deliver', 'id': 'date_to_deliver'},
                                    {'name':'Total Sales Amount €', 'id':'sale_amount'},
                                    {'name':'Total Sales Amount Paid €', 'id':'sale_amount_paid'},
                                ],
                                style_cell={
                                     'textAlign': 'center',
                                     'backgroundColor': 'rgb(50, 50, 50)',
                                     'color': 'white'
                                },
                                style_as_list_view=True,
                                style_header={'backgroundColor': '#313131'},
                                style_data_conditional=[
                                    {
                                         'if': {'row_index': 'odd'},
                                         'backgroundColor': '#646464'
                                    }
                                ],
                            ),
                            dcc.Interval(id='update', interval=1000 * 1000, n_intervals=0),
                    ], xs=12, className="mb-5")
                ])
            ]
        )
    ],
)

@app.callback(Output("sales-datatable", "data"), Input("update", "n_intervals"))
def client_table_update(n):
    con = sql.connect(DATABASE)
    # Load the data into a DataFrame
    df = pd.read_sql_query("SELECT * from Sale", con)
    con.close()
    return df.to_dict('records')


def populate_products_card():
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()

    rows = get_all_products(cursor, connection)

    cards = []
    for row in rows:
        # parsing elements of each row
        name = row[1]
        price = row[2]
        unit = row[3]
        stock = row[5]
        active = row[6]
        url = "../{}".format(row[7])
        description = row[8]

        # if its not active for sale
        if active == "yes" and stock > 0:
            card = html.Div([dbc.Card(
                [
                    dbc.CardImg(src=url, top=True, className="img-fluid"),
                    dbc.CardBody(
                        [
                            html.H3(name, className="card-title text-uppercase fw-bold"),
                            html.P(description, className="card-text"),
                            html.H5("Price: {} €".format(price), className="card-text"),
                            html.H5("In stock: {} {}".format(stock, unit), className="card-text"),
                        ]
                    )
                ], className="grow"
            )], className="col-12 col-md-4 col-lg-3 py-3")
        elif active == 'yes' and stock == 0:
            card = html.Div([dbc.Card(
                [
                    dbc.CardImg(src=url, top=True, className="img-fluid"),
                    dbc.CardBody(
                        [
                            html.H3("{} (out of stock)".format(name), className="card-title text-uppercase fw-bold"),
                            html.P(description, className="card-text"),
                            html.H5("Price: {} €".format(price), className="card-text"),
                            html.H5("In stock: {} {}".format(stock, unit), className="card-text"),
                        ]
                    )
                ],
                className="disabled grow",
            )], className="col-12 col-md-4 col-lg-3 py-3")
        else:
            card = html.Div([dbc.Card(
                [
                    dbc.CardImg(src=url, top=True, className="img-fluid",),
                    dbc.CardBody(
                        [
                            html.H3("{} (not for sale)".format(name), className="card-title text-uppercase fw-bold"),
                            html.P(description, className="card-text"),
                            html.H5("Price: {} €".format(price), className="card-text"),
                            html.H5("In stock: {} {}".format(stock, unit), className="card-text"),
                        ]
                    )
                ],
                className="disabled grow"
            )], className="col-12 col-md-4 col-lg-3 py-3")

        cards.append(card)

    return cards


@app.callback(
    Output("card-group-area", "children"),
    [Input("cards-update", "n_intervals")]
)
def populate_cards(_):
    return populate_products_card()


@app.callback(Output("add-new-status", "children"),
              [
                  Input("save_new_item_button", "n_clicks"),
                  Input("name-row", "value"),
                  Input("description-row", "value"),
                  Input("price-row", "value"),
                  Input("unit-row", "value"),
                  Input("limited-row", "value"),
                  Input("stock-row", "value"),
                  Input("active-row", "value"),
                  Input("new_item_uploader", "isCompleted"),
              ],
              State("new_item_uploader", "fileNames")
              )
def add_new_item(n, name, desc, price, unit, limited, stock, active, isCompleted, filename):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    if n:
        if name is None or len(name) > 20:
            return "Enter a correct name."
        if desc is None:
            return "Enter a correct description."
        if price is None or price <= 0:
            return "Enter a number bigger than 0 in price field."
        if unit is None:
            return "Enter a correct Basic Unit."
        if limited is None or limited != "yes" and limited != "no":
            return "Enter 'yes' or 'no' in limited field."
        if stock is None or stock < 0:
            return "Enter a number equal or bigger than 0 in stock field."
        if active is None or active != "yes" and active != "no":
            return "Enter 'yes' or 'no' in active field."
        if not isCompleted:
            return "Wait until file is uploaded."
        if filename is None:
            return "No file uploaded yet."
        else:

            filename = "static/img/{}".format(filename[0])
            for (dirpath, dirnames, filenames) in os.walk('./static/img/'):
                print(dirpath, dirnames, filenames)
                print('--------')
            add_product(cursor, connection, name, price, unit, limited, stock, active, filename, desc)
            print("added")
            return "Added successfully"


@app.callback(
    Output("modal_add_new", "is_open"),
    [Input("add_new_item_btn", "n_clicks"), Input("close_modal_add_new", "n_clicks")],
    [State("modal_add_new", "is_open")],
)
def toggle_modal_new_item(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal_modify", "is_open"),
    [Input("modify_item_btn", "n_clicks"), Input("close_modal_modify", "n_clicks")],
    [State("modal_modify", "is_open")],
)
def toggle_modal_modify(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal_new_sale", "is_open"),
    [Input("new_sale_button", "n_clicks"), Input("new_sale_close", "n_clicks")],
    [State("modal_new_sale", "is_open")],
)
def toggle_model_new_sale(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("products_dropdown", "options"),
    Output("customers_dropdown", "options"),
    [Input("new_sale_button", "n_clicks")]
)
def populate_products_list(n):
    products_options = []
    customers_options = []
    if n:
        # CONNECT TO SQLITE3 DATABASE
        connection = sql.connect(DATABASE)
        cursor = connection.cursor()
        products = get_products_list(cursor, connection)
        customers = get_customers_list(cursor, connection)
        for product in products:
            products_options.append({"label": product[0], "value": product[0]})
        for customer in customers:
            customers_options.append({"label": customer[0], "value": customer[0]})
        return products_options, customers_options
    raise PreventUpdate


@app.callback(
    Output("price_of_sale", "children"),
    [
        Input("products_dropdown", "value"),
        Input("product_quantity", "value"),
        Input("calc_price", "n_clicks")
    ]
)
def calculate_sale_amount(name, quantity, calc):
    if calc:
        if name is not None:
            if quantity is not None and quantity > 0:
                # CONNECT TO SQLITE3 DATABASE
                connection = sql.connect(DATABASE)
                cursor = connection.cursor()
                price = get_product_price(cursor, connection, name)
                print(price)
                total_cost = price[0] * quantity
                print(total_cost)
                return "{} €".format(total_cost)
            return "Error - Quantity must be bigger than 0"
        return "Error - Must choose a product"
    return


@app.callback(
    Output("new-sale-status", "children"),
    [
          Input("new_sale_save", "n_clicks"),
          Input("products_dropdown", "value"),
          Input("product_quantity", "value"),
          Input("date-to-deliver", "date"),
          Input("address", "value"),
          Input("customers_dropdown", "value")
    ]
)
def register_sale(n, product, quantity, date_value, address, customer):
    # TODO Implement a way to register multi products for a single sale
    if n:
        # CONNECT TO SQLITE3 DATABASE
        connection = sql.connect(DATABASE)
        cursor = connection.cursor()
        if customer is None:
            return "Select a customer."
        elif product is None:
            return "Select a product."
        elif quantity is None or quantity <= 0:
            return "Enter a valid quantity."
        elif date_value is None:
            return "Pick a date"
        elif address is None:
            return "Enter an address."
        else:
            current_stock = get_product_stock(cursor, connection, product)[0]
            if current_stock - quantity < 0:
                return "Not enough {} in stock.".format(product)

            date_obj = date.fromisoformat(date_value)
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            date_picked = date_obj.strftime("%d/%m/%Y")
            price = get_product_price(cursor, connection, product)[0]
            sale_amount = price * quantity
            customer_id = get_customer_id(cursor, connection, customer)[0]

            print("CURRENT TIME = {} | DATE PICKED = {}".format(current_time, date_picked))
            print("SALE AMOUNT = {}".format(sale_amount))
            print("CUSTOMER ID = {}".format(customer_id))
            print("ADDRESS = {}".format(address))
            print("PRICE = {}".format(price))
            print("QUANTITY = {}".format(quantity))
            print(type(price))

            register_sale_sql(cursor, connection, current_time, date_picked, sale_amount, sale_amount, customer_id, address)
            sale_id = get_sale_id(cursor, connection, current_time)[0]
            product_id = get_product_id(cursor, connection, product)[0]
            register_sale_item(cursor, connection, quantity, price, sale_amount, sale_id, product_id)
            set_sale_status(cursor, connection, "Processing")
            update_customer_sale_amount(cursor, connection, customer_id, sale_amount)
            update_product_stock(cursor, connection, product_id, product, quantity)
            return
    return