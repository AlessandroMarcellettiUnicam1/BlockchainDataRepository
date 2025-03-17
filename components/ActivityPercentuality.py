import plotly.graph_objects as go

# GRAFICO PER LA PERCENTUALE DI ATTIVITà PRESENTI NELL'INTERO DATABASE
def create_pie_chart(df, color_map):

    activity_counts = df["Activity"].value_counts()

    # Crea una lista dei colori associati alle attività in base alla color_map
    colors = [color_map[activity] for activity in activity_counts.index]

    activity_pie_fig = go.Figure(
        data=[
            go.Pie(
                labels=activity_counts.index,  
                values=activity_counts.values,  
                textinfo="label+percent",  # Mostra etichette e percentuali
                hoverinfo="label+value",  # Mostra etichette e valori al passaggio del mouse
                marker=dict(colors=colors) 
            )
        ]
    )
    
    # Impostazioni del layout del grafico a torta
    activity_pie_fig.update_layout(
        template="plotly_white",
        width=500, 
        height=400, 
    )
    return activity_pie_fig