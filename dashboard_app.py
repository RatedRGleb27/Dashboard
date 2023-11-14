import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit app
def run_app():
    st.title("Interactive Sales Dashboard")

    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    
    # Display file contents when a file is uploaded
    if uploaded_file is not None:
        # Read the uploaded file
        data = pd.read_csv(uploaded_file)

        # Convert Year and Month to string for grouping
        data['Year'] = data['Year'].astype(str)
        data['Month'] = data['Month'].astype(str)

        # Creating the pivot table
        pivot_table = pd.pivot_table(data,
                                     values=['Sales excl Tax EUR', 'Quantity'],
                                     index=['Country', 'Status', 'Store', 'Year', 'Month'],
                                     aggfunc='sum').reset_index()

        # Filters for the sidebar
        selected_country = st.sidebar.multiselect('Select Country', options=pivot_table['Country'].unique())
        selected_status = st.sidebar.multiselect('Select Status', options=pivot_table['Status'].unique())
        selected_store = st.sidebar.multiselect('Select Store', options=pivot_table['Store'].unique())

        # Apply filters to the pivot table
        if selected_country:
            pivot_table = pivot_table[pivot_table['Country'].isin(selected_country)]
        if selected_status:
            pivot_table = pivot_table[pivot_table['Status'].isin(selected_status)]
        if selected_store:
            pivot_table = pivot_table[pivot_table['Store'].isin(selected_store)]

        # Create a pivot table-like view using plotly express
        title_text = f'Sum of Sales excl Tax EUR by Month for {", ".join(selected_country)}, {", ".join(selected_status)}, {", ".join(selected_store)}'
        pivot_fig = px.bar(
            pivot_table,
            x='Month',
            y='Sales excl Tax EUR',
            color='Year',
            labels={'Month': 'Month', 'Sales excl Tax EUR': 'Sum of Sales excl Tax EUR'},
            title=title_text
        )

        # Display the pivot table-like view
        st.plotly_chart(pivot_fig)

# Run the app
if __name__ == '__main__':
    run_app()
