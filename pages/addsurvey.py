from dash import html
from dash import dcc, ctx, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from nav import navigation
import dash
from pymongo import MongoClient
from database import mongodb_config,mongodb_utility
import json
import pandas as pd
import uuid
import certifi

dash.register_page(__name__,path='/addsurvey',title="Add Survey")

breadcrumb=dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Breadcrumb(
                items=[
                    {"label": "Home", "href": "/", "external_link": False},
                    {"label": "Admin", "href": "/admin",},
                    {"label": "Add Survey", "active": True},
                ],
            )
        )
    ),
    fluid=True
)


client_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.DropdownMenu(
                children=[], 
                style ={"width":"100%", "text-align": "center"}, 
                id="input-addsurvey-client-name-dd",
                direction="start",
                label="Client"),
                dbc.Input(id="input-addsurvey-client-name-textbox", placeholder="Select Client"),
            ]
        ),
    ],
    className="mb-3",
)],
fluid=False)

domain_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.DropdownMenu(
                children=[], 
                style ={"width":"100%", "text-align": "center"}, 
                id="input-addsurvey-domain-name-dd",
                direction="start",
                label="Domain"),
                dbc.Input(id="input-addsurvey-domain-name-textbox", placeholder="Select Domain"),
            ]
        ),
    ],
    className="mb-3",
)],
fluid=False)

pillar_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.DropdownMenu(
                children=[], 
                id="input-addsurvey-pillar-name-dd",
                direction="start",
                label="Pillar"),
                dbc.Input(id="input-addsurvey-pillar-name-textbox", placeholder="Select Pillar"),
            ]
        ),
    ],
    className="mb-3",
)],
fluid=False)

lever_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.DropdownMenu(
                children=[], 
                id="input-addsurvey-lever-name-dd",
                direction="start",
                label="Lever"),
                dbc.Input(id="input-addsurvey-lever-name-textbox", placeholder="Select Lever"),
            ]
        ),
    ],
    className="mb-3",
)],
fluid=False)


variables_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.DropdownMenu( 
                children=[], 
                id="input-addsurvey-variable-name-dd",
                direction="start",
                label="Variable"),
                dbc.Input(id="input-addsurvey-variable-name-textbox", placeholder="Select Variable"),
            ]
        ),
    ],
    className="mb-3",
)],
fluid=False)

submit_btn_input = dbc.Container([
    dbc.Row(
    [
        dbc.Col([
            dbc.Button("Show Questions", color="danger",id="input-addsurvey-submit-btn")
        ],
        width={"offset": 5})
    ],
    className="mb-3",
)],
fluid=True)

add_survey_btn_input = dbc.Container([
    dbc.Row(
    [
        dbc.Col([
            dbc.Button("Create Survey", color="danger",id="input-addsurvey-addsurvey-btn",style={'display':'none'})
        ],
        width={"offset": 5})
    ],
    className="mb-3",
)],
fluid=True)

form = dbc.Card([
    dbc.CardHeader("FILTER QUESTIONS"),
    dbc.CardBody(
        [
           dbc.Form(
        [
            dbc.Row([
                    dbc.Col([
                        client_input
                    ]),
                    dbc.Col([
                        domain_input
                    ]),
                    dbc.Col([
                        #pillar_input
                    ]),
                   
            ]),
            dbc.Row([
                    dbc.Col([
                        #lever_input
                    ]),
                    dbc.Col([
                        #variables_input
                    ]),
                    dbc.Col([
                        html.Br()
                    ]),
                   
                   
            ]),
           
        ],
        id="input-addsurvey-main-form"),
        submit_btn_input
            
        ]
    ),
],
outline=False,
color="Gainsboro" , 
#inverse=True,
#style={"width": "115rem"},
)

add_survey_layout_main = dbc.Container([
    dbc.Row([
        dbc.Col([
            form
        ])
    ]),
],
fluid=True)

save_as_survey_toast = html.Div(
                            id="save-as-survey-toast-div",
                            children=[
                               dbc.Modal(
                                    [
                                        dbc.ModalHeader(
                                            dbc.ModalTitle("Success"), close_button=False
                                        ),
                                        dbc.ModalBody(
                                            "Survey created successfully."
                                        ),
                                        dbc.ModalFooter(dbc.Button("OK",href="/admin")),
                                    ],
                                    id="save-as-survey-toast",
                                    keyboard=False,
                                    backdrop="static",
                                    centered=True,
                                    is_open=False
                                ),
                            ]
                        )

layout = html.Div(children=[
    navigation.navbar,
    breadcrumb,
    add_survey_layout_main,
    html.Br(),
    html.Div(id="addsurvey-question-table-div",children=[]),
    html.Br(),
    add_survey_btn_input,
    save_as_survey_toast,
    html.Div(id='dummy_div1'),
],
className="add-survey-page-main-div")

