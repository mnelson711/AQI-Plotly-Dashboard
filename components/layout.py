# components/layout.py
from dash import html, dcc
from figures.exampleFig import create_line_chart
import pandas as pd

# Example data
df = pd.DataFrame({
    "Date": ["2021-01-01", "2021-01-02", "2021-01-03"],
    "Value": [10, 15, 13]
})

# Creating a figure using the function defined in charts.py
fig = create_line_chart(df, "Date", "Value", "Sample Line Chart")

def serve_layout():
    layout = html.Div(children=[
        html.H1(children='My Dashboard'),
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])
    return layout
