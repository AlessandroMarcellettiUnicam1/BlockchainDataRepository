import plotly.graph_objects as go
import pandas as pd

# GRAFICO PER IL GAS MEDIO TOTALE A SECONDA DELLE ATTIVITà PER L'INTERO DATABASE
def create_bar_chart(df):
    
    df["gasUsed"] = pd.to_numeric(df["gasUsed"], errors="coerce")
    gas_used_by_activity = df.groupby("Activity")["gasUsed"].mean().reset_index()
    gas_bar_fig = go.Figure(
        data=[
            go.Bar(
                x=gas_used_by_activity["Activity"],
                y=gas_used_by_activity["gasUsed"],
                marker_color="indianred",
            )
        ]
    )

    gas_bar_fig.update_layout(
        xaxis_title="Activity",
        yaxis_title="Average gas used",
        template="plotly_white",
        width=500,
        height=400,
    )

    return gas_bar_fig