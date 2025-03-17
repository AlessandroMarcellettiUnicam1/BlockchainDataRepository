from dash import html, dcc
import pandas as pd
import plotly.express as px

from components.tableEventsOcel import create_data_table as create_data_table_event
from components.tableObjectsOcel import create_data_table as create_data_table_object
from components.tableEventsRelations import create_data_table as create_data_table_events_relationships
from components.tableObjectsRelations import create_data_table as create_data_table_objects_relationships

from data_from_backend import fetch_ocel_time_events

df = pd.DataFrame(fetch_ocel_time_events())
df["Day"] = pd.to_datetime(df["Day"]).dt.date

activity_per_day = df.groupby(["Day", "Activity"]).size().reset_index(name="activityCount")

activity_per_day = activity_per_day.pivot(index="Day", columns="Activity", values="activityCount").fillna(0).reset_index()
activity_per_day = activity_per_day.melt(id_vars="Day", var_name="Activity", value_name="activityCount")

fig = px.line(
    activity_per_day,
    x="Day",
    y="activityCount",
    color="Activity",
    title="Timeline Activity",
    labels={"Day": "Day", "activityCount": "Occurrencies"}, 
    height=600 
)

#Layout Analisi di documenti Ocel_2.0
def layout():
    return html.Div(
        style={"display": "flex", "flexDirection": "column", "height": "100vh"}, 
        children=[
            
            html.Div(
                style={
                    "position": "absolute", "top": "0", "left": "50%", "transform": "translateX(-50%)", "marginTop": "20px", 
                    "display": "flex", "justifyContent": "center", "gap": "20px", "marginBottom": "20px"
                },
                children=[
                    dcc.Link(
                        html.Button("Back to the home page", style={"marginBottom": "10px", "padding": "10px", "fontSize": "16px"}),
                        href="/"
                    ),
                ]
            ),

            html.Div(
                style={
                    "display": "flex", 
                    "flexDisposition": "row",
                    "gap": "30px",  
                    "marginTop": "80px",  
                    "flexWrap": "wrap",
                },
                children=[
                    html.Div(
                        style={
                            "flex": 1, 
                            "justifyContent": "center",
                            "overflow": "auto",  
                            "marginBottom": "50px", 
                        },
                        children=[
                            html.H2("Event type occurrencies", style={"textAlign": "center"}),
                            create_data_table_event(),
                        ],
                    ),
                    html.Div(
                        children=[
                            html.H2("Object type occurrencies", style={"textAlign": "center"}),
                            create_data_table_object(),
                        ],
                    ),
                ]
            ),

            html.Div(
                style={
                    "display": "flex",
                    "flexDisposition": "row",
                    "justifyContent": "center",
                    "width": "100%",
                    "marginTop": "80px", 
                    "flexWrap": "wrap",
                },
                children=[
                    html.Div(
                        style={
                            "width": "50%",
                            "overflow": "auto",   
                            "marginBottom": "50px",  
                        },
                        children=[
                            html.H2("Relations' occurrencies by Event", style={"textAlign": "center"}),
                            create_data_table_events_relationships(),
                        ],
                    ),
                    html.Div(
                        style={
                            "width": "50%",
                            "overflow": "auto", 
                            "marginBottom": "50px",  
                        },
                        children=[
                            html.H2("Relations' occurrencies by Object", style={"textAlign": "center"}),
                            create_data_table_objects_relationships(),
                        ],
                    ),
                ]
            ),

            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "width": "100%",
                    "marginTop": "80px",
                    "flexWrap": "wrap",
                },
                children=[
                    html.Div(
                        style={"width": "80%", "maxWidth": "800px", "overflowX": "auto"},
                        children=[
                            html.H2("Timeline Events", style={"textAlign": "center"}),
                            dcc.Graph(
                                figure=fig,
                                style={"flex": "1", "marginTop": "20px"},  
                            ),
                        ],
                    ),
                ]
            ),
        ]
    )


