import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash import html
from urllib.parse import quote as urlquote
import os
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd
from database import mongodb_config,mongodb_utility
import json

## Callback for table pagination
for table,num_rows_to_display in [['user-dtl-table','num-row-to-display-numeric-au'],['pillar-dtl-table','num-row-to-display-numeric-ap'],['lever-dtl-table','num-row-to-display-numeric-al'],['variable-dtl-table','num-row-to-display-numeric-av'],['question-dtl-table','num-row-to-display-numeric-aq'],['template-dtl-table','num-row-to-display-numeric-at'],['assessment-dtl-table','num-row-to-display-numeric-aa']]:
    @dash.callback(
        Output(table, 'page_size'),
        Input(num_rows_to_display, 'value'),
        prevent_initial_call=True
    )
    def table_pagination(pagination_value):
        return pagination_value

def question_template_download_link():
    location = "/download/templates/question_upload_template.xlsx"
    return html.A("template", href=location)

def uploaded_question_file_download_link(folder_name,filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}/{}".format(folder_name,urlquote(filename))
    return html.A(filename, href=location)

def validate_uploaded_question_file(file_path):
    df = pd.read_excel(file_path)
    #is_valid = all(x in df.columns for x in ['question_text', 'default_variable', 'question_type', 'no_of_options','question_group', 'question_group_primary_member', 'doc_upload_flag']) and all(x.split("_")[-1].isdigit() for x in df.columns if x.startswith("option_text_") or x.startswith("option_internal_score_") or x.startswith("option_absolute_score_"))
    is_valid = all(x in df.columns for x in ['question_text', 'variable_name', 'question_type', 'no_of_options','options','option_absolute_score','option_internal_score','question_group', 'question_group_primary_member', 'doc_upload_flag'])
    return "VALID" if is_valid else "INVALID"

def uploaded_question_file_lister(folder_name):
    UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__),'..','uploaded_evidence', folder_name)
    files = []
    download_links = []
    file_validation_dict = {}
    if os.path.exists(UPLOAD_DIRECTORY):
        for filename in os.listdir(UPLOAD_DIRECTORY):
            path = os.path.join(UPLOAD_DIRECTORY, filename)
            if os.path.isfile(path):
                files.append(filename)
                is_valid = validate_uploaded_question_file(path)
                file_validation_dict[filename] = is_valid
    #print(files)
    if len(files) == 0:
        download_links.append(html.Li("No file uploaded!"))
    else:
        download_links.append(
            [
                dmc.Group(
                    children=[
                        html.Li(uploaded_question_file_download_link(folder_name,filename)), 
                        dbc.Button(
                            id={"type":"uploaded-question-file-remove-btn","filename": filename},
                            className="bi bi-x  py-0 px-1 mx-0 my-0", 
                            color="danger", 
                            outline=True, 
                            style={"border":"None"},
                            n_clicks =0
                        ),
                        dmc.Badge(file_validation_dict[filename], color="green" if file_validation_dict[filename] == "VALID" else "red", variant="light"),
                    ],
                    #direction = "row",
                    position = "left",
                    spacing = "sm"  
                )
                for filename in files
            ]
        )
    return download_links,file_validation_dict


        