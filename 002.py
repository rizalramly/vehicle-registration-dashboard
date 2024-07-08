import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('cars_2024.csv')

# Streamlit application layout
st.title("Vehicle Sales Dashboard")

# Sidebar for dropdown selections
st.sidebar.header("Filter Options")

# Dropdown for selecting state in the sidebar
selected_state = st.sidebar.selectbox(
    "Select State:",
    options=df['state'].unique()
)

# Dropdown for selecting vehicle type in the sidebar
selected_type = st.sidebar.selectbox(
    "Select Vehicle Type:",
    options=df['type'].unique()
)

# Filter the dataframe based on selections
filtered_df = df[(df['state'] == selected_state) & (df['type'] == selected_type)]

# Group the data by date_reg and maker, and count the number of vehicles
grouped_df = filtered_df.groupby(['date_reg', 'maker']).size().reset_index(name='count')

# Plot the filtered data as a line chart
fig = px.line(grouped_df, x='date_reg', y='count', color='maker', title=f"Vehicle Sales in {selected_state} for {selected_type} Type")

# Display the plot
st.plotly_chart(fig)
