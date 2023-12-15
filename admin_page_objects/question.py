from dash import html
import dash_mantine_components as dmc
from utils.common_ui_elements import submenu_button,mantine_text_box,mantine_modal,success_toast,bootstrap_popover,mantine_select,mantine_table,dash_table_interactivity_helptext,dash_datatable
import dash_bootstrap_components as dbc
from database import mongodb_config,mongodb_utility
import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State, ALL, MATCH
import uuid
import dictdiffer  
from dash.exceptions import PreventUpdate
from admin_page_objects import common
import dash_uploader as du
import os
import json
import pandas as pd

question_table = html.Div([
                    dmc.Space(h="lg"),
                    ## Data input Modals
                    html.Div(
                        id = "bulk-upload-question-modal-div",
                        children= []
                    ),
                    html.Div(
                        id="delete-question-modal-div",
                        children = [
                            mantine_modal(
                                title="Alert",
                                id="delete-question-modal",
                                size='20%',
                                is_open=False,
                                modal_component_list=[
                                    dmc.Title("Are you sure?", size="lg"),
                                ],
                                submit_btn_id="modal-submit-button-dq",
                                cancel_btn_id="modal-cancel-button-dq",
                                submit_btn_text="Yes"
                            ),
                        ]
                    ),

                    ## Success toasts
                    success_toast(id="question-add-success-toast",is_open=False),
                    success_toast(id="question-update-success-toast",is_open=False),
                    success_toast(id="question-delete-success-toast",is_open=False),

                    ## data tables
                    html.Div(
                        children=[
                            dbc.Container([
                                    dbc.Row([
                                        #mantine_table(id= "user-dtl-table",table_data=mongodb_utility.create_table_from_df(pd.DataFrame(mongodb_utility.get_user_collection_dump()))),
                                        dash_datatable(
                                            id= "question-dtl-table",
                                            data_dict=mongodb_utility.get_question_collection_dump(),
                                            export_format='none',
                                            title="",
                                            action_btn_list=[
                                                submenu_button("Delete","ep:delete-filled","subtle","red","sm","del-btn-aq",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"0px","marginTop":"20px","marginBottom":"20px"}),
                                                submenu_button("Sync to DB","mdi:database-sync","subtle","gray","sm","sync-btn-aq",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("De-Select All","material-symbols:deselect","subtle","violet","sm","de-select-all-btn-aq",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Select All","fluent:select-all-on-20-regular","subtle","grape","sm","select-all-btn-aq",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Refresh","uil:refresh","subtle","blue","sm","refresh-btn-aq",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button(label="Bulk Upload",icon_class="ic:round-upload",varient="subtle",color="lime",size="sm",id="bulk-upload-question-btn",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                dash_table_interactivity_helptext(),
                                                daq.NumericInput(
                                                    id="num-row-to-display-numeric-aq",
                                                    min=1,
                                                    max=100,
                                                    value=10,
                                                        style={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"18px","color":"dark"},
                                                ),
                                            ],
                                            non_editable_col_list=["question_unique_id"],
                                            column_with_dropdown_names_list = ['variable_name'],
                                            column_dropdowns_data_dict = {
                                                'variable_name': {
                                                    'options': [
                                                        {'label': i, 'value': i}
                                                        for i in mongodb_utility.get_distinct_values("variable","variable_name")
                                                    ]
                                                },
                                                'question_type': {
                                                    'options': [
                                                        {'label': i, 'value': i}
                                                        for i in ["multi_select","single_select","text"]
                                                    ]
                                                }
                                            },
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
                    html.Div()
                ])
        
## Callback to create bulk upload question modal
@dash.callback(
        Output("bulk-upload-question-modal-div","children"),
        Input("bulk-upload-question-btn", "n_clicks"),
        prevent_initial_call=True
)
def create_upload_question_modal(n_aq):
    ctx = dash.callback_context
    upload_question_modal_div_children = []
    if ctx.triggered_id == "bulk-upload-question-btn" and n_aq:
        upload_question_modal_div_children = mantine_modal(
                                title="Upload Questions",
                                id="upload-question-modal",
                                size='60%',
                                is_open=True,
                                modal_component_list=[
                                    html.Div(
                                        [
                                            dmc.Stepper(
                                                id="question-upload-stepper",
                                                active=0,
                                                breakpoint="sm",
                                                size='md',
                                                orientation="horizontal",
                                                color="green",
                                                children=[
                                                    dmc.StepperStep(
                                                        label="First step",
                                                        description="Download the template",
                                                        children=[
                                                            dmc.Space(h="lg"),
                                                            dmc.Text(
                                                                [
                                                                    "Please download the ",
                                                                    common.question_template_download_link(),
                                                                    " and follow instructions provided there to fill it up.",
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    dmc.StepperStep(
                                                        label="Second step",
                                                        description="Upload file",
                                                        children=[
                                                            dmc.Space(h="lg"),
                                                            du.Upload(
                                                                id="question-uploader",
                                                                max_file_size=1800,  # 1800 Mb
                                                                text='Upload question: Only xlsx allowed',
                                                                text_completed='Uploaded: ',
                                                                cancel_button=True,
                                                                pause_button=True,
                                                                default_style = {
                                                                    'width': '100%',
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
                                                                filetypes=['xlsx'],
                                                                upload_id="question_upload_" + str(uuid.uuid4())
                                                            )
                                                        ]
                                                    ),
                                                    dmc.StepperStep(
                                                        label="Final step",
                                                        description="Validate & Sync to DB",
                                                        children=[
                                                            dmc.Space(h="lg"),
                                                            html.Div(
                                                                id="question-upload-final-step-div"
                                                            ),
                                                            dmc.Space(h="lg"),
                                                            dmc.Text("Please click on Next Step button to upload this data to DB", align="left"),

                                                        ]
                                                    ),
                                                    dmc.StepperCompleted(
                                                        children=[
                                                            html.Div(
                                                                id="question-upload-complete-step-div"
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                            ),
                                            dmc.Group(
                                                position="left",
                                                mt="xl",
                                                children=[
                                                    submenu_button("Back","ion:arrow-back-circle-sharp","outline","dark","md","question-upload-stepper-back"),
                                                    submenu_button("Next step","material-symbols:next-plan-rounded","filled","violet","md","question-upload-stepper-next")
                                                ],
                                            ),
                                        ]
                                    )
                                ],
                                submit_btn_id="modal-submit-button-aq",
                                cancel_btn_id=None,
                                submit_btn_text="Done"
                            )
    return upload_question_modal_div_children

def sync_question_file_to_db(folder_name,file_name):
    data = {}
    data_list=[]
    file_path = os.path.join(os.path.dirname(__file__),'..','uploaded_evidence', folder_name, file_name)
    df = pd.read_excel(file_path)
    df_json = df.to_json(orient="records")
    df_json = json.loads(df_json)
    for d in df_json:
        data = d
        data["question_unique_id"] = str(uuid.uuid4())
        data["options"] = json.loads(d["options"])
        data["option_internal_score"] = json.loads(d["option_internal_score"])
        data["option_absolute_score"] = json.loads(d["option_absolute_score"])
        data_list.append(data)
    #print(data_list)
    return mongodb_utility.insert_many_doc("question",data_list)

## Callback to move around question upload stepper.
@dash.callback(
    Output("question-upload-stepper", "active"),
    Output("question-upload-final-step-div", "children"),
    Output("question-upload-complete-step-div", "children"),
    Output("question-dtl-table", "data", allow_duplicate=True),
    Input("question-upload-stepper-back", "n_clicks"),
    Input("question-upload-stepper-next", "n_clicks"),
    State("question-upload-stepper", "active"),
    State("question-uploader", "upload_id"),
    prevent_initial_call=True,
)
def move_around(n_back, n_next, current,upload_id):
    ctx = dash.callback_context
    button_id = ctx.triggered_id
    min_step = 0
    max_step = 3
    active = 0
    step = current if current is not None else active
    if button_id == "question-upload-stepper-back" and n_back:
        step = step - 1 if step > min_step else step
    if button_id == "question-upload-stepper-next" and n_next:
        step = step + 1 if step < max_step else step
    #print("Step: {}".format(step))
    download_links,file_validation_dict = common.uploaded_question_file_lister(upload_id)
    if step == 2:
        return step,download_links[0],[],mongodb_utility.get_question_collection_dump()
    if step == 3:
        for file_name in file_validation_dict.keys():
            if file_validation_dict[file_name] == "VALID":
                if sync_question_file_to_db(upload_id,file_name):
                    return step,[],"Sync to DB was successful.",mongodb_utility.get_question_collection_dump()
                else:
                    return step,[],"Sync to DB failed, please try again.",mongodb_utility.get_question_collection_dump()
    return step,[],[],mongodb_utility.get_question_collection_dump()


## Callback to change the state of the upload question modal
@dash.callback(
    Output("upload-question-modal", "opened"),
    Input("modal-submit-button-aq", "n_clicks"),
    prevent_initial_call=True
)
def handle_done(n):
    if n:
        return False
    
## Callback to handle delete uploaded file button
@dash.callback(
    Output("question-upload-final-step-div", "children", allow_duplicate=True),
    Input({"type":"uploaded-question-file-remove-btn", "filename": ALL}, "n_clicks"),
    State("question-uploader", "upload_id"),
    State("question-upload-final-step-div", "children"),
    prevent_initial_call=True
)
def handle_del(n,folder_name,current_files):
    ctx = dash.callback_context
    print(n)
    if 1 in n:
        filename = ctx.triggered_id["filename"]
        ## Deleting the evidence
        UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__),'..','uploaded_evidence', folder_name)
        if os.path.exists(UPLOAD_DIRECTORY):
            for f in os.listdir(UPLOAD_DIRECTORY):
                if f == filename:
                    print(f)
                    os.remove(os.path.join(UPLOAD_DIRECTORY,f))
            download_links,file_validation_dict = common.uploaded_question_file_lister(folder_name)
            return download_links[0]
    return current_files


# Callback to refresh question dtl table
@dash.callback(
        Output("question-dtl-table", "data"),
        Output("question-dtl-table", "dropdown"),
        Input("refresh-btn-aq", "n_clicks"),
        prevent_initial_call=True
)
def handle_refresh(n):
    if n:
        column_dropdowns_data_dict = {
            'variable_name': {
                'options': [
                    {'label': i, 'value': i}
                    for i in mongodb_utility.get_distinct_values("variable","variable_name")
                ]
            },
            'question_type': {
                'options': [
                    {'label': i, 'value': i}
                    for i in ["multi_select","single_select","text"]
                ]
            }
        }
        return mongodb_utility.get_question_collection_dump(),column_dropdowns_data_dict
    

## callback to sync question table to db
@dash.callback(
    [
        Output("question-update-success-toast", "is_open"),
        Output("question-update-success-toast", "children"),
    ],
    [
        Input("sync-btn-aq", "n_clicks"),
    ],
    [
        State("question-dtl-table", "data"),
    ],
    prevent_initial_call=True
)
def sync_question_table(n_sb,modified_tbl_data):
    if n_sb:
        current_data_from_db = mongodb_utility.get_question_collection_dump()
        changes = list(dictdiffer.diff(current_data_from_db, modified_tbl_data))
        if len(changes) == 0:
            raise PreventUpdate
        for change in changes:
            #print(change)
            if change[0] == "change":
                unique_id = modified_tbl_data[change[1][0]]["question_unique_id"]
                filter_for_db = {"question_unique_id": unique_id}
                updated_data_dict = {str(change[1][1]): change[2][1]}
                if "options" in updated_data_dict:
                    updated_data_dict["options"] = json.loads(updated_data_dict["options"])
                if "option_internal_score" in updated_data_dict:
                    updated_data_dict["option_internal_score"] = json.loads(updated_data_dict["option_internal_score"])
                if "option_absolute_score" in updated_data_dict:
                    updated_data_dict["option_absolute_score"] = json.loads(updated_data_dict["option_absolute_score"])
                print(updated_data_dict)
                mongodb_utility.update_one_doc("question",filter_for_db,updated_data_dict)
                #print(unique_user_id)
        return [True,"question(s) updated successfully"]

## callback to select and deselect all rows in question table
@dash.callback(
    Output('question-dtl-table', 'selected_rows'),
    Input('select-all-btn-aq', 'n_clicks'),
    Input('de-select-all-btn-aq', 'n_clicks'),
    Input('modal-submit-button-dq', 'n_clicks'),
    State('question-dtl-table', 'derived_virtual_indices'),
    State('question-dtl-table', 'selected_rows'),
    prevent_initial_call=True
)
def select_deselect_lever(select_n_clicks, deselect_n_clicks,del_n_clicks, filtered_rows_indices,already_selected_rows):
    # print(filtered_rows_indices)
    # print(already_selected_rows)
    """Select or deselect all rows."""
    ctx = dash.callback_context
    if ctx.triggered_id == 'select-all-btn-aq':
        if select_n_clicks:
            if filtered_rows_indices is None:
                return []
            else:
                return filtered_rows_indices + already_selected_rows if already_selected_rows is not None else []
    if ctx.triggered_id == 'de-select-all-btn-aq':
        if deselect_n_clicks:
            return []
    if ctx.triggered_id == 'modal-submit-button-dq':
        if del_n_clicks:
            return []

## Callback to delete data from question table
@dash.callback(
    Output('delete-question-modal', 'opened'),
    Output("question-delete-success-toast", "is_open"),
    Output("question-delete-success-toast", "children"),
    Output("question-dtl-table", "data", allow_duplicate=True),
    Input('del-btn-aq', 'n_clicks'),
    Input('modal-cancel-button-dq', 'n_clicks'),
    Input('modal-submit-button-dq', 'n_clicks'),
    State('question-dtl-table', 'selected_rows'),
    State('question-dtl-table', 'data'),
    prevent_initial_call=True
)
def delete_data(n_d,n_c,n_s,selected_rows,full_table_data):
    ctx = dash.callback_context
    data_to_be_deleted = {}
    if n_d and ctx.triggered_id == 'del-btn-aq':
        return True,False,"",mongodb_utility.get_question_collection_dump()
    if n_c and ctx.triggered_id == 'modal-cancel-button-dq':
        return False,False,"",mongodb_utility.get_question_collection_dump()
    if n_s and ctx.triggered_id == 'modal-submit-button-dq':
        #print(selected_rows)
        if len(selected_rows) > 0:
            for row_id in selected_rows:
                data_to_be_deleted=full_table_data[row_id]
                query = {"question_unique_id":data_to_be_deleted["question_unique_id"]}
                #print(query)
                mongodb_utility.delete_one_doc("question",query)
            text = "Selected questions(s) deleted successfully"
            return False,True,text,mongodb_utility.get_question_collection_dump()
        else:
            text = "Nothing to delete" 
            return False,True,text,mongodb_utility.get_question_collection_dump() 