import pandas as pd
import plotly.graph_objects as go
import numpy as np
import calendar

def plot_polar_avg_aqi(csv_files, city_names):
    avg_aqi_by_month = {calendar.month_name[i]: [] for i in range(1, 13)}
    traces = []

    for file, city in zip(csv_files, city_names):
        df = pd.read_csv(file)
        df['Month'] = df['Month'].apply(lambda x: calendar.month_name[int(x)])
        avg_aqi_monthly = df.groupby('Month')['aqi'].mean().reset_index()
        for index, row in avg_aqi_monthly.iterrows():
            avg_aqi_by_month[row['Month']].append(row['aqi'])

        avg_aqi_overall = [np.mean(avg_aqi_by_month[calendar.month_name[i]]) for i in range(1, 13)]
        avg_aqi_overall_reordered = avg_aqi_overall[6:] + avg_aqi_overall[:6]

        theta = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]

        traces.append(go.Scatterpolar(
            r=avg_aqi_overall_reordered,
            theta=theta,
            mode='markers',
            name=city,  
            marker=dict(
                size=8, 
                symbol='circle'
            )
        ))

    fig = go.Figure(data=traces)

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([val for sublist in avg_aqi_by_month.values() for val in sublist])]
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=np.linspace(0, 360, 12, endpoint=False),
                ticktext=list(calendar.month_name)[1:] 
            )
        ),
        title='Average AQI by Month',
        showlegend=True  
    )

    return fig

