'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from etl import top_locations, top_locations_mappable, tickets_in_top_locations
st.set_page_config(layout="wide")

data = pd.read_csv('./cache/tickets_in_top_locations.csv')
st.title('Top Locations for Parking Tickets within Syracuse')

# Sidebar for location selection
location_options = ['All locations'] + sorted(data['location'].unique().tolist())
location = st.sidebar.selectbox('Select a location:', location_options)

# Filter data
if location == 'All locations':
    filtered_data = data
else:
    filtered_data = data[data['location'] == location]

# Layout columns
col1, col2 = st.columns(2)

# Metrics and plots
def plot_by_hour(df):
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="hourofday", y="count", estimator="sum", hue="hourofday", ax=ax)
    ax.set_title('Tickets Issued by Hour of Day')
    return fig

def plot_by_day(df):
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="dayofweek", y="count", estimator="sum", hue="dayofweek", ax=ax)
    ax.set_title('Tickets Issued by Day of Week')
    return fig
def show_metrics_and_plots():
    with col1:
        st.metric("Total tickets issued", filtered_data.shape[0])
        fig_hour = plot_by_hour(filtered_data)
        st.pyplot(fig_hour)

    with col2:
        st.metric("Total amount", f"$ {filtered_data['amount'].sum()}")
        fig_day = plot_by_day(filtered_data)
        st.pyplot(fig_day)
# Run visualizations
show_metrics_and_plots()

# Show map
st.map(filtered_data[['lat', 'lon']])