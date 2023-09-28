# import pandas as pd
# import plotly.express as px
# from fastapi import FastAPI
#
# df = pd.read_csv('cities_with_geocodes_final.csv')
#
# app = FastAPI()
#
#
# def plot_world_map(df):
#     # Create a bubble map showing all cities
#     fig = px.scatter_geo(
#         df,  # Use the original DataFrame with all cities
#         lat='Latitude',
#         lon='Longitude',
#         hover_data=['city', 'population'],  # Display additional data on hover
#         size='population',  # Use 'Population' for bubble size
#         projection='natural earth',  # You can change the projection as needed
#         title='City Bubble Map',
#     )
#
#     # Customize the layout (optional)
#     fig.update_geos(
#         showcoastlines=True,
#         coastlinecolor="grey",
#         showland=True,
#         landcolor="dark blue",
#     )
#
#     return fig
#
#
# # fig = plot_world_map(df)
# #
# # # # Show the map
# # fig.show()
# # fig.write_html('bubble_map.html')





from fastapi import FastAPI, Query
import pandas as pd
import plotly.express as px

app = FastAPI()

# Load your DataFrame
df = pd.read_csv('df1_with_datetime.csv')

# Define a FastAPI endpoint to filter and create the bubble map
@app.get("/generate_bubble_map/")
async def generate_bubble_map(start_date: str = Query(...), end_date: str = Query(...)):
    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Assuming 'datetime' column contains date and time as strings
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Perform the comparison using Timestamp objects
    filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
    print(f"start_date: {start_date}, type: {type(start_date)}")
    print(f"end_date: {end_date}, type: {type(end_date)}")

    # Group the filtered DataFrame by city without aggregating other columns
    grouped_df = filtered_df.groupby('city')

    # Create temp_df including 'city' and 'population'
    temp_df = grouped_df['city', 'population'].sum().reset_index()

    # Check if 'city' column exists before dropping it
    if 'city' in temp_df.columns:
        temp_df = temp_df.merge(grouped_df.first(), on='city')

    # Create a bubble map using Plotly Express
    fig = px.scatter_geo(
        temp_df,
        lat='Latitude',
        lon='Longitude',
        hover_data=['city', 'population'],
        size='population',
        projection='natural earth',
        title='City Bubble Map',
    )

    # Customize the layout (optional)
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="grey",
        showland=True,
        landcolor="dark blue",
    )

    # Save the bubble map as an HTML file
    fig.write_html('bubble_map.html')

    return {'message': 'Bubble map generated successfully'}

