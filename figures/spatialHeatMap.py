import plotly.express as px


def generate_heatmap(df):
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="aqi",
        color_continuous_scale=px.colors.sequential.Viridis,
        hover_name="location_name",
        size_max=15,
        zoom=3,
    )
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
