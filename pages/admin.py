from dash import html
from dash import dcc,dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL, MATCH
from nav import navigation
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import base64
from database import mongodb_config,mongodb_utility
import uuid
import pandas as pd
from flask_login import current_user
from utils.login_handler import require_login
from utils.common_ui_elements import submenu_button,mantine_text_box,mantine_modal,success_toast,bootstrap_popover,mantine_select,mantine_table,dash_table_interactivity_helptext,dash_datatable
from flask import  session
import json
import dictdiffer  
from dash.exceptions import PreventUpdate
import dash_daq as daq
from admin_page_objects import common,pillar,lever,variable,question,assessment_template,assessment

dash.register_page(__name__,path='/admin',title="Administer")
require_login(__name__)

admin_layout = html.Div(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.A(
                            dmc.Button(
                                "Assessment data Management",
                                leftIcon=[DashIconify(icon="wpf:survey")],
                                variant="subtle",
                                color="dark",
                                size="sm",
                                id="survey-mgmt-btn"
                            ),
                        ),
                ],width="auto"),
                 dbc.Col([
                    html.A(
                            dmc.Button(
                                "User Management",
                                leftIcon=[DashIconify(icon="mdi:user-card-details")],
                                variant="subtle",
                                color="dark",
                                size="sm",
                                id="user-mgmt-btn"
                            ),
                        ),
                ],width="auto"),
                dbc.Col([
                    html.A(
                            dmc.Button(
                                "Customer Management",
                                leftIcon=[DashIconify(icon="carbon:ibm-cloud-pak-business-automation")],
                                variant="subtle",
                                color="dark",
                                size="sm",
                                id="client-mgmt-btn",
                                className="admin-screen-menu-btn",
                            ),
                        ),
                        
                ],width="auto"),
                 dbc.Col([
                    html.A(
                            dmc.Button(
                                "Reporting",
                                leftIcon=[DashIconify(icon="mdi:report-bar")],
                                variant="subtle",
                                color="dark",
                                size="sm",
                                id="reports-btn"
                            ),
                        ),
                ],width="auto"),
            ]),
            dbc.Row([
                dmc.Divider(style={"marginBottom": 0, "marginTop": 0},color='gray',size='sm'),
            ])
    ],fluid=True),
    style={"backgroundColor": "LightGray","overflow-x":"hidden"}
)

def layout():
    #print(str(session["_user_id"] if session else ""))
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])
    
    if mongodb_utility.get_user_role(str(session["_user_id"] if session else "")) != "admin":
        return html.Div(["You need to be an admin user to access this page.", "Go ",dcc.Link("back", href="/takesurvey")])

    layout = html.Div(children=[
        navigation.navbar,
        dmc.Divider(style={"marginBottom": 0, "marginTop": 0},color='gray',size='sm'),
        html.Div(children=[
            #breadcrumb,
            html.Div(admin_layout),
            dmc.Space(h=10),
            html.Div(id="admin-screen-sub-menu-div")
        ],
    className="admin-page-main-div")
    ])

    return layout


## Callback to display submenu

