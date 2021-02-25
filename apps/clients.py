import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import sqlite3 as sql
import pandas as pd

from app import app, DATABASE
from sql_functions import *

name_input = dbc.FormGroup(
    [
        dbc.Label("Name", html_for="name-row", width=2, className="text-dark"),
        dbc.Col(
            dbc.Input(type="text", id="name-row", placeholder="Enter name"),
            width=10,
        ),
    ],
    row=True,
)

age_input = dbc.FormGroup(
    [
        dbc.Label("Age", html_for="age-row", width=2, className="text-dark"),
        dbc.Col(
            dbc.Input(type="number", id="age-row", placeholder="Enter age"),
            width=10,
        ),
    ],
    row=True,
)

address_input = dbc.FormGroup(children=[
    dbc.Label([html.I(className="fas fa-map-marker-alt"), " Address"], html_for="address-row", width=2, className="text-dark"),
    dbc.Col(children=[
        dbc.Input(type="text", id="address-row", placeholder="Enter address"),
        ], width=10)
], row=True)

phone_number_input = dbc.FormGroup(children=[
    dbc.Label([html.I(className="fas fa-phone-alt"), " Number"], html_for="phone-number-row", width=2, className="text-dark"),
    dbc.Col(children=[
        dbc.Input(type="number", id="phone-number-row", placeholder="Enter phone number")
    ], width=10)
], row=True)

instagram_input = dbc.FormGroup(children=[
    dbc.Label([html.I(className="fab fa-instagram text-dark"), " Instagram"], html_for="instagram-row", width=2, className="text-dark"),
    dbc.Col(children=[
        dbc.Input(type="text", id="instagram-row", placeholder="Enter Instagram's username")
    ], width=10)
], row=True)

title_form = html.H3("Register New Client", className="text-dark text-center text-bold py-3")

register_button = dbc.FormGroup(children=[
    dbc.Col(children=[
        dbc.Button(children=[html.I(className="fas fa-plus text-white"), " Register"],
               className="btn btn-danger btn-block btn-lg", id="register-button"),
        html.Div(id="register-status")
    ], width=12)
], className="text-center pb-3", row=True)



form = dbc.Form([title_form, name_input, phone_number_input, instagram_input, age_input, address_input, register_button])

layout = html.Div(id="clients", children=[
    html.Div(className="container", children=[
        dbc.Row(children=[
            dbc.Col(children=[
                html.H1("our clients", className="text-uppercase text-white text-center fw-bold"),
                dbc.Button(children=[html.I(className="fas fa-plus text-white"), " NEW CLIENT"],
                           className="btn btn-danger my-4", href="#new-client-form"),
                html.Div(id="table", className="py-4"),
                html.Div(children=[
                    form
                ], className="container", id="new-client-form"),
                dcc.Interval(id='update', interval=1000 * 1000, n_intervals=0)
            ], xs=12, className="text-center")
        ], className="py-3")
    ])
])


@app.callback(Output("table", "children"), Input("update", "n_intervals"))
def client_table_update(n):
    con = sql.connect(DATABASE)
    # Load the data into a DataFrame
    df = pd.read_sql_query("SELECT * from Customer", con)
    df.rename({'id': 'ID', 'name': 'Name', 'age': 'Age', 'address': 'Address', 'sales_amount': 'Total Sales Amount', 'PhoneNumber': 'Phone Number'}, axis='columns', inplace=True)
    con.close()
    return dbc.Table.from_dataframe(df, striped=False, bordered=False, hover=True)

@app.callback(Output("register-status", "children"),
              [
                  Input("register-button", "n_clicks"),
                  Input("name-row", "value"),
                  Input("phone-number-row", "value"),
                  Input("instagram-row", "value"),
                  Input("age-row", "value"),
                  Input("address-row", "value")
              ])
def register_client(clicked, name, phone, insta, age, address):
    if clicked:
        # VALIDATE THE INPUTS
        if name is None:
            return dbc.Alert("Enter a valid name!", color="warning", className="my-2")
        elif phone is None:
            return dbc.Alert("Enter a valid phone number!", color="warning", className="my-2")
        elif insta is None:
            return dbc.Alert("Enter a valid Instagram's username!", color="warning", className="my-2")
        elif age is None:
            return dbc.Alert("Enter a valid age!", color="warning", className="my-2")
        elif address is None:
            return dbc.Alert("Enter a valid address!", color="warning", className="my-2")
        else:
            # CONNECT TO DATABASE
            connection = sql.connect(DATABASE)
            cursor = connection.cursor()

            add_customer(cursor, connection, name, phone, insta, age, address)
            return dbc.Alert("Client registered successfully!", color="success", className="my-2")
    return