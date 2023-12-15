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
import json

assessment_table = html.Div([
                    dmc.Space(h="lg"),
                    ## Data input Modals
                    html.Div(
                        id = "add-assessment-modal-div",
                        children= [
                            mantine_modal(
                                title="Add assessment",
                                id="add-assessment-modal",
                                size='40%',
                                is_open=False,
                                modal_component_list=[
                                    mantine_text_box(label="assessment Name : *",id="assessment-name-txt-aa",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_select(
                                        label="Template : *",
                                        required=False,
                                        icon_class="radix-icons:magnifying-glass",
                                        size='sm',
                                        style_dict={"width": 400},
                                        id="template-select-aa",
                                        dropdown_data= mongodb_utility.get_distinct_values("template","template_name")
                                    ),
                                ],
                                submit_btn_id="modal-submit-button-aa",
                                cancel_btn_id="modal-cancel-button-aa"
                            ),
                        ]
                    ),
                    html.Div(
                        id="delete-assessment-modal-div",
                        children = [
                            mantine_modal(
                                title="Alert",
                                id="delete-assessment-modal",
                                size='20%',
                                is_open=False,
                                modal_component_list=[
                                    dmc.Title("Are you sure?", size="lg"),
                                ],
                                submit_btn_id="modal-submit-button-da",
                                cancel_btn_id="modal-cancel-button-da",
                                submit_btn_text="Yes"
                            ),
                        ]
                    ),

                    ## Success toasts
                    success_toast(id="assessment-add-success-toast",is_open=False),
                    success_toast(id="assessment-update-success-toast",is_open=False),
                    success_toast(id="assessment-delete-success-toast",is_open=False),

                    ## data tables
                    html.Div(
                        id = "assessment-dtl-table-div",
                        children=[
                            dbc.Container([
                                    dbc.Row([
                                        #mantine_table(id= "user-dtl-table",table_data=mongodb_utility.create_table_from_df(pd.DataFrame(mongodb_utility.get_user_collection_dump()))),
                                        dash_datatable(
                                            id= "assessment-dtl-table",
                                            data_dict = mongodb_utility.get_assessment_collection_dump(),
                                            export_format='none',
                                            title="",
                                            action_btn_list=[
                                                submenu_button("Delete","ep:delete-filled","subtle","red","sm","del-btn-aa",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"0px","marginTop":"20px","marginBottom":"20px"}),
                                                submenu_button("Sync to DB","mdi:database-sync","subtle","gray","sm","sync-btn-aa",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("De-Select All","material-symbols:deselect","subtle","violet","sm","de-select-all-btn-aa",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Select All","fluent:select-all-on-20-regular","subtle","grape","sm","select-all-btn-aa",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Refresh","uil:refresh","subtle","blue","sm","refresh-btn-aa",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button(label="Add Assessment",icon_class="ri:survey-fill",varient="subtle",color="lime",size="sm",id="add-assessment-btn",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                dash_table_interactivity_helptext(),
                                                daq.NumericInput(
                                                    id="num-row-to-display-numeric-aa",
                                                    min=1,
                                                    max=100,
                                                    value=10,
                                                        style={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"18px","color":"dark"},
                                                ),
                                            ],
                                            non_editable_col_list=["survey_unique_id"],
                                            column_with_dropdown_names_list = ['pillar','lever','variable'],
                                            column_dropdowns_data_dict = {
                                                'pillar': {
                                                    'options': [
                                                        {'label': i, 'value': i}
                                                        for i in mongodb_utility.get_distinct_values("pillar","pillar_name")
                                                    ]
                                                },
                                                'lever': {
                                                    'options': [
                                                        {'label': i, 'value': i}
                                                        for i in mongodb_utility.get_distinct_values("lever","lever_name")
                                                    ]
                                                },
                                                'variable': {
                                                    'options': [
                                                        {'label': i, 'value': i}
                                                        for i in mongodb_utility.get_distinct_values("variable","variable_name")
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
    

## Callback to create add assessment modal
@dash.callback(
        Output("add-assessment-modal-div","children"),
        Input("add-assessment-btn", "n_clicks"),
        prevent_initial_call=True
)
def create_add_lever_modal(n_al):
    ctx = dash.callback_context
    add_lever_modal_div_children = []
    if ctx.triggered_id == "add-assessment-btn" and n_al:
        add_lever_modal_div_children = mantine_modal(
                                title="Add assessment",
                                id="add-assessment-modal",
                                size='40%',
                                is_open=True,
                                modal_component_list=[
                                    mantine_text_box(label="assessment Name : *",id="assessment-name-txt-aa",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_select(
                                        label="Template : *",
                                        required=False,
                                        icon_class="radix-icons:magnifying-glass",
                                        size='sm',
                                        style_dict={"width": 400},
                                        id="template-select-aa",
                                        dropdown_data= mongodb_utility.get_distinct_values("template","template_name")
                                    ),
                                ],
                                submit_btn_id="modal-submit-button-aa",
                                cancel_btn_id="modal-cancel-button-aa"
                            )
    return add_lever_modal_div_children


# Callback to handle assessment modal cancel btn
@dash.callback(
        Output("add-assessment-modal", "opened", allow_duplicate=True),
        Input("modal-cancel-button-aa", "n_clicks"),
        prevent_initial_call=True
)
def handle_cancel(n):
    if n:
        return False
    

# Callback to refresh assessment dtl table
@dash.callback(
        Output("assessment-dtl-table", "data", allow_duplicate=True),
        Output("assessment-dtl-table", "dropdown"),
        Input("refresh-btn-aa", "n_clicks"),
        prevent_initial_call=True
)
def handle_refresh(n):
    if n:
        column_dropdowns_data_dict = {
            'pillar': {
                'options': [
                    {'label': i, 'value': i}
                    for i in mongodb_utility.get_distinct_values("pillar","pillar_name")
                ]
            },
            'lever': {
                'options': [
                    {'label': i, 'value': i}
                    for i in mongodb_utility.get_distinct_values("lever","lever_name")
                ]
            },
            'variable': {
                'options': [
                    {'label': i, 'value': i}
                    for i in mongodb_utility.get_distinct_values("variable","variable_name")
                ]
            }
        }
        return mongodb_utility.get_assessment_collection_dump(),column_dropdowns_data_dict


## Callback to add assessment data to DB and manage assessment modal state
@dash.callback(
     [
        Output("add-assessment-modal", "opened"),
        Output("assessment-add-success-toast", "is_open"),
        Output("assessment-add-success-toast", "children"),
        Output("assessment-name-txt-aa", "value"),
        Output("template-select-aa", "value"),
        Output("assessment-dtl-table", "data"),
    ],
     [
        Input("modal-submit-button-aa", "n_clicks"),
    ],
     [
        State("assessment-name-txt-aa", "value"),
        State("template-select-aa", "value"),
    ],
    prevent_initial_call=True
)
def add_assessment(n_ms,assessment_name,template_name):
    ctx = dash.callback_context
    #print(ctx.triggered_id)
    toast_msg = ""
    survey_unique_id = str(uuid.uuid4())
    if ctx.triggered_id == "modal-submit-button-aa" and n_ms:
        data_dict_list = []
        pillar_lever_dict = {}
        lever_weightage_dict = {}
        if assessment_name =="" or template_name == "" or template_name is None:
            return [True,False,"",assessment_name,template_name,mongodb_utility.get_assessment_collection_dump()]
        list_of_levers = mongodb_utility.get_assessment_template_collection_dump(query={'template_name': template_name})[0]["associated_levers"]
        list_of_levers = json.loads(list_of_levers)
        #print(list_of_levers)
        for l in list_of_levers:
            associated_pillar = mongodb_utility.get_lever_collection_dump(query={"lever_name": l})[0]["pillar_name"]
            if str(associated_pillar) in pillar_lever_dict.keys():
                pillar_lever_dict[str(associated_pillar)].append(l)
            else:
                pillar_lever_dict[str(associated_pillar)] = [l]
        for key in pillar_lever_dict.keys():
            pillar_weightage = mongodb_utility.get_pillar_collection_dump({'pillar_name':key})[0]['pillar_weightage']
            for l in pillar_lever_dict[key]:
                lever_weightage_dict[l] = float(pillar_weightage) / len(pillar_lever_dict[key])
        for lever in list_of_levers:
            list_of_variables = mongodb_utility.get_variable_collection_dump(query={"lever_name": lever})
            #print("List of Variables {}".format(list_of_variables))
            variable_weightage = float(lever_weightage_dict[lever]) / len(list_of_variables)
            for variable in  list_of_variables:
                list_of_questions = mongodb_utility.get_question_collection_dump(query={'variable_name':variable["variable_name"]})
                #print(list_of_questions)
                question_weightage = float(variable_weightage) / len(list_of_questions)
                for question in list_of_questions:
                    data={}
                    data["survey_unique_id"] = survey_unique_id
                    data["status"] = "Active"
                    data["survey_name"] = assessment_name
                    data["template_name"] = template_name
                    data["pillar"] = mongodb_utility.get_lever_collection_dump(query={'lever_name': lever})[0]["pillar_name"]
                    data["lever"] = lever
                    data["variable"] = variable["variable_name"]
                    data["question_text"] = question["question_text"]
                    data["question_unique_id"] = question["question_unique_id"]
                    data["weightage"] = question_weightage
                    data_dict_list.append(data)
        #print(data_dict_list)
        mongodb_utility.insert_many_doc("survey_dtl",data_dict_list)
        toast_msg ="Assessment created successfully"
        return [False,True,toast_msg,"","",mongodb_utility.get_assessment_collection_dump()]
    else:
        return [True,False,toast_msg,"","",mongodb_utility.get_assessment_collection_dump()]
    


## callback to sync assessment table to db
@dash.callback(
    [
        Output("assessment-update-success-toast", "is_open"),
        Output("assessment-update-success-toast", "children"),
    ],
    [
        Input("sync-btn-aa", "n_clicks"),
    ],
    [
        State("assessment-dtl-table", "data"),
    ],
    prevent_initial_call=True
)
def sync_lever_table(n_sb,modified_tbl_data):
    if n_sb:
        current_data_from_db = mongodb_utility.get_assessment_collection_dump()
        changes = list(dictdiffer.diff(current_data_from_db, modified_tbl_data))
        if len(changes) == 0:
            raise PreventUpdate
        for change in changes:
            #print(change)
            if change[0] == "change":
                survey_unique_id = modified_tbl_data[change[1][0]]["survey_unique_id"]
                question_unique_id = modified_tbl_data[change[1][0]]["question_unique_id"]
                filter_for_db = {"survey_unique_id": survey_unique_id,"question_unique_id":question_unique_id}
                updated_data_dict = {str(change[1][1]): change[2][1]}
                mongodb_utility.update_one_doc("survey_dtl",filter_for_db,updated_data_dict)
                #print(unique_user_id)
        return [True,"Assessment(s) updated successfully"]


## Callback to delete data from assessment table
@dash.callback(
    Output('delete-assessment-modal', 'opened'),
    Output("assessment-delete-success-toast", "is_open"),
    Output("assessment-delete-success-toast", "children"),
    Output("assessment-dtl-table", "data", allow_duplicate=True),
    Input('del-btn-aa', 'n_clicks'),
    Input('modal-cancel-button-da', 'n_clicks'),
    Input('modal-submit-button-da', 'n_clicks'),
    State('assessment-dtl-table', 'selected_rows'),
    State('assessment-dtl-table', 'data'),
    prevent_initial_call=True
)
def delete_data(n_d,n_c,n_s,selected_rows,full_table_data):
    ctx = dash.callback_context
    data_to_be_deleted = {}
    if n_d and ctx.triggered_id == 'del-btn-aa':
        return True,False,"",mongodb_utility.get_assessment_collection_dump()
    if n_c and ctx.triggered_id == 'modal-cancel-button-da':
        return False,False,"",mongodb_utility.get_assessment_collection_dump()
    if n_s and ctx.triggered_id == 'modal-submit-button-da':
        #print(selected_rows)
        if len(selected_rows) > 0:
            for row_id in selected_rows:
                data_to_be_deleted=full_table_data[row_id]
                mongodb_utility.delete_one_doc("survey_dtl",data_to_be_deleted)
            text = "Selected assessment(s) deleted successfully"
            return False,True,text,mongodb_utility.get_assessment_collection_dump()
        else:
            text = "Nothing to delete" 
            return False,True,text,mongodb_utility.get_assessment_collection_dump() 
        

## callback to select and deselect all rows in assessment table
@dash.callback(
    Output('assessment-dtl-table', 'selected_rows'),
    Input('select-all-btn-aa', 'n_clicks'),
    Input('de-select-all-btn-aa', 'n_clicks'),
    Input('modal-submit-button-da', 'n_clicks'),
    State('assessment-dtl-table', 'derived_virtual_indices'),
    State('assessment-dtl-table', 'selected_rows'),
    prevent_initial_call=True
)
def select_deselect_lever(select_n_clicks, deselect_n_clicks,del_n_clicks, filtered_rows_indices,already_selected_rows):
    # print(filtered_rows_indices)
    # print(already_selected_rows)
    """Select or deselect all rows."""
    ctx = dash.callback_context
    if ctx.triggered_id == 'select-all-btn-aa':
        if select_n_clicks:
            if filtered_rows_indices is None:
                return []
            else:
                return filtered_rows_indices + already_selected_rows if already_selected_rows is not None else []
    if ctx.triggered_id == 'de-select-all-btn-aa':
        if deselect_n_clicks:
            return []
    if ctx.triggered_id == 'modal-submit-button-da':
        if del_n_clicks:
            return []