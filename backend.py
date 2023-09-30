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
start_date = '2020-10-10'
end_date = '2020-10-20'
# Define a FastAPI endpoint to filter and create the bubble map
@app.get("/generate_bubble_map/")
async def generate_bubble_map(start_date: str = Query(...), end_date: str = Query(...)):
# def generate_bubble_map(start_date, end_date):
    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Assuming 'datetime' column contains date and time as strings
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Perform the comparison using Timestamp objects
    filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
    print(f"start_date: {start_date}, type: {type(start_date)}")
    print(f"end_date: {end_date}, type: {type(end_date)}")
    # print(filtered_df.columns)

    # # Create a new DataFrame with unique cities and all other columns
    # grouped_df = filtered_df.groupby('city').first().reset_index()
    # grouped_df['temp_population'] = grouped_df.groupby('city')['city'].transform('count')
    # print(grouped_df)

    # Group by 'city' and count rows
    grouped_df = filtered_df.groupby('city').size().reset_index(name='count')

    # Step 4: Add 'Latitude', 'Longitude', 'population', and 'country' columns to 'temp_city_df'
    grouped_df = grouped_df.merge(
        df[['city', 'Latitude', 'Longitude', 'population', 'country']].drop_duplicates(),
        on='city',
        how='left'
    )

    print(grouped_df)
    # Create a bubble map using Plotly Express
    fig = px.scatter_geo(
        grouped_df,
        lat='Latitude',
        lon='Longitude',
        hover_data=['city', 'population'],
        size='count',
        projection='natural earth',
        title='City Bubble Map',
    )

    # Customize the layout (optional)
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="grey",
        showland=True,
        landcolor="dark red",
    )

    # Save the bubble map as an HTML file
    fig.write_html('bubble_map7.html')

    print({'message': 'Bubble map generated successfully'})
    # print(fig)
    # return fig

# generate_bubble_map(start_date, end_date)

@app.get("/generate_city_chart/")
async def generate_city_chart(start_date: str = Query(...), end_date: str = Query(...)):
    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Assuming 'datetime' column contains date and time as strings
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Perform the comparison using Timestamp objects
    filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
    print(f"start_date: {start_date}, type: {type(start_date)}")
    print(f"end_date: {end_date}, type: {type(end_date)}")

    # Group by 'city' and count rows
    grouped_df = filtered_df.groupby('city').size().reset_index(name='count')

    # Create the Pie chart
    # fig = px.pie(grouped_df, values='count', names='city', title='City Distribution')

    # Create a bar chart using Plotly Express
    fig = px.bar(grouped_df, x='city', y='count', title='City-wise Count')
    fig.update_xaxes(title='City')
    fig.update_yaxes(title='Count')

    # Save the bubble map as an HTML file
    fig.write_html('city_chart.html')

    print({'message': 'City Chart generated successfully'})


@app.get("/generate_line_chart/")
async def generate_line_chart(start_date: str = Query(...), end_date: str = Query(...)):
    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Assuming 'datetime' column contains date and time as strings
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Perform the comparison using Timestamp objects
    filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
    print(f"start_date: {start_date}, type: {type(start_date)}")
    print(f"end_date: {end_date}, type: {type(end_date)}")

    # Group by 'city' and count rows
    grouped_df = filtered_df.groupby('city').size().reset_index(name='count')

    # Group by 'city' and count rows
    grouped_df = filtered_df.groupby(['city', filtered_df['datetime'].dt.date]).size().reset_index(name='count')

    # Create a line plot using Plotly Express
    fig = px.line(grouped_df, x='datetime', y='count', color='city',
                  labels={'count': 'Tweet Count', 'datetime': 'Date'},
                  title='Tweet Count by City Over Time')

    # Customize the appearance of the plot
    fig.update_layout(xaxis_title_font=dict(size=18), yaxis_title_font=dict(size=18),
                      xaxis_tickangle=-45, xaxis_tickfont=dict(size=14),
                      yaxis_tickfont=dict(size=14), legend_title=dict(text='City'))

    # Display the plot in Streamlit
    # fig.show()

    # Save the bubble map as an HTML file
    fig.write_html('line_chart.html')

    print({'message': 'Line chart generated successfully'})

# generate_line_chart(start_date, end_date)


from forecast_data_by_date_and_city import predict_future_tweet_count


@app.post("/predict_future_tweet_count/")
async def predict(predict_date: str = Query(...), select_city: str = Query(...)):
    # Your prediction logic here
    # print({"message": "Prediction result"})
    predicted_count = predict_future_tweet_count(predict_date, select_city)
    print(predicted_count)
    return predicted_count