## Callback to update the dynamic dropdowns
@dash.callback(
    [
        Output("input-addsurvey-client-name-dd", "children"),
        Output("input-addsurvey-domain-name-dd", "children"),
        #Output("input-addsurvey-pillar-name-dd", "children"),
        #Output("input-addsurvey-lever-name-dd", "children"),
        #Output("input-addsurvey-variable-name-dd", "children"),
    ],
    [
        Input('dummy_div1', 'children')
    ]
)
def update_dynamic_dropdowns(n_modla_submit):
    client_name_list,domain_name_list,pillar_name_list,lever_name_list,variables_name_list = mongodb_utility.get_distinct("client_dtl")
    client_name_list = [" "] + client_name_list
    domain_name_list = [" "] + domain_name_list
    pillar_name_list = [" "] + pillar_name_list
    lever_name_list = [" "] + lever_name_list
    variables_name_list = [" "] + variables_name_list
    client_name_dd_items =[dbc.DropdownMenuItem("Select Client")] + [dbc.DropdownMenuItem(divider=True)]  + [dbc.DropdownMenuItem(client, id={"type":"dynamic-survey-client", "identifier":client}) for client in client_name_list]
    domain_name_dd_items =[dbc.DropdownMenuItem("Select Domain")] + [dbc.DropdownMenuItem(divider=True)]  + [dbc.DropdownMenuItem(domain, id={"type":"dynamic-survey-domain", "identifier":domain}) for domain in domain_name_list]
    pillar_name_dd_items =[dbc.DropdownMenuItem("Select Pillar")] + [dbc.DropdownMenuItem(divider=True)]  + [dbc.DropdownMenuItem(pillar, id={"type":"dynamic-survey-pillar", "identifier":pillar}) for pillar in pillar_name_list]
    lever_name_dd_items =[dbc.DropdownMenuItem("Select Lever")] + [dbc.DropdownMenuItem(divider=True)]  +  [dbc.DropdownMenuItem(lever, id={"type":"dynamic-survey-lever", "identifier":lever}) for lever in lever_name_list]
    variables_name_dd_items =[dbc.DropdownMenuItem("Select Variable")] + [dbc.DropdownMenuItem(divider=True)]  +  [dbc.DropdownMenuItem(variable, id={"type":"dynamic-survey-variable", "identifier":variable}) for variable in variables_name_list]
    return [client_name_dd_items,
            domain_name_dd_items,
            #pillar_name_dd_items,
            #lever_name_dd_items,
            #variables_name_dd_items
            ]



## Callback to handle the client name dropdown
@dash.callback(
    Output("input-addsurvey-client-name-textbox", "value"),
    [
        Input({"type": "dynamic-survey-client", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])



## Callback to handle the domain name dropdown
@dash.callback(
    Output("input-addsurvey-domain-name-textbox", "value"),
    [
        Input({"type": "dynamic-survey-domain", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])


## Callback to handle the pillar name dropdown
# @dash.callback(
#     Output("input-addsurvey-pillar-name-textbox", "value"),
#     [
#         Input({"type": "dynamic-survey-pillar", "identifier": ALL}, "n_clicks"),
#     ],
#     prevent_initial_call=True
# )
# def on_button_click(n):
#     ctx = dash.callback_context
#     return str(ctx.triggered_id["identifier"])


## Callback to handle the lever name dropdown
# @dash.callback(
#     Output("input-addsurvey-lever-name-textbox", "value"),
#     [
#         Input({"type": "dynamic-survey-lever", "identifier": ALL}, "n_clicks"),
#     ],
#     prevent_initial_call=True
# )
# def on_button_click(n):
#     ctx = dash.callback_context
#     return str(ctx.triggered_id["identifier"])


## Callback to handle the variable name dropdown
# @dash.callback(
#     Output("input-addsurvey-variable-name-textbox", "value"),
#     [
#         Input({"type": "dynamic-survey-variable", "identifier": ALL}, "n_clicks"),
#     ],
#     prevent_initial_call=True
# )
# def on_button_click(n):
#     ctx = dash.callback_context
#     return str(ctx.triggered_id["identifier"])


## Callback to show the dash table
@dash.callback(
    [Output("addsurvey-question-table-div", "children"),
    Output("input-addsurvey-addsurvey-btn", "style"),],
    [
        Input("input-addsurvey-submit-btn", "n_clicks"),
    ],
    [
        State("input-addsurvey-client-name-textbox", "value"),
        State("input-addsurvey-domain-name-textbox", "value"),
        #State("input-addsurvey-pillar-name-textbox", "value"),
        #State("input-addsurvey-lever-name-textbox", "value"),
        #State("input-addsurvey-variable-name-textbox", "value"),
    ],
    prevent_initial_call=True
)
def render_questions_table(n,client_dd_val,domain_dd_val):
    return_div = []
    if n:
        table_data = mongodb_utility.get_survey_questions("questions",client_dd_val,domain_dd_val)
        return_div = dbc.Container([
            dbc.Row([
                dash_table.DataTable(
                    id='input-addsurvey-questions-datatable',
                    data=table_data,
                    editable=False,
                    #filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                    style_table={'overflowX': 'auto'},
                    style_data={'whiteSpace': 'normal','height': 'auto'},
                    style_cell={
                        'height': 'auto',
                        'whiteSpace': 'normal',
                        'textAlign': 'left'
                    },
                    style_header={
                        'backgroundColor': 'black',
                        'fontWeight': 'bold',
                        'color': 'white',
                    },
                ),
            ])
        ],
        fluid=True)
    return [return_div,{'display':'block'}]


## Callback to get selected question in the dash table
@dash.callback(
    Output("save-as-survey-toast", "is_open"),
    [
        Input('input-addsurvey-addsurvey-btn', "n_clicks"),
        State("input-addsurvey-questions-datatable", "derived_virtual_data"),
        State('input-addsurvey-questions-datatable', "derived_virtual_selected_rows")
    ],
    prevent_initial_call=True
)
def show_selected_questions(n,rows,selected_rows_index):
    #print(selected_rows_index)
    if n:
        #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
        client = mongodb_utility.connect_to_mongodb(mongodb_config.conn_str)
        #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
        db = client["esg"]
        collection = db["survey_dtl"]
        survey_unique_id = str(uuid.uuid4())
        for sr in selected_rows_index:
            current_survey_question = rows[sr]
            current_survey_question['survey_unique_id'] = survey_unique_id
            current_survey_question['status'] = "Active"
            collection.insert_one(current_survey_question)
        return [True]