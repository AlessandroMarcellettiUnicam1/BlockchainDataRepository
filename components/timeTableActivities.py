import pandas as pd
import plotly.express as px

def layoutTable(dataFrame, color_map):

    df = dataFrame.copy()

    # Convertire il timestamp in formato datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Estrarre la data (anno, mese, giorno)
    df['date'] = df['timestamp'].dt.date

    # Raggruppare per data ed event_type, e contare il numero di eventi per ciascun gruppo
    activity_counts = df.groupby(['date', 'Activity']).size().reset_index(name='activity_count')

    # Calcolare il numero di giorni distinti nel dataset
    num_days = len(activity_counts["date"].unique())

    # Calcolare dinamicamente la larghezza e l'altezza del grafico
    graph_width = max(600, num_days * 50)  # Minimo 300px, ma aumenta con più giorni
    graph_height = max(600, len(activity_counts["Activity"].unique()) * 50)  # Altezza basata sul numero di attività

    fig = px.line(
        activity_counts,
        x="date",
        y="activity_count",
        color="Activity",  
        title="Timeline Activities",
        labels={"date": "Date", "activity_count": "Activity occurrency", "activity_type": "Activity type"},
        markers=True,
    )
    
    fig.update_xaxes(type="category")

    for trace in fig.data:
        activity_name = trace.name 
        # Imposta i colori della linea e dei marker in base a color_map
        trace.update(
            line=dict(color=color_map.get(activity_name, '#000000')),  
            marker=dict(color=color_map.get(activity_name, '#000000'))  
        )
        subset = activity_counts[activity_counts["Activity"] == activity_name] 
        trace.text = subset["activity_count"]  
        trace.textposition = "top center"
        trace.mode = "lines+markers+text" 

    return fig, graph_height, graph_width

    