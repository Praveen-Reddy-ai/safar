
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from nav import navigation
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify


dash.register_page(__name__,path='/',title="Sustainability Assessment Framework")

layout = html.Div(
    children=[
        navigation.navbar,
        dmc.Divider(style={"marginBottom": 0, "marginTop": 0},color='gray',size='sm'),
        html.Div(
            className="homebackgroundimg",
            children=[
                dbc.Container(
                    [
                        dbc.Row([
                                html.Div(
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col([
                                                        #dmc.Space(w="lg"),
                                                        dmc.Image(src=dash.get_asset_url('Env.svg'),width=241*2.5, height=217*2.5,withPlaceholder=True),
                                                    ], lg={'size':4, 'offset': 0}, md={'size':4, 'offset': 0},sm={'size':4, 'offset': 0}),
                                                    dbc.Col([
                                                        #dmc.Space(w="lg"),
                                                        dmc.Image(src=dash.get_asset_url('Soc.svg'),width=241*2.5, height=217*2.5,withPlaceholder=True),
                                                    ], lg={'size':4, 'offset': 0}, md={'size':4, 'offset': 0},sm={'size':4, 'offset': 0}),
                                                    dbc.Col([
                                                        #dmc.Space(w="lg"),
                                                        dmc.Image(src=dash.get_asset_url('Gov.svg'),width=241*2.5, height=217*2.5,withPlaceholder=True),
                                                    ], lg={'size':4, 'offset': 0}, md={'size':4, 'offset': 0},sm={'size':4, 'offset': 0})
                                                ]),
                                            ],fluid=False),
                                        ],
                                    className="esg-logo-div"
                                ),
                        ]),
                        dbc.Row([
                                html.Div(
                                    children=[
                                        dbc.Container([
                                            dbc.Row([
                                                    dbc.Col([
                                                        dmc.Group(
                                                            position="left",
                                                           align="center",
                                                            grow=0,
                                                            children=[
                                                                dmc.Image(src=dash.get_asset_url('global-reporting-initiative-gri-logo-vector.svg'),width=652*0.1, height=652*0.1,withPlaceholder=True, alt="S&P Global"),
                                                                dmc.Image(src=dash.get_asset_url('sustainability-accounting-standards-board-sasb-vector-logo.svg'),width=50, height=50, withPlaceholder=True, alt="CDP"),
                                                                dmc.Image(src=dash.get_asset_url('tcfd.png'),width=311*0.40, height=162*0.40 , withPlaceholder=True, alt="FTSE")                                
                                                        ],
                                                    ),
                                                    dmc.Text("Based on above standards",color="black",weight=500,style={"fontSize": 12,"paddingLeft": 40},)
                                            ],align="center"),
                                            dbc.Col([
                                                        dmc.Group(
                                                            position="right",
                                                            align="center",
                                                            grow=0,
                                                            children=[
                                                            dmc.Image(src=dash.get_asset_url('Carbon_Disclosure_Project_logo.svg'),width=75, height=26, withPlaceholder=True, alt="CDP"),
                                                            dmc.Image(src=dash.get_asset_url('New_Bloomberg_Logo.svg'),width=200*0.5, height=36.6*0.5, withPlaceholder=True, alt="bloombarg"),
                                                            dmc.Image(src=dash.get_asset_url('MSCI_logo_2019.svg'),width=150*0.5, height=40*0.5, withPlaceholder=True, alt="msci"),
                                                        ],
                                                    ),
                                                    dmc.Group(
                                                            position="right",
                                                            align="center",
                                                            grow=0,
                                                            children=[
                                                            dmc.Image(src=dash.get_asset_url('sustainalytics-seeklogo.com.svg'),width=140*0.7, height=140*0.7, withPlaceholder=True, alt="sustainalytics"),
                                                            dmc.Image(src=dash.get_asset_url('s-p-global-seeklogo.com.svg'),width=100, height=100,withPlaceholder=True, alt="S&P Global"),
                                                            dmc.Image(src=dash.get_asset_url('ftse-russell-seeklogo.com.svg'),width=50*1.2, height=50*1.2, withPlaceholder=True, alt="FTSE"),
                                                        ],
                                                    ),
                                                    dmc.Text("Inspired from above rating platforms",color="black",weight=500,style={"fontSize": 12,"paddingLeft": 380},)
                                            ],align="start")
                                        ])
                                    ])
                                    ]
                                )
                        ])
                    ]
                )
            ]
        ),
    ]
    
)

