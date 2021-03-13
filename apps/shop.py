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
    children=[html.I(className="fas fa-plus text-white"), " New Item"]
)

# MODAL FORM INPUT
name_input = dbc.FormGroup(
    [
        dbc.Label("Name", html_for="name-row", width=2),
        dbc.Col(dbc.Input(type="text", id="name-row", placeholder="Enter name"),width=10)
    ], row=True,
)

description_input = dbc.FormGroup(
    [
        dbc.Label("Description", html_for="description-row", width=3),
        dbc.Col(dbc.Textarea(id="description-row", placeholder="Enter description"), width=9)
    ], row=True,
)

price_input = dbc.FormGroup(
    [
        dbc.Label("Price per Unit", html_for="price-row", width=4),
        dbc.Col(dbc.Input(type="number", id="price-row", placeholder="Enter price"), width=8)
    ], row=True,
)

unit_input = dbc.FormGroup(
    [
        dbc.Label("Basic Unit", html_for="unit-row", width=2),
        dbc.Col(dbc.Input(type="text", id="unit-row", placeholder="Enter unit"), width=10)
    ], row=True,
)

limited_input = dbc.FormGroup(
    [
        dbc.Label("Limited", html_for="limited-row", width=2),
        dbc.Col(dbc.Input(type="text", id="limited-row", placeholder="Enter 'yes' or 'no'"), width=10)
    ], row=True,
)

stock_input = dbc.FormGroup(
    [
        dbc.Label("In stock", html_for="stock-row", width=3),
        dbc.Col(dbc.Input(type="number", id="stock-row", placeholder="Enter stock"), width=9)
    ], row=True,
)

active_input = dbc.FormGroup(
    [
        dbc.Label("Active for sale", html_for="active-row", width=3),
        dbc.Col(dbc.Input(type="text", id="active-row", placeholder="Enter 'yes' or 'no'"), width=9)
    ]
)

image_upload = du.Upload(id='new_item_uploader', filetypes=['png', 'jpg', 'jpeg', 'gif'])

save_button = dbc.Button("Add", id="save_new_item_button", className="btn btn-danger", type="button")

close_button_add_new = dbc.Button("Close", id="close_modal_add_new", className="btn btn-outline-danger")

category_input = dbc.FormGroup(
    [
        dbc.Label("Category", html_for="category-row", width=3),
        dbc.Col(dcc.Dropdown(id="category-row", className="py-2"), width=9)
    ], row=True,
)

add_new_item_modal = dbc.Modal(
    [
        dbc.ModalHeader("ADD NEW ITEM TO THE STORE"),
        dbc.ModalBody(
            [
                name_input, category_input, description_input, price_input, unit_input,
                limited_input, stock_input, active_input, image_upload
            ],
        ),
        dbc.ModalFooter(
            [
                html.Div(id="add-new-status", className="pt-3"),
                save_button,
                close_button_add_new
            ]
        )
    ], backdrop="static", scrollable=True, id="modal_add_new"
)

########################################################################################################################
modify_item_button = dbc.Button(
    id="modify_item_btn",
    type="button",
    className="btn btn-danger m-5",
    children=[html.I(className="fas fa-tools text-white"), " Modify Item"]
)
close_button_modify = dbc.Button("Close", id="close_modal_modify", className="btn btn-outline-danger", type="button")
save_button_modify = dbc.Button("Save", id="save_modal_modify", className="btn btn-danger", type="button")
choose_item = dbc.FormGroup([dbc.Label("Choose the item:", width=5),
                             dbc.Col(dcc.Dropdown(id="choose-item-dp", className="pt-2", clearable=False), width=7)],
                            row=True)
edit_name = dbc.FormGroup([dbc.Label("Name", html_for="name-edit", width=2),
                           dbc.Col(dbc.Input(type="text", id="name-edit"), width=10)], row=True)
edit_price_per_unit = dbc.FormGroup([dbc.Label("Price per unit", html_for="price-per-unit-edit", width=5),
                           dbc.Col(dbc.Input(type="number", id="price-per-unit-edit"), width=7)], row=True)
edit_basic_unit = dbc.FormGroup([dbc.Label("Basic Unit", html_for="basic-unit-edit", width=3),
                           dbc.Col(dbc.Input(type="text", id="basic-unit-edit"), width=9)], row=True)
