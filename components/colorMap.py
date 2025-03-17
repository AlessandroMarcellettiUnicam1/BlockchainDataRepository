import plotly.express as px

def generate_color_map(df):
    unique_activities = df['Activity'].unique()
    # Associare un colore unico per ogni attività
    color_map = {activity: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] 
                 for i, activity in enumerate(unique_activities)}
    return color_map