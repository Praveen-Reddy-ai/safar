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

pillar_table = html.Div([
                    dmc.Space(h="lg"),
                    ## Data input Modals
                    html.Div(
                        children= [
                            mantine_modal(
                                title="Add Pillar",
                                id="add-pillar-modal",
                                size='40%',
                                is_open=False,
                                modal_component_list=[
                                    mantine_text_box(label="Pillar Name : *",id="pillar-name-txt-ap",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    mantine_text_box(label="Weightage : *",id="pillar-weightage-txt-ap",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False)
                                ],
                                submit_btn_id="modal-submit-button-ap",
                                cancel_btn_id="modal-cancel-button-ap"
                            ),
                            mantine_modal(
                                title="Alert",
                                id="delete-pillar-modal",
                                size='20%',
                                is_open=False,
                                modal_component_list=[
                                    dmc.Title("Are you sure?", size="lg"),
                                ],
                                submit_btn_id="modal-submit-button-dp",
                                cancel_btn_id="modal-cancel-button-dp",
                                submit_btn_text="Yes"
                            ),
                        ]
                    ),

                    ## Success toasts
                    success_toast(id="pillar-add-success-toast",is_open=False),
                    success_toast(id="pillar-update-success-toast",is_open=False),
                    success_toast(id="pillar-delete-success-toast",is_open=False),

                    ## data tables
                    html.Div(
                        children=[
                            dbc.Container([
                                    dbc.Row([
                                        #mantine_table(id= "user-dtl-table",table_data=mongodb_utility.create_table_from_df(pd.DataFrame(mongodb_utility.get_user_collection_dump()))),
                                        dash_datatable(
                                            id= "pillar-dtl-table",
                                            data_dict=mongodb_utility.get_pillar_collection_dump(),
                                            export_format='none',
                                            title="",
                                            action_btn_list=[
                                                submenu_button("Delete","ep:delete-filled","subtle","red","sm","del-btn-ap",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"0px","marginTop":"20px","marginBottom":"20px"}),
                                                submenu_button("Sync to DB","mdi:database-sync","subtle","gray","sm","sync-btn-ap",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("De-Select All","material-symbols:deselect","subtle","violet","sm","de-select-all-btn-ap",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Select All","fluent:select-all-on-20-regular","subtle","grape","sm","select-all-btn-ap",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Refresh","uil:refresh","subtle","blue","sm","refresh-btn-ap",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button(label="Add Pillar",icon_class="mdi:pillar",varient="subtle",color="lime",size="sm",id="add-pillar-btn",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                dash_table_interactivity_helptext(),
                                                 daq.NumericInput(
                                                        id="num-row-to-display-numeric-ap",
                                                        min=1,
                                                        max=100,
                                                        value=10,
                                                        style={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"18px","color":"dark"},
                                                    ),
                                            ],
                                            non_editable_col_list=["pillar_unique_id"],
                                            #table_height_px = "200px"
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
                                    ]),
                                ],fluid=False)
                        ]
                    ),
                ])
        

## Callback to add pillar data to DB and manage pillar modal state
@dash.callback(
     [
        Output("add-pillar-modal", "opened"),
        Output("pillar-add-success-toast", "is_open"),
        Output("pillar-add-success-toast", "children"),
        Output("pillar-name-txt-ap", "value"),
        Output("pillar-weightage-txt-ap", "value"),
        Output("pillar-dtl-table", "data"),
    ],
     [
        Input("add-pillar-btn", "n_clicks"),
        Input("modal-cancel-button-ap", "n_clicks"),
        Input("modal-submit-button-ap", "n_clicks"),
        Input("refresh-btn-ap", "n_clicks"),
        Input('modal-submit-button-dp', 'n_clicks'),
    ],
     [
        State("pillar-name-txt-ap", "value"),
        State("pillar-weightage-txt-ap", "value"),
        State('pillar-dtl-table', 'selected_rows'),
        State('pillar-dtl-table', 'data'),
    ],
    prevent_initial_call=True
)
def add_pillar(n_ap,n_mc,n_ms,n_r,n_dp,pillar_name,pillar_weightage,selected_row_ids,full_table_data):
    ctx = dash.callback_context
    toast_msg = ""
    if ctx.triggered_id == "add-pillar-btn" and n_ap:
        return [True,False,toast_msg,"","",mongodb_utility.get_pillar_collection_dump()]
    if ctx.triggered_id == "modal-cancel-button-ap" and n_mc:
        return [False,False,toast_msg,"","",mongodb_utility.get_pillar_collection_dump()]
    if ctx.triggered_id == "modal-submit-button-ap" and n_ms:
        data={}
        if pillar_name =="" or pillar_weightage == "":
            return [True,False,"",pillar_name,pillar_weightage,mongodb_utility.get_pillar_collection_dump()]
        data["pillar_unique_id"] = str(uuid.uuid4())
        data["pillar_name"] = pillar_name
        data["pillar_weightage"] = pillar_weightage
        toast_msg ="Pillar created successfully"
        mongodb_utility.insert_one_doc("pillar",data)
        return [False,True,toast_msg,"","",mongodb_utility.get_pillar_collection_dump()]
    if ctx.triggered_id == "refresh-btn-ap" and n_r:
        return [False,False,toast_msg,"","",mongodb_utility.get_pillar_collection_dump()]
    if ctx.triggered_id == "modal-submit-button-dp" and n_dp:
        if len(selected_row_ids)>0:
            for row_id in selected_row_ids:
                data_to_be_deleted=full_table_data[row_id]
                mongodb_utility.delete_one_doc("pillar",data_to_be_deleted)
            return [False,False,toast_msg,"","",mongodb_utility.get_pillar_collection_dump()]


## callback to sync pillar table to db
@dash.callback(
    [
        Output("pillar-update-success-toast", "is_open"),
        Output("pillar-update-success-toast", "children"),
    ],
    [
        Input("sync-btn-ap", "n_clicks"),
    ],
    [
        State("pillar-dtl-table", "data"),
    ],
    prevent_initial_call=True
)
def sync_pillar_table(n_sb,modified_tbl_data):
    if n_sb:
        current_data_from_db = mongodb_utility.get_pillar_collection_dump()
        changes = list(dictdiffer.diff(current_data_from_db, modified_tbl_data))
        if len(changes) == 0:
            raise PreventUpdate
        for change in changes:
            #print(change)
            if change[0] == "change":
                unique_id = modified_tbl_data[change[1][0]]["pillar_unique_id"]
                filter_for_db = {"pillar_unique_id": unique_id}
                updated_data_dict = {str(change[1][1]): change[2][1]}
                mongodb_utility.update_one_doc("pillar",filter_for_db,updated_data_dict)
                #print(unique_user_id)
        return [True,"Pillar(s) updated successfully"]
    
## callback to select and deselect all rows in Pillar table
@dash.callback(
    Output('pillar-dtl-table', 'selected_rows'),
    Input('select-all-btn-ap', 'n_clicks'),
    Input('de-select-all-btn-ap', 'n_clicks'),
    Input('modal-submit-button-dp', 'n_clicks'),
    State('pillar-dtl-table', 'derived_virtual_indices'),
    State('pillar-dtl-table', 'selected_rows'),
    prevent_initial_call=True
)
def select_deselect_pillar(select_n_clicks, deselect_n_clicks,del_pillar_n_clicks, filtered_rows_indices,already_selected_rows):
    # print(filtered_rows_indices)
    # print(already_selected_rows)
    """Select or deselect all rows."""
    ctx = dash.callback_context
    if ctx.triggered_id == 'select-all-btn-ap':
        if select_n_clicks:
            if filtered_rows_indices is None:
                return []
            else:
                return filtered_rows_indices + already_selected_rows if already_selected_rows is not None else []
    if ctx.triggered_id == 'de-select-all-btn-ap':
        if deselect_n_clicks:
            return []
    if ctx.triggered_id == 'modal-submit-button-dp':
        if del_pillar_n_clicks:
            return []
        

## Callback to delete data from pillar table
@dash.callback(
    Output('delete-pillar-modal', 'opened'),
    Output("pillar-delete-success-toast", "is_open"),
    Output("pillar-delete-success-toast", "children"),
    Input('del-btn-ap', 'n_clicks'),
    Input('modal-cancel-button-dp', 'n_clicks'),
    Input('modal-submit-button-dp', 'n_clicks'),
    State('pillar-dtl-table', 'selected_rows'),
    prevent_initial_call=True
)
def delete_data(n_d,n_c,n_s,selected_rows):
    ctx = dash.callback_context
    data_to_be_deleted = {}
    if n_d and ctx.triggered_id == 'del-btn-ap':
        return True,False,""
    if n_c and ctx.triggered_id == 'modal-cancel-button-dp':
        return False,False,""
    if n_s and ctx.triggered_id == 'modal-submit-button-dp':
        print(selected_rows)
        if len(selected_rows) > 0:
            text = "Selected pillars deleted successfully"
            return False,True,text
        else:
            text = "Nothing to delete" 
            return False,True,text 