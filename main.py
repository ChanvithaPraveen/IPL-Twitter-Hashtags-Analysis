import pandas as pd
import plotly.express as px
from fastapi import FastAPI

df = pd.read_csv('cities_with_geocodes_final.csv')

app = FastAPI()


def plot_world_map(df):
    # Create a bubble map showing all cities
    fig = px.scatter_geo(
        df,  # Use the original DataFrame with all cities
        lat='Latitude',
        lon='Longitude',
        hover_data=['city', 'population'],  # Display additional data on hover
        size='population',  # Use 'Population' for bubble size
        projection='natural earth',  # You can change the projection as needed
        title='City Bubble Map',
    )

    # Customize the layout (optional)
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="grey",
        showland=True,
        landcolor="dark blue",
    )

    return fig


fig = plot_world_map(df)

# # Show the map
fig.show()
