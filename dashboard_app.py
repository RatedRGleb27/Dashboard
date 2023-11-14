import pandas as pd
import streamlit as st

# Streamlit app
def run_app():
    st.title("Interactive Sales Dashboard")

    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
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
        selected_year = st.sidebar.multiselect('Select Year', options=pivot_table['Year'].unique())

        # Apply filters to the pivot table
        if selected_country:
            pivot_table = pivot_table[pivot_table['Country'].isin(selected_country)]
        if selected_status:
            pivot_table = pivot_table[pivot_table['Status'].isin(selected_status)]
        if selected_year:
            pivot_table = pivot_table[pivot_table['Year'].isin(selected_year)]

        # Display pivot table
        st.write(pivot_table)

# Run the app
if __name__ == '__main__':
    run_app()
