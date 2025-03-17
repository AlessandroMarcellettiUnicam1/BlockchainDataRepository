from dash import dash_table


def create_details_table(df, columnsName, height, width, name):
    return dash_table.DataTable(
        id=f"transaction-table_{name}",
        columns=[{"name": col, "id": col} for col in columnsName],
        data=df.to_dict("records"),
        style_table={
            "overflowX": "auto",  # abilita lo scroll orizzontale se necessario
            "overflowY": "auto",  # abilita lo scroll verticale se necessario
            "height": height,  
            "width": width,  
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
        page_size=8,
    )