import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_parquet('cars.parquet')

# Convert 'date_reg' to datetime format if not already done
df['date_reg'] = pd.to_datetime(df['date_reg'], errors='coerce')

# Create a 'year' column
df['year'] = df['date_reg'].dt.year

# Group the data by year and maker, then count the number of vehicles in each group
grouped_yearly_df = df.groupby(['year', 'maker']).size().reset_index(name='count')

# Streamlit application layout
st.title("Vehicle Sales Dashboard")

# Sidebar for dropdown selections
st.sidebar.header("Filter Options")

# Dropdown for selecting year in the sidebar
years = df['year'].unique()
selected_year = st.sidebar.selectbox("Select Year:", options=years)

# Dropdown for selecting state in the sidebar
states = df['state'].unique()
selected_state = st.sidebar.selectbox("Select State:", options=states)

# Dropdown for selecting vehicle type in the sidebar
types = df['type'].unique()
selected_type = st.sidebar.selectbox("Select Vehicle Type:", options=types)

# Filter the dataframe based on selections
filtered_df = df[(df['state'] == selected_state) & (df['type'] == selected_type)]

# Group the filtered data by year, maker, and count the number of vehicles
filtered_df_grouped = filtered_df.groupby(['year', 'maker']).size().reset_index(name='count')

# Plot the yearly data
fig_yearly = px.line(filtered_df_grouped, x='year', y='count', color='maker',
                     title="Yearly Vehicle Sales by Maker")

# Display the yearly plot
st.plotly_chart(fig_yearly)

if selected_year:
    # Filter the dataframe based on the selected year
    yearly_filtered_df = filtered_df[filtered_df['year'] == selected_year]

    # Group the data by year_month and maker, and count the number of vehicles
    yearly_filtered_df['year_month'] = yearly_filtered_df['date_reg'].dt.to_period('M').astype(str)
    grouped_df = yearly_filtered_df.groupby(['year_month', 'maker']).size().reset_index(name='count')

    # Get the top 5 makers
    top_makers = grouped_df.groupby('maker')['count'].sum().nlargest(5).index
    top_5_df = grouped_df[grouped_df['maker'].isin(top_makers)]

    # Plot the top 5 makers data as a line chart
    fig_top_5 = px.line(top_5_df, x='year_month', y='count', color='maker',
                        title=f"Top 5 Vehicle Makers in {selected_state} for {selected_type} Type in {selected_year}")

    # Display the top 5 plot
    st.plotly_chart(fig_top_5)
else:
    st.write("Please select a year to display the top 5 chart.")
