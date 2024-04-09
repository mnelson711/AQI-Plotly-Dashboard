import plotly.express as px
import pandas as pd

def create_line_chart(dataframe, x_column, y_column, title):
    fig = px.line(dataframe, x=x_column, y=y_column, title=title)
    return fig