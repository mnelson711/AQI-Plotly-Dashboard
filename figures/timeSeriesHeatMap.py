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


def month_year_heatmap(df, title='Month-Year Heatmap', colormap=custom_colorscale):
    
    tick_values = [0, 50, 100, 150, 200, 300, 450]
    tick_text = ["0 Good", "50 Moderate", "100 Unhealthy for Sensitive Groups", "150 Unhealthy", "200 Very Unhealthy", "300 Hazardous", "450+"]

    df_filled = df.fillna(-1)
    fig = go.Figure(data=go.Heatmap(
        z=df_filled.values,
        x=df_filled.columns,
        y=df_filled.index,
        colorscale=colormap,
        colorbar=dict(
            title='AQI',
            title_font_color='white',
            titleside='top',
            tickmode='array',
            tickvals=tick_values,
            ticktext=tick_text,
            tickcolor='white',
            ticks='inside',
            tickfont=dict(color='white'),
        ),
        zmin=-1,
        zmax=450
    ))

    fig.update_layout(
        title=title,
        title_font_color='white',
        xaxis=dict(title='Year', type='category',title_font=dict(color='white'),
        tickfont=dict(color='white'),
        tickcolor='green'),
        yaxis=dict(title='Month', autorange='reversed', title_font=dict(color='white'),
        tickfont=dict(color='white'),
        tickcolor='white'),
        plot_bgcolor='hsla(228, 3%, 35%, 0.971)',
        paper_bgcolor='hsla(228, 3%, 35%, 0.971)',
        height=400,
    )

    return fig

def gradient_heatmap(data, years, months, colormap=custom_colorscale, title="Data Visualization", x_label="Years"):
    x_data = list(range(len(data)))
    y_data = [1] * len(data)
    
    categories = []
    for value in data:
        if value <= 50:
            category = 'Good'
        elif value <= 100:
            category = 'Moderate'
        elif value <= 150:
            category = 'Unhealthy for Sensitive Groups'
        elif value <= 200:
            category = 'Unhealthy'
        elif value <= 300:
            category = 'Very Unhealthy'
        else:
            category = 'Hazardous'
        categories.append(category)

    hover_texts = [
        f"Month: {month}<br>Year: {year}<br>AQI: {value}<br>Category: {category}"
        for month, year, value, category in zip(months, years, data, categories)
    ]

    fig = go.Figure(data=go.Bar(
        x=x_data,
        y=y_data,
        text=hover_texts,
        hoverinfo="text",
        marker=dict(
            color=data,
            colorscale=colormap,
            line=dict(color='rgba(255,255,255,0)'),
        ),
        width=1.1,
    ))
    first_year, last_year = years[0], years[-1]
    fig.update_layout(
        xaxis=dict(
            title=x_label,
            title_font_color='white',
            tickmode='array',
            tickvals=[5, len(years) - 5],
            ticktext=[first_year, last_year],
            title_font=dict(color='white'),
            tickfont=dict(color='white'),
            tickcolor='white'
        ),
        yaxis=dict(
            showticklabels=False,
            title="",
        ),
        title=title,
        title_font_color='white',
        plot_bgcolor='hsla(228, 3%, 35%, 0.971)',
        paper_bgcolor='hsla(228, 3%, 35%, 0.971)',
        margin=dict(l=40, r=40, t=40, b=40),
        height=250
    )
    
    return fig
