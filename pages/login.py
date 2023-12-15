
from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify



dash.register_page(__name__,path='/login')

email_input = dbc.Row(
    [
        dbc.Col([
             dbc.Input(
                type="text", id="uname-box", placeholder="Enter userid",size="lg"
            ),
            html.Br(),
        ],
        width=10,
        ),
    ],
    className="mb-3",
)

password_input = dbc.Row(
    [
        dbc.Col(
            dbc.Input(
                type="password",
                id="pwd-box",
                placeholder="Enter password",
                size="lg"
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

remember_forgot_input = dbc.Row(
    [
        dbc.Col(
           dbc.Checklist(
                options=[
                    {"label": "Remember me", "value": "remember_me"}
                ],
                value=[1],
                id="remember-me-checklist",
                switch=True,
            ),
            width=3,
        ),
        dbc.Col([
             dcc.Link("Forgot password?", href="/"),
             html.Br(),
             html.Br(),
        ],
         width={"size": 3, "order": "last", "offset": 5},
        ),
    ],
    className="mb-3",
    justify="start",
)

login_button = dbc.Row(
    [
        dbc.Col(
            #dbc.Button( "Login", color="primary", className="g-0", n_clicks=0, type="submit",size="lg", id="login-button"),
             dmc.Button(
                    "Login", 
                    leftIcon=[DashIconify(
                                icon="uiw:login",
                                width=20,
                                height=20,
                                #rotate=1,
                                #flip="horizontal",
                            )],
                    color="dark",
                    id="login-button",
                    loading=False,
                ),
            width="auto",
        ),
        dbc.Col([
            html.Div(children="", id="output-state", style={"color":"red"}),
        ])
    ],
    className="mb-3",
)

register_link = dbc.Row(
    [
        dbc.Col(
            html.P(html.B("Don't have an account?")),
            width="auto"
        ),
        dbc.Col([
             dcc.Link("Register", href="/register"),
        ]
        )
    ],
    className="mb-3",
)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url_login', refresh=True),
            html.Img(src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp",height="500px",width="700px"),
        ],
         align="center"),
        dbc.Col([
            dbc.Form([email_input, password_input, remember_forgot_input, login_button, register_link])
        ],
         align="end")
    ])
],
fluid=True
)