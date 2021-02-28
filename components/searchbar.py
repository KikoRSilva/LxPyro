import dash_html_components as html
import dash_bootstrap_components as dbc

# SEARCH BAR
search_bar = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(id='keyword', placeholder='Product keyword',
                                  className="text-white p-3")
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
                                {"label": "Torch", "value": "Tocha"}
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
)