@dash.callback(
    Output("admin-screen-sub-menu-div", "children"), 
    Output("client-mgmt-btn", "color"),
    #Output("hierarchy-mgmt-btn", "color"),
    #Output("question-mgmt-btn", "color"),
    Output("survey-mgmt-btn", "color"),
    Output("reports-btn", "color"),
    Output("user-mgmt-btn", "color"),
    Input("client-mgmt-btn", "n_clicks"),
    #Input("hierarchy-mgmt-btn", "n_clicks"),
    #Input("question-mgmt-btn", "n_clicks"),
    Input("survey-mgmt-btn", "n_clicks"),
    Input("reports-btn", "n_clicks"),
    Input("user-mgmt-btn", "n_clicks"),
    prevent_initial_call=True
)
def render_tab_submenu(n_cm,n_sm,n_r,n_um):
    ctx = dash.callback_context
    if ctx.triggered_id == "client-mgmt-btn" and n_cm:
        options = html.Div([
                    #dmc.Space(h="xs"),
                    html.Div(
                        dmc.Group(
                                    [
                                        dmc.Space(w="lg"),
                                        html.A(
                                            dmc.Button(
                                                "Setup Customer",
                                                leftIcon=[DashIconify(icon="codicon:git-pull-request-create")],
                                                variant="outline",
                                                color="dark",
                                                size="sm",
                                                id="add-customer-btn"
                                            ),
                                            href="/addclient"
                                        ),
                                        #dmc.Divider(orientation="vertical", style={"height": 40}, color='cyan',size='md'),
                                        html.A(
                                            dmc.Button(
                                                "Delete Customer",
                                                leftIcon=[DashIconify(icon="fluent:person-delete-24-filled")],
                                                variant="outline",
                                                color="dark",
                                                size="sm",
                                                id="del-customer-btn"
                                            ),
                                                href="/delclient"
                                        ),
                                        #dmc.Divider(orientation="vertical", style={"height": 40}, color='cyan',size='md'),
                                    ]
                            )
                    ),
                    dmc.Space(h="lg"),
                    html.Div(id="add-customer-div"),
                ])
        return [options,'violet','dark','dark','dark']
    
    
    if ctx.triggered_id == "survey-mgmt-btn" and n_sm:
        options = dmc.Tabs(
                    [
                        dmc.TabsList(
                            [
                                dmc.Tab("Pillars", value="Pillars",icon=DashIconify(icon="mdi:pillar",color=dmc.theme.DEFAULT_COLORS["blue"][6],width=20)),
                                dmc.Tab("Levers", value="Levers",icon=DashIconify(icon="game-icons:lever",color=dmc.theme.DEFAULT_COLORS["red"][6],width=20)),
                                dmc.Tab("Variables", value="Variables",icon=DashIconify(icon="material-symbols:variables",color=dmc.theme.DEFAULT_COLORS["green"][6],width=20)),
                                dmc.Tab("Questions", value="Questions",icon=DashIconify(icon="mdi:question-box-multiple-outline",color=dmc.theme.DEFAULT_COLORS["blue"][6],width=20)),
                                dmc.Tab("Templates", value="Assessment templates",icon=DashIconify(icon="file-icons:templatetoolkit",color=dmc.theme.DEFAULT_COLORS["violet"][6],width=20)),
                                dmc.Tab("Assessments", value="Assessments",icon=DashIconify(icon="wpf:survey",color=dmc.theme.DEFAULT_COLORS["pink"][6],width=20)),
                            ]
                        ),
                        dmc.TabsPanel(pillar.pillar_table, value="Pillars"),
                        dmc.TabsPanel(lever.lever_table, value="Levers"),
                        dmc.TabsPanel(variable.variable_table, value="Variables"),
                        dmc.TabsPanel(question.question_table, value="Questions"),
                        dmc.TabsPanel(assessment_template.template_table, value="Assessment templates"),
                        dmc.TabsPanel(assessment.assessment_table, value="Assessments"),
                    ],
                    color="red",
                    orientation="horizontal",
                    variant="outline",
                    loop=True,
                    placement="right"
                )
        return [options,'dark','violet','dark','dark']
    
    if ctx.triggered_id == "reports-btn" and n_r:
        options = html.Div([
                    html.Div(
                        dmc.Group(
                                            [
                                                dmc.Space(w="xs"),
                                                submenu_button(label="Download Survey Data",icon_class="fluent:drawer-arrow-download-20-filled",varient="outline",color="dark",size="sm",id="reporting-download-survey-report"),
                                            ]
                            )
                    ),
                    dmc.Space(h="lg"),
                    html.Div(id="reporting-survey-id-table"),
                    dmc.Space(h="lg"),
                    html.Div(id="reporting-entire-survey-data-table"),
                ])
        return [options,'dark','dark','violet','dark']

    if ctx.triggered_id == "user-mgmt-btn" and n_um:
        user_table = html.Div([
                    dmc.Space(h="lg"),

                    ## Data input Modals
                    html.Div(
                        children= [
                            mantine_modal(
                                title="Add User",
                                id="add-user-modal",
                                size='40%',
                                is_open=False,
                                modal_component_list=[
                                    mantine_text_box(label="User Name : *",id="user-name-txt-au",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_text_box(label="User id : *",id="user-id-txt-au",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_text_box(label="Password : *",id="password-txt-au",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=True),
                                    mantine_select(
                                        label="User Type : *",
                                        required=False,
                                        icon_class="radix-icons:magnifying-glass",
                                        size='sm',
                                        style_dict={"width": 400},
                                        id="user-type-select-au",
                                        dropdown_data=[
                                                                    {"value": "admin", "label": "Admin"},
                                                                    {"value": "customer", "label": "Customer"},
                                        ]
                                    ),
                                    mantine_select(
                                        label="Customer Name : *",
                                        required=False,
                                        icon_class="radix-icons:magnifying-glass",
                                        size='sm',
                                        style_dict={"width": 400},
                                        id="customer-name-select-au",
                                        dropdown_data=mongodb_utility.get_distinct_values("client_dtl","client")
                                    ),
                                    mantine_text_box(label="Domain : *",id="domain-name-txt-au",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    bootstrap_popover(body="User already exists",targer_component_id="user-id-txt-au",id="user-id-txt-au-popover"),
                                ],
                                submit_btn_id="modal-submit-button-au",
                                cancel_btn_id="modal-cancel-button-au"
                            ),
                            mantine_modal(
                                title="Alert",
                                id="delete-user-modal",
                                size='20%',
                                is_open=False,
                                modal_component_list=[
                                    dmc.Title("Are you sure?", size="lg"),
                                ],
                                submit_btn_id="modal-submit-button-du",
                                cancel_btn_id="modal-cancel-button-du",
                                submit_btn_text="Yes"
                            ),
                        ]
                    ),

                    ## Success toasts
                    success_toast(id="user-add-success-toast",is_open=False),
                    success_toast(id="user-update-success-toast",is_open=False),
                    success_toast(id="user-delete-success-toast",is_open=False),

                    ## data tables
                    html.Div(
                        children=[
                            dbc.Container([
                                    dbc.Row([
                                        #mantine_table(id= "user-dtl-table",table_data=mongodb_utility.create_table_from_df(pd.DataFrame(mongodb_utility.get_user_collection_dump()))),
                                        dash_datatable(
                                            id= "user-dtl-table",
                                            data_dict=mongodb_utility.get_user_collection_dump(),
                                            export_format='none',
                                            title="",
                                            action_btn_list=[
                                                submenu_button("Delete","ep:delete-filled","subtle","red","sm","del-btn-au",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"0px","marginTop":"20px","marginBottom":"20px"}),
                                                submenu_button("Sync to DB","mdi:database-sync","subtle","gray","sm","sync-btn-au",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("De-Select All","material-symbols:deselect","subtle","violet","sm","de-select-all-btn-au",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Select All","fluent:select-all-on-20-regular","subtle","grape","sm","select-all-btn-au",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Refresh","uil:refresh","subtle","blue","sm","refresh-btn-au",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button(label="Add User",icon_class="mdi:user-add",varient="subtle",color="lime",size="sm",id="add-user-btn",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                 dash_table_interactivity_helptext(),
                                                 daq.NumericInput(
                                                        id="num-row-to-display-numeric-au",
                                                        min=1,
                                                        max=100,
                                                        value=10,
                                                         style={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"18px","color":"dark"},
                                                    ),
                                            ],
                                            non_editable_col_list=["user_unique_id","user_id"],
                                            table_css=[{
                                                'selector': '.Select-menu-outer',
                                                'rule': '''
                                                    display : block !important;
                                                    border-style: solid;
                                                    border-color: teal;
                                                    border-bottom: 3px solid teal;
                                                '''
                                            }],
                                            table_style={'overflowX': 'auto','height': "auto",'overflowY': 'auto','minWidth': '100%'},
                                        )
                                    ])
                                ],fluid=False)
                        ]
                    ),
                ])
        options = dmc.Tabs(
                    [
                        dmc.TabsList(
                            [
                                dmc.Tab("Users", value="Users",icon=DashIconify(icon="tabler:user",color=dmc.theme.DEFAULT_COLORS["blue"][6],width=20)),
                                dmc.Tab("Roles", value="Roles",icon=DashIconify(icon="carbon:user-role",color=dmc.theme.DEFAULT_COLORS["red"][6],width=20))
                            ]
                        ),
                        dmc.TabsPanel(user_table, value="Users"),
                        dmc.TabsPanel(html.Div("Some content"), value="Roles"),
                    ],
                    color="red",
                    orientation="horizontal",
                    variant="outline",
                    loop=True,
                    placement="right"
                )
        return [options,'dark','dark','dark','violet']

## Callback to display the add user Modal & save user data to mongodb
@dash.callback(
    [
        Output("add-user-modal", "opened"),
        Output("user-add-success-toast", "is_open"),
        Output("user-add-success-toast", "children"),
        Output("user-name-txt-au", "value"),
        Output("user-id-txt-au", "value"),
        Output("password-txt-au", "value"),
        Output("user-type-select-au", "value"),
        Output("customer-name-select-au", "value"),
        Output("domain-name-txt-au", "value"),
        Output("user-dtl-table", "data"),
    ],
    [
        Input("add-user-btn", "n_clicks"),
        Input("modal-cancel-button-au", "n_clicks"),
        Input("modal-submit-button-au", "n_clicks"),
        Input("refresh-btn-au", "n_clicks"),
        Input('modal-submit-button-du', 'n_clicks'),
    ],
    [
        State("user-name-txt-au", "value"),
        State("user-id-txt-au", "value"),
        State("password-txt-au", "value"),
        State("user-type-select-au", "value"),
        State("customer-name-select-au", "value"),
        State("domain-name-txt-au", "value"),
        State('user-dtl-table', 'selected_rows'),
        State('user-dtl-table', 'data'),
    ],
    prevent_initial_call=True
)
def add_user(n_au,n_mc,n_ms,n_refresh,n_submit_del,user_name,user_id,password,user_type,customer_name,domain_name,selected_row_ids,full_table_data):
    ctx = dash.callback_context
    toast_msg = ""
    if ctx.triggered_id == "add-user-btn" and n_au:
        return [True,False,toast_msg,"","","","","","",mongodb_utility.get_user_collection_dump()]
    if ctx.triggered_id == "modal-cancel-button-au" and n_mc:
        return [False,False,toast_msg,"","","","","","",mongodb_utility.get_user_collection_dump()]
    if ctx.triggered_id == "modal-submit-button-au" and n_ms:
        data = {}
        if user_name == "" or user_id == ""  or password == "" or user_type == "" or customer_name == "" or domain_name == "":
            return [True,False,toast_msg,user_name,user_id,password,user_type,customer_name,domain_name,mongodb_utility.get_user_collection_dump()]
        data["user_name"] = user_name
        data["user_id"] = user_id
        data["user_unique_id"] = str(uuid.uuid4())
        data["password"] = password
        data["user_type"] = user_type
        data["customer_name"] = customer_name
        data["domain_name"] = domain_name
        toast_msg ="User created successfully"
        mongodb_utility.insert_one_doc("user",data)
        return [False,True,toast_msg,"","","","","","",mongodb_utility.get_user_collection_dump()]
    if ctx.triggered_id == "refresh-btn-au" and n_refresh:
        return [False,False,"","","","","","","",mongodb_utility.get_user_collection_dump()]
    if ctx.triggered_id == "modal-submit-button-du" and n_submit_del:
        if len(selected_row_ids)>0:
            for row_id in selected_row_ids:
                data_to_be_deleted=full_table_data[row_id]
                mongodb_utility.delete_one_doc("user",data_to_be_deleted)
        return [False,False,"","","","","","","",mongodb_utility.get_user_collection_dump()]

## Callback to display survey table
@dash.callback(
    [
        Output("reporting-entire-survey-data-table", "children"),
    ],
    [
        Input({"survey_id": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def render_survey_table(n):
    ctx = dash.callback_context
    survey_id = ctx.triggered_id["survey_id"]
    survey_table = []
    selected_survey_dtl = mongodb_utility.get_survey_dtls(survey_id)
    data = []
    
    #print(selected_survey_dtl)
    ## Preparing data for the table
    for ss in selected_survey_dtl:
        each_row = {}
        each_row["survey_unique_id"] = ss["survey_unique_id"]
        each_row["question_unique_id"] = ss["question_unique_id"]
        #each_row["client"] = ss["client"]
        #each_row["domain"] = ss["domain"]
        each_row["pillar"] = ss["pillar"]
        each_row["lever"] = ss["lever"]
        each_row["variable"] = ss["variable"]
        each_row["question_text"] = ss["question_text"]
        if 'question' in ss.keys():
            each_row["question_type"] = ss['question']["question_type"]
            each_row["doc_upload_flag"] = ss['question']["doc_upload_flag"]
            each_row["weightage"] = ss["weightage"]
            each_row["question options"] = '***'.join(ss['question']["options"])
            each_row["absolute score"] = ','.join(ss['question']["option_absolute_score"])
            each_row["internal score"] = ','.join(ss['question']["option_internal_score"])
        if 'question_scores' in ss.keys():
            #each_row["selected options"] = ','.join([ss['question']["options"][int(i)] for i in ss['question_scores']["question_selected_score_indices"]])
            each_row["selected options index"] = ','.join(ss['question_scores']["question_selected_score_indices"])
            if 'answer_text' in ss['question_scores'].keys():
                each_row["answer_text"] = ss["question_scores"]["answer_text"]
            else:
                each_row["answer_text"] = " "
        data.append(each_row)

    print(n)

    if 1 in n:
        survey_table = dbc.Container([
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(
                        id='input-addsurvey-questions-datatable',
                        data=data,
                        editable=False,
                        #filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable=False,
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                        page_size= 20,
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'DarkSlateGray',
                            'color': 'rgb(210, 210, 210)',
                            'fontWeight': 'bold'
                        },
                        css=[{
                            'selector': '.dash-spreadsheet td div',
                            'rule': '''
                                line-height: 15px;
                                max-height: 30px; min-height: 30px; height: 30px;
                                display: block;
                                overflow-y: hidden;
                            '''
                        }],
                        export_format='xlsx' 
                )
                ],width=12)
            ]),
            dbc.Row([
                 dmc.Space(h="lg"),
            ])
        ],fluid=True)
    return [survey_table]

## Callback to display survey id table
@dash.callback(
    [
        Output("reporting-survey-id-table", "children"),
    ],
    [
        Input("reporting-download-survey-report", "n_clicks"),
    ],
    prevent_initial_call=True
)
def render_survey_id_table(n):
    if n:
        header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("SURVEY ID",style={'color':'Dark'}),
                    ]
                )
            )
        ]

        survey_id_list = mongodb_utility.get_distinct_survey_id()
        #print(survey_id_list)

        td_list = [
            html.Tr(
                [
                    html.Td(
                        dmc.Button(
                            s,
                            leftIcon=[DashIconify(icon="game-icons:click",width=30,)],
                            variant="subtle",
                            color="teal",
                            size="sm",
                            id={"survey_id":s}
                        ),
                        style={'color':'GreenYellow'}
                    )
                ]
            )
        for s in survey_id_list]

        body = [html.Tbody(td_list)]

        returned_table = dbc.Container([
                            dbc.Row([
                                dbc.Col([
                                    dmc.Table(header + body)
                                ],width=12)
                            ])
                        ],fluid=True)

        return [returned_table]


