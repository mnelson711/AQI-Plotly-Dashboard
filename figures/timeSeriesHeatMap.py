#TO DO
# aqi data prep
# get value per month, highest AQI value and also average AQI value
# add time series heatmap
# add gradient heatmap after

import pandas as pd
import plotly.graph_objects as go

def month_year_heatmap(df, title='Month-Year Heatmap', colormap='Viridis'):
    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        x=df.columns,
        y=df.index,
        colorscale=colormap + "_r",
        colorbar=dict(title='Magnitude'),
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(title='Year', type='category'),
        yaxis=dict(title='Month'),
    )
    
    return fig  # Return the figure object instead of showing or saving it
