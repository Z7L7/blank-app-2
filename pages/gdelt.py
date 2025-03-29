import streamlit as st
from modules.actors import gdelt_wrapper, crisis_cameo_codes, country_code

def app():
    st.title("GDELT Data Viewer")
    st.write("Analyze global events through the GDELT dataset")

    # Get lists of available options
    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())

    # Initialize session state for GDELT data
    if 'gdelt_data' not in st.session_state:
        st.session_state['gdelt_data'] = None
    if 'gdelt_country' not in st.session_state:
        st.session_state['gdelt_country'] = st.session_state.get('global_country', countries[0])
    if 'gdelt_keyword' not in st.session_state:
        st.session_state['gdelt_keyword'] = st.session_state.get('global_keyword', keywords[0])

     # Display current selections from sidebar
    current_country = st.session_state.get('global_country', countries[0])
    current_keyword = st.session_state.get('global_keyword', keywords[0])

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Current Country:** {current_country}")
    with col2:
        st.write(f"**Current Keyword:** {current_keyword}")

    # # Display current selections (can be overridden)
    # col1, col2 = st.columns(2)
    # with col1:
    #     current_country = st.selectbox(
    #         "Select Country",
    #         countries,
    #         index=countries.index(st.session_state['gdelt_country']),
    #         key='gdelt_country_select'
    #     )
    # with col2:
    #     current_keyword = st.selectbox(
    #         "Select Keyword",
    #         keywords,
    #         index=keywords.index(st.session_state['gdelt_keyword']),
    #         key='gdelt_keyword_select'
    #     )

    # # Update session state with current selections
    # st.session_state['gdelt_country'] = current_country
    # st.session_state['gdelt_keyword'] = current_keyword

    # Fetch data button - only fetch when clicked
    if st.button("Fetch GDELT Data"):
        with st.spinner(f"Fetching data for {current_country} with keyword '{current_keyword}'..."):
            data = gdelt_wrapper(current_country, current_keyword)

            if not data.empty:
                st.session_state['gdelt_data'] = data
                st.success("Data fetched successfully!")
            else:
                st.session_state['gdelt_data'] = None
                st.warning("No data found for the selected parameters")

    # Display results if available
    if st.session_state['gdelt_data'] is not None:
        data = st.session_state['gdelt_data']

        st.header("GDELT Data Results")
        st.dataframe(data)

        # Download option
        st.download_button(
            label="Download as CSV",
            data=data.to_csv(index=False).encode('utf-8'),
            file_name=f"gdelt_{current_country}_{current_keyword}.csv",
            mime="text/csv"
        )

        st.header("Description vs Goldstein Scale")
        st.write("A scale developed by Joshua S. Goldstein that measures international events from -10.0 to +10.0. Negative values indicate conflict, positive values indicate cooperation.")
        st.bar_chart(data, x="CAMEOCodeDescription", y="GoldsteinScale", color="#ffaa00", horizontal=True)