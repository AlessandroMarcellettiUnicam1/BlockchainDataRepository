from dash import dash_table, dcc, html
from app import app

from data_from_backend import fetch_all_data

from dash.dependencies import Input, Output, State
import pandas as pd

columnsName = ["Transaction Hash", "Block Number", "Activity", "From"]

def create_general_table(df):
     return html.Div([
        dash_table.DataTable(
            id="transaction-table",
            columns=[{"name": col, "id": col} for col in columnsName],
            data=df.to_dict("records"),
            style_table={
                "overflowX": "auto",  # abilita lo scroll orizzontale se necessario
                "overflowY": "auto",  # abilita lo scroll verticale se necessario
                "height": "300px",  
                "width": "900px",  
            },
            style_cell={
                "textAlign": "center",
                "padding": "10px",
                "fontSize": 10,
                "fontFamily": "Arial",
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
            editable=True,
            page_size=8,
        )
     ]) 