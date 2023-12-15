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

initial_values = [
    [
        {"value": lever, "label": lever, "group": "Lever"}
        for lever in mongodb_utility.get_distinct_values("lever","lever_name")
    ],
    [],
]

template_table = html.Div([
                    dmc.Space(h="lg"),
                    ## Data input Modals
                    html.Div(
                        id = "add-template-modal-div",
                        children= [
                            mantine_modal(
                                title="Add template",
                                id="add-template-modal",
                                size='50%',
                                is_open=False,
                                modal_component_list=[
                                    mantine_text_box(label="Template Name : *",id="template-name-txt-at",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    html.Div(
                                        [
                                            dmc.TransferList(
                                                id="transfer-list-tl", 
                                                value=initial_values,
                                                listHeight="400",
                                                #titles=["Current Pillar-Lever Structure","Filtered Pillar-Lever Structure"],
                                                searchPlaceholder=['Search item to add...', 'Search item to remove...'],
                                                nothingFound=['Cannot find item to add', 'Cannot find item to remove'],
                                                placeholder=['No item left to add', 'No item left ro remove']),
                                            #html.Div(id="transfer-list-values-2"),
                                        ]
                                    )
                                ],
                                submit_btn_id="modal-submit-button-at",
                                cancel_btn_id="modal-cancel-button-at"
                            ),
                        ]
                    ),
                    html.Div(
                        id="delete-template-modal-div",
                        children = [
                            mantine_modal(
                                title="Alert",
                                id="delete-template-modal",
                                size='20%',
                                is_open=False,
                                modal_component_list=[
                                    dmc.Title("Are you sure?", size="lg"),
                                ],
                                submit_btn_id="modal-submit-button-dt",
                                cancel_btn_id="modal-cancel-button-dt",
                                submit_btn_text="Yes"
                            ),
                        ]
                    ),

                    ## Success toasts
                    success_toast(id="template-add-success-toast",is_open=False),
                    success_toast(id="template-update-success-toast",is_open=False),
                    success_toast(id="template-delete-success-toast",is_open=False),

                    ## data tables
                    html.Div(
                        id = "template-dtl-table-div",
                        children=[
                            dbc.Container([
                                    dbc.Row([
                                        #mantine_table(id= "user-dtl-table",table_data=mongodb_utility.create_table_from_df(pd.DataFrame(mongodb_utility.get_user_collection_dump()))),
                                        dash_datatable(
                                            id= "template-dtl-table",
                                            data_dict = mongodb_utility.get_assessment_template_collection_dump(),
                                            export_format='none',
                                            title="",
                                            action_btn_list=[
                                                submenu_button("Delete","ep:delete-filled","subtle","red","sm","del-btn-at",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"0px","marginTop":"20px","marginBottom":"20px"}),
                                                submenu_button("Sync to DB","mdi:database-sync","subtle","gray","sm","sync-btn-at",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("De-Select All","material-symbols:deselect","subtle","violet","sm","de-select-all-btn-at",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Select All","fluent:select-all-on-20-regular","subtle","grape","sm","select-all-btn-at",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button("Refresh","uil:refresh","subtle","blue","sm","refresh-btn-at",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                submenu_button(label="Add Template",icon_class="ri:survey-fill",varient="subtle",color="lime",size="sm",id="add-template-btn",style_dict={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"20px"}),
                                                dash_table_interactivity_helptext(),
                                                daq.NumericInput(
                                                    id="num-row-to-display-numeric-at",
                                                    min=1,
                                                    max=100,
                                                    value=10,
                                                        style={"float":"right","padding":"2px 4px 2px 4px","marginRight":"10px","marginTop":"18px","color":"dark"},
                                                ),
                                            ],
                                            non_editable_col_list=["template_unique_id"],
                                            #column_with_dropdown_names_list = ['pillar','lever','variable'],
                                            # column_dropdowns_data_dict = {
                                            #     'pillar': {
                                            #         'options': [
                                            #             {'label': i, 'value': i}
                                            #             for i in mongodb_utility.get_distinct_values("pillar","pillar_name")
                                            #         ]
                                            #     },
                                            #     'lever': {
                                            #         'options': [
                                            #             {'label': i, 'value': i}
                                            #             for i in mongodb_utility.get_distinct_values("lever","lever_name")
                                            #         ]
                                            #     },
                                            #     'variable': {
                                            #         'options': [
                                            #             {'label': i, 'value': i}
                                            #             for i in mongodb_utility.get_distinct_values("variable","variable_name")
                                            #         ]
                                            #     }
                                            # },
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
    

## Callback to create add template modal
@dash.callback(
        Output("add-template-modal-div","children"),
        Input("add-template-btn", "n_clicks"),
        prevent_initial_call=True
)
def create_add_template_modal(n_at):
    ctx = dash.callback_context
    add_template_modal_div_children = []
    if ctx.triggered_id == "add-template-btn" and n_at:
        initial_values = [
            [
                {"value": lever, "label": lever, "group": "Lever"}
                for lever in mongodb_utility.get_distinct_values("lever","lever_name")
            ],
            [],
        ]
        add_template_modal_div_children = mantine_modal(
                                title="Add Template",
                                id="add-template-modal",
                                size='50%',
                                is_open=True,
                                modal_component_list=[
                                    mantine_text_box(label="Template Name : *",id="template-name-txt-at",required=False,size='sm',style_dict={"width": 400},icon_class="fluent:options-16-filled",is_password=False),
                                    html.Div(
                                        [
                                            dmc.TransferList(
                                                id="transfer-list-tl", 
                                                value=initial_values,
                                                listHeight="400",
                                                #titles=["Current Pillar-Lever Structure","Filtered Pillar-Lever Structure"],
                                                searchPlaceholder=['Search item to add...', 'Search item to remove...'],
                                                nothingFound=['Cannot find item to add', 'Cannot find item to remove'],
                                                placeholder=['No item left to add', 'No item left ro remove']),
                                            #html.Div(id="transfer-list-values-2"),
                                        ]
                                    )
                                ],
                                submit_btn_id="modal-submit-button-at",
                                cancel_btn_id="modal-cancel-button-at"
                            )
    return add_template_modal_div_children


# Callback to handle template modal cancel btn
@dash.callback(
        Output("add-template-modal", "opened", allow_duplicate=True),
        Input("modal-cancel-button-at", "n_clicks"),
        prevent_initial_call=True
)
def handle_cancel(n):
    if n:
        return False
    

# Callback to refresh template dtl table
@dash.callback(
        Output("template-dtl-table", "data", allow_duplicate=True),
        Input("refresh-btn-at", "n_clicks"),
        prevent_initial_call=True
)
def handle_refresh(n):
    if n:
        return mongodb_utility.get_assessment_template_collection_dump()


## Callback to add template data to DB and manage template modal state
@dash.callback(
     [
        Output("add-template-modal", "opened"),
        Output("template-add-success-toast", "is_open"),
        Output("template-add-success-toast", "children"),
        Output("template-name-txt-at", "value"),
        Output("transfer-list-tl", "value"),
        Output("template-dtl-table", "data"),
    ],
     [
        Input("modal-submit-button-at", "n_clicks"),
    ],
     [
        State("template-name-txt-at", "value"),
        State("transfer-list-tl", "value"),
    ],
    prevent_initial_call=True
)
def add_template(n_ms,template_name,transfer_list_val):
    ctx = dash.callback_context
    #print(ctx.triggered_id)
    toast_msg = ""
    if ctx.triggered_id == "modal-submit-button-at" and n_ms:
        data={}
        if template_name =="" or template_name is None:
            return [True,False,"",template_name,transfer_list_val,mongodb_utility.get_assessment_template_collection_dump()]
        data["template_unique_id"] = str(uuid.uuid4())
        data["template_name"] = template_name
        data["associated_levers"] = [item["value"] for item in transfer_list_val[1]]
        toast_msg ="Template created successfully"
        mongodb_utility.insert_one_doc("template",data)
        toast_msg ="Template created successfully"
        return [False,True,toast_msg,"",transfer_list_val,mongodb_utility.get_assessment_template_collection_dump()]
    else:
        return [True,False,toast_msg,"",transfer_list_val,mongodb_utility.get_assessment_template_collection_dump()]
    


## callback to sync template table to db
@dash.callback(
    [
        Output("template-update-success-toast", "is_open"),
        Output("template-update-success-toast", "children"),
    ],
    [
        Input("sync-btn-at", "n_clicks"),
    ],
    [
        State("template-dtl-table", "data"),
    ],
    prevent_initial_call=True
)
def sync_lever_table(n_sb,modified_tbl_data):
    if n_sb:
        current_data_from_db = mongodb_utility.get_assessment_template_collection_dump()
        changes = list(dictdiffer.diff(current_data_from_db, modified_tbl_data))
        if len(changes) == 0:
            raise PreventUpdate
        for change in changes:
            #print(change)
            if change[0] == "change":
                template_unique_id = modified_tbl_data[change[1][0]]["template_unique_id"]
                filter_for_db = {"template_unique_id": template_unique_id}
                updated_data_dict = {str(change[1][1]): change[2][1]}
                mongodb_utility.update_one_doc("template",filter_for_db,updated_data_dict)
                #print(unique_user_id)
        return [True,"Template(s) updated successfully"]


## Callback to delete data from template table
@dash.callback(
    Output('delete-template-modal', 'opened'),
    Output("template-delete-success-toast", "is_open"),
    Output("template-delete-success-toast", "children"),
    Output("template-dtl-table", "data", allow_duplicate=True),
    Input('del-btn-at', 'n_clicks'),
    Input('modal-cancel-button-dt', 'n_clicks'),
    Input('modal-submit-button-dt', 'n_clicks'),
    State('template-dtl-table', 'selected_rows'),
    State('template-dtl-table', 'data'),
    prevent_initial_call=True
)
def delete_data(n_d,n_c,n_s,selected_rows,full_table_data):
    ctx = dash.callback_context
    data_to_be_deleted = {}
    if n_d and ctx.triggered_id == 'del-btn-at':
        return True,False,"",mongodb_utility.get_assessment_template_collection_dump()
    if n_c and ctx.triggered_id == 'modal-cancel-button-dt':
        return False,False,"",mongodb_utility.get_assessment_template_collection_dump()
    if n_s and ctx.triggered_id == 'modal-submit-button-dt':
        #print(selected_rows)
        if len(selected_rows) > 0:
            for row_id in selected_rows:
                data_to_be_deleted=full_table_data[row_id]
                query = {"template_unique_id":data_to_be_deleted["template_unique_id"]}
                mongodb_utility.delete_one_doc("template",query)
            text = "Selected template(s) deleted successfully"
            return False,True,text,mongodb_utility.get_assessment_template_collection_dump()
        else:
            text = "Nothing to delete" 
            return False,True,text,mongodb_utility.get_assessment_template_collection_dump() 
        

## callback to select and deselect all rows in template table
@dash.callback(
    Output('template-dtl-table', 'selected_rows'),
    Input('select-all-btn-at', 'n_clicks'),
    Input('de-select-all-btn-at', 'n_clicks'),
    Input('modal-submit-button-dt', 'n_clicks'),
    State('template-dtl-table', 'derived_virtual_indices'),
    State('template-dtl-table', 'selected_rows'),
    prevent_initial_call=True
)
def select_deselect_lever(select_n_clicks, deselect_n_clicks,del_n_clicks, filtered_rows_indices,already_selected_rows):
    # print(filtered_rows_indices)
    # print(already_selected_rows)
    """Select or deselect all rows."""
    ctx = dash.callback_context
    if ctx.triggered_id == 'select-all-btn-at':
        if select_n_clicks:
            if filtered_rows_indices is None:
                return []
            else:
                return filtered_rows_indices + already_selected_rows if already_selected_rows is not None else []
    if ctx.triggered_id == 'de-select-all-btn-at':
        if deselect_n_clicks:
            return []
    if ctx.triggered_id == 'modal-submit-button-dt':
        if del_n_clicks:
            return []
        