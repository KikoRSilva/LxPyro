import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app


layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Container(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    id='keyword',
                                                    placeholder='Product keyword',
                                                    className="text-white p-3"
                                                )
                                            ],
                                            xs=12, sm=6, md=3,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Select(
                                                    options=[
                                                        {"label": "Petard", "value": "Petardo"},
                                                        {"label": "Strobe", "value": "Estroboscópico"},
                                                        {"label": "Smoke", "value": "Potes de Fumo"},
                                                        {"label": "Torche", "value": "Tocha"}
                                                    ],
                                                    placeholder='Categories',
                                                    id='category',
                                                    className="p-3"
                                                )
                                            ],
                                            xs=12, sm=6, md=3,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Select(
                                                    options=[
                                                        {"label": "Lowest to Highest", "value": "lowtohigh"},
                                                        {"label": "Highest to Lowest", "value": "Estroboscópico"},

                                                    ],
                                                    id='price_order',
                                                    placeholder='Price order',
                                                    className="p-3"
                                                )
                                            ],
                                            xs=12, sm=6, md=3,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Button(
                                                    [
                                                        'Search ',
                                                        html.I(className="fas fa-search text-white")
                                                    ],
                                                    className="justify-space-between btn-danger p-3 rounded text-center"
                                                )
                                            ],
                                            xs=12, sm=6, md=3,
                                            className="text-center"
                                        )
                                    ],
                                    className="g-3"
                                )
                            ],
                            className="mt-4 bg-light rounded my-2 py-1 mx-5"
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1("Our Products", className="text-white text-center"),
                            ],
                            xs=12
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardImg(src="../static/img/logoInsta.png", top=True),
                                                dbc.CardBody(
                                                    [
                                                        html.H4('C4 Small', className="card-title"),
                                                        html.P(
                                                            "Este é um petardo nao muito forte "
                                                            "mas faz muito barulho.",
                                                            className="card-text",
                                                        ),
                                                        dbc.ButtonGroup(
                                                            [
                                                                dbc.Input(placeholder="Quantity"),
                                                                dbc.Button("Buy", className="btn-danger"),
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    xs=12, sm=6, md=4, lg=3
                                )
                            ]
                        ),

                    ],
                    className="my-4"
                )
            ]
        )
    ],
)
