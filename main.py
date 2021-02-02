import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# connect to main app.py file
from app import app
from app import server

# connect to app pages
from apps import shop, dashboard, error

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
                                    "Bem-vindo À DashBoard da LxPyro",
                                    className="lead text-white text-center mt-2"
                                ),
                                dbc.Nav(
                                    [
                                        dbc.NavLink("HOME", href="/", active="True", className="grow text-white text-center fs-3 pb-4"),
                                        dbc.NavLink("DASHBOARD", href="/apps/dashboard", active="True", className="grow text-white text-center fs-3 fw-bold py-4"),
                                        dbc.NavLink("LOJA", href="/apps/shop", active="True", className="grow text-white text-center fs-3 fw-bold py-4"),
                                    ],
                                    vertical=True,
                                    className="mt-5"
                                ),
                            ],
                            md=12,
                            className='pt-4'
                        )
                    ]
                )
            ],
            fluid=False,

        )

    ],
    id='main-sidebar'
)


content = html.Div(
    [
        dbc.Container(
            [
                html.H1('LXPYRO WEB APP', className="title text-center text-white pt-3"),
                html.H4('NO PYRO, NO PARTY', className="subtitle text-center text-white"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='main-sales',
                                    figure={
                                        'layout': go.Layout(
                                            paper_bgcolor = 'rgba(0,0,0,0)',
                                            plot_bgcolor = 'rgba(0,0,0,0)'
                                        )
                                    }
                                )
                            ],
                            md=6, xs=12
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='main-products',
                                    figure={
                                        'layout': go.Layout(
                                            paper_bgcolor = 'rgba(0,0,0,0)',
                                            plot_bgcolor = 'rgba(0,0,0,0)'
                                        )
                                    }
                                )
                            ],
                            md=6, xs=12
                        )
                    ],
                    className="px-3"
                )
            ],
            fluid=True,
        )
    ],
    id='main-content'
)

app.layout = html.Div(
    className="container-fluid",
    children = [
        html.Div(
            children= [
                html.Div(
                    className = "col-lg-2 left-panel bg-semi-dark",
                    children = [
                        sidebar,
                    ]
                ),

                html.Div(
                    className = "col-lg-10 right-panel bg-dark",
                    children = [],
                    id='page-content'
                )
            ],
            className="row",

        ),
        dcc.Location(id="url"),
    ]
)


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/apps/shop':
        return shop.layout
    elif pathname == '/apps/dashboard':
        return dashboard.layout
    elif pathname =='/':
        return content
    else:
        return error.layout


if __name__ == '__main__':
    app.run_server(debug=True)
