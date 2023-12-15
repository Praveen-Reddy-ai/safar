from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from nav import navigation
import dash
import dash_daq as daq
from database import mongodb_utility
from pymongo import MongoClient
from database import mongodb_config
import json
import uuid
import certifi


dash.register_page(__name__,path='/addquestion',title="Add Question")

breadcrumb=dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Breadcrumb(
                items=[
                    {"label": "Home", "href": "/", "external_link": False},
                    {"label": "Admin", "href": "/admin",},
                    {"label": "Add Question", "active": True},
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
                id="input-addquestion-client-name-dd",
                direction="start",
                label="Client"),
                dbc.Input(id="input-addquestion-client-name-textbox", placeholder="Select Client"),
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
                id="input-addquestion-domain-name-dd",
                direction="start",
                label="Domain"),
                dbc.Input(id="input-addquestion-domain-name-textbox", placeholder="Select Domain"),
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
                id="input-addquestion-pillar-name-dd",
                direction="start",
                label="Pillar"),
                dbc.Input(id="input-addquestion-pillar-name-textbox", placeholder="Select Pillar"),
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
                id="input-addquestion-lever-name-dd",
                direction="start",
                label="Lever"),
                dbc.Input(id="input-addquestion-lever-name-textbox", placeholder="Select Lever"),
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
                id="input-addquestion-variable-name-dd",
                direction="start",
                label="Variable"),
                dbc.Input(id="input-addquestion-variable-name-textbox", placeholder="Select Variable"),
            ]
        ),
    ],
    className="mb-3",
)],
fluid=False)



serial_no_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupText("Serial No."),
                dbc.Input(id="input-addquestion-serialno-name-textbox"),
            ]
        )
    ],
    className="mb-3",
)],
fluid=False)


question_text_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupText("Question Text"),
                dbc.Textarea(id="input-addquestion-questiontext-name-textbox"),
            ]
        )
    ],
    className="mb-3",
)],
fluid=False)


number_of_option_input = dbc.Container([
    dbc.Row(
    [
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Number Of Options"),
                    dbc.Input(id="input-addquestion-optionnos-name-textbox"),
                ]
            )
    ],
    className="mb-3",
)],
fluid=False)

options_input = dbc.Container([
    dbc.Row(
    [
        html.Div(
            children=[],
            className="mb-3",
            id="input-addquestion-option-textboxes"
        ),
    ],
    className="mb-3",
)],
fluid=False)

options_internal_score_input= dbc.Container([
    dbc.Row(
    [
        html.Div(
            children=[],
            className="mb-3",
            id="input-addquestion-option-intr-score-textboxes"
        ),
    ],
    className="mb-3",
)],
fluid=False)

options_absolute_score_input= dbc.Container([
    dbc.Row(
    [
        html.Div(
            children=[],
            className="mb-3",
            id="input-addquestion-option-abs-score-textboxes"
        ),
    ],
    className="mb-3",
)],
fluid=False)

question_type_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.DropdownMenu( 
                [
                    dbc.DropdownMenuItem("Multiple Choice", id={"type":"dynamic-questiontype", "identifier":"Multiple Choice"}),
                    dbc.DropdownMenuItem("Multiselect", id={"type":"dynamic-questiontype", "identifier":"Multiselect"}),
                    dbc.DropdownMenuItem("Text", id={"type":"dynamic-questiontype", "identifier":"Text"}),
                ], 
                id="input-addquestion-questiontype-name-dd",
                direction="start",
                label="Question Type"),
                dbc.Input(id="input-addquestion-questiontype-name-textbox"),
            ]
        ),
    ],
    className="mb-3",
)],
fluid=False)

weightage_input = dbc.Container([
    dbc.Row(
    [
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Weightage"),
                    dbc.Input(id="input-addquestion-weightage-name-textbox"),
                ]
            )
    ],
    className="mb-3",
)],
fluid=False)


