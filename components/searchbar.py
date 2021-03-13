import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

# SEARCH BAR
search_bar = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(id='keyword', placeholder='Product keyword',
                                  className="text-dark p-3")
                    ],
                    xs=12, sm=6, md=3,
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            placeholder='Categories',
                            id='category',
                            className="p-3"
                        )
                    ],
                    xs=12, sm=6, md=3,
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
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
                            className="justify-space-between btn-danger rounded text-center"
                        )
                    ],
                    xs=12, sm=6, md=3,
                    className="text-center p-3"
                )
            ],
            className="g-3"
        )
    ],
    className="mt-4 bg-light rounded my-2 py-1 mx-5"
)
