import pandas as pd
import streamlit as st
import plotly.express as px

# Load your CSV data into a DataFrame
df = pd.read_csv('/Users/glebpeshkov/PycharmProjects/dashboard/Dashboard - Sheet1.csv')

# Sidebar options for filtering
st.sidebar.title("Filter Options")
selected_country = st.sidebar.selectbox("Select Country", df['Country'].unique())
selected_status = st.sidebar.selectbox("Select Status", df['Status'].unique())
selected_store = st.sidebar.selectbox("Select Store", df['Store'].unique())

# Filter data based on selected options
filtered_data = df[(df['Country'] == selected_country) & (df['Status'] == selected_status) & (df['Store'] == selected_store)]

# Group and aggregate data by Year, Month, and other columns as needed
grouped_data = filtered_data.groupby(['Year', 'Month']).agg({'Sales excl Tax EUR': 'sum', 'Quantity': 'sum'}).reset_index()

# Create a pivot table-like view using plotly express
pivot_table = px.bar(
    grouped_data,
    x='Month',
    y='Sales excl Tax EUR',
    color='Year',
    labels={'Month': 'Month', 'Sales excl Tax EUR': 'Sum of Sales excl Tax EUR'},
    title=f'Sum of Sales excl Tax EUR by Month for {selected_country}, {selected_status}, {selected_store}'
)

# Display the pivot table-like view
st.plotly_chart(pivot_table)

# Add a download link for the filtered data
st.sidebar.markdown("### Download Filtered Data")
filtered_data_link = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Filtered Data",
    data=filtered_data_link,
    file_name="filtered_data.csv",
)

# Optional: Wrap the pivot table by Year
if st.checkbox("Wrap by Year"):
    wrapped_pivot = px.bar(
        grouped_data,
        x='Month',
        y='Sales excl Tax EUR',
        color='Year',
        facet_row='Year',
        labels={'Month': 'Month', 'Sales excl Tax EUR': 'Sum of Sales excl Tax EUR'},
        title=f'Sum of Sales excl Tax EUR by Month for {selected_country}, {selected_status}, {selected_store}'
    )
    st.plotly_chart(wrapped_pivot)