doc_upload_flag_input = dbc.Container([
    dbc.Row(
    [
        dbc.InputGroup(
            [
                dbc.DropdownMenu( 
                [
                    dbc.DropdownMenuItem("Yes", id={"type":"dynamic-upload", "identifier":"Yes"}),
                    dbc.DropdownMenuItem("No", id={"type":"dynamic-upload", "identifier":"No"})
                ], 
                id="input-addquestion-upload-name-dd",
                direction="start",
                label="Enable Attachment"),
                dbc.Input(id="input-addquestion-upload-name-textbox"),
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
            dbc.Button("Submit Question", color="danger",id="input-addquestion-submit-btn")
        ],
        width={"offset": 5})
    ],
    className="mb-3",
)],
fluid=True)

save_success_toast = html.Div(
                            id="save-success-toast-div",
                            children=[
                               dbc.Modal(
                                    [
                                        dbc.ModalHeader(
                                            dbc.ModalTitle("Info"), close_button=False
                                        ),
                                        dbc.ModalBody(
                                            "Question data details has been added to database successfully."
                                        ),
                                        dbc.ModalFooter(dbc.Button("OK",id="input-addquestion-save-success-modal-submit",href="/admin")),
                                    ],
                                    id="save-success-toast",
                                    keyboard=False,
                                    backdrop="static",
                                    centered=True,
                                    is_open=False
                                ),
                            ]
                        )


form = dbc.Card([
    dbc.CardHeader("QUESTION DETAILS"),
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
                        pillar_input
                    ]),
                   
            ]),
            dbc.Row([
                    dbc.Col([
                        lever_input
                    ]),
                    dbc.Col([
                        variables_input
                    ]),
                    dbc.Col([
                        question_type_input
                        
                    ]),
                   
            ]),
            dbc.Row([
                    dbc.Col([
                            doc_upload_flag_input
                        ],
                    width={"size":"4","offset":"0"}),
                    dbc.Col([
                        question_text_input
                    ],
                    width={"size":"8","offset":"0"}),
                    
                    
                   
            ]),
            dbc.Row([
                dbc.Col([
                        serial_no_input
                    ]),
                    dbc.Col([
                        weightage_input
                    ]),
                    dbc.Col([
                        number_of_option_input
                    ]),
                    
                   
            ]),
             dbc.Row([
                    dbc.Col([
                        options_input
                    ]),
                    dbc.Col([
                        options_internal_score_input
                    ]) ,
                    dbc.Col([
                        options_absolute_score_input
                    ])     
            ]),
        ],
        id="input-addquestion-main-form"),
        submit_btn_input
            
        ]
    ),
],
outline=False,
color="Gainsboro" , 
#inverse=True,
#style={"width": "115rem"},
)

add_question_layout_main = dbc.Container([
    dbc.Row([
        dbc.Col([
            form
        ])
    ]),
    dbc.Row([
        dbc.Col(
            save_success_toast
        )
    ])
],
fluid=True)


layout = html.Div(children=[
    navigation.navbar,
    breadcrumb,
    add_question_layout_main,
    html.Div(id='dummy_div'),
],
className="add-question-page-main-div")


