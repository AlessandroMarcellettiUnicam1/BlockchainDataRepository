import pandas as pd
import plotly.express as px
from data_from_backend import fetch_ocel_time_events


df = pd.DataFrame(fetch_ocel_time_events())

# Convertire il timestamp in formato datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Estrarre la data (anno, mese, giorno)
df['date'] = df['timestamp'].dt.date

# Raggruppare per data ed event_type, e contare il numero di eventi per ciascun gruppo
event_counts = df.groupby(['date', 'event_type']).size().reset_index(name='event_count')

fig = px.line(
    event_counts,
    x="date",
    y="event_count",
    color="event_type",  
    title="Timeline Events",
    labels={"date": "Date", "event_count": "Event occurrency", "event_type": "Event type"},
)

fig.update_xaxes(type="category")
