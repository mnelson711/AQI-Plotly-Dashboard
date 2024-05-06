import pandas as pd
import numpy as np
import calendar
import plotly.graph_objects as go

def polarchart(csv_file, city_name):
    df = pd.read_csv(csv_file)


    # parts = csv_file.split('_')
    # city_name = parts[2].replace('.csv', '')
    # if(city_name == 'New'):
    #     city_name = city_name + ' York'
    # print(city_name)

    if(city_name == 'Los'):
        city_name = city_name + ' Angeles'

    df['Month'] = df['Month'].apply(lambda x: calendar.month_name[int(x)])

    filtered_data = {}
    for month in calendar.month_name[1:]:
        monthly_data = df[df['Month'] == month]['aqi']
        filtered_data[month] = monthly_data[monthly_data > 100].tolist()

    r_values = []
    theta_values = []

    for month, aqi_values in filtered_data.items():
        for aqi in aqi_values:
            r_values.append(aqi)
            theta_values.append(list(calendar.month_name[1:]).index(month) * (360 / 12))  

    trace = go.Scatterpolar(
        r=r_values,
        theta=theta_values,
        mode='markers',
        name=city_name,
        marker=dict(
            size=10,
            symbol='circle',
            color='red'  
        )
    )

    fig = go.Figure(data=[trace])

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(r_values) + 10] if r_values else [0, 100],  
                tickfont=dict(
                    size=10,  
                    color='grey'  
                )
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=np.linspace(0, 360, 12, endpoint=False),
                ticktext=list(calendar.month_name)[1:],
                tickfont=dict(
                    size=12,  
                    color='white'  
                )
            ),
            bgcolor='lightblue' 
        ),
        title=f'AQI values over 100  - {city_name}',
        title_font=dict(
            size=16,  
            color='white'  
        ),
        showlegend=True,
         legend=dict(
        title_font=dict(color='red'),  
        font=dict(color='white')  
        ),
        margin=dict(l=40, r=40, t=80, b=40),  
        paper_bgcolor='hsla(228, 3%, 35%, 0.971)',
    )

    return fig


