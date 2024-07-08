import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# Function to load parquet data
@st.cache_data
def load_data():
    return pd.read_parquet('cars.parquet')

# Load the data
data = load_data()

# Convert the date_reg column to datetime
data['date_reg'] = pd.to_datetime(data['date_reg'])

# Sidebar date filter
st.sidebar.title("Filter")
min_date = data['date_reg'].min().date()
max_date = data['date_reg'].max().date()

date_filter = st.sidebar.slider("Select date range:",
                                min_value=min_date, 
                                max_value=max_date,
                                value=(min_date, max_date))

# Convert selected dates back to datetime
start_date = pd.to_datetime(date_filter[0])
end_date = pd.to_datetime(date_filter[1])

filtered_data = data[(data['date_reg'] >= start_date) & (data['date_reg'] <= end_date)]

# Navigation Menu
selected = option_menu(
    menu_title="Main Menu",  # required
    options=["Yearly Registration", "Detailed Analysis"],  # required
    icons=["calendar", "bar-chart"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
)

if selected == "Yearly Registration":
    st.title("Yearly Vehicle Registration")

    # Group data by year
    data['year'] = data['date_reg'].dt.year
    yearly_data = data.groupby('year').size()

    # Plot line chart
    st.write("Yearly Registered Vehicles")
    st.line_chart(yearly_data)

elif selected == "Detailed Analysis":
    st.title("Vehicle Registration Dashboard")

    # Info boxes
    total_vehicles = filtered_data.shape[0]
    total_petrol = filtered_data[filtered_data['fuel'] == 'petrol'].shape[0]
    total_diesel = filtered_data[filtered_data['fuel'] == 'diesel'].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Vehicles Sales", total_vehicles)
    col2.metric("Total Petrol Vehicles Sales", total_petrol)
    col3.metric("Total Diesel Vehicles Sales", total_diesel)

    # Plot a histogram of vehicle types
    st.write("Vehicle Types Distribution")
    st.bar_chart(filtered_data['type'].value_counts())

    # Plot a pie chart of vehicle makers
    st.write("Top 5 Vehicle Makers Distribution")
    top_5_makers = filtered_data['maker'].value_counts().nlargest(5)
    fig, ax = plt.subplots()
    top_5_makers.plot.pie(autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

    # Display the filtered dataframe at the bottom
    st.write("Filtered Data")
    st.write(filtered_data)

    # Display statistics at the bottom
    st.write("Statistics")
    st.write(filtered_data.describe())
