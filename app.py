import dash
import re
from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State

import pandas as pd

from data_from_backend import all_collections_name

# Inizializzazione dell'app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

import pages.general as general
import pages.details as details
import pages.ocel as ocel

collections = all_collections_name()

# Layout della schermata iniziale con i pulsanti per selezionare la collezione da analizzare
def homepage():
    return html.Div(
        style={
            "display": "flex", "flexDirection": "column", 
            "justifyContent": "center", "alignItems": "center", 
            "height": "100vh"
        },
        children=[
            html.H1("choose the type of contract for the analysis", style={"marginBottom": "20px"}),
            *[
                dcc.Link(
                    html.Button(collection, style={"marginBottom": "10px", "padding": "10px", "fontSize": "16px"}),
                    href="/ocel" if "ocel" in collection.lower() else f"/general/{collection}"
                ) for collection in collections
            ]
        ]
    )


# Gestire la navigazione tra le pagine
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):

    if pathname.startswith("/general"):

        if pathname.endswith("/contracts_details"):
            match = re.match(r"^/general/([\w\d]+)/contracts_details", pathname)
            param = match.group(1) if match else None
            return details.layout(param) 
        else:
            match = re.match(r"^/general/([\w\d]+)", pathname)
            param = match.group(1) if match else None
            return general.layout(param) 

    elif pathname == "/ocel":
        return ocel.layout()
    else:
        return homepage()


@app.callback(
    [
        Output("transaction-table", "data"),
        Output("activity", "options"),
        Output("blockNumber", "options"),
        Output("sender", "options"),
    ],
    [
        Input("activity", "value"),
        Input("blockNumber", "value"),
        Input("sender", "value"),
    ],
    [State("df-store", "data")]
)
def update_table_and_filters(selected_activity, selected_blockNumber, selected_sender, df_data):
    
    if df_data is None:
        return [], [], [], []

    df = pd.DataFrame(df_data)

    df_filtered = df.copy()
    print(type(str(selected_blockNumber)))
    print(type(df_filtered["Block Number"].iloc[0]))

    # Filtra i dati in base ai filtri selezionati
    if selected_activity:
        df_filtered = df_filtered[df_filtered["Activity"] == selected_activity]
    if selected_blockNumber:
        df_filtered = df_filtered[df_filtered["Block Number"] == selected_blockNumber]
    if selected_sender:
        df_filtered = df_filtered[df_filtered["From"] == selected_sender]

    activity_options = [{"label": activity, "value": activity} for activity in df_filtered["Activity"].unique()]
    blockNumber_options = [{"label": block, "value": block} for block in df_filtered["Block Number"].unique()]
    sender_options = [{"label": sender, "value": sender} for sender in df_filtered["From"].unique()]

    return df_filtered.to_dict("records"), activity_options, blockNumber_options, sender_options


