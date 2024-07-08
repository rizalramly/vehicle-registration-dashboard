import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('cars_2024.csv')

# Convert the date_reg column to datetime
data['date_reg'] = pd.to_datetime(data['date_reg'])

# Set the title
st.title("Vehicle Registration Dashboard")

# Display the dataframe
st.write(data)

# Convert dates to string for the slider
min_date = data['date_reg'].min().date()
max_date = data['date_reg'].max().date()

# Filter data by date
date_filter = st.slider("Select date range:",
                        min_value=min_date, 
                        max_value=max_date,
                        value=(min_date, max_date))

# Convert selected dates back to datetime
start_date = pd.to_datetime(date_filter[0])
end_date = pd.to_datetime(date_filter[1])

filtered_data = data[(data['date_reg'] >= start_date) & (data['date_reg'] <= end_date)]

# Display filtered data
st.write(filtered_data)

# Show statistics
st.write("Statistics")
st.write(filtered_data.describe())

# Plot a histogram of vehicle types
st.write("Vehicle Types Distribution")
st.bar_chart(filtered_data['type'].value_counts())

# Plot a pie chart of vehicle makers
st.write("Vehicle Makers Distribution")
fig, ax = plt.subplots()
filtered_data['maker'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
st.pyplot(fig)

# Plot a line chart of registrations over time
st.write("Registrations Over Time")
st.line_chart(filtered_data.groupby(filtered_data['date_reg'].dt.to_period('M')).size())