## Callback to update the dynamic dropdowns
@dash.callback(
    [
        Output("input-addquestion-client-name-dd", "children"),
        Output("input-addquestion-domain-name-dd", "children"),
        Output("input-addquestion-pillar-name-dd", "children"),
        Output("input-addquestion-lever-name-dd", "children"),
        Output("input-addquestion-variable-name-dd", "children"),
    ],
    [
        Input('dummy_div', 'children')
    ]
)
def update_dynamic_dropdowns(n_modla_submit):
    client_name_list,domain_name_list,pillar_name_list,lever_name_list,variables_name_list = mongodb_utility.get_distinct("client_dtl")
    client_name_list = [" "] + client_name_list
    domain_name_list = [" "] + domain_name_list
    pillar_name_list = [" "] + pillar_name_list
    lever_name_list = [" "] + lever_name_list
    variables_name_list = [" "] + variables_name_list
    client_name_dd_items =[dbc.DropdownMenuItem("Select Client")] + [dbc.DropdownMenuItem(divider=True)]  + [dbc.DropdownMenuItem(client, id={"type":"dynamic-client", "identifier":client}) for client in client_name_list]
    domain_name_dd_items =[dbc.DropdownMenuItem("Select Domain")] + [dbc.DropdownMenuItem(divider=True)]  + [dbc.DropdownMenuItem(domain, id={"type":"dynamic-domain", "identifier":domain}) for domain in domain_name_list]
    pillar_name_dd_items =[dbc.DropdownMenuItem("Select Pillar")] + [dbc.DropdownMenuItem(divider=True)]  + [dbc.DropdownMenuItem(pillar, id={"type":"dynamic-pillar", "identifier":pillar}) for pillar in pillar_name_list]
    lever_name_dd_items =[dbc.DropdownMenuItem("Select Lever")] + [dbc.DropdownMenuItem(divider=True)]  +  [dbc.DropdownMenuItem(lever, id={"type":"dynamic-lever", "identifier":lever}) for lever in lever_name_list]
    variables_name_dd_items =[dbc.DropdownMenuItem("Select Variable")] + [dbc.DropdownMenuItem(divider=True)]  +  [dbc.DropdownMenuItem(variable, id={"type":"dynamic-variable", "identifier":variable}) for variable in variables_name_list]
    return [client_name_dd_items,domain_name_dd_items,pillar_name_dd_items,lever_name_dd_items,variables_name_dd_items]



