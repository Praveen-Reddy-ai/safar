import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

dash.register_page(__name__,path='/logout')

layout = html.Div(
    [
        dbc.Container([
            dbc.Row(dmc.Space(h="lg"),),
            dbc.Row([
                dbc.Col([
                    html.Div(html.H4("You have been logged out"),id="logout_msg"),
                ],width="auto"),
                dbc.Col([
                    dbc.Button("Please Login", size="sm", id="home_btn",href="/login"),
                ],width="auto"),
            ],justify="start")
        ])
    ]
    ,className="bg"
)