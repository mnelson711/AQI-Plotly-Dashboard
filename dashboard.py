# app.py
from dash import Dash
# from components.layout import serve_layout

app = Dash(__name__)

# components/layout.py
from dash import html, dcc
from figures.exampleFig import create_line_chart
from figures.timeSeriesHeatMap import month_year_heatmap
import pandas as pd
import numpy as np
import calendar
from dash.dependencies import Input, Output

@app.callback(
    Output('month-year-heatmap', 'figure'),
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



# def serve_layout():
#     layout = html.Div(children=[
#         html.H1(children='Air Quality Index (AQI)',className='center-text'),
#         dcc.Dropdown(
#         id='city-dropdown',
#         options=[
#             {'label': 'Boston', 'value': './csv/aqi_cleaned_Boston.csv'},
#             {'label': 'New York', 'value': './csv/aqi_cleaned_New_York.csv'},
#             {'label': 'Los Angeles', 'value': './csv/aqi_cleaned_LA.csv'},
#             {'label': 'Bakersfield', 'value': './csv/aqi_cleaned_Bakersfield.csv'},
#             {'label': 'Visalia', 'value': './csv/aqi_cleaned_Visalia.csv'},
#             {'label': 'Reno', 'value': './csv/aqi_cleaned_Reno.csv'},
#             {'label': 'Phoenix', 'value': './csv/aqi_cleaned_Phoenix.csv'},
#             {'label': 'Denver', 'value': './csv/aqi_cleaned_Denver.csv'},
#         ],
#         value='./csv/aqi_cleaned_Boston.csv',
#         className='half-width-dropdown'
#     ), className='center-text',
#     dcc.Graph(id='month-year-heatmap')
#     ], className='app-container')
#     return layout


def serve_layout():
    layout = html.Div(children=[
        html.Div(
            className="app-header",
            children=[
                html.Div('United States Air Quality Index', className="app-header--title")
            ]
        ),
        html.Div(dcc.Dropdown(
            id='city-dropdown',
        options=[
            {'label': 'Boston', 'value': './csv/aqi_cleaned_Boston.csv'},
            {'label': 'New York', 'value': './csv/aqi_cleaned_New_York.csv'},
            {'label': 'Los Angeles', 'value': './csv/aqi_cleaned_LA.csv'},
            {'label': 'Bakersfield', 'value': './csv/aqi_cleaned_Bakersfield.csv'},
            {'label': 'Visalia', 'value': './csv/aqi_cleaned_Visalia.csv'},
            {'label': 'Reno', 'value': './csv/aqi_cleaned_Reno.csv'},
            {'label': 'Phoenix', 'value': './csv/aqi_cleaned_Phoenix.csv'},
            {'label': 'Denver', 'value': './csv/aqi_cleaned_Denver.csv'},
        ],
            value='./csv/aqi_cleaned_Boston.csv',  # default value
            className='half-width-dropdown'
        ), className='center-text'),
        dcc.Graph(id='month-year-heatmap', className='month-year-heatmap')
    ], className='app-container')
    
    return layout

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
