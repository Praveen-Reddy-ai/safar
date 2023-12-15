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

variable_table = html.Div([
                    dmc.Space(h="lg"),
                    ## Data input Modals
                    html.Div(
                        id = "add-variable-modal-div",
                        children= [
                            mantine_modal(
                                title="Add Variable",
                                id="add-variable-modal",
                                size='40%',
                                is_open=False,
                                modal_component_list=[
                                    mantine_text_box(label="Variable Name : *",id="variable-name-txt-av",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_select(
                                        label="Lever : *",
                                        required=False,
                                        icon_class="radix-icons:magnifying-glass",
                                        size='sm',
                                        style_dict={"width": 400},
                                        id="lever-select-av",
                                        dropdown_data= mongodb_utility.get_distinct_values("lever","lever_name")
                                    ),
                                ],
                                submit_btn_id="modal-submit-button-av",
                                cancel_btn_id="modal-cancel-button-av"
                            ),
                            mantine_modal(
                                title="Alert",
                                id="delete-variable-modal",
                                size='20%',
                                is_open=False,
                                modal_component_list=[
                                    dmc.Title("Are you sure?", size="lg"),
                                ],
                                submit_btn_id="modal-submit-button-dv",
                                cancel_btn_id="modal-cancel-button-dv",
                                submit_btn_text="Yes"
                            ),
                        ]
                    ),

                    ## Success toasts
                    success_toast(id="variable-add-success-toast",is_open=False),
                    success_toast(id="variable-update-success-toast",is_open=False),
                    success_toast(id="variable-delete-success-toast",is_open=False),

                    ## data tables
                    html.Div(
                        children=[
                            dbc.Container([
                                    dbc.Row([
                                        #mantine_table(id= "user-dtl-table",table_data=mongodb_utility.create_table_from_df(pd.DataFrame(mongodb_utility.get_user_collection_dump()))),
                                        dash_datatable(
                                            id= "variable-dtl-table",
                                            data_dict=mongodb_utility.get_variable_collection_dump(),
                                            export_format='none',
                                            title="",
                                            action_btn_list=[
                                                submenu_button("Delete","ep:delete-filled","subtle","red","sm","del-btn-av",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"0px","marginTop":"20px","marginBottom":"20px"}),
                                                submenu_button("Sync to DB","mdi:database-sync","subtle","gray","sm","sync-btn-av",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("De-Select All","material-symbols:deselect","subtle","violet","sm","de-select-all-btn-av",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Select All","fluent:select-all-on-20-regular","subtle","grape","sm","select-all-btn-av",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Refresh","uil:refresh","subtle","blue","sm","refresh-btn-av",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button(label="Add Variable",icon_class="material-symbols:variables",varient="subtle",color="lime",size="sm",id="add-variable-btn",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                dash_table_interactivity_helptext(),
                                                daq.NumericInput(
                                                    id="num-row-to-display-numeric-av",
                                                    min=1,
                                                    max=100,
                                                    value=10,
                                                        style={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"18px","color":"dark"},
                                                ),
                                            ],
                                            non_editable_col_list=["variable_unique_id"],
                                            column_with_dropdown_names_list = ['lever_name'],
                                            column_dropdowns_data_dict = {
                                                'lever_name': {
                                                    'options': [
                                                        {'label': i, 'value': i}
                                                        for i in mongodb_utility.get_distinct_values("lever","lever_name")
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
                                        )
                                    ])
                                ],fluid=False)
                        ]
                    ),
                ])

## Callback to create add variable modal
@dash.callback(
        Output("add-variable-modal-div","children"),
        Input("add-variable-btn", "n_clicks"),
        prevent_initial_call=True
)
def create_add_variable_modal(n_av):
    ctx = dash.callback_context
    add_variable_modal_div_children = []
    if ctx.triggered_id == "add-variable-btn" and n_av:
        add_variable_modal_div_children = mantine_modal(
                                title="Add variable",
                                id="add-variable-modal",
                                size='40%',
                                is_open=True,
                                modal_component_list=[
                                    mantine_text_box(label="variable Name : *",id="variable-name-txt-al",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_select(
                                        label="Lever : *",
                                        required=False,
                                        icon_class="radix-icons:magnifying-glass",
                                        size='sm',
                                        style_dict={"width": 400},
                                        id="lever-select-av",
                                        dropdown_data= mongodb_utility.get_distinct_values("lever","lever_name")
                                    ),
                                ],
                                submit_btn_id="modal-submit-button-av",
                                cancel_btn_id="modal-cancel-button-av"
                            )
    return add_variable_modal_div_children

# Callback to handle variable modal cancel btn
@dash.callback(
        Output("add-variable-modal", "opened"),
        Input("modal-cancel-button-av", "n_clicks"),
        prevent_initial_call=True
)
def handle_cancel(n):
    if n:
        return False


# Callback to refresh variable dtl table
@dash.callback(
        Output("variable-dtl-table", "data", allow_duplicate=True),
        Output("variable-dtl-table", "dropdown", allow_duplicate=True),
        Input("refresh-btn-av", "n_clicks"),
        prevent_initial_call=True
)
def handle_submit(n):
    if n:
        column_dropdowns_data_dict = {
            'lever_name': {
                'options': [
                    {'label': i, 'value': i}
                    for i in mongodb_utility.get_distinct_values("lever","lever_name")
                ]
            }
        }
        return mongodb_utility.get_variable_collection_dump(),column_dropdowns_data_dict
    

## Callback to add variable data to DB and manage variable modal state
@dash.callback(
     [
        Output("add-variable-modal", "opened", allow_duplicate=True),
        Output("variable-add-success-toast", "is_open"),
        Output("variable-add-success-toast", "children"),
        Output("variable-name-txt-al", "value"),
        Output("lever-select-av", "value"),
        Output("variable-dtl-table", "data"),
    ],
     [
        Input("modal-submit-button-av", "n_clicks"),
    ],
     [
        State("variable-name-txt-al", "value"),
        State("lever-select-av", "value"),
    ],
    prevent_initial_call=True
)
def add_variable(n_ms,variable_name,lever_name):
    ctx = dash.callback_context
    toast_msg = ""
    if ctx.triggered_id == "modal-submit-button-av" and n_ms:
        data={}
        if variable_name =="" or lever_name == "" or lever_name is None:
            return [True,False,"",variable_name,lever_name,mongodb_utility.get_variable_collection_dump()]
        data["variable_unique_id"] = str(uuid.uuid4())
        data["variable_name"] = variable_name
        data["lever_name"] = lever_name
        toast_msg ="variable created successfully"
        mongodb_utility.insert_one_doc("variable",data)
        return [False,True,toast_msg,"","",mongodb_utility.get_variable_collection_dump()]
    else:
        return [True,False,toast_msg,"","",mongodb_utility.get_variable_collection_dump()]
    


## callback to sync variable table to db
@dash.callback(
    [
        Output("variable-update-success-toast", "is_open"),
        Output("variable-update-success-toast", "children"),
    ],
    [
        Input("sync-btn-av", "n_clicks"),
    ],
    [
        State("variable-dtl-table", "data"),
    ],
    prevent_initial_call=True
)
def sync_variable_table(n_sb,modified_tbl_data):
    if n_sb:
        current_data_from_db = mongodb_utility.get_variable_collection_dump()
        changes = list(dictdiffer.diff(current_data_from_db, modified_tbl_data))
        if len(changes) == 0:
            raise PreventUpdate
        for change in changes:
            #print(change)
            if change[0] == "change":
                unique_id = modified_tbl_data[change[1][0]]["variable_unique_id"]
                filter_for_db = {"variable_unique_id": unique_id}
                updated_data_dict = {str(change[1][1]): change[2][1]}
                mongodb_utility.update_one_doc("variable",filter_for_db,updated_data_dict)
                #print(unique_user_id)
        return [True,"variable(s) updated successfully"]
    

## Callback to delete data from variable table
@dash.callback(
    Output('delete-variable-modal', 'opened'),
    Output("variable-delete-success-toast", "is_open"),
    Output("variable-delete-success-toast", "children"),
    Output("variable-dtl-table", "data", allow_duplicate=True),
    Input('del-btn-av', 'n_clicks'),
    Input('modal-cancel-button-dv', 'n_clicks'),
    Input('modal-submit-button-dv', 'n_clicks'),
    State('variable-dtl-table', 'selected_rows'),
    State('variable-dtl-table', 'data'),
    prevent_initial_call=True
)
def delete_data(n_d,n_c,n_s,selected_rows,full_table_data):
    ctx = dash.callback_context
    data_to_be_deleted = {}
    if n_d and ctx.triggered_id == 'del-btn-av':
        return True,False,"",mongodb_utility.get_variable_collection_dump()
    if n_c and ctx.triggered_id == 'modal-cancel-button-dv':
        return False,False,"",mongodb_utility.get_variable_collection_dump()
    if n_s and ctx.triggered_id == 'modal-submit-button-dv':
        print(selected_rows)
        if len(selected_rows) > 0:
            for row_id in selected_rows:
                data_to_be_deleted=full_table_data[row_id]
                mongodb_utility.delete_one_doc("variable",data_to_be_deleted)
            text = "Selected variable(s) deleted successfully"
            return False,True,text,mongodb_utility.get_variable_collection_dump()
        else:
            text = "Nothing to delete" 
            return False,True,text,mongodb_utility.get_variable_collection_dump() 
        

## callback to select and deselect all rows in variable table
@dash.callback(
    Output('variable-dtl-table', 'selected_rows'),
    Input('select-all-btn-av', 'n_clicks'),
    Input('de-select-all-btn-av', 'n_clicks'),
    Input('modal-submit-button-dv', 'n_clicks'),
    State('variable-dtl-table', 'derived_virtual_indices'),
    State('variable-dtl-table', 'selected_rows'),
    prevent_initial_call=True
)
def select_deselect_variable(select_n_clicks, deselect_n_clicks,del_n_clicks, filtered_rows_indices,already_selected_rows):
    # print(filtered_rows_indices)
    # print(already_selected_rows)
    """Select or deselect all rows."""
    ctx = dash.callback_context
    if ctx.triggered_id == 'select-all-btn-av':
        if select_n_clicks:
            if filtered_rows_indices is None:
                return []
            else:
                return filtered_rows_indices + already_selected_rows if already_selected_rows is not None else []
    if ctx.triggered_id == 'de-select-all-btn-av':
        if deselect_n_clicks:
            return []
    if ctx.triggered_id == 'modal-submit-button-dv':
        if del_n_clicks:
            return []