@app.callback(
    [
        Output("transaction-table_inputs", "data"),
        Output("transaction-table_storageState", "data"),
        Output("transaction-table_internalTxs", "data"),
        Output("transaction-table_approve&Transfer", "data"),
        Output("transaction-table_sendFrom", "data"),
        Output("transaction-table_transferOwnership", "data"),
        Output("transaction-table_safeTransferFrom", "data"),
        Output("transaction-table_setApprovalForAll", "data"),
        Output("activity_details", "options"),
        Output("blockNumber_details", "options"),
        Output("sender_details", "options"),
        Output("transaction_details", "options"),
    ],
    [
        Input("activity_details", "value"),
        Input("blockNumber_details", "value"),
        Input("sender_details", "value"),
        Input("transaction_details", "value"),
    ],
    [
        State("df-inputs", "data"),
        State("df-storageState", "data"),
        State("df-internalTxs", "data"),
        State("df-events_approve_transfer", "data"),
        State("df-events_sendFrom", "data"),
        State("df-events_transferOwnership", "data"),
        State("df-events_safeTransferFrom", "data"),
        State("df-events_setApprovalForAll", "data"),
        State("df-general", "data")
    ]
)
def update_details_table_inputs(selected_activity, selected_blockNumber, selected_sender, transaction, df_input, df_storageState, df_internalTxs, df_approve, df_sendFrom, df_transferOwnership, df_safeTransferFrom, df_setApprovalForAll, df_general):
        
    generalDf = pd.DataFrame(df_general)
    inputs = pd.DataFrame(df_input)
    storage = pd.DataFrame(df_storageState)
    internal = pd.DataFrame(df_internalTxs)
    eventApprove = pd.DataFrame(df_approve)
    eventSendFrom = pd.DataFrame(df_sendFrom)
    eventTransferOwnership = pd.DataFrame(df_transferOwnership)
    eventSafeTransferFrom = pd.DataFrame(df_safeTransferFrom)
    eventSetApprovalForAll = pd.DataFrame(df_setApprovalForAll)

    # Filtra i dati in base ai filtri selezionati
    if selected_activity:
        generalDf = generalDf[generalDf["Activity"] == selected_activity]
        if inputs.empty: inputs = inputs
        else: inputs = inputs[inputs["Activity"] == selected_activity] 
        if storage.empty: storage = storage
        else: storage = storage[storage["Activity"] == selected_activity]
        if internal.empty: internal = internal
        else: internal = internal[internal["Activity"] == selected_activity]
    if selected_blockNumber:
        
        generalDf = generalDf[generalDf["Block Number"] == selected_blockNumber]
        if inputs.empty: inputs = inputs
        else: inputs = inputs[inputs["Block Number"] == selected_blockNumber] 
        if storage.empty: storage = storage
        else: storage = storage[storage["Block Number"] == selected_blockNumber]
        if internal.empty: internal = internal
        else: internal = internal[internal["Block Number"] == selected_blockNumber]
        if eventApprove.empty: eventApprove = eventApprove
        else: eventApprove = eventApprove[eventApprove["Block Number"] == selected_blockNumber]
        if eventSendFrom.empty: eventSendFrom = eventSendFrom
        else: eventSendFrom = eventSendFrom[eventSendFrom["Block Number"] == selected_blockNumber]
        if eventTransferOwnership.empty: eventTransferOwnership = eventTransferOwnership
        else: eventTransferOwnership = eventTransferOwnership[eventTransferOwnership["Block Number"] == selected_blockNumber]
        if eventSafeTransferFrom.empty: eventSafeTransferFrom = eventSafeTransferFrom
        else: eventSafeTransferFrom = eventSafeTransferFrom[eventSafeTransferFrom["Block Number"] == selected_blockNumber]
        if eventSetApprovalForAll.empty: eventSetApprovalForAll = eventSetApprovalForAll
        else: eventSetApprovalForAll = eventSetApprovalForAll[eventSetApprovalForAll["Block Number"] == selected_blockNumber]

    if selected_sender:
        generalDf = generalDf[generalDf["From"] == selected_sender]
        if inputs.empty: inputs = inputs
        else: inputs = inputs[inputs["From"] == selected_sender] 
        if storage.empty: storage = storage
        else: storage = storage[storage["From"] == selected_sender]
        if internal.empty: internal = internal
        else: internal = internal[internal["From"] == selected_sender]
        if eventApprove.empty: eventApprove = eventApprove
        else: eventApprove = eventApprove[eventApprove["Sender"] == selected_sender]
        if eventSendFrom.empty: eventSendFrom = eventSendFrom
        else: eventSendFrom = eventSendFrom[eventSendFrom["Sender"] == selected_sender]
        if eventTransferOwnership.empty: eventTransferOwnership = eventTransferOwnership
        else: eventTransferOwnership = eventTransferOwnership[eventTransferOwnership["Sender"] == selected_sender]
        if eventSafeTransferFrom.empty: eventSafeTransferFrom = eventSafeTransferFrom
        else: eventSafeTransferFrom = eventSafeTransferFrom[eventSafeTransferFrom["Sender"] == selected_sender]
        if eventSetApprovalForAll.empty: eventSetApprovalForAll = eventSetApprovalForAll
        else: eventSetApprovalForAll = eventSetApprovalForAll[eventSetApprovalForAll["Sender"] == selected_sender]

    if transaction:
        generalDf = generalDf[generalDf["Transaction Hash"] == transaction]
        if inputs.empty: inputs = inputs
        else: inputs = inputs[inputs["Transaction Hash"] == transaction] 
        if storage.empty: storage = storage
        else: storage = storage[storage["Transaction Hash"] == transaction]
        if internal.empty: internal = internal
        else: internal = internal[internal["Transaction Hash"] == transaction]
        if eventApprove.empty: eventApprove = eventApprove
        else: eventApprove = eventApprove[eventApprove["Transaction Hash"] == transaction]
        if eventSendFrom.empty: eventSendFrom = eventSendFrom
        else: eventSendFrom = eventSendFrom[eventSendFrom["Transaction Hash"] == transaction]
        if eventTransferOwnership.empty: eventTransferOwnership = eventTransferOwnership
        else: eventTransferOwnership = eventTransferOwnership[eventTransferOwnership["Transaction Hash"] == transaction]
        if eventSafeTransferFrom.empty: eventSafeTransferFrom = eventSafeTransferFrom
        else: eventSafeTransferFrom = eventSafeTransferFrom[eventSafeTransferFrom["Transaction Hash"] == transaction]
        if eventSetApprovalForAll.empty: eventSetApprovalForAll = eventSetApprovalForAll
        else: eventSetApprovalForAll = eventSetApprovalForAll[eventSetApprovalForAll["Transaction Hash"] == transaction]

    activity_options = [{"label": activity, "value": activity} for activity in generalDf["Activity"].unique()]
    blockNumber_options = [{"label": block, "value": block} for block in generalDf["Block Number"].unique()]
    sender_options = [{"label": sender, "value": sender} for sender in generalDf["From"].unique()]
    transaction_options = [{"label": transactionValue, "value": transactionValue} for transactionValue in generalDf["Transaction Hash"].unique()]

    return inputs.to_dict("records"), storage.to_dict("records"), internal.to_dict("records"), eventApprove.to_dict("records"), eventSendFrom.to_dict("records"), eventTransferOwnership.to_dict("records"), eventSafeTransferFrom.to_dict("records"), eventSetApprovalForAll.to_dict("records"), activity_options, blockNumber_options, sender_options, transaction_options

# Layout principale
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Gestisce la navigazione
    html.Div(id="page-content")  # Mostra il contenuto della pagina corrente
])


if __name__ == "__main__":
    app.run_server(debug=True)

