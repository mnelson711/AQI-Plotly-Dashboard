# #TO DO
# # aqi data prep
# # get value per month, highest AQI value and also average AQI value
# # add time series heatmap
# # add gradient heatmap after

# import pandas as pd
# import plotly.graph_objects as go
# import numpy as np

# # def month_year_heatmap(df, title='Month-Year Heatmap', colormap='Viridis'):
# #     fig = go.Figure(data=go.Heatmap(
# #         z=df.values,
# #         x=df.columns,
# #         y=df.index,
# #         colorscale=colormap + "_r",
# #         colorbar=dict(title='Magnitude'),
# #     ))

# #     fig.update_layout(
# #         title=title,
# #         xaxis=dict(title='Year', type='category'),
# #         yaxis=dict(title='Month'),
# #     )
    
# #     return fig  # Return the figure object instead of showing or saving it

# import plotly.graph_objects as go

# custom_colorscale = [
#     [-1.0, "grey"], #missing values
#     [0.0, "green"],   # AQI 0
#     [0.11, "green"],  # AQI 50 - Good
#     [0.22, "yellowgreen"],  # AQI 100 - Moderate
#     [0.33, "yellow"], # AQI 150
#     [0.44, "gold"],   # AQI 200 - Unhealthy for Sensitive Groups
#     [0.56, "orange"], # AQI 300 - Unhealthy
#     [1.0, "red"]      # AQI 450 - Hazardous
# ]

# # Setting tick values and text for colorbar
tick_values = [0, 50, 100, 150, 200, 300, 450]
tick_text = ["0 Good", "50 Moderate", "100 Unhealthy for Sensitive Groups", "150 Unhealthy", "200 Very Unhealthy", "300 Hazardous", "450+"]


# def month_year_heatmap(df, title='Month-Year Heatmap', colormap=custom_colorscale):
#     df_filled = df.fillna(-1)
#     fig = go.Figure(data=go.Heatmap(
#         z=df_filled.values,
#         x=df_filled.columns,
#         y=df_filled.index,
#         colorscale=colormap,
#         colorbar=dict(
#             title='AQI',
#             titleside='right',
#             tickmode='array',
#             tickvals=tick_values,
#             ticktext=tick_text,
#             ticks='outside'
#         ),
#         # missingcolor="grey",
#         zmin=-1,  # Minimum value of color scale
#         zmax=450  # Maximum value of color scale
#     ))


#     fig.update_layout(
#         title=title,
#         xaxis=dict(title='Year', type='category'),
#         yaxis=dict(title='Month', autorange='reversed')
#     )
#     return fig



import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Redefine the custom colorscale
# Colors are set according to the proportionate positions of the AQI thresholds
custom_colorscale = [
    [0.0, "grey"],                     # Missing values (-1) at 0% of the scale
    [(1+0)/451, "green"],              # AQI 0 at ~0.22% of the scale (proportion of 1 in 0 to 450)
    [(1+50)/451, "green"],             # AQI 50 at 11.31% of the scale
    [(1+100)/451, "yellowgreen"],      # AQI 100 at 22.39% of the scale
    [(1+150)/451, "yellow"],           # AQI 150 at 33.48% of the scale
    [(1+200)/451, "gold"],             # AQI 200 at 44.57% of the scale
    [(1+300)/451, "orange"],           # AQI 300 at 66.74% of the scale
    [1.0, "red"]                       # AQI 450 at 100% of the scale
]

# # Setting tick values and text for colorbar
# tick_values = [(-1+1)/451, (50+1)/451, (100+1)/451, (150+1)/451, (200+1)/451, (300+1)/451, 1]
# tick_text = ["Missing", "Good (50)", "Moderate (100)", "Unhealthy for Sensitive Groups (150)", "Unhealthy (200)", "Very Unhealthy (300)", "Hazardous (450)"]

def month_year_heatmap(df, title='Month-Year Heatmap', colormap=custom_colorscale):
    df_filled = df.fillna(-1)  # Fill NaNs with -1 for 'missing' category
    fig = go.Figure(data=go.Heatmap(
        z=df_filled.values,
        x=df_filled.columns,
        y=df_filled.index,
        colorscale=colormap,
        colorbar=dict(
            title='AQI',
            titleside='top',
            tickmode='array',
            tickvals=tick_values,
            ticktext=tick_text,
            ticks='outside'
        ),
        zmin=-1,  # Minimum value of color scale
        zmax=450  # Maximum value of color scale
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(title='Year', type='category'),
        yaxis=dict(title='Month', autorange='reversed'),
        plot_bgcolor='rgba(0,0,0,0)',  # Makes plot background transparent
        # paper_bgcolor='#F4F4F8'
    )

    return fig
