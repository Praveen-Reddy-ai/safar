from dash import html
from dash import dcc, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from nav import navigation
import dash
from pymongo import MongoClient
from database import mongodb_config
import json
import certifi
from database import mongodb_utility

dash.register_page(__name__,path='/addclient',title="Add Client")

breadcrumb=dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Breadcrumb(
                items=[
                    {"label": "Home", "href": "/", "external_link": False},
                    {"label": "Admin", "href": "/admin",},
                    {"label": "Add Client", "active": True},
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
                dbc.InputGroupText("Client Name"),
                dbc.Input(id="input-addclient-client-name", placeholder="Enter client Name"),
            ]
        )
    ],
    className="mb-3",
)],
fluid=False)

domain_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupText("Domain Name"),
                dbc.Input(id="input-addclient-domain-name", placeholder="Enter domain Name"),
            ]
        )
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
                [
                    dbc.DropdownMenuItem("Environment", id="input-addclient-pillar-name-dd-item-env"),
                    dbc.DropdownMenuItem("Social", id="input-addclient-pillar-name-dd-item-soc"),
                    dbc.DropdownMenuItem("Governance", id="input-addclient-pillar-name-dd-item-gov")
                ], 
                label="Pillar Name"),
                dbc.Input(id="input-addclient-pillar-name", placeholder="Select pillar Name"),
            ]
        )
    ],
    className="mb-3",
)],
fluid=False)

pillar_weightage_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupText("Pillar Weight"),
                dbc.Input(id="input-addclient-pillar-weightage", placeholder="Enter Pillar Weightage"),
            ]
        )
    ],
    className="mb-3",
)],
fluid=False)

pillar_weightage_popover = dbc.Popover(
                                dbc.PopoverBody("Pillar weightage must be integer"),
                                target="input-addclient-pillar-weightage",
                                #trigger="focus",
                                is_open=False,
                                id="input-addclient-pillar-weightage-popover"
                            )

lever_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupText("Lever Name"),
                dbc.Input(id="input-addclient-lever-name", placeholder="Enter Lever Name"),
            ]
        )
    ],
    className="mb-3",
)],
fluid=False)

lever_weightage_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupText("Lever Weight"),
                dbc.Input(id="input-addclient-lever-weightage", placeholder="Enter Lever Weightage"),
            ]
        )
    ],
    className="mb-3",
)],
fluid=False)

lever_weightage_popover = dbc.Popover(
                                dbc.PopoverBody("Lever weightage must be numeric"),
                                target="input-addclient-lever-weightage",
                                #trigger="focus",
                                is_open=False,
                                id="input-addclient-lever-weightage-popover"
                            )


no_of_variable_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupText("No. Of Variables"),
                dbc.Input(id="input-addclient-no-of-var", placeholder="Enter a Number"),
            ]
        )
    ],
    className="mb-3",
)],
fluid=False)

variables_input = dbc.Container([
    dbc.Row(
    [
        html.Div(
            children=[
            ],
            className="mb-3",
            id="input-addclient-var-textboxes"
        ),
    ],
    className="mb-3",
)],
fluid=False)

submit_btn_input = dbc.Container([
    dbc.Row(
    [
        dbc.Col([
            dbc.Button("Submit Client", color="danger", id="input-addclient-submit-btn", disabled=False, n_clicks=0)
        ],
        width={"offset": 5})
    ],
    className="mb-3",
)],
fluid=True)


save_as_client_toast = html.Div(
                            id="save-as-client-toast-div",
                            children=[
                               dbc.Modal(
                                    [
                                        dbc.ModalHeader(
                                            dbc.ModalTitle("Success"), close_button=False
                                        ),
                                        dbc.ModalBody(
                                            "Master data details has been added to database successfully."
                                        ),
                                        dbc.ModalFooter(dbc.Button("OK",href="/admin")),
                                    ],
                                    id="save-as-client-toast",
                                    keyboard=False,
                                    backdrop="static",
                                    centered=True,
                                ),
                            ]
                        )

# form = dbc.Card([
#     dbc.CardHeader("CLIENT DETAILS"),
#     dbc.CardBody(
#         [
#            dbc.Form(
#         [
#             client_input,
#             domain_input,
#             pillar_input,
#             pillar_weightage_input,
#             pillar_weightage_popover,
#             lever_input,
#             lever_weightage_input,
#             lever_weightage_popover,
#             no_of_variable_input,
#             variables_input,
#             #submit_btn_input,
#         ],
#         id="input-addclient-main-form"),
#         submit_btn_input
            
#         ]
#     ),
# ],
# outline=False,
# color="Gainsboro" , 
# #inverse=True,
# style={"width": "80rem"},)

form = dbc.Card([
    dbc.CardHeader("CLIENT DETAILS"),
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
                   
                ]),
                dbc.Row([
                     dbc.Col([
                        pillar_input
                    ]),
                    dbc.Col([
                        pillar_weightage_input,
                        pillar_weightage_popover
                    ]),
                   
                ]),
                dbc.Row([
                     dbc.Col([
                        lever_input
                    ]),
                    dbc.Col([
                        lever_weightage_input,
                        lever_weightage_popover
                    ]),
                    
                ]),
                dbc.Row([
                    dbc.Col([
                        no_of_variable_input
                    ]),
                    dbc.Col([
                        variables_input
                    ])
                ])
            ],
        id="input-addclient-main-form"),
        submit_btn_input
            
        ]
    ),
],
outline=False,
color="Gainsboro" , 
#inverse=True,
#style={"width": "115rem"},
)



