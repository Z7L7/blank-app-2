# pages/gdlt.py

import streamlit as st
from modules.actors import gdelt_wrapper, crisis_cameo_codes, country_code  # Import dictionaries correctly

def app():
    st.title("GDELT Data Viewer")
    st.write("Welcome to the Humanitarian Aid Website!")

    # Get the list of countries and keywords
    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())

    # Dropdown for countries
    country = st.selectbox("Select a Country", countries)

    # Dropdown for keywords
    keyword = st.selectbox("Select a Keyword", keywords)

    if st.button("Fetch Data"):
        # Fetch the GDELT data
        data = gdelt_wrapper(country, keyword)

        if not data.empty:
            st.success("Data fetched successfully!")
            # Display the data in a table
            st.dataframe(data)
            # Download button for CSV
            st.download_button(
                label="Download as CSV",
                data=data.to_csv(index=False).encode('utf-8'),
                file_name="gdelt_data.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data found for the selected country and keyword.")