## Callback to handle the client name dropdown
@dash.callback(
    Output("input-addquestion-client-name-textbox", "value"),
    [
        Input({"type": "dynamic-client", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])



## Callback to handle the domain name dropdown
@dash.callback(
    Output("input-addquestion-domain-name-textbox", "value"),
    [
        Input({"type": "dynamic-domain", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])


## Callback to handle the pillar name dropdown
@dash.callback(
    Output("input-addquestion-pillar-name-textbox", "value"),
    [
        Input({"type": "dynamic-pillar", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])


## Callback to handle the lever name dropdown
@dash.callback(
    Output("input-addquestion-lever-name-textbox", "value"),
    [
        Input({"type": "dynamic-lever", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])


## Callback to handle the variable name dropdown
@dash.callback(
    Output("input-addquestion-variable-name-textbox", "value"),
    [
        Input({"type": "dynamic-variable", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])


## Callback to handle the questiontype name dropdown
@dash.callback(
    Output("input-addquestion-questiontype-name-textbox", "value"),
    [
        Input({"type": "dynamic-questiontype", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])


## Callback to handle the upload name dropdown
@dash.callback(
    Output("input-addquestion-upload-name-textbox", "value"),
    [
        Input({"type": "dynamic-upload", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])



## Callback to render number of textboxes based on number of question options
@dash.callback(
     [Output("input-addquestion-option-textboxes", "children"),
     Output("input-addquestion-option-intr-score-textboxes", "children"),
     Output("input-addquestion-option-abs-score-textboxes", "children")],
    [Input("input-addquestion-optionnos-name-textbox", "value")],
    prevent_initial_call=True
)

def render_variable_textboxes(number_of_options):
    textboxes = []
    int_scr_textboxes = []
    abs_scr_textboxes = []
    default_val_list = []
    default_internal_score_list = []
    default_abs_score_list = []
    if number_of_options:
        for i in range(int(number_of_options)):
            default_val_list.append("{}. Option text".format(i+1))
            default_internal_score_list.append("{}. Option Internal Score".format(i+1))
            default_abs_score_list.append("{}. Option Absolute Score".format(i+1))
        if int(number_of_options)>0 and int(number_of_options)<=9999:
            textboxes = [
                    dbc.Textarea(className="mb-3", placeholder=default_val, id=default_val+str("optionstextarea"))
                    for default_val in default_val_list
                ]
            int_scr_textboxes = [
                    dbc.Textarea(className="mb-3", placeholder=default_val, id=default_val+str("optionsintscrtextarea"))
                    for default_val in default_internal_score_list
                ]
            abs_scr_textboxes = [
                    dbc.Textarea(className="mb-3", placeholder=default_val, id=default_val+str("optionsabsscrtextarea"))
                    for default_val in default_abs_score_list
                ]
    return [textboxes,int_scr_textboxes,abs_scr_textboxes]


# Callback to save question data to DB
@dash.callback([Output("save-success-toast", "is_open")],
              [Input("input-addquestion-submit-btn", "n_clicks")],
              [State("input-addquestion-main-form", "children")],
            prevent_initial_call=True)
def save_client_to_db(n_clicks,form_content):
    if n_clicks:
        #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
        client = mongodb_utility.connect_to_mongodb(mongodb_config.conn_str)
        #client = MongoClient(mongodb_config.conn_str)
        db = client["esg"]
        collection = db["questions"]
        data = {}
        options_name_list = []
        options_int_score_list = []
        options_abs_score_list = []
        for f_element in form_content:
            elemets_in_each_row = f_element["props"]["children"]
            for element in elemets_in_each_row:
                if "optionstextarea" in json.dumps(element) or "optionsintscrtextarea" in json.dumps(element) or "optionsabsscrtextarea" in json.dumps(element):
                    pass
                else:
                    element_id = element["props"]["children"][0]["props"]["children"][0]["props"]["children"][0]["props"]["children"][1]["props"]["id"]
                    element_value = element["props"]["children"][0]["props"]["children"][0]["props"]["children"][0]["props"]["children"][1]["props"]["value"]
                #print("{} :  {}".format(element_id,element_value))
                if element_id == "input-addquestion-client-name-textbox":
                        data["client"] = element_value
                if element_id == "input-addquestion-domain-name-textbox":
                        data["domain"] = element_value
                if element_id == "input-addquestion-pillar-name-textbox":
                        data["pillar"] = element_value
                if element_id == "input-addquestion-lever-name-textbox":
                        data["lever"] = element_value
                if element_id == "input-addquestion-variable-name-textbox":
                        data["variable"] = element_value
                if element_id == "input-addquestion-serialno-name-textbox":
                        data["serial_no"] = element_value
                if element_id == "input-addquestion-questiontext-name-textbox":
                        data["question_text"] = element_value
                if element_id == "input-addquestion-optionnos-name-textbox":
                        data["options_count"] = element_value
                if element_id == "input-addquestion-questiontype-name-textbox":
                        data["question_type"] = element_value
                if element_id == "input-addquestion-weightage-name-textbox":
                        data["weightage"] = element_value
                if element_id == "input-addquestion-upload-name-textbox":
                        data["doc_upload_flag"] = element_value
                if "optionstextarea" in json.dumps(element):
                    options_props_list = element["props"]["children"][0]["props"]["children"][0]["props"]["children"][0]["props"]["children"]
                    for props in options_props_list:
                        options_name_list.append(props['props']['value'])
                    data["options"] = options_name_list
                if "optionsintscrtextarea" in json.dumps(element):
                    options_props_list = element["props"]["children"][0]["props"]["children"][0]["props"]["children"][0]["props"]["children"]
                    for props in options_props_list:
                        options_int_score_list.append(props['props']['value'])
                    data["options_internal_score"] = options_int_score_list
                if "optionsabsscrtextarea" in json.dumps(element):
                    options_props_list = element["props"]["children"][0]["props"]["children"][0]["props"]["children"][0]["props"]["children"]
                    for props in options_props_list:
                        options_abs_score_list.append(props['props']['value'])
                    data["options_absolute_score"] = options_abs_score_list
        #print(data)
        question_unique_id = str(uuid.uuid4())
        data["question_unique_id"] = question_unique_id
        collection.insert_one(data)
        return [True]
    return [False]