## Callback to check whether user_id is unique
@dash.callback(
    [
        Output("user-id-txt-au-popover", "is_open"),
        Output("modal-submit-button-au", "disabled")
    ],
    [
        Input("user-id-txt-au", "value"),
    ],
    prevent_initial_call=True
)
def unique_user_check(user_id):
    if user_id is not None and mongodb_utility.is_user_id_unique(user_id):
        return [False,False]
    else:
        return [True,True]

## callback to sync user table to db
@dash.callback(
    [
        Output("user-update-success-toast", "is_open"),
        Output("user-update-success-toast", "children"),
    ],
    [
        Input("sync-btn-au", "n_clicks"),
    ],
    [
        State("user-dtl-table", "data"),
    ],
    prevent_initial_call=True
)
def sync_user_table(n_sb,modified_tbl_data):
    if n_sb:
        current_user_data_from_db = mongodb_utility.get_user_collection_dump()
        changes = list(dictdiffer.diff(current_user_data_from_db, modified_tbl_data))
        if len(changes) == 0:
            raise PreventUpdate
        for change in changes:
            #print(change)
            if change[0] == "change":
                unique_user_id = modified_tbl_data[change[1][0]]["user_unique_id"]
                filter_for_db = {"user_unique_id": unique_user_id}
                updated_data_dict = {str(change[1][1]): change[2][1]}
                mongodb_utility.update_one_doc("user",filter_for_db,updated_data_dict)
                #print(unique_user_id)
        return [True,"User(s) updated successfully"]



