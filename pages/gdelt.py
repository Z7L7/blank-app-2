import streamlit as st
from modules.actors import gdelt_wrapper, crisis_cameo_codes, country_code  # Import dictionaries correctly

def app():
    st.title("GDELT Data Viewer")
    st.write("Welcome to the Humanitarian Aid Website!")

    # Get the list of countries and keywords
    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())

    # Use session state to persist country, keyword, and fetched data
    if 'country' not in st.session_state:
        st.session_state['country'] = countries[0]  # Default to the first country

    if 'keyword' not in st.session_state:
        st.session_state['keyword'] = keywords[0]  # Default to the first keyword

    if 'gdelt_data' not in st.session_state:
        st.session_state['gdelt_data'] = None  # Initialize GDELT data as None

    # Dropdown for countries
    country = st.selectbox("Select a Country", countries, index=countries.index(st.session_state['country']))

    # Dropdown for keywords
    keyword = st.selectbox("Select a Keyword", keywords, index=keywords.index(st.session_state['keyword']))

    # Update session state with the new selections
    st.session_state['country'] = country
    st.session_state['keyword'] = keyword

    # Fetch GDELT data only if the country or keyword changes, or data is not already fetched
    if st.session_state['gdelt_data'] is None or st.session_state['country'] != country or st.session_state['keyword'] != keyword:
        if st.button("Fetch Data"):
            # Fetch the GDELT data
            data = gdelt_wrapper(st.session_state['country'], st.session_state['keyword'])

            if not data.empty:
                st.success("Data fetched successfully!")
                # Store the fetched data in session state
                st.session_state['gdelt_data'] = data
            else:
                st.warning("No data found for the selected country and keyword.")
                st.session_state['gdelt_data'] = None  # Reset data if no results

    # Use the fetched data from session state
    if st.session_state['gdelt_data'] is not None:
        data = st.session_state['gdelt_data']
        st.dataframe(data)
        # Download button for CSV
        st.download_button(
            label="Download as CSV",
            data=data.to_csv(index=False).encode('utf-8'),
            file_name="gdelt_data.csv",
            mime="text/csv"
        )