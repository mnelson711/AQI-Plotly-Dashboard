import plotly.graph_objects as go

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

def lineplot(data, x_values, y_values, title="Line Plot", x_label="X Axis", y_label="Y Axis"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', marker=dict(color='blue')))
    fig.update_layout(
        title=title,
        xaxis=dict(title=x_label),
        yaxis=dict(title=y_label),
        plot_bgcolor='hsla(228, 3%, 35%, 0.971)',
        paper_bgcolor='hsla(228, 3%, 35%, 0.971)',
        font=dict(color='white')
    )
    return fig
