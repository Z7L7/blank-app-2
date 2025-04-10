# pages/news.py

import streamlit as st
import requests
from datetime import datetime
from modules.actors import crisis_cameo_codes, country_code  # Import dictionaries correctly
from modules.charts import time_series_chart, bar_chart, word_cloud_image



@st.cache_data(ttl=600)  # Cache data for 10 minutes


def fetch_reliefweb_data(limit, country):
    
    """
    Fetch reports from the ReliefWeb API.

    Args:
        limit (int): Number of reports to fetch.

    Returns:
        dict or None: JSON response from the API or None if the request fails.
    """
    url = ("https://api.reliefweb.int/v1/reports?appname=REPLACE-WITH-A-DOMAIN-OR-APP-NAME&filter[field]=country&filter[value][]=%s&filter[value]"%country)
    params = {
        "appname": "apidoc",       # Replace with your actual app name if different
        "limit": limit, 
        "profile": "full",
        "sort[]": "date:desc"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from ReliefWeb API: {e}")
        return None

def app():
    """
    Render the ReliefWeb Reports page.
    """
    st.title("ReliefWeb Reports")
    st.write("Stay updated with the latest humanitarian reports from ReliefWeb.")


    # Add a slider for the user to select the number of reports
    num_reports = st.slider(
        "Select number of reports to fetch",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )
    
    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())

    # Display current selections from sidebar
    country = st.session_state.get('global_country', countries[0])
    keyword = st.session_state.get('global_keyword', keywords[0])


    # Use session state to persist country, keyword, and fetched data
    if 'country' not in st.session_state:
        st.session_state['country'] = countries[0]  # Default to the first country

    if 'keyword' not in st.session_state:
        st.session_state['keyword'] = keywords[0]  # Default to the first keyword

    if 'gdelt_data' not in st.session_state:
        st.session_state['gdelt_data'] = None  # Initialize GDELT data as None

    # # Dropdown for countries
    # country = st.selectbox("Select a Country", countries, index=countries.index(st.session_state['country']))

    # # Dropdown for keywords
    # keyword = st.selectbox("Select a Keyword", keywords, index=keywords.index(st.session_state['keyword']))

    # Update session state with the new selections
    st.session_state['country'] = country
    st.session_state['keyword'] = keyword


    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Current Country:** {country}")
    with col2:
        st.write(f"**Current Keyword:** {keyword}")

    

    #Found problem where if the website doesn't have a report on the topic it just uses the initial search conditions instead
    # Button to fetch data
    if st.button("Fetch Reports"):
        with st.spinner("Fetching reports..."):
            data = fetch_reliefweb_data(num_reports, country)

        if data:
            reports = data.get("data", [])
            st.success(f"Number of reports fetched: {len(reports)}")
            

            for report in reports:
                fields = report.get("fields", {})
                title = fields.get("title", "No Title")
                date_info = fields.get("date", {})
                date_str = date_info.get("created", "No Date")

                # Parse and format the date
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
                    formatted_date = date.strftime("%B %d, %Y %H:%M:%S %Z")
                except (ValueError, TypeError):
                    formatted_date = "No Date"

                summary = fields.get("body-html", "No Summary Available")

                st.subheader(title)
                st.write(f"**Date:** {formatted_date}")
                st.markdown(summary, unsafe_allow_html=True)
                st.markdown("---")
                if summary != "No Summary Available":
                    word_cloud_image(summary)
    else:
        st.info("Use the slider and button above to fetch the latest reports.")
