import pandas as pd
import plotly.graph_objects as go
import numpy as np
import calendar

def plot_polar_avg_aqi(csv_files, city_names):
    """
    Plot a polar graph showing the average AQI value for each month across different years, with dots representing the average values and different colors for each city.

    Parameters:
        csv_files (list): List of CSV filenames for the cities.
        city_names (list): List of city names corresponding to the CSV files.

    Returns:
        None (displays the plot).
    """
    # Initialize a dictionary to store average AQI values for each month
    avg_aqi_by_month = {calendar.month_name[i]: [] for i in range(1, 13)}

    # Initialize a list to store traces for the plot
    traces = []

    # Iterate through each CSV file and city name
    for file, city in zip(csv_files, city_names):
        # Read the CSV file
        df = pd.read_csv(file)
        # Convert 'Month' column to month names
        df['Month'] = df['Month'].apply(lambda x: calendar.month_name[int(x)])
        # Group by month and calculate average AQI for each month
        avg_aqi_monthly = df.groupby('Month')['aqi'].mean().reset_index()
        # Store average AQI values for each month in the dictionary
        for index, row in avg_aqi_monthly.iterrows():
            avg_aqi_by_month[row['Month']].append(row['aqi'])

        # Calculate the overall average AQI for each month across different years
        avg_aqi_overall = [np.mean(avg_aqi_by_month[calendar.month_name[i]]) for i in range(1, 13)]
        # Rearrange the avg_aqi_overall list to match the order of months
        avg_aqi_overall_reordered = avg_aqi_overall[6:] + avg_aqi_overall[:6]

        # Convert months to radians for polar plot
        theta = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]

        # Add a trace for each city
        traces.append(go.Scatterpolar(
            r=avg_aqi_overall_reordered,
            theta=theta,
            mode='markers',
            name=city,  # Name used for the legend
            marker=dict(
                size=8,  # Adjust the size of the dots as needed
                symbol='circle'
            )
        ))

    # Create the figure with all the traces
    fig = go.Figure(data=traces)

    # Update the layout of the figure
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([val for sublist in avg_aqi_by_month.values() for val in sublist])]
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=np.linspace(0, 360, 12, endpoint=False),
                ticktext=list(calendar.month_name)[1:]  # Ensure this matches the order of your data
            )
        ),
        title='Average AQI by Month',
        showlegend=True  # Show the legend
    )

    # Show the plot
    fig.show()

csv_files = ['./csv/aqi_cleaned_Bakersfield.csv', './csv/aqi_cleaned_Boston.csv', './csv/aqi_cleaned_Denver.csv',
             './csv/aqi_cleaned_LA.csv', './csv/aqi_cleaned_New_York.csv', './csv/aqi_cleaned_Phoenix.csv',
             './csv/aqi_cleaned_Reno.csv', './csv/aqi_cleaned_Visalia.csv']  # Replace with your CSV filenames
city_names = ['Bakersfield', 'Boston', 'Denver', 'LA', 'New York', 'Phoenix', 'Reno', 'Visalia']  # Replace with your actual city names
plot_polar_avg_aqi(csv_files, city_names)
#plot_polar_avg_aqi(csv_files)