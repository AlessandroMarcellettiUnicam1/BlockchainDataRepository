import pandas as pd
from dash import html, dcc
import plotly.express as px
from data_from_backend import fetch_all_data, fetch_details_events, fetch_details_input, fetch_details_storageState, fetch_details_internalTxs

from components.detailsTable import create_details_table

# Layout della schermata "Grafici Dettagliati"
def layout(contract_type):

    df_general = pd.DataFrame(fetch_all_data(contract_type))

    df = pd.DataFrame(fetch_details_input(contract_type))
    columns = df.columns.to_list()
    columnsNew = [col for col in columns if col not in ["Transaction Hash", "Block Number", "Activity", "From"]]


    df2 = pd.DataFrame(fetch_details_storageState(contract_type))
    storageState_div = None
    if not df2.empty:
        columns2 = df2.columns.to_list()
        columns2new = [col for col in columns2 if col not in ["Transaction Hash", "Block Number", "Activity", "From"]]
        storageState_div = html.Div(
            style={
                "width": "100%", 
                "display": "flex",  
                "flexDirection": "column",
                "justifyContent": "center",  
                "alignItems": "center",  
                "marginTop": "10px"
            },
            id = "storage_table_div",
            children=[
                html.H2("StorageState information", style={"textAlign": "center"}),
                create_details_table(df2, columns2new, "320px", "1300px", "storageState"),
            ]
        )
    else: storageState_div = html.Div(
            id="transaction-table_storageState",
            children=[
                html.P("StorageState information: Nessun dato presente", style={"textAlign": "center", "fontWeight": "bold", "fontSize": "24px"}
                )
            ],
            style={"display": "block"}
        )
    
    df3 = pd.DataFrame(fetch_details_internalTxs(contract_type))
    internalTxs_div = None
    if not df3.empty:
        columns3 = df3.columns.to_list()
        columns3new = [col for col in columns3 if col not in ["Transaction Hash", "Block Number", "Activity", "From"]]
        internalTxs_div = html.Div(
            style={
                "width": "100%", 
                "display": "flex", 
                "flexDirection": "column",
                "justifyContent": "center", 
                "alignItems": "center",
                "marginTop": "10px"
            },
            id = "internalTxs_table_div",
            children=[
                html.H2("InternalTxs information", style={"textAlign": "center"}),
                create_details_table(df3, columns3new, "300px", "900px", "internalTxs"),
            ]
        )
    else: internalTxs_div = html.Div(
            id="transaction-table_internalTxs",
            children=[
                html.P(
                    "InternalTxs information: Nessun dato disponibile",
                    style={"textAlign": "center", "fontWeight": "bold", "fontSize": "24px"}
                )
            ],
            style={"display": "block"}
        )

    df4 = pd.DataFrame(fetch_details_events(contract_type, activities="approve,transfer,transferFrom"))
    eventApproveTransfer_div = None
    if not df4.empty:
        columns4 = df4.columns.to_list()
        columns4new = [col for col in columns4 if col not in ["Transaction Hash", "Block Number", "Activity", "From"]]
        eventApproveTransfer_div = html.Div(
            style={
                "width": "100%",  
                "display": "flex", 
                "flexDirection": "column",
                "justifyContent": "center", 
                "alignItems": "center",  
                "marginTop": "10px"
            },
            id = "event_type1_table_div",
            children=[
                html.H3("Activity: approve, transfer and transferFrom"),
                create_details_table(df4, columns4new, "320px", "1200px", "approve&Transfer")
            ]
        )
    else: eventApproveTransfer_div = html.Div(
            id="transaction-table_approve&Transfer",
            children=[],
            style={"display": "none"}
        )

    df5 = pd.DataFrame(fetch_details_events(contract_type, activities="sendFrom"))
    eventSendFrom_div = None
    if not df5.empty:
        columns5 = df5.columns.to_list()
        columns5new = [col for col in columns5 if col not in ["Transaction Hash", "Block Number", "Activity", "From"]]
        eventSendFrom_div = html.Div(
            style={
                "width": "100%", 
                "display": "flex", 
                "flexDirection": "column",
                "justifyContent": "center", 
                "alignItems": "center", 
                "marginTop": "10px"
            },
            id = "event_type2_table_div",
            children=[
                html.H3("Activity: sendFrom"),
                create_details_table(df5, columns5new, "320px", "1200px", "sendFrom")
            ]
        )
    else: eventSendFrom_div = html.Div(
            id="transaction-table_sendFrom",
            children=[],
            style={"display": "none"}
        )

    df6 = pd.DataFrame(fetch_details_events(contract_type, activities="transferOwnership"))
    eventTransferOwnership_div = None
    if not df6.empty:
        columns6 = df6.columns.to_list()
        columns6new = [col for col in columns6 if col not in ["Transaction Hash", "Block Number", "Activity", "From"]]
        eventTransferOwnership_div = html.Div(
            style={
                "width": "100%", 
                "display": "flex", 
                "flexDirection": "column",
                "justifyContent": "center", 
                "alignItems": "center",
                "marginTop": "10px"
            },
            id = "event_type3_table_div",
            children=[
                html.H3("Activity: transferOwnership"),
                create_details_table(df6, columns6new, "320px", "1200px", "transferOwnership")
            ]
        ) 
    else: eventTransferOwnership_div = html.Div(
            id="transaction-table_transferOwnership",
            children=[],
            style={"display": "none"}
        ) 

    df7 = pd.DataFrame(fetch_details_events(contract_type, activities="safeTransferFrom"))
    eventSafeTransferFrom_div = None
    if not df7.empty:
        columns7 = df7.columns.to_list()
        columns7new = [col for col in columns7 if col not in ["Transaction Hash", "Block Number", "Activity", "From"]]
        eventSafeTransferFrom_div = html.Div(
            style={
                "width": "100%", 
                "display": "flex",  
                "flexDirection": "column",
                "justifyContent": "center",  
                "alignItems": "center", 
                "marginTop": "10px"
            },
            id = "event_type4_table_div",
            children=[
                html.H3("Activity: safeTransferFrom"),
                create_details_table(df7, columns7new, "320px", "1200px", "safeTransferFrom")
            ]
        )
    else: eventSafeTransferFrom_div = html.Div(
            id="transaction-table_safeTransferFrom",
            children=[],
            style={"display": "none"}
        )
    
    df8 = pd.DataFrame(fetch_details_events(contract_type, activities="setApprovalForAll"))
    eventSetApprovalForAll_div = None
    if not df8.empty:
        columns8 = df8.columns.to_list()
        columns8new = [col for col in columns8 if col not in ["Transaction Hash", "Block Number", "Activity", "From"]]
        eventSetApprovalForAll_div = html.Div(
            style={
                "width": "100%",
                "display": "flex", 
                "flexDirection": "column",
                "justifyContent": "center",
                "alignItems": "center", 
                "marginTop": "10px"
            },
            id = "event_type5_table_div",
            children=[
                html.H3("Activity: setApprovalForAll"),
                create_details_table(df8, columns8new, "320px", "1200px", "setApprovalForAll")
            ]
        )
    else: eventSetApprovalForAll_div = html.Div(
            id="transaction-table_setApprovalForAll",
            children=[],
            style={"display": "none"}
        )
    

    return html.Div(
        style={"display": "flex", "flexDirection": "column", "height": "100vh"}, 
        children=[
            html.Div(
                style={
                    "position": "absolute", "top": "0", "left": "50%", "transform": "translateX(-50%)", "marginTop": "20px", 
                    "display": "flex", "flexDirection": "row", "justifyContent": "center", "gap": "20px", "marginBottom": "20px"
                },
                children=[
                    dcc.Link(
                        html.Button("Back to General graphs", style={"marginBottom": "10px", "padding": "10px", "fontSize": "16px"}),
                        href= f"/general/{contract_type}"
                    ),
                    dcc.Link(
                        html.Button("Back to Home page", style={"padding": "10px", "fontSize": "16px"}),
                        href="/"
                    ),
                ]
            ),
            dcc.Store(id="df-inputs", data=df.to_dict("records")),
            dcc.Store(id="df-storageState", data=df2.to_dict("records")),
            dcc.Store(id="df-internalTxs", data=df3.to_dict("records")),
            dcc.Store(id="df-events_approve_transfer", data=df4.to_dict("records")),
            dcc.Store(id="df-events_sendFrom", data=df5.to_dict("records")),
            dcc.Store(id="df-events_transferOwnership", data=df6.to_dict("records")),
            dcc.Store(id="df-events_safeTransferFrom", data=df7.to_dict("records")),
            dcc.Store(id="df-events_setApprovalForAll", data=df8.to_dict("records")),

            dcc.Store(id="df-general", data=df_general.to_dict("records")),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="activity_details",
                                options=[{"label": activityValue, "value": activityValue} for activityValue in df_general["Activity"].unique()],
                                placeholder="Select activity",
                                value=None,
                                style={"width": "250px"},
                            ),
                            dcc.Dropdown(
                                id="blockNumber_details",
                                options=[{"label": blockNumber, "value": blockNumber} for blockNumber in df_general["Block Number"].unique()],
                                placeholder="Select block number",
                                value=None,
                                style={"width": "250px", "marginLeft": "10px"},
                            ),
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "center", 
                            "alignItems": "center"
                        },
                    ),

                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="sender_details",
                                options=[{"label": sender, "value": sender} for sender in df_general["From"].unique()],
                                placeholder="Select sender",
                                value=None,
                                style={"width": "500px"},
                            ),
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "center", 
                            "alignItems": "center",
                            "marginTop": "20px" 
                        }
                    ),
                    
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="transaction_details",
                                options=[{"label": transaction, "value": transaction} for transaction in df_general["Transaction Hash"].unique()],
                                placeholder="Select transaction hash",
                                value=None,
                                style={"width": "650px"},
                            )
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "center", 
                            "alignItems": "center",
                            "marginTop": "20px" 
                        }
                    )
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center", 
                    "alignItems": "center", 
                    "marginTop": "80px",
                    "marginBottom": "20px", 
                },
            ),

            html.Div(
                style={
                    "width": "100%",  
                    "display": "flex", 
                    "flexDirection": "column",
                    "justifyContent": "center",  
                    "alignItems": "center",
                    "marginTop": "20px"
                },
                id = "input_table_div",
                children=[
                    html.H2("All inputs informations", style={"textAlign": "center"}),
                    create_details_table(df, columnsNew, "300px", "850px", "inputs")
                ]
            ),

            storageState_div,

            internalTxs_div,

            html.Div(
                style={
                    "width": "100%", 
                    "display": "flex",  
                    "flexDirection": "column",
                    "justifyContent": "center",  
                    "alignItems": "center", 
                    "marginTop": "10px"
                },
                children=[
                    html.H2("Events information", style={"textAlign": "center"}),
                    eventApproveTransfer_div,
                    eventSendFrom_div,
                    eventTransferOwnership_div,
                    eventSafeTransferFrom_div,
                    eventSetApprovalForAll_div
                ]
            ),
            
        ]
    )