import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output

import sqlite3 as sql
import pandas as pd

from app import app, DATABASE
from sql_functions import *

name_input = dbc.FormGroup(
    [
        dbc.Label("Name", html_for="name-row", width=4, className="text-dark"),
        dbc.Col(
            dbc.Input(type="text", id="name-row", placeholder="Enter name"),
            width=8,
        ),
    ],
    row=True,
)

age_input = dbc.FormGroup(
    [
        dbc.Label("Age", html_for="age-row", width=4, className="text-dark"),
        dbc.Col(
            dbc.Input(type="number", id="age-row", placeholder="Enter age"),
            width=8,
        ),
    ],
    row=True,
)

address_input = dbc.FormGroup(children=[
    dbc.Label([html.I(className="fas fa-map-marker-alt"), " Address"], html_for="address-row", width=4,
              className="text-dark"),
    dbc.Col(children=[
        dbc.Input(type="text", id="address-row", placeholder="Enter address"),
        ], width=8)
], row=True)

phone_number_input = dbc.FormGroup(children=[
    dbc.Label(children=[html.I(className="fas fa-phone-alt")], html_for="phone-number-row", width=4,
              className="text-dark text-center"),
    dbc.Col(children=[
        dbc.Input(type="number", id="phone-number-row", placeholder="Enter phone number")
    ], width=8)
], row=True)

instagram_input = dbc.FormGroup(children=[
    dbc.Label([html.I(className="fab fa-instagram text-dark"), " Instagram"], html_for="instagram-row", width=4,
              className="text-dark"),
    dbc.Col(children=[
        dbc.Input(type="text", id="instagram-row", placeholder="Enter Instagram's username")
    ], width=8)
], row=True)

title_form = html.H3("Register New Client", className="text-dark text-center text-bold py-3")

register_button = dbc.FormGroup(children=[
    dbc.Col(children=[
        dbc.Button(children=[html.I(className="fas fa-plus text-white"), " Register"],
                   className="btn btn-danger btn-block btn-lg", id="register-button"),
        html.Div(id="register-status")
    ], width=12)
], className="text-center p-3", row=True)


form = dbc.Form([title_form, name_input, phone_number_input, instagram_input,
                 age_input, address_input, register_button], id="new-client-form")

layout = html.Div(id="clients", children=[
    html.Div(className="container", children=[
        dbc.Row(children=[
            dbc.Col(children=[
                html.H1("our clients", className="text-uppercase text-white text-center fw-bold"),
                html.A([html.I(className="fas fa-plus text-white subtitle p-4")], href="/apps/clients#new-client-form"),
                html.A([html.I(className="fas fa-sync-alt text-white subtitle p-4")], href="/apps/clients"),
                html.Div(children=[
                    dt.DataTable(id="clients-datatable", columns=[
                        {'name': 'ID', 'id': 'id'},
                        {'name': 'Name', 'id': 'name'},
                        {'name': 'Instagram', 'id': 'Instagram'},
                        {'name': 'Age', 'id': 'age'},
                        {'name': 'Address', 'id': 'address'},
                        {'name': 'Phone Number', 'id': 'PhoneNumber'},
                        {'name': 'Total Sales Amount', 'id': 'sales_amount'},
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
                                 )
                ], id="table", className="py-4"),
                html.Div(children=[form], className="container my-5"),
                dcc.Interval(id='update', interval=1000 * 1000, n_intervals=0),
            ], xs=12, className="text-center")
        ], className="py-3")
    ])
])


@app.callback(Output("clients-datatable", "data"), Input("update", "n_intervals"))
def client_table_update(_):
    con = sql.connect(DATABASE)
    # Load the data into a DataFrame
    df = pd.read_sql_query("SELECT * from Customer", con)
    con.close()
    return df.to_dict('records')


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