edit_limited = dbc.FormGroup([dbc.Label("Limited", html_for="limited-edit", width=2),
                           dbc.Col(dbc.Input(type="text", id="limited-edit", placeholder="Enter 'yes' or 'no'"),
                                   width=10)], row=True)
edit_active_for_sale = dbc.FormGroup([dbc.Label("Active for sale", html_for="active-for-sale-edit", width=5),
                           dbc.Col(dbc.Input(type="text", id="active-for-sale-edit", placeholder="Enter 'yes' or 'no'"),
                                   width=7)], row=True)
image_upload_edit = du.Upload(id='edit_item_uploader', filetypes=['png', 'jpg', 'jpeg', 'gif'],
                              text="Drag and Drop Here to Change Image!")
edit_description = dbc.FormGroup([dbc.Label("Description", html_for="description-edit", width=3),
                           dbc.Col(dbc.Input(type="text", id="description-edit"), width=9)], row=True)
modify_item_modal = dbc.Modal(
    [
        dbc.ModalHeader("MODIFY ITEM FROM THE STORE"),
        dbc.ModalBody(children=[
            choose_item,
            edit_name,
            edit_description,
            edit_price_per_unit,
            edit_basic_unit,
            edit_limited,
            edit_active_for_sale,
            image_upload_edit,
        ]),
        dbc.ModalFooter([html.Div(id="edit-item-status", className="pt-3"), save_button_modify, close_button_modify])
    ], backdrop="static", scrollable=True, id="modal_modify"
)

@app.callback(Output("edit-item-status", "children"),
               [Input("save_modal_modify", "n_clicks"),
               Input("choose-item-dp", "value"),
               Input("name-edit", "value"),
               Input("description-edit", "value"),
               Input("price-per-unit-edit", "value"),
               Input("basic-unit-edit", "value"),
               Input("limited-edit", "value"),
               Input("active-for-sale-edit", "value")],
              [State("edit_item_uploader", "fileNames")])
def save_item_modifications(save, product, name, description, price_per_unit, basic_unit,
                            limited, active_for_sale, ImageUrl):
    if save:
        # CONNECT TO SQLITE3 DATABASE
        connection = sql.connect(DATABASE)
        cursor = connection.cursor()
        if description is not None:
            update_product_description(cursor, connection, product, description)
        if price_per_unit is not None and price_per_unit > 0:
            update_product_price_per_unit(cursor, connection, product, price_per_unit)
        elif price_per_unit is not None and price_per_unit <= 0:
            return dbc.Alert("Enter a valid price!", color="warning")
        if basic_unit is not None:
            update_product_basic_unit(cursor, connection, product, basic_unit)
        if limited is not None and limited in ['yes', 'no']:
            update_product_limited(cursor, connection, product, limited)
        elif limited is not None and limited not in ['yes', 'no']:
            return dbc.Alert("Enter 'yes' or 'no'!", color="warning")
        if active_for_sale is not None and active_for_sale in ['yes', 'no']:
            update_product_active_for_sale(cursor, connection, product, active_for_sale)
        elif active_for_sale is not None and active_for_sale not in ['yes', 'no']:
            dbc.Alert("Enter 'yes' or 'no'!", color="warning")
        if ImageUrl is not None:
            update_product_ImageUrl(cursor, connection, product, ImageUrl)
        if name is not None:
            update_product_name(cursor, connection, product, name)
        return dbc.Alert("All changes where saved!", color='success')
    return
######################################################################################################
# NEW SALE MODAL
new_sale_button = dbc.Button(children=[html.I(className="fas fa-plus text-white"), " NEW SALE"], id="new_sale_button",
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
        dbc.ModalFooter(children=[html.Div(id="new-sale-status", className="pt-3"), new_sale_save, new_sale_close])
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
                        dbc.Col([add_new_item_button, add_new_item_modal], className="text-center", xs=4),
                        dbc.Col([modify_item_button, modify_item_modal], className="text-center", xs=4),
                        dbc.Col([new_sale_button, new_sale_modal], className="text-center", xs=4),
                        dbc.Col(html.H1("Products", className="text-white fw-bold title text-center"), xs=12),
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
                    dbc.Col(html.H1("Sales", className="text-white text-center title fw-bold py-4"), xs=12),
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
                                editable=False,
                                sort_action="native",
                                sort_mode="multi",
                                row_deletable=False,
                                row_selectable="multi",
                                selected_rows=[],
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
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
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
                  Input("category-row", "value"),
              ],
              State("new_item_uploader", "fileNames")
              )