# layout = html.Div(children=[
#     navigation.navbar,
#     #breadcrumb,
#     dmc.Divider(style={"marginBottom": 0, "marginTop": 0},color='gray',size='sm'),
#     #html.Div(id="user-status-header"),
#     #dmc.Divider(style={"marginBottom": 0, "marginTop": 0},color='gray',size='sm'),
#     html.Div(),
#     html.Div(children=[
#          html.Div(
#             children=[
#                 dbc.Container([
#                     dbc.Row([
#                         dmc.Space(h="lg"),
#                     ]),
#                     dbc.Row([
#                         dmc.Space(h="lg"),
#                     ]),
#                     dbc.Row([
#                         dbc.Col([
#                             dmc.Space(w="lg"),
#                             dmc.Image(src=dash.get_asset_url('Env.svg'),width=241*2.5, height=217*2.5,withPlaceholder=True),
#                         ], lg={'size':4, 'offset': 0}, md={'size':4, 'offset': 0},sm={'size':4, 'offset': 0}),
#                         dbc.Col([
#                             dmc.Space(w="lg"),
#                             dmc.Image(src=dash.get_asset_url('Soc.svg'),width=241*2.5, height=217*2.5,withPlaceholder=True),
#                         ], lg={'size':4, 'offset': 0}, md={'size':4, 'offset': 0},sm={'size':4, 'offset': 0}),
#                         dbc.Col([
#                             dmc.Space(w="lg"),
#                             dmc.Image(src=dash.get_asset_url('Gov.svg'),width=241*2.5, height=217*2.5,withPlaceholder=True),
#                         ], lg={'size':4, 'offset': 0}, md={'size':4, 'offset': 0},sm={'size':4, 'offset': 0})
#                     ]),
#                 ],fluid=False),
#             ],
#         className="esg-logo-div"
#         ),
#     # html.Div(
#     #     children=[
#     #         dbc.Container([
#     #             # dbc.Row([
#     #             #     dmc.Space(h="lg"),
#     #             # ])
#     #             #dbc.Row([
#     #             #    dbc.Col([
#     #             #        dmc.Text(
#     #             #            "Framework is based on the following standard:",
#     #                         #cite="- Ironman",
#     #                         #icon=[DashIconify(icon="ooui:references-ltr", width=30)],
#     #             #            color="blue",
#     #             #        )
#     #             #    ],width="auto")
#     #             #],justify='center')
#     #         ])
#     #     ]
#     # ),
#     html.Div(
#         children=[
#             dbc.Container([
#                 dbc.Row([
#                         dbc.Col([
#                             dmc.Group(
#                                 position="left",
#                                 #align="end",
#                                 grow=0,
#                                 children=[
#                                     dmc.Image(src=dash.get_asset_url('global-reporting-initiative-gri-logo-vector.svg'),width=652*0.1, height=652*0.1,withPlaceholder=True, alt="S&P Global"),
#                                     dmc.Image(src=dash.get_asset_url('sustainability-accounting-standards-board-sasb-vector-logo.svg'),width=50, height=50, withPlaceholder=True, alt="CDP"),
#                                     dmc.Image(src=dash.get_asset_url('tcfd.png'),width=311*0.40, height=162*0.40 , withPlaceholder=True, alt="FTSE")                                
#                             ],
#                         ),
#                 ]),
#                 dbc.Col([
#                             dmc.Group(
#                                 position="right",
#                                 align="end",
#                                 grow=0,
#                                 children=[
#                                 dmc.Image(src=dash.get_asset_url('Carbon_Disclosure_Project_logo.svg'),width=75, height=26, withPlaceholder=True, alt="CDP"),
#                                 dmc.Image(src=dash.get_asset_url('New_Bloomberg_Logo.svg'),width=200*0.5, height=36.6*0.5, withPlaceholder=True, alt="bloombarg"),
#                                 dmc.Image(src=dash.get_asset_url('MSCI_logo_2019.svg'),width=150*0.5, height=40*0.5, withPlaceholder=True, alt="msci"),
#                                 dmc.Image(src=dash.get_asset_url('sustainalytics-seeklogo.com.svg'),width=140*0.5, height=140*0.5, withPlaceholder=True, alt="sustainalytics"),
#                                 dmc.Image(src=dash.get_asset_url('s-p-global-seeklogo.com.svg'),width=100, height=100,withPlaceholder=True, alt="S&P Global"),
#                                 dmc.Image(src=dash.get_asset_url('ftse-russell-seeklogo.com.svg'),width=50, height=50, withPlaceholder=True, alt="FTSE"),
#                             ],
#                         ),
#                 ])
#             ])
#         ])
#         ]
#     )
#     ],
#     className="home-top-image")
   
# ],

# )
