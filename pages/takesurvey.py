from dash import html
from dash import dcc, ctx, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL, MATCH
from nav import navigation
import dash
from database import mongodb_config,mongodb_utility
import json
import pandas as pd
import uuid
import certifi
import dash_daq as daq
import base64
import re,os
import dash_uploader as du
from urllib.parse import quote as urlquote
import plotly.graph_objects as go
import plotly.express as px
import textwrap
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from flask_login import current_user
from utils.login_handler import require_login


dash.register_page(__name__,path='/takesurvey',title="Take Survey")
require_login(__name__)



# breadcrumb=dbc.Container(
#     dbc.Row(
#         dbc.Col(
#             dbc.Breadcrumb(
#                 items=[
#                     {"label": "Home", "href": "/", "external_link": False},
#                     {"label": "Take Survey", "active": True},
#                 ],
#             )
#         )
#     ),
#     fluid=True
# )



# tab2_content = dbc.Card(
#     dbc.CardBody(
#         [
#             html.P("This is tab 2!", className="card-text"),
#             dbc.Button("Don't click here", color="danger"),
#         ]
#     ),
#     className="mt-3",
# )

# tab3_content = dbc.Card(
#     dbc.CardBody(
#         [
#             html.P("This is tab 3!", className="card-text"),
#             dbc.Button("Click here", color="success"),
#         ]
#     ),
#     className="mt-3",
# )

# tab4_content = dbc.Card(
#     dbc.CardBody(
#         [
#             html.P("This is tab 4!", className="card-text"),
#             dbc.Button("Click here", color="success"),
#         ]
#     ),
#     className="mt-3",
# )

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px !important',
    #'fontWeight': 'bold'
}

tab_selected_style = {
    'border-style': 'none',
    'borderBottom': '3px solid DarkSlateGray',
    #'backgroundColor': 'DarkSlateGray',
    'color': 'DarkSlateGray',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-top-left-radius': '3px',
    'border-top-right-radius': '3px',
    'background': 'url("/assets/user-rectangle.svg") no-repeat',
    'background-position': 'left center',
    'background-size': '40px 40px',
    'font-size': '100%'
}

tab_selected_style_gov = {
    'border-style': 'none',
    'borderBottom': '3px solid RoyalBlue',
    #'backgroundColor': 'DarkSlateGray',
    'color': 'RoyalBlue',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-top-left-radius': '3px',
    'border-top-right-radius': '3px',
    'background': 'url("/assets/government-fill.svg") no-repeat',
    'background-position': 'left center',
    'background-size': '40px 40px',
    'font-size': '100%'
}

tab_selected_style_env = {
    'border-style': 'none',
    'borderBottom': '3px solid green',
    #'backgroundColor': 'DarkSlateGray',
    'color': 'green',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-top-left-radius': '3px',
    'border-top-right-radius': '3px',
    'background': 'url("/assets/environment.svg") no-repeat',
    'background-position': 'left center',
    'background-size': '40px 40px',
    'font-size': '100%'
}


tab_selected_style_soc = {
    'border-style': 'none',
    'borderBottom': '3px solid DarkGoldenRod',
    #'backgroundColor': 'DarkSlateGray',
    'color': 'DarkGoldenRod',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-top-left-radius': '3px',
    'border-top-right-radius': '3px',
    'background': 'url("/assets/i-social-services.svg") no-repeat',
    'background-position': 'left center',
    'background-size': '40px 40px',
    'font-size': '100%'
}


tab_selected_style_score = {
    'border-style': 'none',
    'borderBottom': '3px solid DarkSlateGray',
    #'backgroundColor': 'DarkSlateGray',
    'color': 'DarkSlateGray',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-top-left-radius': '3px',
    'border-top-right-radius': '3px',
    'background': 'url("/assets/result-new.svg") no-repeat',
    'background-position': 'left center',
    'background-size': '40px 40px',
    'font-size': '100%'
}

tabs = html.Div([
    dcc.Tabs(id="input-takesurvey-tabs", value='intro', children=[
        dcc.Tab(label='INTRODUCTION', value='intro', style=tab_style, selected_style=tab_selected_style,disabled=False,id="input-takesurvey-intro-tab"),
        dcc.Tab(label='ENVIRONMENT', value='environment', style=tab_style, selected_style=tab_selected_style_env,disabled=True,id="input-takesurvey-environment-tab"),
        dcc.Tab(label='SOCIAL', value='social', style=tab_style, selected_style=tab_selected_style_soc,disabled=True,id="input-takesurvey-social-tab"),
        dcc.Tab(label='GOVERNANCE', value='gov', style=tab_style, selected_style=tab_selected_style_gov,disabled=True,id="input-takesurvey-gov-tab"),
        dcc.Tab(label='SCORE', value='submit', style=tab_style, selected_style=tab_selected_style_score,disabled=True,id="input-takesurvey-submit-tab"),
    ], style=tabs_styles),
    html.Div(id='input-takesurvey-tabs-content')
])

def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    layout = html.Div(children=[
        navigation.navbar,
        dmc.Divider(style={"marginBottom": 0, "marginTop": 0},color='gray',size='sm'),
        dcc.Store(id="input-takesurvey-store-survey-id"),
        #breadcrumb,
        tabs
    ],
    className="take-survey-page-main-div",
    id="take-survey-page-main-div-id")

    return layout

