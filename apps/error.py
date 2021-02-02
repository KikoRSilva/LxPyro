import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
    [
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-12 text-center",
                    children=[
                        html.H1(
                            '404 Error',
                            className="text-white text-center title pt-5"
                        ),
                        html.H4(
                            'Ups ... Não devias estar nesta página!',
                            className="text-white subtitle",
                        )
                    ]
                )
            ]
        )
    ]
)


