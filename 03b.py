import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Function to load parquet data
@st.cache_data
def load_data():
    return pd.read_parquet('cars.parquet')

# Load the data
data = load_data()

# Convert the date_reg column to datetime
data['date_reg'] = pd.to_datetime(data['date_reg'])

# Sidebar
st.sidebar.title("Malaysia Vehicle Registration")

# Sidebar tab selection
selected = st.sidebar.radio(
    "Main Menu",
    ["Yearly Registration", "Detailed Analysis"]
)

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

# CSS for infobox style
st.markdown("""
    <style>
    .infobox {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 5px;
        text-align: center;
        flex: 1;
    }
    .infobox h3 {
        font-size: 18px;
        margin: 0;
    }
    .infobox p {
        font-size: 24px;
        margin: 0;
    }
    .infobox-container {
        display: flex;
        justify-content: space-around;
    }
    </style>
    """, unsafe_allow_html=True)

if selected == "Yearly Registration":
    st.title("Yearly Vehicle Registration")

    # Group data by year and filter out 2024
    data['year'] = data['date_reg'].dt.year
    yearly_data = data[data['year'] != 2024].groupby('year').size().reset_index(name='count')

    # Plot line chart using Plotly
    fig = px.line(yearly_data, x='year', y='count', labels={'year': 'Year', 'count': 'Number of Vehicles'}, title='Yearly Registered Vehicles')
    fig.update_layout(xaxis=dict(tickmode='linear', tickangle=60))
    st.plotly_chart(fig)

elif selected == "Detailed Analysis":
    st.title("Vehicle Registration Dashboard")

    # Filtered data for the year 2024
    filtered_data_2024 = filtered_data[filtered_data['date_reg'].dt.year == 2024]

    # Info boxes
    total_vehicles = f"{filtered_data_2024.shape[0]:,}"
    total_petrol = f"{filtered_data_2024[filtered_data_2024['fuel'] == 'petrol'].shape[0]:,}"
    total_diesel = f"{filtered_data_2024[filtered_data_2024['fuel'] == 'diesel'].shape[0]:,}"

    st.markdown(f"""
        <div class="infobox-container">
            <div class="infobox"><h3>Total Vehicles Sales</h3><p>{total_vehicles}</p></div>
            <div class="infobox"><h3>Total Petrol Vehicles Sales</h3><p>{total_petrol}</p></div>
            <div class="infobox"><h3>Total Diesel Vehicles Sales</h3><p>{total_diesel}</p></div>
        </div>
        """, unsafe_allow_html=True)

    # Plot a histogram of vehicle types using Plotly
    st.write("Vehicle Types Distribution")
    type_counts = filtered_data_2024['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    fig = px.bar(type_counts, x='type', y='count', labels={'type': 'Vehicle Type', 'count': 'Number of Vehicles'}, title='Vehicle Types Distribution')
    st.plotly_chart(fig)

    # Plot a pie chart of vehicle makers using Plotly
    st.write("Top 5 Vehicle Makers Distribution")
    top_5_makers = filtered_data_2024['maker'].value_counts().nlargest(5).reset_index()
    top_5_makers.columns = ['maker', 'count']
    fig = px.pie(top_5_makers, values='count', names='maker', title='Top 5 Vehicle Makers Distribution', hole=0.3)
    st.plotly_chart(fig)

    # Display the filtered dataframe at the bottom
    st.write("Filtered Data")
    st.write(filtered_data_2024)

    # Display statistics at the bottom
    st.write("Statistics")
    st.write(filtered_data_2024.describe())