def get_esg_tab_content(survey_id,esg_active_tab):
    overall_structure_lever_var = {}
    overall_structure_var_question = {}
    survey_dtl = mongodb_utility.get_survey_dtls(survey_id["survey_id"])
    survey_progess_percent = mongodb_utility.get_survey_progress(survey_id["survey_id"])["overall_progress_percent"]
    print(survey_dtl)
    for sd in survey_dtl:
        if sd["pillar"] == esg_active_tab:
            if  sd["lever"] in overall_structure_lever_var.keys():
                if sd["variable"] not in overall_structure_lever_var[sd["lever"]]:
                    overall_structure_lever_var[sd["lever"]].append(sd["variable"])
            else:
                overall_structure_lever_var[sd["lever"]] = [sd["variable"]]
            if sd["variable"] in overall_structure_var_question.keys():
                overall_structure_var_question[sd["variable"]].append(sd)
            else:
                overall_structure_var_question[sd["variable"]] = [sd]
    #print(overall_structure_lever_var)
    accordion_lever = html.Div([
                dmc.Progress(id="input-takesurvey-progress-slider", size="xl",value=survey_progess_percent,label=str(survey_progess_percent) + " %",animate=False,striped=False  ),
                html.Br(),
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            dbc.Accordion([
                                dbc.AccordionItem(
                                    [
                                        dbc.Form([
                                            html.Br(),
                                            html.Div(children=[
                                                dbc.Label(str(overall_structure_var_question[var].index(question)+1) + ". " + question["question"]["question_text"],style={"font-weight": "bold"}),
                                                dbc.Checklist(
                                                    options=[{'label':option,'value': question["question"]["question_unique_id"] + '#option_index=' + str(question["question"]["options"].index(option)),'disabled': 'question_scores' in question.keys()} for option in question["question"]["options"]],
                                                    value=[question["question"]["question_unique_id"] + '#option_index=' + str(v) for v in question["question_scores"]["question_selected_score_indices"]] if "question_scores" in question.keys() else [],
                                                    id={"type":"dynamic-checklist", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]},
                                                    switch=True,
                                                ) if question["question"]["question_type"] == "multi_select" else "",
                                                dbc.RadioItems(
                                                    options= [{'label':option,'value': question["question"]["question_unique_id"] + '#option_index=' +  str(question["question"]["options"].index(option)),'disabled': 'question_scores' in question.keys()} for option in question["question"]["options"]],
                                                    value=question["question"]["question_unique_id"] + '#option_index=' + str(question["question_scores"]["question_selected_score_indices"][0]) if "question_scores" in question.keys() else [],
                                                    id={"type":"dynamic-radioitems", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]},
                                                ) if question["question"]["question_type"] == "single_select" else "",
                                                #dbc.Input(id={"type":"dynamic-textbox", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]}, placeholder="Type something...", type="text") if question["question"]["question_type"] == "Text" else "",
                                                dbc.Textarea(
                                                    id={"type":"dynamic-textbox", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]}, 
                                                    placeholder="Type something...", 
                                                    size="lg", 
                                                    value = question["question_scores"]["answer_text"] if "question_scores" in question.keys()  and "answer_text" in question["question_scores"].keys() else "",
                                                    disabled='question_scores' in question.keys()
                                                    ) if question["question"]["question_type"] == "text"  else "",
                                                html.Br(),
                                                dbc.Textarea(
                                                    id={"type":"dynamic-textbox-for-options", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]}, 
                                                    placeholder="Type something...", 
                                                    size="lg", 
                                                    value = question["question_scores"]["answer_text"] if "question_scores" in question.keys()  and "answer_text" in question["question_scores"].keys() else "",
                                                    disabled='question_scores' in question.keys(),
                                                    style={'display':'block'} if "question_scores" in question.keys() and "answer_text" in question["question_scores"].keys() else {'display':'None'}
                                                    ) if question["question"]["question_type"] != "text" and any("specify".upper() in s.upper() for s in question["question"]["options"])  else "",
                                                #html.Div({"type":"dynamic-textbox-for-options", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]}) if question["question"]["question_type"] != "Text"  else "",
                                                html.Br(),
                                                du.Upload(
                                                    id={"type":"dynamic-upload", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]},
                                                    max_file_size=1800,  # 1800 Mb
                                                    text='Upload evidence:  csv,zip,docx,xlsx,png,jpg allowed',
                                                    text_completed='Uploaded: ',
                                                    text_disabled='Upload evidence disabled, please find below the list of uploaded evidence.',
                                                    disabled='question_scores' in question.keys(),
                                                    cancel_button=True,
                                                    pause_button=True,
                                                    default_style = {
                                                        'width': '20%',
                                                        'height': '80px',
                                                        'lineHeight': '60px',
                                                        'borderWidth': '1px',
                                                        'borderStyle': 'dashed',
                                                        'borderRadius': '5px',
                                                        'textAlign': 'center',
                                                        'margin': '0px',
                                                        'margin-bottom' : '10px',
                                                        'color' : 'green'
                                                    },
                                                    filetypes=['csv', 'zip', 'docx', 'txt', 'png', 'jpg', 'xlsx'],
                                                    upload_id=survey_id["survey_id"] + '_' + question["question"]["question_unique_id"],  # question unique id
                                                ) if question["question"]["doc_upload_flag"] == "Yes" else "",
                                                html.H6("Evidence List :") if question["question"]["doc_upload_flag"] == "Yes" else "",
                                                html.Div(
                                                    children = render_list_of_files_for_download_div(survey_id,question["question"]["question_unique_id"])[0],
                                                    id={"type":"dynamic-div-download", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]}
                                                ) if question["question"]["doc_upload_flag"] == "Yes" else "",
                                                html.Br(),
                                                dmc.Group(
                                                    children=[
                                                        dmc.Button(
                                                            "Save", 
                                                            leftIcon=[DashIconify(
                                                                        icon="fluent:save-arrow-right-20-filled",
                                                                        width=20,
                                                                        height=20,
                                                                        #rotate=1,
                                                                        #flip="horizontal",
                                                                    )],
                                                            color="lime",
                                                            id={"type":"dynamic-save", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]},
                                                            loading=False,
                                                            disabled='question_scores' in question.keys()
                                                        ),
                                                        dmc.Tooltip(
                                                            label="Unfreeze question",
                                                            position="right",
                                                            #placement="center",
                                                            #gutter=3,
                                                            children=dmc.Button(
                                                                    "Reset",
                                                                    leftIcon=[DashIconify(
                                                                        icon="material-symbols:lock-reset-rounded",
                                                                        width=20,
                                                                        height=20,
                                                                        #rotate=1,
                                                                        #flip="horizontal",
                                                                    )],
                                                                    color="red",
                                                                    id={"type":"dynamic-reset", "question_id":question["question"]["question_unique_id"], "question_type": question["question"]["question_type"],"doc_upload_flag" : question["question"]["doc_upload_flag"]},
                                                                    #disabled='question_scores' in question.keys()
                                                                )
                                                        ),
                                                    ],
                                                    #direction = "row",
                                                    position = "left",
                                                    spacing = "sm"  
                                                ),
                                                html.Div(id="dynamic-temp-div-takesurvey",style={'display':'None'})
                                            ])
                                        ])
                                        for question in overall_structure_var_question[var]
                                    ],
                                    title=var
                                )
                                for var in overall_structure_lever_var[lever]
                            ]), 
                            title=lever
                        )
                        for lever in overall_structure_lever_var.keys()
                    ],
                    flush=True,
                ),
            ])
    return html.Div([
        dbc.Container([
            dbc.Row([
                html.Br(),
            ]),
            dbc.Row([
                accordion_lever
            ])
        ],
        fluid=True)
    ])

@dash.callback(
            [
                Output('input-takesurvey-tabs-content', 'children'),
                Output('take-survey-page-main-div-id', 'style'),
            ],
            Input('input-takesurvey-tabs', 'value'),
            State("input-takesurvey-store-survey-id", "data"))
