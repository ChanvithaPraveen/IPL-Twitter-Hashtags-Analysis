import numpy as np
import pandas as pd
import streamlit as st
import datetime
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.title("IPL Twitter Data Analyzing Dashboard")

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.date_input('Start date', today)
end_date = st.date_input('End date', tomorrow)
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')


@st.cache
def load_data():
    data = pd.read_csv("../cities_with_geocodes_final.csv")  # Replace with your data source
    return data

data = load_data()

# Calculate the center of the map
center_lat = data['Latitude'].mean()
center_lon = data['Longitude'].mean()

# Create a Folium map
m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

# Add markers for each city
marker_cluster = MarkerCluster().add_to(m)
for index, row in data.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], tooltip=row['City']).add_to(marker_cluster)

# Display the map
folium_static(m)