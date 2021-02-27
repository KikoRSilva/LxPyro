import dash
import dash_bootstrap_components as dbc
import dash_uploader as du
import dash_auth as auth
from users import USERNAME_PASSWORD_PAIRS

external_stylesheets = [
    dbc.themes.MATERIA,
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://fonts.googleapis.com/css?family=Poppins',
    {
        'rel': "stylesheet",
        'href': "https://use.fontawesome.com/releases/v5.15.2/css/all.css",
        'integrity': "sha384-vSIIfh2YWi9wW0r9iZe7RJPrKwp6bG+s9QZMoITbCckVJqGCCRhc+ccxNcdpHuYu",
        'crossorigin': "anonymous"
    }
]

# CONSTANTS
DATABASE = 'data/database.db'
UPLOAD_DIRECTORY = "../static/img"

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0'
        }],
    external_stylesheets=external_stylesheets,
    title='LxPyro',
    update_title=False
    )

du.configure_upload(app, "./static/img", use_upload_id=False)

auth = auth.BasicAuth(
    app,
    USERNAME_PASSWORD_PAIRS
)

server = app.server
