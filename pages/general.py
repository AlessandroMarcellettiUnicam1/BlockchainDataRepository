from dash import dash_table
import pandas as pd  # Aggiungi pandas per creare il DataFrame
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

from components.ActivityPercentuality import create_pie_chart
from components.GasUsedAvarage import create_bar_chart
from components.generalTable import create_general_table as generalTableLayout
from components.timeTableActivities import layoutTable
from components.colorMap import generate_color_map
from data_from_backend import fetch_all_data

from app import app

# Layout analisi dei dati generali
def layout(contract_type):

    print(f"🛠 Generating layout for contract type: {contract_type}")


    df = pd.DataFrame(fetch_all_data(contract_type))

    color_map = generate_color_map(df)

    timelineActivities, timelineActivities_height, timelineActivities_width = layoutTable(df, color_map)

    return html.Div(
        style={"display": "flex", "flexDirection": "column", "height": "100vh"}, 
        children=[
            html.Div(
                style={
                    "position": "absolute", "top": "0", "left": "50%", "transform": "translateX(-50%)", "marginTop": "20px", 
                    "display": "flex", "justifyContent": "center", "gap": "20px"
                },
                children=[
                    dcc.Link(
                        html.Button("Back to Home page", style={"marginBottom": "10px", "padding": "10px", "fontSize": "16px"}),
                        href="/"
                    ),
                    dcc.Link(
                        html.Button("Detailed graphics", style={"padding": "10px", "fontSize": "16px", "marginLeft": "50px"}),
                        href= f"/general/{contract_type}/contracts_details"
                    ),
                ]
            ),

            dcc.Store(id="df-store", data=df.to_dict("records")),

            html.Div(
                children=[
                    dcc.Dropdown(
                        id="activity",
                        options=[{"label": activity, "value": activity} for activity in df["Activity"].unique()],
                        placeholder="Select activity",
                        value=None,
                        style={"width": "250px"},
                    ),
                    dcc.Dropdown(
                        id="blockNumber",
                        options=[{"label": blockNumber, "value": blockNumber} for blockNumber in df["Block Number"].unique()],
                        placeholder="Select block number",
                        value=None,
                        style={"width": "250px", "marginLeft": "10px"},
                    ),
                    dcc.Dropdown(
                        id="sender",
                        options=[{"label": sender, "value": sender} for sender in df["From"].unique()],
                        placeholder="Select sender",
                        value=None,
                        style={"width": "250px", "marginLeft": "10px"},
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "center",  
                    "alignItems": "center",  
                    "marginTop": "80px",
                    "marginBottom": "20px", 
                },
            ),

            html.Div(
                children=[
                    generalTableLayout(df)
                ],
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "width": "100%",
                },
            ),
            
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H2("Activity Analysis", style={"textAlign": "center"}),
                            dcc.Graph(figure=create_pie_chart(df, color_map)),  
                        ],
                        style={"marginTop": "20px"},
                    ), 
                    html.Div(
                        children=[
                            html.H2("Average gasUsed for each activity", style={"textAlign": "center"}),
                            dcc.Graph(figure=create_bar_chart(df)),  
                        ],
                        style={"marginTop": "20px"},
                    ),
                ],
                style={
                    "width": "100%",  
                    "display": "flex", 
                    "flexDirection": "row", 
                    "justifyContent": "center", 
                    "alignItems": "center",  
                },
            ),

            html.Div(
                children=[
                    html.Div(
                        style={"width": "80%", "overflowX": "auto"},
                        children=[
                            html.H2("Timeline Activities", style={"textAlign": "center"}),
                            dcc.Graph(
                                figure=timelineActivities, 
                                style={
                                    "flex": "1", 
                                    "marginTop": "20px", 
                                    "textAlign": "center", 
                                    "height": f"{timelineActivities_height}px", 
                                    "width": f"{timelineActivities_width}px"},
                            ),
                        ],
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "width": "100%",
                    "flexDirection": "row", 
                },
            ),
        ],
    )

