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
                            'Ups ... You are lost! Go back now!',
                            className="text-white subtitle",
                        )
                    ]
                )
            ]
        )
    ]
)