def render_content(tab,survey_id):
    if tab == 'intro':
        client_name_list,domain_name_list,pillar_name_list,lever_name_list,variables_name_list = mongodb_utility.get_distinct("client_dtl")
        client_name_list = [" "] + client_name_list
        domain_name_list = [" "] + domain_name_list
        client_name_dd_items =[dbc.DropdownMenuItem("Select Client")] + [dbc.DropdownMenuItem(divider=True)]  + [dbc.DropdownMenuItem(client, id={"type":"dynamic-take-survey-client", "identifier":client}) for client in client_name_list]
        domain_name_dd_items =[dbc.DropdownMenuItem("Select Domain")] + [dbc.DropdownMenuItem(divider=True)]  + [dbc.DropdownMenuItem(domain, id={"type":"dynamic-take-survey-domain", "identifier":domain}) for domain in domain_name_list]
        introduction_content =   dbc.Container([
                                                # dbc.Row([
                                                #     dbc.Col([
                                                #         html.Br()
                                                #     ])
                                                    
                                                # ]),
                                                # dbc.Row([
                                                #     dbc.Col([
                                                #         dbc.InputGroup(
                                                #             [
                                                #                 dbc.DropdownMenu(
                                                #                 children=client_name_dd_items, 
                                                #                 style ={"width":"100%", "text-align": "center"}, 
                                                #                 id="input-takesurvey-client-name-dd",
                                                #                 direction="start",
                                                #                 label="Client"),
                                                #                 dbc.Input(id="input-takesurvey-client-name-textbox", placeholder="Select Client", class_name="textboxes"),
                                                #             ]
                                                #         ),
                                                #     ]),
                                                #     dbc.Col([
                                                #         dbc.InputGroup(
                                                #             [
                                                #                 dbc.DropdownMenu(
                                                #                 children=domain_name_dd_items, 
                                                #                 style ={"width":"100%", "text-align": "center"}, 
                                                #                 id="input-takesurvey-domain-name-dd",
                                                #                 direction="start",
                                                #                 label="Domain"),
                                                #                 dbc.Input(id="input-takesurvey-domain-name-textbox", placeholder="Select Domain", class_name="textboxes"),
                                                #             ]
                                                #         ),
                                                #     ])
                                                # ]),
                                                # dbc.Row([
                                                #     html.Br()
                                                # ]),
                                                # dbc.Row([
                                                #     dbc.Col([
                                                #         dbc.InputGroup(
                                                #             [
                                                #                 dbc.InputGroupText("Company Name"),
                                                #                 dbc.Input(placeholder="Name of the Company",id="input-takesurvey-company-name-textbox", class_name="textboxes"),
                                                #             ]
                                                #         )
                                                #     ]),
                                                #     dbc.Col([
                                                #         dbc.InputGroup(
                                                #             [
                                                #                 dbc.InputGroupText("Company Size"),
                                                #                 dbc.Input(placeholder="Size of the Company",id="input-takesurvey-company-size-textbox", class_name="textboxes"),
                                                #             ]
                                                #         )
                                                #     ])
                                                    
                                                # ]),
                                                dbc.Row([
                                                    html.Br()
                                                ]),
                                                dbc.Row([
                                                    dbc.Col([
                                                        dbc.InputGroup(
                                                            [
                                                                dbc.InputGroupText("Survey Id"),
                                                                dbc.Input(id="input-takesurvey-surveyid-textbox", placeholder="Please provide the survey id given to you", class_name="textboxes"),
                                                            ]
                                                        )
                                                    ],
                                                    width={'size':'6'})
                                                    
                                                ]),
                                                dbc.Row([
                                                    dbc.Col([
                                                        html.Br(),
                                                        #dbc.Button("Next", color="success",id="input-takesurvey-intro-next-btn"),
                                                        dmc.Button(
                                                                    "Next",
                                                                    leftIcon=[DashIconify(
                                                                        icon="fluent:next-24-filled",
                                                                        width=20,
                                                                        height=20,
                                                                        #rotate=1,
                                                                        #flip="horizontal",
                                                                    )],
                                                                    color="grape",
                                                                    id="input-takesurvey-intro-next-btn"
                                                                )
                                                    ],
                                                    width={'size':'3'})
                                                    
                                                ]),
                                            ],
                                            fluid=True)
        return [html.Div([
            html.Br(),
            introduction_content
        ]),{'backgroundColor':'white'}]
    elif tab == 'environment':
        content=get_esg_tab_content(survey_id,"Environment")
        return [content,{'backgroundColor':'#E2F0D9'}]
    elif tab == 'social':
        content=get_esg_tab_content(survey_id,"Social")
        return [content,{'backgroundColor':'#FFF2CC'}]
    elif tab == 'gov':
        content=get_esg_tab_content(survey_id,"Governance")
        return [content,{'backgroundColor':'#DEEBF7'}]
    elif tab == "submit":
        survey_progress_percent = mongodb_utility.get_survey_progress(survey_id["survey_id"])
        #print(survey_progress_percent)
        env_pie_chart_data = [{'Name':'Answered','Value': float(survey_progress_percent['Environment_progress_percent'])},{'Name':'Unanswered','Value': 100 - float(survey_progress_percent['Environment_progress_percent'])}]
        env_pie_chart_df = pd.DataFrame(env_pie_chart_data)
        #print(env_pie_chart_df)
        env_pie_fig = px.pie(
                        env_pie_chart_df,
                        values='Value', 
                        names='Name',
                        hole=0.3
                    )
        env_pie_fig.update_layout(
            uniformtext=dict(minsize=10,mode=None),
            height=400,
            showlegend=True,
            plot_bgcolor="FloralWhite",
            paper_bgcolor='DarkSlateGray',
            title={
                'text': "Environment",
                'y':0.95,
                'x':0.45,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="white"
            ),
            annotations=[dict(text=str("Score Confidence {}%".format(survey_progress_percent['Environment_progress_percent'])),x=0.5, y=-0.15,font_size = 20, showarrow=False)],
        )

        soc_pie_chart_data = [{'Name':'Answered','Value': float(survey_progress_percent['Social_progress_percent'])},{'Name':'Unanswered','Value': 100 - float(survey_progress_percent['Social_progress_percent'])}]
        soc_pie_chart_df = pd.DataFrame(soc_pie_chart_data)
        #print(env_pie_chart_df)
        soc_pie_fig = px.pie(soc_pie_chart_df,values='Value', names='Name',hole=0.3)
        soc_pie_fig.update_layout(
            uniformtext=dict(minsize=10,mode=None),
            height=400,
            showlegend=True,
            plot_bgcolor="FloralWhite",
            paper_bgcolor='DarkSlateGray',
            title={
                'text': "Social",
                'y':0.95,
                'x':0.45,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="white"
            ),
            annotations=[dict(text=str("Score Confidence {}%".format(survey_progress_percent['Social_progress_percent'])),x=0.5, y=-0.15,font_size = 20, showarrow=False)]
        )

        gov_pie_chart_data = [{'Name':'Answered','Value': float(survey_progress_percent['Governance_progress_percent'])},{'Name':'Unanswered','Value': 100 - float(survey_progress_percent['Governance_progress_percent'])}]
        gov_pie_chart_df = pd.DataFrame(gov_pie_chart_data)
        #print(env_pie_chart_df)
        gov_pie_fig = px.pie(gov_pie_chart_df,values='Value', names='Name',hole=0.3)
        gov_pie_fig.update_layout(
            uniformtext=dict(minsize=10,mode=None),
            height=400,
            showlegend=True,
            plot_bgcolor="FloralWhite",
            paper_bgcolor='DarkSlateGray',
            title={
                'text': "Governance",
                'y':0.95,
                'x':0.45,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="white"
            ),
            annotations=[dict(text=str("Score Confidence {}%".format(survey_progress_percent['Governance_progress_percent'])),x=0.5, y=-0.15,font_size = 20, showarrow=False)]
        )
        #table_data = [mongodb_utility.get_survey_progress(survey_id["survey_id"])]
        return [html.Div([
        dbc.Container([
            dbc.Row([
                html.Br(),
                #dbc.Label("You have answered {}% of the questions, Are you ready to view score?".format(survey_progress_percent),style={"font-weight": "bold"}),
                dmc.Blockquote(
                    "You have answered {}% of the questions, Are you ready to view score?".format(survey_progress_percent["overall_progress_percent"]),
                    #cite="- Ironman",
                    icon=[DashIconify(icon="ci:notification-active", width=30)],
                    color="red",
                )
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=env_pie_fig),
                ],width=4),
                dbc.Col([
                    dcc.Graph(figure=soc_pie_fig),
                ],width=4),
                dbc.Col([
                    dcc.Graph(figure=gov_pie_fig),
                ],width=4),
            ]),
            dbc.Row([
                
                 #html.Br(),
                dbc.Col([
                    html.Br(),
                    #dbc.Button("Submit & View Score", color="success",id="input-takesurvey-final-submit-btn")
                    dmc.Button(
                        "View Score",
                        id="input-takesurvey-final-submit-btn",
                        color="lime",
                        leftIcon=[DashIconify(icon="fluent:send-16-filled")],
                    ),
                ])
            ]),
            dbc.Row([
                html.Div(id="submitted-survey-viewscorediv")
            ])
        ],
        fluid=True)
    ]),{'backgroundColor':'white'}]
        

