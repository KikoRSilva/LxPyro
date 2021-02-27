import dash_html_components as html
import dash_bootstrap_components as dbc

sidebar = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(src="/static/img/LxPyro.png", className="img-fluid mx-auto d-block mb-4"),
                                html.P(
                                    "Welcome to LxPyro's Web App",
                                    className="lead text-white text-center mt-2"
                                ),
                                dbc.Nav(
                                    [
                                        dbc.NavLink("HOME", href="/", active="True",
                                                    className="grow text-white text-center fs-3 pb-4"),
                                        dbc.NavLink("DASHBOARD", href="/apps/dashboard", active="True",
                                                    className="grow text-white text-center fs-3 fw-bold py-4"),
                                        dbc.NavLink("SHOP", href="/apps/shop", active="True",
                                                    className="grow text-white text-center fs-3 fw-bold py-4"),
                                        dbc.NavLink("CLIENTS", href="/apps/clients", active="True",
                                                    className="grow text-white text-center fs-3 fw-bold py-4"),
                                    ],
                                    vertical=True,
                                    className="mt-5",

                                ),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.A(
                                    children=[
                                        html.P(
                                            "@franciscomrsilva",
                                            className="text-white text-center fw-light grow creator"
                                        )
                                    ],
                                    href="https://www.instagram.com/franciscomrsilva/",
                                    target="_blank"
                                ),

                            ],
                            md=12,
                            className='pt-4'
                        ),
                        dbc.NavbarToggler(id="navbar-toggler")
                    ]
                )
            ],
            fluid=False,

        )

    ],
    id='main-sidebar'
)