def add_new_item(n, name, desc, price, unit, limited, stock, active, isCompleted, category, filename):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    if n:
        if name is None or len(name) > 20:
            return dbc.Alert("Enter a valid name", color="warning")
        if category is None:
            return dbc.Alert("Enter a valid category", color="warning")
        if desc is None:
            return dbc.Alert("Enter a valid description", color="warning")
        if price is None or price <= 0:
            return dbc.Alert("Enter a number bigger than 0 in price field", color="warning")
        if unit is None:
            return dbc.Alert("Enter a valid basic unit", color="warning")
        if limited is None or limited != "yes" and limited != "no":
            return dbc.Alert("Enter 'yes' or 'no' in limited field", color="warning")
        if stock is None or stock < 0:
            return dbc.Alert("Enter a number equal or bigger than 0 in stock field", color="warning")
        if active is None or active != "yes" and active != "no":
            return dbc.Alert("Enter 'yes' or 'no' in active field", color="warning")
        if not isCompleted:
            return dbc.Alert("Wait until file is uploaded", color="warning")
        if filename is None:
            return dbc.Alert("No file uploaded yet", color="warning")
        else:
            filename = "static/img/{}".format(filename[0])
            add_product(cursor, connection, name, price, unit, limited, stock, active, filename, desc, category)
            return dbc.Alert("Item Registered Successfully", color="success")


@app.callback(
    Output("modal_add_new", "is_open"),
    Output("category-row", "options"),
    [Input("add_new_item_btn", "n_clicks"), Input("close_modal_add_new", "n_clicks")],
    [State("modal_add_new", "is_open")],
)
def toggle_modal_new_item(n1, n2, is_open):
    if n1 or n2:
        # CONNECT TO SQLITE3 DATABASE
        connection = sql.connect(DATABASE)
        cursor = connection.cursor()
        categories = get_all_categories(cursor)
        return not is_open, categories
    return is_open, []


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
            return dbc.Alert("Select a valid customer", color="warning")
        elif product is None:
            return dbc.Alert("Select a valid product", color="warning")
        elif quantity is None or quantity <= 0:
            return dbc.Alert("Enter a valid quantity", color="warning")
        elif date_value is None:
            return dbc.Alert("Pick a valid date", color="warning")
        elif address is None:
            return dbc.Alert("Enter a valid address", color="warning")
        else:
            current_stock = get_product_stock(cursor, connection, product)[0]
            if current_stock - quantity < 0:
                return dbc.Alert("Not enough {} in stock".format(product), color="warning")
            date_obj = date.fromisoformat(date_value)
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y")
            date_picked = date_obj.strftime("%d/%m/%Y")
            price = get_product_price(cursor, connection, product)[0]
            sale_amount = price * quantity
            customer_id = get_customer_id(cursor, connection, customer)[0]
            register_sale_sql(cursor, connection, date_picked, sale_amount, sale_amount, customer_id, address)
            sale_id = get_last_sale_id(cursor)[0]
            product_id = get_product_id(cursor, connection, product)[0]
            register_sale_item(cursor, connection, quantity, price, sale_amount, sale_id, product_id)
            set_sale_status(cursor, connection, "Processing")
            update_customer_sale_amount(cursor, connection, customer_id, sale_amount)
            update_product_stock(cursor, connection, product_id, product, quantity)
            return dbc.Alert("Sale Registered Successfully", color="success")
    return


@app.callback(Output("choose-item-dp", "options"), [Input("update", "n_intervals")])
def populate_all_products_name(_):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    names = get_all_products_names(cursor)
    options = []
    for name in names:
        option = {'label': name[0], 'value': name[0]}
        options.append(option)
    return options


@app.callback(Output("name-edit", "placeholder"),
              Output("description-edit", "placeholder"),
              Output("price-per-unit-edit", "placeholder"),
              Output("basic-unit-edit", "placeholder"),
              [Input("choose-item-dp", "value")])
def populate_placeholders(product_name):
    # CONNECT TO SQLITE3 DATABASE
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    description = get_product_description(cursor, product_name)
    price_per_unit = get_product_price(cursor, connection, product_name)
    basic_unit = get_product_basic_unit(cursor, product_name)
    if price_per_unit:
        return product_name, description, "{} €".format(price_per_unit[0]), basic_unit
    return ['','','','']