## Callback to handle the client name dropdown
@dash.callback(
    Output("input-takesurvey-client-name-textbox", "value"),
    [
        Input({"type": "dynamic-take-survey-client", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])



## Callback to handle the domain name dropdown
@dash.callback(
    Output("input-takesurvey-domain-name-textbox", "value"),
    [
        Input({"type": "dynamic-take-survey-domain", "identifier": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def on_button_click(n):
    ctx = dash.callback_context
    return str(ctx.triggered_id["identifier"])

## Callback to go to next tab
@dash.callback(
    [Output("input-takesurvey-environment-tab", "disabled"),
    Output("input-takesurvey-social-tab", "disabled"),
    Output("input-takesurvey-gov-tab", "disabled"),
    Output("input-takesurvey-submit-tab", "disabled"),
    Output("input-takesurvey-tabs", "value"),
    Output("input-takesurvey-store-survey-id", "data")],
    [
        Input("input-takesurvey-intro-next-btn", "n_clicks"),
        State("input-takesurvey-surveyid-textbox", "value"),
        #State("input-takesurvey-client-name-textbox", "value"),
        #State("input-takesurvey-domain-name-textbox", "value"),
        # State("input-takesurvey-company-name-textbox", "value"),
        # State("input-takesurvey-company-size-textbox", "value"),
    ],
    prevent_initial_call=True
)
#def go_to_next_tab(n,survey_id,client_name,domain_name,company_name,company_size):
def go_to_next_tab(n,survey_id):
    # ctx = dash.callback_context
    data = {}
    # data_for_db = {}
    # #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
    # client = mongodb_utility.connect_to_mongodb(mongodb_config.conn_str)
    # db = client["esg"]
    # collection = db["survey_client_info"]
    if n:
        if survey_id:
            data["survey_id"] = survey_id
        #     data_for_db["survey_id"] = survey_id
        #     data_for_db["client_name"] = client_name
        #     data_for_db["domain_name"] = domain_name
        #     data_for_db["company_name"] = company_name
        #     data_for_db["company_size"] = company_size
        #     collection.insert_one(data_for_db)
        return [False,False,False,False,"environment",data]
    else:
        return [True,True,True,True,"intro",data]


def file_download_link(filename,survey_id,question_id):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}/{}".format(survey_id + '_' + question_id,urlquote(filename))
    return html.A(filename, href=location)

def render_list_of_files_for_download_div(survey_id,question_id):
    UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__),'..','uploaded_evidence', survey_id["survey_id"] + '_' + question_id)
    files = []
    download_links = []
    if os.path.exists(UPLOAD_DIRECTORY):
        for filename in os.listdir(UPLOAD_DIRECTORY):
            path = os.path.join(UPLOAD_DIRECTORY, filename)
            if os.path.isfile(path):
                files.append(filename)
    #print(files)
    if len(files) == 0:
        download_links.append(html.Li("No evidence uploaded!"))
    else:
        download_links.append(
            [
                # html.Li(file_download_link(filename,survey_id["survey_id"],question_id)) 
                dmc.Group(
                    children=[
                        html.Li(file_download_link(filename,survey_id["survey_id"],question_id)), 
                        dbc.Button(
                            id={"type":"dynamic-remove-evidence", "question_id":question_id, "filename": filename},
                            className="bi bi-x  py-0 px-1 mx-0 my-0", 
                            color="danger", 
                            outline=True, 
                            style={"border":"None"}
                        )
                    ],
                    #direction = "row",
                    position = "left",
                    spacing = "sm"  
                )
                for filename in files
            ]
        )
    return download_links

def get_progress_color(progress_val):
    color = "red"
    if progress_val >= 20:
        color = "blue"
    if progress_val >= 40:
        color = "cyan"
    if progress_val >= 70:
        color = "teal"
    if progress_val == 100:
        color = "green"
    return color

###################################################################
'''
The below callback does the following"
1. Saves the question response to DB upon clicking on the save button.
2. Reset a particular question response upon clicking on the reset button.
3. Remove uploaded evidence upon clicking on the croxx button.
'''
###################################################################

@dash.callback(
    [
        Output("dynamic-temp-div-takesurvey", "children"),
        Output("input-takesurvey-progress-slider", "value"),
        Output("input-takesurvey-progress-slider", "label"),
        Output("input-takesurvey-progress-slider", "color"),
        Output({"type": "dynamic-save", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "disabled"),
        Output({"type": "dynamic-radioitems", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "options"),
        Output({"type": "dynamic-checklist", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "options"),
        Output({"type": "dynamic-upload", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "disabled"),
        Output({"type": "dynamic-textbox", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "disabled"),
        Output({"type": "dynamic-div-download", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "children"),
        Output({"type": "dynamic-textbox-for-options", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "disabled"),
    ],
    [
        Input({"type": "dynamic-save", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "n_clicks"),
        Input({"type": "dynamic-reset", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "n_clicks"),
        Input({"type":"dynamic-remove-evidence", "question_id":ALL, "filename": ALL}, "n_clicks")
    ],
    [
        State({"type": "dynamic-checklist", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "value"),
        State({"type": "dynamic-checklist", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "options"),
        State({"type": "dynamic-radioitems", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "value"),
        State({"type": "dynamic-radioitems", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "options"),
        State({"type": "dynamic-textbox", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "value"),
        State({"type": "dynamic-textbox", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "id"),
        State({"type": "dynamic-textbox", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "disabled"),
        State({"type": "dynamic-upload", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "id"),
        State({"type": "dynamic-upload", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "disabled"),
        State({"type": "dynamic-save", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "disabled"),
        State({"type": "dynamic-save", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "id"),
        State({"type": "dynamic-textbox-for-options", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "value"),
        State({"type": "dynamic-textbox-for-options", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "id"),
        State({"type": "dynamic-textbox-for-options", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "disabled"),
        State({"type":"dynamic-remove-evidence", "question_id":ALL, "filename": ALL}, "id"),
        State({"type": "dynamic-div-download", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "children"),
        State({"type": "dynamic-div-download", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "id"),
        State("input-takesurvey-store-survey-id", "data"),
    ],
    prevent_initial_call=True
)
def on_button_click(
        n,
        n_reset,
        n_del_ev,
        multiselect_value,
        multiselect_options,
        multichoice_value,
        multichoice_options,
        text_value,
        textbox_ids,
        textbox_disable_states,
        uploaded_ids,
        uploaded_disable_states,
        save_btn_cur_state,
        save_btn_ids,
        textbox_for_options_value,
        textbox_for_options_id,
        textbox_for_options_disabled,
        cross_btn_ids,
        download_div_childrens,
        download_div_ids,
        survey_id
    ):
    ctx = dash.callback_context
    question_id = ctx.triggered_id["question_id"]
    if "question_type" in ctx.triggered_id.keys():
        question_type = ctx.triggered_id["question_type"]
    else:
        question_type = " "
    if "doc_upload_flag" in ctx.triggered_id.keys():
        doc_upload_flag = ctx.triggered_id["doc_upload_flag"]
    else:
        doc_upload_flag = " "
    if "filename" in ctx.triggered_id.keys():
        filename = ctx.triggered_id["filename"]
    else:
        filename = " "
    #client = MongoClient(mongodb_config.conn_str,tlsCAFile=certifi.where())
    client = mongodb_utility.connect_to_mongodb(mongodb_config.conn_str)
    db = client["esg"]
    #collection = db["survey_score"]
    collection = db["survey_response"]
    data_for_db = {}
    #print(ctx.triggered_id)
    #print(textbox_for_options_value)
    if ctx.triggered_id == {'doc_upload_flag': doc_upload_flag, 'question_id': question_id, 'question_type': question_type, 'type': 'dynamic-save'}:
        if question_type == "multi_select":
            for data in multiselect_value:
                if len(data) > 0:
                    selected_options_indices = [ d.split('=')[1] for d in data if question_id in d ]
                    if len(selected_options_indices) > 0:
                        data_for_db["survey_unique_id"] = survey_id["survey_id"]
                        data_for_db["question_unique_id"] = question_id
                        data_for_db["question_type"] = question_type
                        data_for_db["question_selected_score_indices"] = selected_options_indices
                        data_for_db["score_submitted"] = "Yes"
            id_for_current_option_textbox = {"type": "dynamic-textbox-for-options", "question_id": question_id, "question_type": question_type,"doc_upload_flag" : doc_upload_flag}
            if id_for_current_option_textbox in textbox_for_options_id:
                index = textbox_for_options_id.index(id_for_current_option_textbox)
                value = textbox_for_options_value[index]
                data_for_db["answer_text"] = value
            collection.insert_one(data_for_db)
        if question_type == "single_select":
            for data in multichoice_value:
                if len(data) > 0:
                    selected_options_indices = [ data.split('=')[1] if question_id in data else "None"]
                    if "None" not in selected_options_indices:
                        data_for_db["survey_unique_id"] = survey_id["survey_id"]
                        data_for_db["question_unique_id"] = question_id
                        data_for_db["question_type"] = question_type
                        data_for_db["question_selected_score_indices"] = selected_options_indices
                        data_for_db["score_submitted"] = "Yes"
            id_for_current_option_textbox = {"type": "dynamic-textbox-for-options", "question_id": question_id, "question_type": question_type,"doc_upload_flag" : doc_upload_flag}
            if id_for_current_option_textbox in textbox_for_options_id:
                index = textbox_for_options_id.index(id_for_current_option_textbox)
                value = textbox_for_options_value[index]
                data_for_db["answer_text"] = value
            #print(data_for_db)
            collection.insert_one(data_for_db)
        if question_type == "text":
            #print(text_value)
            for data in text_value:
                if len(data) > 0:
                    selected_options_indices = []
                    data_for_db["survey_unique_id"] = survey_id["survey_id"]
                    data_for_db["question_unique_id"] = question_id
                    data_for_db["question_type"] = question_type
                    data_for_db["question_selected_score_indices"] = selected_options_indices
                    data_for_db["score_submitted"] = "Yes"
                    data_for_db["answer_text"] = data
            collection.insert_one(data_for_db)
        
        survey_progress_percent = mongodb_utility.get_survey_progress(survey_id["survey_id"])["overall_progress_percent"]
        survey_progress_label = f"{survey_progress_percent} %"
        survey_progress_color = get_progress_color(survey_progress_percent)
        #print(multichoice_value)
        ## Code for disabling the save button and options textboxes (if any) after question answer is getting saved in DB
        clicked_save_btn_id = {"type": "dynamic-save", "question_id": question_id, "question_type": question_type,"doc_upload_flag" : doc_upload_flag}
        clicked_save_btn_index = save_btn_ids.index(clicked_save_btn_id)
        disable_button_list = save_btn_cur_state
        disable_button_list[clicked_save_btn_index] = True
        
        
        diable_option_textbox_list = textbox_for_options_disabled
        if len(textbox_for_options_id) > 0:
            current_option_textbox_id = {"type": "dynamic-textbox-for-options", "question_id": question_id, "question_type": question_type,"doc_upload_flag" : doc_upload_flag}
            if current_option_textbox_id in textbox_for_options_id:
                current_option_textbox_index = textbox_for_options_id.index(current_option_textbox_id)
                diable_option_textbox_list[current_option_textbox_index] = True

        final_option_list_mc = []
        for mc in multichoice_options:
            each_question_option_list_mc = []
            for o in mc:
                if str(question_id) in o["value"]:
                    o["disabled"] = True
                    #print(o)
                each_question_option_list_mc.append(o)
            final_option_list_mc.append(each_question_option_list_mc)
        
        final_option_list_ms = []
        for ms in multiselect_options:
            each_question_option_list_ms = []
            for o in ms:
                if str(question_id) in o["value"]:
                    o["disabled"] = True
                    #print(o)
                each_question_option_list_ms.append(o)
            final_option_list_ms.append(each_question_option_list_ms)
        

        final_list_txt = [i["question_id"]  == question_id and i["question_type"]  == question_type and i["doc_upload_flag"]  == doc_upload_flag for i in textbox_ids]

        disable_upload_button_list = []
        #download_links = []
        for i in uploaded_ids:
            disable_upload_button_list.append(i["question_id"]  == question_id and i["question_type"]  == question_type and i["doc_upload_flag"]  == doc_upload_flag)
            
        download_links = download_div_childrens
        for i in download_div_ids:
            if i["question_id"]  == question_id and i["question_type"]  == question_type and i["doc_upload_flag"]  == doc_upload_flag:
                index = download_div_ids.index(i)
                download_links[index]= render_list_of_files_for_download_div(survey_id,question_id)[0]
        #print(download_links)
    if ctx.triggered_id == {'doc_upload_flag': doc_upload_flag, 'question_id': question_id, 'question_type': question_type, 'type': 'dynamic-reset'}:
        collection.delete_many({'survey_unique_id': survey_id["survey_id"], 'question_unique_id' : question_id})
        survey_progress_percent = mongodb_utility.get_survey_progress(survey_id["survey_id"])["overall_progress_percent"]
        survey_progress_label = f"{survey_progress_percent} %"
        survey_progress_color = get_progress_color(survey_progress_percent)

        clicked_save_btn_id = {"type": "dynamic-save", "question_id": question_id, "question_type": question_type,"doc_upload_flag" : doc_upload_flag}
        clicked_save_btn_index = save_btn_ids.index(clicked_save_btn_id)
        disable_button_list = save_btn_cur_state
        disable_button_list[clicked_save_btn_index] = False
        
        diable_option_textbox_list = textbox_for_options_disabled
        if len(textbox_for_options_id) > 0:
            current_option_textbox_id = {"type": "dynamic-textbox-for-options", "question_id": question_id, "question_type": question_type,"doc_upload_flag" : doc_upload_flag}
            if current_option_textbox_id in textbox_for_options_id:
                current_option_textbox_index = textbox_for_options_id.index(current_option_textbox_id)
                diable_option_textbox_list[current_option_textbox_index] = False

        final_option_list_mc = []
        for mc in multichoice_options:
            each_question_option_list_mc = []
            for o in mc:
                if str(question_id) in o["value"]:
                    o["disabled"] = False
                    #print(o)
                each_question_option_list_mc.append(o)
            final_option_list_mc.append(each_question_option_list_mc)
        
        final_option_list_ms = []
        for ms in multiselect_options:
            each_question_option_list_ms = []
            for o in ms:
                if str(question_id) in o["value"]:
                    o["disabled"] = False
                    #print(o)
                each_question_option_list_ms.append(o)
            final_option_list_ms.append(each_question_option_list_ms)
        
        final_list_txt = [not (i["question_id"]  == question_id and i["question_type"]  == question_type and i["doc_upload_flag"]  == doc_upload_flag) for i in textbox_ids]
        
        disable_upload_button_list = []
        
        for i in uploaded_ids:
            disable_upload_button_list.append( not (i["question_id"]  == question_id and i["question_type"]  == question_type and i["doc_upload_flag"]  == doc_upload_flag))
        
        download_links = download_div_childrens
        for i in download_div_ids:
            if i["question_id"]  == question_id and i["question_type"]  == question_type and i["doc_upload_flag"]  == doc_upload_flag:
                index = download_div_ids.index(i)
                download_links[index]= render_list_of_files_for_download_div(survey_id,question_id)[0]
    
    if ctx.triggered_id == {"type":"dynamic-remove-evidence", "question_id":question_id, "filename": filename}: 

        ## returning the survey progress percent as is
        survey_progress_percent = mongodb_utility.get_survey_progress(survey_id["survey_id"])["overall_progress_percent"]
        survey_progress_label = f"{survey_progress_percent} %"
        survey_progress_color = get_progress_color(survey_progress_percent)

        ## returning the current state of teh save button as is
        disable_button_list = save_btn_cur_state

        ## returning the multi choice question options as is
        final_option_list_mc = multichoice_options

        ## returning the multiselect options as is
        final_option_list_ms = multiselect_options

        ## Keeping the uploaded button in their current state
        disable_upload_button_list = uploaded_disable_states

        ## Keeping the textboxes in their own state
        final_list_txt = textbox_disable_states

        ## keeping option level textboxes in their own state
        diable_option_textbox_list = textbox_for_options_disabled

        ## Deleting the evidence
        UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__),'..','uploaded_evidence', survey_id["survey_id"] + '_' + question_id)
        if os.path.exists(UPLOAD_DIRECTORY):
            for f in os.listdir(UPLOAD_DIRECTORY):
                if f == filename:
                    print(f)
                    os.remove(os.path.join(UPLOAD_DIRECTORY,f))
        
        ## refreshing the evidence list div
        download_links = download_div_childrens
        for i in download_div_ids:
            if i["question_id"]  == question_id:
                index = download_div_ids.index(i)
                download_links[index]= render_list_of_files_for_download_div(survey_id,question_id)[0]

    return [str(question_id),survey_progress_percent,survey_progress_label,survey_progress_color,disable_button_list,final_option_list_mc,final_option_list_ms,disable_upload_button_list,final_list_txt,download_links,diable_option_textbox_list]


def customwrap(s,width=12):
    return "<br>".join(textwrap.wrap(s,width=width))


def get_color_map(percent_value):
    if percent_value > 70 :
        return '#83B254'
    elif percent_value >=40 and percent_value <=70:
        return '#FFCC00'
    else:
        return '#EB5555'

## Callback to calculate score
@dash.callback(
    Output("submitted-survey-viewscorediv", "children"),
    [
        Input("input-takesurvey-final-submit-btn", "n_clicks"),
    ],
    [
        State("input-takesurvey-store-survey-id", "data")
    ],
    prevent_initial_call=True
)
def view_score(n,survey_id):
    if n:
        submitted_survey_dtl = mongodb_utility.get_survey_dtls(survey_id["survey_id"])
        final_scoring_structure = []
        e_score = 0
        s_score = 0
        g_score = 0
        esg_level=" "
        esg_level_color="red"
        msg = ""
        indv_question_score = 0

        max_pos_score_by_pillar,max_pos_score_by_lever = mongodb_utility.get_max_possible_scores(survey_id["survey_id"])
        print(max_pos_score_by_pillar)
        print(max_pos_score_by_lever)

        for response in submitted_survey_dtl:
            if "question_scores" in response.keys():
                if response["question"]["question_type"] == "single_select":
                    selected_option_abs_score = float(response["question"]["option_absolute_score"][int(response["question_scores"]["question_selected_score_indices"][0])])
                    indv_question_score = selected_option_abs_score *  float(response["weightage"])
                    #print(indv_question_score)
                elif response["question"]["question_type"] == "multi_select":
                    selected_option_abs_score = []
                    for score_index in response["question_scores"]["question_selected_score_indices"]:
                        selected_option_abs_score.append(float(response["question"]["option_absolute_score"][int(score_index)]))
                    selected_option_abs_score_sum = sum(selected_option_abs_score)
                    indv_question_score = selected_option_abs_score_sum *  float(response["weightage"])
                    #print(indv_question_score)
                if response['pillar'] == 'Environment':
                    e_score += indv_question_score
                if response['pillar'] == 'Social':
                    s_score += indv_question_score
                if response['pillar'] == 'Governance':
                    g_score += indv_question_score  

                final_scoring_structure.append(
                    {
                        "Pillar": response["pillar"],
                        "lever": response["lever"],
                        #"variable": response["question"]["variable"],
                        "indv_question_score": indv_question_score,
                        #"color" : "green",
                        'label_category': 'lever'
                    }
                )

        combined_score = e_score + s_score  + g_score

        if combined_score >= 70:
            esg_level="LEADER" 
            esg_level_color = "#83B254"
            msg="The organization is leading in managing ESG risks and opportunities."
            msgdetail="The activity of the organization is compatible with long term sustainable economy. The organization already contributes to reduce its impacts towards ESG balances through actively reducing the carbon footprints and energy consumption while sustainably utilizing resources (through Business, Workforce and IT operations)."
            esg_level_badge = dmc.Badge(
                                esg_level, 
                                size="xl",
                                variant="gradient",
                                gradient={"from": esg_level_color, "to": esg_level_color},
                                color="dark" 
                            )
            esg_msg_badge = dmc.Badge(
                                msg, 
                                size="xl",
                                variant="gradient",
                                gradient={"from": esg_level_color, "to": esg_level_color},
                                color="dark" 
                            )
            esg_msgdtl_paper = dmc.Paper(msgdetail,shadow="xl", style={'border-color': 'DarkSlateGray','border-style': 'solid','background-image': 'linear-gradient(to right,' +  esg_level_color + ', white )'})
        elif combined_score < 70 and combined_score > 40:
            esg_level="REACTIVE"
            esg_level_color="#FFCC00"
            msg="The organization is having mixed or reactive track record of managing ESG risks."
            msgdetail="The activity of the organization is not sustainable. The organization needs to work more actively for reduction of the carbon footprints and energy consumption while sustainably utilizing resources. The organization demonstrates willingness to reduce its impacts on the wider environment and community (through Business, Workforce and IT operations)."
            esg_level_badge = dmc.Badge(
                                esg_level, 
                                size="xl",
                                variant="gradient",
                                gradient={"from": esg_level_color, "to": esg_level_color},
                                color="dark" 
                            )
            esg_msg_badge = dmc.Badge(
                                msg, 
                                size="xl",
                                variant="gradient",
                                gradient={"from": esg_level_color, "to": esg_level_color},
                                color="dark" 
                            )
            esg_msgdtl_paper = dmc.Paper(msgdetail,shadow="xl", style={'border-color': 'DarkSlateGray','border-style': 'solid','background-image': 'linear-gradient(to right,' +  esg_level_color + ', white )'})
        elif combined_score <= 40:
            esg_level="LAGGARD"
            esg_level_color = "#EB5555"
            msg="The organization is lagging on ESG parameters with highlighted inability to manage ESG risks."
            msgdetail="The activity of the organization is not sustainable. The organization is not working towards reduction of carbon footprints and sustainable utilization of resources contributing to a rapid deterioration of environment. The organization also does not demonstrate willingness to reduce its impacts on the wider environment and community (through Business, Workforce and IT operations)."
            esg_level_badge = dmc.Badge(
                                esg_level, 
                                size="xl",
                                variant="gradient",
                                gradient={"from": esg_level_color, "to": esg_level_color},
                                color="dark" 
                            )
            esg_msg_badge = dmc.Badge(
                                msg, 
                                size="xl",
                                variant="gradient",
                                gradient={"from": esg_level_color, "to": esg_level_color},
                                color="dark" 
                            )
            esg_msgdtl_paper = dmc.Paper(msgdetail,shadow="xl", style={'border-color': 'DarkSlateGray','border-style': 'solid','background-image': 'linear-gradient(to right,' +  esg_level_color + ', white )'})
        
        final_scoring_structure.append({"Pillar" : esg_level, "lever" : 'Environment',  'indv_question_score' : e_score,'label_category': 'pillar'})
        final_scoring_structure.append({"Pillar" : esg_level, "lever" : 'Social',  'indv_question_score' : s_score,'label_category': 'pillar'})
        final_scoring_structure.append({"Pillar" : esg_level, "lever" : 'Governance',  'indv_question_score' : g_score,'label_category': 'pillar'})
        final_scoring_df = pd.DataFrame(final_scoring_structure)
        final_scoring_df = final_scoring_df.groupby(['Pillar','lever','label_category'],as_index = False)['indv_question_score'].sum()
        colors = []
        output_df = final_scoring_df
        for index, row in final_scoring_df.iterrows():
            if row["label_category"] == "pillar":
                if row["lever"] == "Environment":
                    e_score_percent_pillar_level = (e_score/max_pos_score_by_pillar["e_possible_score"]) * 100
                    colors.append(get_color_map(e_score_percent_pillar_level))
                if row["lever"] == "Social":
                    s_score_percent_pillar_level = (s_score/max_pos_score_by_pillar["s_possible_score"]) * 100
                    colors.append(get_color_map(s_score_percent_pillar_level))
                if row["lever"] == "Governance":
                    g_score_percent_pillar_level = (g_score/max_pos_score_by_pillar["g_possible_score"]) * 100
                    colors.append(get_color_map(g_score_percent_pillar_level))
            elif row["label_category"] == "lever":
                if row["Pillar"] + "###" + row["lever"] in max_pos_score_by_lever.keys() and float(max_pos_score_by_lever[row["Pillar"] + "###" + row["lever"]]) > 0:
                    score_percent =  (float(row["indv_question_score"]) /  float(max_pos_score_by_lever[row["Pillar"] + "###" + row["lever"]])) * 100
                else:
                    score_percent = 0
                colors.append(get_color_map(score_percent))
        output_df["color"] = colors 
        #print(output_df)
        

        fig = go.Figure(
                go.Sunburst(
                labels=output_df["lever"].map(customwrap).tolist(),
                parents=output_df["Pillar"].map(customwrap).tolist(),
                values = output_df["indv_question_score"].tolist(),
                branchvalues="total",
                texttemplate = "",
                marker=dict(colors=output_df["color"].tolist()),
                #hoverinfo='none'
                )
            )
        fig.update_layout(uniformtext=dict(minsize=10,mode=None),height=600,showlegend=True,plot_bgcolor="FloralWhite",paper_bgcolor='DarkSlateGray')
        fig.update_layout(annotations=[dict(text=str("360-Degree Overview of the Organization"),x=0.5, y=-0.1,font_size = 20,font_color="FloralWhite", showarrow=False)])
        fig.update_traces(name="",textfont=dict(size=[15,12,10]),insidetextorientation="auto",hovertext="")

        returned_div_content = dbc.Container([
            dbc.Row([
                html.Br()
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="scoring_fig_sunbrust",figure=fig),
                ],width = 6),
                dbc.Col([
                    dmc.Group(
                        [
                            esg_level_badge,
                            esg_msg_badge
                        ], 
                    ),
                    html.Br(),
                    esg_msgdtl_paper,
                    html.Br(),
                    html.Div(id="esg-sub-level-header-div"),
                    html.Br(),
                    html.Div(id="esg-sub-level-dtl-div"),
                ],width = 6)
            ]),
             dbc.Row([
                html.Br()
            ]),
            dbc.Row([
                dbc.Col([
                    dmc.SimpleGrid(
                        cols=3,
                        children=[
                            html.Div(
                                dmc.Text(
                                    "< 40%", 
                                    size="md", 
                                    align="center", 
                                    color='dark', 
                                    style={'font-size':'20px'}, 
                                    weight='bolder'
                                ),
                                style={"backgroundColor": "white",'border-style': 'solid','border-color': 'red',  'border-bottom': '3px solid red'}
                            ),
                            html.Div(
                                dmc.Text(
                                    "40%-70%", 
                                    size="md", 
                                    align="center", 
                                    color='dark', 
                                    style={'font-size':'20px'}, 
                                    weight='bolder'
                                ),
                                style={"backgroundColor": "white",'border-style': 'solid','border-color': 'yellow',  'border-bottom': '3px solid yellow'}
                            ),
                            html.Div(
                                dmc.Text(
                                    "> 70%", 
                                    size="md", 
                                    align="center", 
                                    color='dark', 
                                    style={'font-size':'20px'}, 
                                    weight='bolder'
                                ),
                                style={"backgroundColor": "white",'border-style': 'solid','border-color': 'green',  'border-bottom': '3px solid green'}
                            ),
                        ],
                        spacing='sm'
                    )
                ],width=6)
            ]),
            dbc.Row([
                html.Br()
            ]),

        ],
        fluid=True)
    return returned_div_content


## Callback to display textbox based on selected options
@dash.callback(
    Output({"type": "dynamic-textbox-for-options", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "style"),
    [
        Input({"type": "dynamic-checklist", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "value"),
        Input({"type": "dynamic-radioitems", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "value"),
    ],
    [
        State({"type": "dynamic-textbox-for-options", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "style"),
        State({"type": "dynamic-textbox-for-options", "question_id": ALL, "question_type": ALL,"doc_upload_flag" : ALL}, "id")
    ],
    prevent_initial_call=True
)
def render_textbox(checklist_val,radioitems_val,current_style_states,current_style_ids):
    ctx = dash.callback_context
    question_id = ctx.triggered_id["question_id"]
    question_type = ctx.triggered_id["question_type"]
    doc_upload_flag = ctx.triggered_id["doc_upload_flag"]
    returned_list = []
    desired_option_selected = False
    client = mongodb_utility.connect_to_mongodb(mongodb_config.conn_str)
    db = client["esg"]
    question_collection_obj = db["questions"]
    #print(question_id)
    if question_type == "multi_select":
        selected_options = []
        for o in checklist_val:
            for s in o:
                if question_id in s:
                    selected_options.append(s.split("=")[1])
        data = question_collection_obj.find({"question_unique_id": { '$in' : [question_id] }})
        data_to_use = list(data)
        for o in selected_options:
            if 'specify'.upper() in list(data_to_use)[0]['options'][int(o)].upper():
                desired_option_selected = True
    if question_type == "single_select":
        if any(question_id in s for s in radioitems_val):
            matched_values = [s for s in radioitems_val if question_id in s]
            selected_option = matched_values[0].split("=")[1]
            data = question_collection_obj.find({"question_unique_id": { '$in' : [question_id] }})
            if 'specify'.upper() in list(data)[0]['options'][int(selected_option)].upper():
                desired_option_selected = True

    returned_list = current_style_states
    for id in current_style_ids:
        if id["question_id"] == question_id and desired_option_selected:
            index = current_style_ids.index(id)
            returned_list[index] = {'display':'block'}
        if id["question_id"] == question_id and not desired_option_selected:
            index = current_style_ids.index(id)
            returned_list[index] = {'display':'None'}
    return returned_list



## Callback to display esg sub levels
@dash.callback(
    [
        Output("esg-sub-level-header-div", "children"),
        Output("esg-sub-level-dtl-div", "children"),
    ],
    [
        Input("scoring_fig_sunbrust", "clickData"),
    ],
    prevent_initial_call=True
)
def render_textbox(clickdata):
    #print(clickdata)
    #esg_list =  ['Environment','Social','Governance']
    label = clickdata['points'][0]['label']
    parent = clickdata['points'][0]['parent']
    color = clickdata['points'][0]['color']
    if color == "#EB5555":
        esg_sub_label =  "DEFAULTER"
    if color == "#FFCC00":
        esg_sub_label = "SUPPORTER"
    if color == "#83B254":
        esg_sub_label = "TRAILBLAZER"

    if label == 'Environment' or parent == 'Environment':
        if esg_sub_label == "DEFAULTER":
            pillarmsg1="The organization doesn’t have an adequate vision and is not working towards reduction of carbon footprint."
            pillarmsg2="The organization doesn’t properly manage natural resources which is leading to rapid deterioration of environment."
            pillarmsg3="There is a lack of concrete efforts towards sustainable utilization of enterprise applications."
            pillarmsg4="Further, there is a clear imperative to actively manage the lifecycle of hardware i.e. from procurement to disposal."

            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#BC4328", "to": "#BC4328"},
                        color="dark" 
                    ),
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl",style={'border-color': '#E6F0DD','border-style': 'solid','background-image': 'linear-gradient(to right, white , #E6F0DD)'}),
                    dmc.Paper(pillarmsg2,shadow="xl",style={'border-color': '#E6F0DD','border-style': 'solid','background-image': 'linear-gradient(to right, white , #E6F0DD)'}),
                    dmc.Paper(pillarmsg3,shadow="xl",style={'border-color': '#E6F0DD','border-style': 'solid','background-image': 'linear-gradient(to right, white , #E6F0DD)'}),
                    dmc.Paper(pillarmsg4,shadow="xl",style={'border-color': '#E6F0DD','border-style': 'solid','background-image': 'linear-gradient(to right, white , #E6F0DD)'}),
                ]
            )

        if esg_sub_label == "SUPPORTER":
            pillarmsg1="The organization has an advanced vision and is working towards carbon footprints reduction but there's scope for improvement."
            pillarmsg2="The organization displays considerate efforts on Resource management that would lead to reduction in its contribution to environmental deterioration."
            pillarmsg3="There are key strategies implemented towards sustainable utilisation of Enterprise applications, with few lagging areas."
            pillarmsg4="Further, the organization is conscious about managing the lifecycle of hardware i.e. from procurement to disposal."

            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#E6B600", "to": "#E6B600"},
                    ),
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl", style={'border-color': '#CDE0BB','border-style': 'solid','background-image': 'linear-gradient(to right, white , #CDE0BB)'}),
                    dmc.Paper(pillarmsg2,shadow="xl", style={'border-color': '#CDE0BB','border-style': 'solid','background-image': 'linear-gradient(to right, white , #CDE0BB)'}),
                    dmc.Paper(pillarmsg3,shadow="xl", style={'border-color': '#CDE0BB','border-style': 'solid','background-image': 'linear-gradient(to right, white , #CDE0BB)'}),
                    dmc.Paper(pillarmsg4,shadow="xl", style={'border-color': '#CDE0BB','border-style': 'solid','background-image': 'linear-gradient(to right, white , #CDE0BB)'}),
                ]
            )
        if esg_sub_label == "TRAILBLAZER":
            pillarmsg1="The organization has an advanced & clear vision and is working towards reduction of carbon footprints."
            pillarmsg2="The organization deploys advanced efforts on Resource management that would lead to reduction in its contribution to  environmental deterioration."
            pillarmsg3="There are key strategies implemented towards sustainable utilisation of Enterprise applications., ensuring greater efficiency."
            pillarmsg4="Further, the organization is taking stringent measures to  manage the lifecycle of hardware i.e. from procurement to disposal."

            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#00B050", "to": "#00B050"},
                        color="dark" 
                    ),
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl", style={'border-color': '#B5D198','border-style': 'solid','background-image': 'linear-gradient(to right, white , #B5D198)'}),
                    dmc.Paper(pillarmsg2,shadow="xl",style={'border-color': '#B5D198','border-style': 'solid','background-image': 'linear-gradient(to right, white , #B5D198)'}),
                    dmc.Paper(pillarmsg3,shadow="xl",style={'border-color': '#B5D198','border-style': 'solid','background-image': 'linear-gradient(to right, white , #B5D198)'}),
                    dmc.Paper(pillarmsg4,shadow="xl",style={'border-color': '#B5D198','border-style': 'solid','background-image': 'linear-gradient(to right, white , #B5D198)'}),
                ]
            )
    
    elif label == 'Social' or parent == 'Social':
        if esg_sub_label == "DEFAULTER":
            pillarmsg1="The organization has insufficient strategies towards sustainable utilization of networking and communication platforms and is not providing adequate training to the employees."
            pillarmsg2="The organization doesn’t act for the betterment of its human capital and is not fulfilling basic employee needs."
            pillarmsg3="There is lack of initiative in addressing responsibilities towards the wider community, through CSR initiatives."

            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#BC4328", "to": "#BC4328"},
                        color="dark" 
                    ),
            
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl", style={'border-color': '#FFF9E1','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFF9E1)'}),
                    dmc.Paper(pillarmsg2,shadow="xl", style={'border-color': '#FFF9E1','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFF9E1)'}),
                    dmc.Paper(pillarmsg3,shadow="xl", style={'border-color': '#FFF9E1','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFF9E1)'})
                ]
            )
        if esg_sub_label == "SUPPORTER":
            pillarmsg1="The organization is  working towards sustainable utilization of networking and communication platforms across the organization and is progressing towards providing adequate training to the employees."
            pillarmsg2="The organization implements concerted efforts towards betterment of its human capital and is in-track for fulfilling basic employee needs."
            pillarmsg3="There is a presence of initiative in addressing responsibilities towards the wider community, through CSR initiatives."

            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#E6B600", "to": "#E6B600"},
                        color="dark" 
                    ),
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl", style={'border-color': '#FFF3C7','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFF3C7)'}),
                    dmc.Paper(pillarmsg2,shadow="xl", style={'border-color': '#FFF3C7','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFF3C7)'}),
                    dmc.Paper(pillarmsg3,shadow="xl", style={'border-color': '#FFF3C7','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFF3C7)'})
                ]
            )
        if esg_sub_label == "TRAILBLAZER":
            pillarmsg1="The organization is has clear and efficient strategies towards sustainable utilization of networking and communication platforms across the organization and is providing adequate training to the employees."
            pillarmsg2="The organization highly values its human capital and is proactive in investing and inclusion."
            pillarmsg3="There is a presence of active and focused initiative in addressing responsibilities towards the wider community, through CSR initiatives."

            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#00B050", "to": "#00B050"},
                        color="dark" 
                    ),
            
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl", style={'border-color': '#FFE88F','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFE88F)'}),
                    dmc.Paper(pillarmsg2,shadow="xl", style={'border-color': '#FFE88F','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFE88F)'}),
                    dmc.Paper(pillarmsg3,shadow="xl", style={'border-color': '#FFE88F','border-style': 'solid','background-image': 'linear-gradient(to right, white , #FFE88F)'})
                ]
            )
    
    elif label == 'Governance' or parent == 'Governance':
        if esg_sub_label == "DEFAULTER":
            pillarmsg1="The organization is lagging in purpose & strategy with highlighted inability to manage ESG risks."
            pillarmsg2="Organization does not work towards sound Asset governance."
            pillarmsg3="Organization needs to manages data resources while ensuring effective Data Management."
            pillarmsg4="There is a lack of accountability and oversight vis-à-vis sustainability initiatives."

            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#BC4328", "to": "#BC4328"},
                        color="dark" 
                    ),
            
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl", style={'border-color': '#E1E7F3','border-style': 'solid','background-image': 'linear-gradient(to right, white , #E1E7F3)'}),
                    dmc.Paper(pillarmsg2,shadow="xl", style={'border-color': '#E1E7F3','border-style': 'solid','background-image': 'linear-gradient(to right, white , #E1E7F3)'}),
                    dmc.Paper(pillarmsg3,shadow="xl", style={'border-color': '#E1E7F3','border-style': 'solid','background-image': 'linear-gradient(to right, white , #E1E7F3)'}),
                    dmc.Paper(pillarmsg4,shadow="xl", style={'border-color': '#E1E7F3','border-style': 'solid','background-image': 'linear-gradient(to right, white , #E1E7F3)'}),
                ]
            )
        if esg_sub_label == "SUPPORTER":
            pillarmsg1="The organization is working on purpose & strategy with inability to manage ESG risks."
            pillarmsg2=" Organization works towards sound Asset governance."
            pillarmsg3=" Organization considerably tracks and manages data resources while ensuring effective Data Management."
            pillarmsg4="There is adequate presence of accountability and oversight vis-à-vis sustainability initiatives."
            
            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#E6B600", "to": "#E6B600"},
                        color="dark" 
                    ),
            
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl", style={'border-color': '#C2CEE6','border-style': 'solid','background-image': 'linear-gradient(to right, white , #C2CEE6)'}),
                    dmc.Paper(pillarmsg2,shadow="xl", style={'border-color': '#C2CEE6','border-style': 'solid','background-image': 'linear-gradient(to right, white , #C2CEE6)'}),
                    dmc.Paper(pillarmsg3,shadow="xl", style={'border-color': '#C2CEE6','border-style': 'solid','background-image': 'linear-gradient(to right, white , #C2CEE6)'}),
                    dmc.Paper(pillarmsg4,shadow="xl", style={'border-color': '#C2CEE6','border-style': 'solid','background-image': 'linear-gradient(to right, white , #C2CEE6)'}),
                ]
            )
        if esg_sub_label == "TRAILBLAZER":
            pillarmsg1="The organization has clear and defined purpose & strategy with exceptional ability to manage ESG risks."
            pillarmsg2="Organization has robust Asset governance mechanisms."
            pillarmsg3="Organization tracks and actively manages data resources while ensuring effective Data Management."
            pillarmsg4="There is substantial  presence of accountability and oversight vis-à-vis sustainability initiatives, ensuring effective governance."

            header_object = dmc.Badge(
                        esg_sub_label, 
                        size="xl",
                        variant="gradient",
                        gradient={"from": "#00B050", "to": "#00B050"},
                        color="dark" 
                    ),
            
            
            dtl_object = dmc.Stack(
                [
                    dmc.Paper(pillarmsg1,shadow="xl", style={'border-color': '#A4B6DA','border-style': 'solid','background-image': 'linear-gradient(to right, white , #A4B6DA)'}),
                    dmc.Paper(pillarmsg2,shadow="xl", style={'border-color': '#A4B6DA','border-style': 'solid','background-image': 'linear-gradient(to right, white , #A4B6DA)'}),
                    dmc.Paper(pillarmsg3,shadow="xl", style={'border-color': '#A4B6DA','border-style': 'solid','background-image': 'linear-gradient(to right, white , #A4B6DA)'}),
                    dmc.Paper(pillarmsg4,shadow="xl", style={'border-color': '#A4B6DA','border-style': 'solid','background-image': 'linear-gradient(to right, white , #A4B6DA)'}),
                ]
            )
    

    return header_object,dtl_object