add_client_layout_main = dbc.Container([
    # dbc.Row([
    #     dbc.Col([
    #         html.Br(),
    #         #dcc.Location(id="")
    #     ])
    # ]),
    dbc.Row([
        dbc.Col([
            form
        ]),
        dbc.Col([
            save_as_client_toast
        ])
    ])
],
fluid=True)


layout = html.Div(children=[
    navigation.navbar,
    breadcrumb,
    add_client_layout_main
],
className="add-client-page-main-div")






## Callback to render number of textboxes based on number of variables
@dash.callback(
     [Output("input-addclient-var-textboxes", "children"),],
    [Input("input-addclient-no-of-var", "value")],
    prevent_initial_call=True
)

def render_variable_textboxes(number_of_options):
    textboxes = []
    default_val_list = []
    if number_of_options:
        for i in range(int(number_of_options)):
            default_val_list.append("{}. Variable Name".format(i+1))
        if int(number_of_options)>0 and int(number_of_options)<=9999:
            textboxes = [
                    dbc.Textarea(className="mb-3", placeholder=default_val, id=default_val+str("variablestextarea"))
                    for default_val in default_val_list
                ]
    return [textboxes]

## Callback to check Pillar & Lever Weight is integer
@dash.callback(
     [Output("input-addclient-pillar-weightage-popover", "is_open"),
     Output("input-addclient-lever-weightage-popover", "is_open"),
     Output("input-addclient-submit-btn", "disabled")],
    [Input("input-addclient-pillar-weightage", "value"),
    Input("input-addclient-lever-weightage", "value")],
    prevent_initial_call=True
)
def check_pillar_weightage_datatype(pillar_weightage,lever_weightage):
    show_pillar_popover = False
    show_lever_popover = False
    disable_submit = False
    callback_source = ctx.triggered_id
    try:
        if callback_source == "input-addclient-pillar-weightage":
            pillar_weightage = float(pillar_weightage)
        if callback_source == "input-addclient-lever-weightage":
            lever_weightage = float(lever_weightage)
    except Exception:
        if callback_source == "input-addclient-pillar-weightage":
            show_pillar_popover = True
        if callback_source == "input-addclient-lever-weightage":
            show_lever_popover = True
        disable_submit = True
    return show_pillar_popover,show_lever_popover,disable_submit


## Callback to handle the pillar name dropdown
@dash.callback(
    Output("input-addclient-pillar-name", "value"),
    [
        Input("input-addclient-pillar-name-dd-item-env", "n_clicks"),
        Input("input-addclient-pillar-name-dd-item-soc", "n_clicks"),
        Input("input-addclient-pillar-name-dd-item-gov", "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n_env, n_soc, n_gov):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "input-addclient-pillar-name-dd-item-env":
        return "Environment"
    elif button_id == "input-addclient-pillar-name-dd-item-soc":
        return "Social"
    elif button_id == "input-addclient-pillar-name-dd-item-gov":
        return "Governance"


# Callback to save client data to DB
@dash.callback([Output("save-as-client-toast", "is_open")],
              [Input("input-addclient-submit-btn", "n_clicks")],
              [State("input-addclient-main-form", "children")],
            prevent_initial_call=True)
def save_client_to_db(save_as_client_btn_n_click,form_content):
    if save_as_client_btn_n_click:
        #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
        client = mongodb_utility.connect_to_mongodb(mongodb_config.conn_str)
        #client = MongoClient(mongodb_config.conn_str)
        db = client["esg"]
        collection = db["client_dtl"]
        data = {}
        variables_name_list = []
        for f_element in form_content:
            #print(f_element)
            elemets_in_each_row = f_element["props"]["children"]
            for element in elemets_in_each_row:
                #print(element)
                if "variablestextarea" not in json.dumps(element):
                    element_id = element["props"]["children"][0]["props"]["children"][0]["props"]["children"][0]["props"]["children"][1]["props"]["id"]
                    element_value = element["props"]["children"][0]["props"]["children"][0]["props"]["children"][0]["props"]["children"][1]["props"]["value"]
                #print("{} {}".format(element_id,element_value))
                if element_id == "input-addclient-client-name":
                    data["client"] = element_value
                if element_id == "input-addclient-domain-name":
                    data["domain"] = element_value
                if element_id == "input-addclient-pillar-name":
                    data["pillar"] = element_value
                if element_id == "input-addclient-pillar-weightage":
                    data["pillar_weight"] = element_value
                if element_id == "input-addclient-lever-name":
                    data["lever"] = element_value
                if element_id == "input-addclient-lever-weightage":
                    data["lever_weight"] = element_value
                if element_id == "input-addclient-no-of-var":
                    data["variable_count"] = element_value
                if "variablestextarea" in json.dumps(element):
                    variable_props_list = element["props"]["children"][0]["props"]["children"][0]["props"]["children"][0]["props"]["children"]
                    for props in variable_props_list:
                        variables_name_list.append(props['props']['value'])
                    data["variables"] = variables_name_list
        #print(data)
        collection.insert_one(data)
        return [True]
    return [False]

