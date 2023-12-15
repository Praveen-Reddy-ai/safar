from dash import html
from dash import dcc,dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd

## Methods to create different common components

def submenu_button(label,icon_class,varient,color,size,id,style_dict={},class_name=""):
    return html.A(
                    dmc.Button(
                        label,
                        leftIcon=[DashIconify(icon=icon_class)],
                        variant=varient,
                        color=color,
                        size=size,
                        id=str(id),
                        style=style_dict,
                        className=class_name
                    ),
                )

def mantine_text_box(label,id,required,size,style_dict,icon_class,is_password,placeholder=""):
    return dmc.TextInput(
                    label=label,
                    id=str(id),
                    required=required,
                    size=size,
                    type='password' if is_password else 'text',
                    style=style_dict,
                    rightSection=[DashIconify(icon=icon_class,width=20)],
                    placeholder=placeholder
                )

def mantine_modal(title,id,size,is_open,modal_component_list,submit_btn_id,cancel_btn_id,submit_btn_text="Submit"):
    return dmc.Modal(
                    title=title,
                    id=str(id),
                    size=size,
                    opened=is_open,
                    children=[
                        dmc.Paper(
                            children=[
                                dbc.Container(
                                [
                                    #dbc.Row(dmc.Space(h="md")),
                                    dbc.Row([
                                        dbc.Col([
                                            dmc.Space(h="md"),
                                            component,
                                        ],width="auto"),
                                    ])
                                    for component in modal_component_list
                                ]),
                                dmc.Space(h="xl")
                            ],
                            shadow="xl",
                            withBorder=True,
                            radius='md',
                        ),
                        dmc.Space(h="md"),
                        dmc.Group(
                            [
                                dmc.Button(submit_btn_text, id=submit_btn_id) if submit_btn_id else "",
                                dmc.Button(
                                    "Cancel",
                                    id=cancel_btn_id,
                                ) if cancel_btn_id else "",
                            ],
                            position="right",
                        ),
                    ],
                )

def success_toast(id,is_open):
    return dbc.Toast(
                    children=[],
                    id=str(id),
                    header="Success",
                    is_open=is_open,
                    dismissable=True,
                    icon="success",
                    duration=2000,
                    # top: 66 positions the toast below the navbar
                    style={"position": "fixed", "top": 60, "right": 10, "width": 350},
                )

def bootstrap_popover(body,targer_component_id,id):
    return dbc.Popover(
                    dbc.PopoverBody(body),
                    target=targer_component_id,
                    autohide=True,
                    is_open=False,
                    id=id
                )

def mantine_select(label,required,icon_class,size,style_dict,id,dropdown_data,placeholder="Select one",iconWidth=20):
    return dmc.Select(
                    label=label,
                    placeholder=placeholder,
                    required=required,
                    shadow='sm',
                    transition='skew-down',
                    searchable=True,
                    creatable=True, 
                    nothingFound="No options found",
                    clearable=True,
                    dropdownPosition="flip",
                    selectOnBlur=True,
                    icon=[DashIconify(icon=icon_class)],
                    iconWidth=iconWidth,
                    size=size,
                    style=style_dict,
                    id=id,
                    data=dropdown_data
                )

def mantine_table(id,table_data):
    return dmc.Table(
                    id = id,
                    striped=True,
                    highlightOnHover=True,
                    withBorder=True,
                    withColumnBorders=True,
                    children= table_data
                )

def dash_table_interactivity_helptext():
    component = dmc.HoverCard(
                            withArrow=True,
                            width=500,
                            shadow="md",
                            style={"float":"right","marginRight":"10px","marginTop":"20px"},
                            children=[
                                dmc.HoverCardTarget(dmc.Button("Help",leftIcon=[DashIconify(icon="material-symbols:help-center-rounded")],variant="subtle",color="gray")),
                                dmc.HoverCardDropdown(
                                    children = [
                                        dmc.Space(h="xs"),
                                        html.Div(["   Filter: ", dmc.Kbd("Click filter data cell") ," + ",dmc.Kbd("type text")," + ", dmc.Kbd("press enter")]),
                                        dmc.Space(h="xs"),
                                        html.Div(["   Edit: ",dmc.Kbd("double click cell")," + ", dmc.Kbd("type text")," + ", dmc.Kbd("press enter")," + ", dmc.Kbd("click sync to DB")]),
                                        dmc.Space(h="xs"),
                                    ]
                                ),
                            ],
                        )
    return component

def dash_datatable(id,data_dict,export_format,title,action_btn_list,non_editable_col_list,column_with_dropdown_names_list=[],column_dropdowns_data_dict={},table_style={},table_css=[]):
    table = html.Div([
        html.Div(children=action_btn_list),
        dmc.Title("", order=3),
        dmc.Space(h="xl"),
        dmc.Space(h="xl"),
        dash_table.DataTable(
                id=id,
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False,"editable":False if i in non_editable_col_list else True,"hideable":False, 'presentation': 'dropdown' if i in column_with_dropdown_names_list else 'input'} for i in pd.DataFrame(data_dict).columns
                ],
                editable=True,
                data=data_dict,
                filter_action="native",
                filter_options={"case":"insensitive","placeholder_text":"filter data..."},
                sort_action="native",
                sort_mode="multi",
                column_selectable=False,
                row_selectable="multi",
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 10,
                style_table=table_style,
                style_header={
                    'backgroundColor': 'PaleTurquoise',
                    'color': 'dark',
                    'fontWeight': 'bold',
                    'textTransform': 'uppercase'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'GhostWhite',
                    }
                ],
                style_cell={'textAlign': 'left'},
                css=table_css,
                export_format=export_format,
                dropdown = column_dropdowns_data_dict
        ),
        #html.Div(children=action_btn_list),
    ])
    return table