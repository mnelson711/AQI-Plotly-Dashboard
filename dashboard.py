from dash import Dash, dcc, html, callback_context
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import calendar
from figures.timeSeriesHeatMap import month_year_heatmap, gradient_heatmap
from figures.lineplot import lineplot
from figures.polargraph import polarchart
from figures.exampleFig import create_line_chart
from figures.spatialHeatMap import generate_heatmap
from datetime import datetime

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

spatial_df = pd.read_csv('./csv/AQI_after_2020_before_2023.csv')
spatial_df['Date Local'] = pd.to_datetime(spatial_df['Date Local'])
unique_dates = pd.to_datetime(spatial_df['Date Local']).dt.date.unique()

# Convert the date objects to strings
date_strings = [str(date) for date in unique_dates]

# Convert the date strings to datetime objects
date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in date_strings]
date_objects.sort()

slider_marks = {
    i: {
        'label': date.strftime('%m-%d') if i % 100 == 0 else '',
        'style': {
            'transform': 'rotate(-45deg)',
            'white-space': 'nowrap'
        }
    } for i, date in enumerate(date_objects)
}

def aqi_info_modal():
    return html.Div([
        dbc.Button("Learn More About AQI", id="open-modal", n_clicks=0, className="mb-3"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Air Quality Index (AQI) Information")),
                dbc.ModalBody(html.Div([
                    html.H5("What is AQI?", className="info-heading"),
                    html.P("The Air Quality Index (AQI) is used to communicate how polluted the air currently is or how polluted it is forecast to become. As the AQI increases, it signifies worsening levels of air pollution and more serious public health concerns."),
                    html.H5("AQI Levels", className="info-heading"),
                    html.Ul([
                        html.Li("0 to 50: Good"),
                        html.Li("51 to 100: Moderate"),
                        html.Li("101 to 150: Unhealthy for Sensitive Groups"),
                        html.Li("151 to 200: Unhealthy"),
                        html.Li("201 to 300: Very Unhealthy"),
                        html.Li("301 to 500: Hazardous")
                    ]),
                ])),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-modal", className="ml-auto")
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ])

def generate_spatial_heatmap(selected_date):
    custom_colorscale = [
        [0.0, "grey"],
        [(1+0)/451, "green"],
        [(1+50)/451, "green"],
        [(1+100)/451, "yellowgreen"],
        [(1+150)/451, "yellow"],
        [(1+200)/451, "gold"],
        [(1+300)/451, "orange"],
        [1.0, "red"]                      
    ]
    selected_date = date_objects[selected_date]
    filtered_data = spatial_df[spatial_df['Date Local'] == str(selected_date)]
    fig = go.Figure(go.Scattermapbox(
        lat=filtered_data['Latitude'],
        lon=filtered_data['Longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color=filtered_data['Ozone'],
            colorscale= custom_colorscale,  
            cmin=filtered_data['Ozone'].min(),
            cmax=filtered_data['Ozone'].max(),
            colorbar=dict(title='Ozone Value'),
        )
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 37.0902, "lon": -95.7129},
        plot_bgcolor='hsla(228, 3%, 35%, 0.971)',
        paper_bgcolor='hsla(228, 3%, 35%, 0.971)',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(
            color='white'
        )
    )

    return fig

@app.callback(
    Output('spatial-heatmap', 'figure'),
    [Input('date-slider', 'value')]  # Assuming you have a slider for selecting dates
)
def update_spatial_heatmap(selected_date):
    return generate_spatial_heatmap(selected_date)

@app.callback(
    Output('selected-date-label', 'children'),
    [Input('date-slider', 'value')]
)
def update_date_label(slider_value):
    selected_date = date_objects[slider_value]  # Retrieve the date from date_objects using the slider value
    return f"Selected Date: {selected_date.strftime('%Y-%m-%d')}"

@app.callback(
    [Output('month-year-heatmap', 'figure'), Output('gradient-bar-plot', 'figure'), Output('line-plot', 'figure'), Output('polar-plot', 'figure')],
    [Input('Boston', 'n_clicks'),
     Input('New_York', 'n_clicks'),
     Input('Los_Angeles', 'n_clicks'),
     Input('Denver', 'n_clicks'),
     Input('Phoenix', 'n_clicks'),
     Input('Reno', 'n_clicks'),
     Input('Bakersfield', 'n_clicks'),
     Input('Visalia', 'n_clicks'),
     ]
)
def update_output(boston_clicks, ny_clicks, la_clicks, denver_clicks, reno_clicks, visalia_clicks, phoenix_clicks, bakersfield_clicks):
    ctx = callback_context

    if not ctx.triggered:
        selected_city_file = './csv/aqi_cleaned_Boston.csv' #default to boston
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        selected_city_file = f'./csv/aqi_cleaned_{button_id}.csv'

    processed_df = pd.read_csv(selected_city_file)
    processed_df['Year'] = processed_df['Year'].astype(str)
    processed_df['Month'] = processed_df['Month'].apply(lambda x: calendar.month_name[int(x)])
    month_order = [calendar.month_name[i] for i in range(1, 13)]
    processed_df['Month'] = pd.Categorical(processed_df['Month'], categories=month_order, ordered=True)
    
    pivot_df = processed_df.pivot(index="Month", columns="Year", values="aqi")
    heatmap_fig = month_year_heatmap(pivot_df)

    gradient_data = processed_df['aqi'].tolist()
    years = processed_df['Year'].tolist()
    months = processed_df['Month'].tolist()
    gradient_fig = gradient_heatmap(gradient_data, years, months, title="AQI Gradient Plot")

    line_fig = lineplot(processed_df,years,processed_df['aqi'],title='AQI Line Plot')  # Assuming create_line_chart is a function that creates a line chart
    polar_fig = polarchart(selected_city_file)

    return heatmap_fig, gradient_fig, line_fig, polar_fig

@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal", "n_clicks"), Input("close-modal", "n_clicks")],
    [State("modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

def serve_layout():
    return dbc.Container(
        [
            dbc.Row([
                dbc.Col(html.H1('United States Air Quality Index (AQI)', className="text-center mb-4"), width=12)
            ]),
            dbc.Row([
                dbc.Col(aqi_info_modal(), className="aqi-modal",width={'size': 6, 'offset': 3})
            ]),
            dbc.Row([
                dbc.Col(html.H4('Spatial Heatmap', className="text-center mb-4"), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='spatial-heatmap',className='plot-container'), width=12)
            ]),
            dbc.Row(
                dbc.Col(
                    html.Div(id='selected-date-label', className='text-center'),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Slider(
                        id='date-slider',
                        min=0,
                        max=len(date_objects) - 1,
                        value=0,  # Initial value
                        marks=None,
                        step=1
                    ),
                    className="slider",
                    width={'size': 6, 'offset': 3}
                )
            ),
            dbc.Row(
                dbc.Col(
                    dbc.DropdownMenu(
                        label="Select City",
                        children=[
                            dbc.DropdownMenuItem("Boston", id="Boston"),
                            dbc.DropdownMenuItem("New York", id="New_York"),
                            dbc.DropdownMenuItem("Los Angeles", id="Los_Angeles"),
                            dbc.DropdownMenuItem("Denver", id="Denver"),
                            dbc.DropdownMenuItem("Phoenix", id="Phoenix"),
                            dbc.DropdownMenuItem("Reno", id="Reno"),
                            dbc.DropdownMenuItem("Visalia", id="Visalia"),
                            dbc.DropdownMenuItem("Bakersfield", id="Bakersfield"),
                        ],
                        id="city-dropdown",
                    ),
                    className="dropdown",
                    width={'size': 6, 'offset': 3}
                )
            ),
            dbc.Row([
                dbc.Col(dcc.Graph(id='month-year-heatmap',className='plot-container'), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='gradient-bar-plot',className='plot-container'), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='line-plot', className='plot-container'), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='polar-plot', className='plot-container'), width=12)
            ]),
        ],
        fluid=True,
        className='py-3'
    )

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
