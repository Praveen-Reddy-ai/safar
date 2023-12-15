from pydoc import classname
import dash_bootstrap_components as dbc
#import dash_html_components as html
from dash import html
#from app import app
from dash.dependencies import Input, Output, State
import dash
import dash_mantine_components as dmc
from flask import  session


navbar = dbc.Navbar(
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col([
                            html.Img(src=dash.get_asset_url('planet-earth.png'), height="40px"),
                            dbc.NavbarBrand("Sustainability Assessment Framework", className="ms-2")
                        ],
                        width={"size":"auto"})
                    ],
                    align="center",
                    className="g-0"),

                    dbc.Row([
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink("Home", href="/")),
                                dbc.NavItem(dbc.NavLink("My Surveys", href="/takesurvey")),
                                dbc.NavItem(dbc.NavLink("Admin", href="/admin")) ,
                                #dbc.NavItem(html.Div(id="user-status-header"))
                            ],
                            navbar=True
                            )
                        ],
                        width={"size":"auto"})
                    ],
                    align="center"),
                    dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
                    
                    dbc.Row([
                        dbc.Col(
                             dbc.Collapse(
                                dbc.Nav([
                                    dbc.NavItem(html.Div(id="user-status-header")),
                                    dmc.Space(w="lg"),
                                    dbc.NavItem( html.Img(src=dash.get_asset_url('ntt-data-logo.svg'), height="30px")),
                                    #html.Img(src=dash.get_asset_url('ntt-data-logo.svg'), height="30px")
                                ]
                                ),
                                id="navbar-collapse",
                                is_open=False,
                                navbar=True
                             )
                        )
                    ],
                    align="center")
                ],
            fluid=True
            ),
    color="DarkSlateGray",
    dark=True,
    #light=True,
)


@dash.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open