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



lever_table = html.Div([
                    dmc.Space(h="lg"),
                    ## Data input Modals
                    html.Div(
                        id = "add-lever-modal-div",
                        children= [
                            mantine_modal(
                                title="Add Lever",
                                id="add-lever-modal",
                                size='40%',
                                is_open=False,
                                modal_component_list=[
                                    mantine_text_box(label="Lever Name : *",id="lever-name-txt-al",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_select(
                                        label="Pillar : *",
                                        required=False,
                                        icon_class="radix-icons:magnifying-glass",
                                        size='sm',
                                        style_dict={"width": 400},
                                        id="pillar-select-al",
                                        dropdown_data= mongodb_utility.get_distinct_values("pillar","pillar_name")
                                    ),
                                ],
                                submit_btn_id="modal-submit-button-al",
                                cancel_btn_id="modal-cancel-button-al"
                            ),
                        ]
                    ),
                    html.Div(
                        id="delete-lever-modal-div",
                        children = [
                            mantine_modal(
                                title="Alert",
                                id="delete-lever-modal",
                                size='20%',
                                is_open=False,
                                modal_component_list=[
                                    dmc.Title("Are you sure?", size="lg"),
                                ],
                                submit_btn_id="modal-submit-button-dl",
                                cancel_btn_id="modal-cancel-button-dl",
                                submit_btn_text="Yes"
                            ),
                        ]
                    ),

                    ## Success toasts
                    success_toast(id="lever-add-success-toast",is_open=False),
                    success_toast(id="lever-update-success-toast",is_open=False),
                    success_toast(id="lever-delete-success-toast",is_open=False),

                    ## data tables
                    html.Div(
                        children=[
                            dbc.Container([
                                    dbc.Row([
                                        #mantine_table(id= "user-dtl-table",table_data=mongodb_utility.create_table_from_df(pd.DataFrame(mongodb_utility.get_user_collection_dump()))),
                                        dash_datatable(
                                            id= "lever-dtl-table",
                                            data_dict=mongodb_utility.get_lever_collection_dump(),
                                            export_format='none',
                                            title="",
                                            action_btn_list=[
                                                submenu_button("Delete","ep:delete-filled","subtle","red","sm","del-btn-al",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"0px","marginTop":"20px","marginBottom":"20px"}),
                                                submenu_button("Sync to DB","mdi:database-sync","subtle","gray","sm","sync-btn-al",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("De-Select All","material-symbols:deselect","subtle","violet","sm","de-select-all-btn-al",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Select All","fluent:select-all-on-20-regular","subtle","grape","sm","select-all-btn-al",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Refresh","uil:refresh","subtle","blue","sm","refresh-btn-al",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button(label="Add Lever",icon_class="game-icons:lever",varient="subtle",color="lime",size="sm",id="add-lever-btn",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                dash_table_interactivity_helptext(),
                                                daq.NumericInput(
                                                    id="num-row-to-display-numeric-al",
                                                    min=1,
                                                    max=100,
                                                    value=10,
                                                        style={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"18px","color":"dark"},
                                                ),
                                            ],
                                            non_editable_col_list=["lever_unique_id"],
                                            column_with_dropdown_names_list = ['pillar_name'],
                                            column_dropdowns_data_dict = {
                                                'pillar_name': {
                                                    'options': [
                                                        {'label': i, 'value': i}
                                                        for i in mongodb_utility.get_distinct_values("pillar","pillar_name")
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
                    html.Div()
                ])
        

## Callback to create add lever modal
@dash.callback(
        Output("add-lever-modal-div","children"),
        Input("add-lever-btn", "n_clicks"),
        prevent_initial_call=True
)
def create_add_lever_modal(n_al):
    ctx = dash.callback_context
    add_lever_modal_div_children = []
    if ctx.triggered_id == "add-lever-btn" and n_al:
        add_lever_modal_div_children = mantine_modal(
                                title="Add Lever",
                                id="add-lever-modal",
                                size='40%',
                                is_open=True,
                                modal_component_list=[
                                    mantine_text_box(label="Lever Name : *",id="lever-name-txt-al",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_select(
                                        label="Pillar : *",
                                        required=False,
                                        icon_class="radix-icons:magnifying-glass",
                                        size='sm',
                                        style_dict={"width": 400},
                                        id="pillar-select-al",
                                        dropdown_data= mongodb_utility.get_distinct_values("pillar","pillar_name")
                                    ),
                                ],
                                submit_btn_id="modal-submit-button-al",
                                cancel_btn_id="modal-cancel-button-al"
                            )
    return add_lever_modal_div_children

# Callback to handle lever modal cancel btn
@dash.callback(
        Output("add-lever-modal", "opened"),
        Input("modal-cancel-button-al", "n_clicks"),
        prevent_initial_call=True
)
def handle_cancel(n):
    if n:
        return False
    

# Callback to refresh lever dtl table
@dash.callback(
        Output("lever-dtl-table", "data", allow_duplicate=True),
        Output("lever-dtl-table", "dropdown", allow_duplicate=True),
        Input("refresh-btn-al", "n_clicks"),
        prevent_initial_call=True
)
def handle_refresh(n):
    if n:
        column_dropdowns_data_dict = {
            'pillar_name': {
                'options': [
                    {'label': i, 'value': i}
                    for i in mongodb_utility.get_distinct_values("pillar","pillar_name")
                ]
            }
        }
        return mongodb_utility.get_lever_collection_dump(),column_dropdowns_data_dict
    

## Callback to add lever data to DB and manage lever modal state
@dash.callback(
     [
        Output("add-lever-modal", "opened", allow_duplicate=True),
        Output("lever-add-success-toast", "is_open"),
        Output("lever-add-success-toast", "children"),
        Output("lever-name-txt-al", "value"),
        Output("pillar-select-al", "value"),
        Output("lever-dtl-table", "data"),
        Output("lever-dtl-table", "dropdown"),
    ],
     [
        Input("modal-submit-button-al", "n_clicks"),
        #Input('modal-submit-button-dl', 'n_clicks'),
    ],
     [
        State("lever-name-txt-al", "value"),
        State("pillar-select-al", "value"),
        #State('lever-dtl-table', 'selected_rows'),
        #State('lever-dtl-table', 'data'),
    ],
    prevent_initial_call=True
)
def add_lever(n_ms,lever_name,pillar_name):
    ctx = dash.callback_context
    #print(ctx.triggered_id)
    toast_msg = ""
    column_dropdowns_data_dict = {
        'pillar_name': {
            'options': [
                {'label': i, 'value': i}
                for i in mongodb_utility.get_distinct_values("pillar","pillar_name")
            ]
        }
    }
    if ctx.triggered_id == "modal-submit-button-al" and n_ms:
        data={}
        if lever_name =="" or pillar_name == "" or pillar_name is None:
            return [True,False,"",lever_name,pillar_name,mongodb_utility.get_lever_collection_dump(),column_dropdowns_data_dict]
        data["lever_unique_id"] = str(uuid.uuid4())
        data["lever_name"] = lever_name
        data["pillar_name"] = pillar_name
        toast_msg ="Lever created successfully"
        mongodb_utility.insert_one_doc("lever",data)
        return [False,True,toast_msg,"","",mongodb_utility.get_lever_collection_dump(),column_dropdowns_data_dict]
    else:
        return [True,False,toast_msg,"","",mongodb_utility.get_lever_collection_dump(),column_dropdowns_data_dict]

## callback to sync lever table to db
@dash.callback(
    [
        Output("lever-update-success-toast", "is_open"),
        Output("lever-update-success-toast", "children"),
    ],
    [
        Input("sync-btn-al", "n_clicks"),
    ],
    [
        State("lever-dtl-table", "data"),
    ],
    prevent_initial_call=True
)
def sync_lever_table(n_sb,modified_tbl_data):
    if n_sb:
        current_data_from_db = mongodb_utility.get_lever_collection_dump()
        changes = list(dictdiffer.diff(current_data_from_db, modified_tbl_data))
        if len(changes) == 0:
            raise PreventUpdate
        for change in changes:
            #print(change)
            if change[0] == "change":
                unique_id = modified_tbl_data[change[1][0]]["lever_unique_id"]
                filter_for_db = {"lever_unique_id": unique_id}
                updated_data_dict = {str(change[1][1]): change[2][1]}
                mongodb_utility.update_one_doc("lever",filter_for_db,updated_data_dict)
                #print(unique_user_id)
        return [True,"Lever(s) updated successfully"]
    
## Callback to delete data from lever table
@dash.callback(
    Output('delete-lever-modal', 'opened'),
    Output("lever-delete-success-toast", "is_open"),
    Output("lever-delete-success-toast", "children"),
    Output("lever-dtl-table", "data", allow_duplicate=True),
    Input('del-btn-al', 'n_clicks'),
    Input('modal-cancel-button-dl', 'n_clicks'),
    Input('modal-submit-button-dl', 'n_clicks'),
    State('lever-dtl-table', 'selected_rows'),
    State('lever-dtl-table', 'data'),
    prevent_initial_call=True
)
def delete_data(n_d,n_c,n_s,selected_rows,full_table_data):
    ctx = dash.callback_context
    data_to_be_deleted = {}
    if n_d and ctx.triggered_id == 'del-btn-al':
        return True,False,"",mongodb_utility.get_lever_collection_dump()
    if n_c and ctx.triggered_id == 'modal-cancel-button-dl':
        return False,False,"",mongodb_utility.get_lever_collection_dump()
    if n_s and ctx.triggered_id == 'modal-submit-button-dl':
        print(selected_rows)
        if len(selected_rows) > 0:
            for row_id in selected_rows:
                data_to_be_deleted=full_table_data[row_id]
                mongodb_utility.delete_one_doc("lever",data_to_be_deleted)
            text = "Selected lever(s) deleted successfully"
            return False,True,text,mongodb_utility.get_lever_collection_dump()
        else:
            text = "Nothing to delete" 
            return False,True,text,mongodb_utility.get_lever_collection_dump() 
        

## callback to select and deselect all rows in lever table
@dash.callback(
    Output('lever-dtl-table', 'selected_rows'),
    Input('select-all-btn-al', 'n_clicks'),
    Input('de-select-all-btn-al', 'n_clicks'),
    Input('modal-submit-button-dl', 'n_clicks'),
    State('lever-dtl-table', 'derived_virtual_indices'),
    State('lever-dtl-table', 'selected_rows'),
    prevent_initial_call=True
)
def select_deselect_lever(select_n_clicks, deselect_n_clicks,del_n_clicks, filtered_rows_indices,already_selected_rows):
    # print(filtered_rows_indices)
    # print(already_selected_rows)
    """Select or deselect all rows."""
    ctx = dash.callback_context
    if ctx.triggered_id == 'select-all-btn-al':
        if select_n_clicks:
            if filtered_rows_indices is None:
                return []
            else:
                return filtered_rows_indices + already_selected_rows if already_selected_rows is not None else []
    if ctx.triggered_id == 'de-select-all-btn-al':
        if deselect_n_clicks:
            return []
    if ctx.triggered_id == 'modal-submit-button-dl':
        if del_n_clicks:
            return []