## callback to select and deselect all rows in User table
@dash.callback(
        Output('user-dtl-table', 'selected_rows'),
        Input('select-all-btn-au', 'n_clicks'),
        Input('de-select-all-btn-au', 'n_clicks'),
        Input('modal-submit-button-du', 'n_clicks'),
        State('user-dtl-table', 'derived_virtual_indices'),
        State('user-dtl-table', 'selected_rows'),
        prevent_initial_call=True
    )
def select_deselect_user(select_n_clicks, deselect_n_clicks,del_user_n_clicks, filtered_rows_indices,already_selected_rows):
    print(filtered_rows_indices)
    print(already_selected_rows)
    """Select or deselect all rows."""
    ctx = dash.callback_context
    if ctx.triggered_id == 'select-all-btn-au':
        if select_n_clicks:
            if filtered_rows_indices is None:
                return []
            else:
                return filtered_rows_indices + already_selected_rows if already_selected_rows is not None else []
    if ctx.triggered_id == 'de-select-all-btn-au':
        if deselect_n_clicks:
            return []
    if ctx.triggered_id == 'modal-submit-button-du':
        if del_user_n_clicks:
            return []


## Callback to delete data from user table
@dash.callback(
    Output('delete-user-modal', 'opened'),
    Output("user-delete-success-toast", "is_open"),
    Output("user-delete-success-toast", "children"),
    Input('del-btn-au', 'n_clicks'),
    Input('modal-cancel-button-du', 'n_clicks'),
    Input('modal-submit-button-du', 'n_clicks'),
    State('user-dtl-table', 'selected_rows'),
    # State('user-dtl-table', 'data'),
    prevent_initial_call=True
)
def delete_data(n_d,n_c,n_s,selected_rows):
    ctx = dash.callback_context
    data_to_be_deleted = {}
    if n_d and ctx.triggered_id == 'del-btn-au':
        return True,False,""
    if n_c and ctx.triggered_id == 'modal-cancel-button-du':
        return False,False,""
    if n_s and ctx.triggered_id == 'modal-submit-button-du':
        print(selected_rows)
        if len(selected_rows) > 0:
            text = "Selected users deleted successfully"
        else:
            text = "Nothing to delete"  
        return False,True,text                                        

                  
