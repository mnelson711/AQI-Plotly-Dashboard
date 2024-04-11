# components/layout.py
from dash import html, dcc
from figures.exampleFig import create_line_chart
from figures.timeSeriesHeatMap import month_year_heatmap
import pandas as pd
import numpy as np
import calendar
from dash.dependencies import Input, Output

@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_heatmap(selected_city_file):
    # Load and process the dataset for the selected city
    
    processed_df = pd.read_csv(selected_city_file)
    # Convert 'Year' and 'Month' to string to ensure they are treated as categorical data
    processed_df['Year'] = processed_df['Year'].astype(str)
    processed_df['Month'] = processed_df['Month'].apply(lambda x: calendar.month_name[int(x)])
    month_order = [calendar.month_name[i] for i in range(1, 13)]  # January to December
    processed_df['Month'] = pd.Categorical(processed_df['Month'], categories=month_order, ordered=True)

    pivot_df = processed_df.pivot("Month", "Year", "aqi")
    fig = month_year_heatmap(pivot_df)
    return fig



def serve_layout():
    layout = html.Div(children=[
        html.H1(children='My Dashboard'),
        dcc.Dropdown(
        id='city-dropdown',
        options=[
            {'label': 'Boston', 'value': 'aqi_cleaned_Boston.csv'},
            {'label': 'New York', 'value': 'aqi_cleaned_New_York.csv'},
            # Add more cities as needed
        ],
        value='aqi_cleaned_Boston.csv'  # Default value
    ),
    dcc.Graph(id='month-year-heatmap')
    ])
    return layout
