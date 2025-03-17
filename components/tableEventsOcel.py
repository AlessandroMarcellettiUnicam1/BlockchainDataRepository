from dash import dash_table
from data_from_backend import fetch_ocel_data_event

columnsName = ["Event Type", "Occurency"]

def create_data_table():
    return dash_table.DataTable(
        id="transaction-table",
        columns=[{"name": col, "id": col} for col in columnsName],
        data=fetch_ocel_data_event(),
        style_table={
            "overflowX": "auto",  # abilita lo scroll orizzontale se necessario
            "overflowY": "auto",  # abilita lo scroll verticale se necessario
            "height": "auto",  
            "width": "auto",  
            "marginLeft": "60px",
        },
        style_cell={
            "textAlign": "center",
            "padding": "10px",
            "fontSize": 12,
            "fontFamily": "Arial",
            "width": "auto",  
        },
        style_header={
            "backgroundColor": "lightblue",
            "fontWeight": "bold",
            "textAlign": "center",
            "position": "sticky", 
            "top": "0",  
            "zIndex": "1", 
        },
        style_filter={
            "backgroundColor": "lightyellow",
            "textAlign": "center",
            "position": "sticky",  
            "top": "38px", 
            "zIndex": "1", 
        },
        style_data={"backgroundColor": "white", "color": "black"},
        sort_action="native",
        filter_action="none",
        page_size=8,
    )