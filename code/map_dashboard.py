'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

# Load the data
data = pd.read_csv('./cache/top_locations_mappable.csv')

st.title('Top Locations for Parking Tickets within Syracuse')

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    data,
    geometry=gpd.points_from_xy(data['lon'], data['lat']),
)

# Base map
m = folium.Map(location=CUSE, zoom_start=ZOOM)

# Add points to the map
for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"Location: {row['location']}<br>Amount: {row['amount']}",
    ).add_to(m)

# Add a color scale
folium.LayerControl().add_to(m)

# Add the map to the Streamlit app
st.subheader('Map of Top Locations for Parking Tickets')
st.write("This map shows the top locations for parking tickets within Syracuse. The size of the circle markers indicates the number of tickets issued at that location.")
st_folium = sf.st_folium(m, width=700, height=500)           