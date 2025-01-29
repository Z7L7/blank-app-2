# pages/news.py

import streamlit as st
import requests
from datetime import datetime

@st.cache_data(ttl=600)  # Cache data for 10 minutes
def fetch_reliefweb_data(limit):
    """
    Fetch reports from the ReliefWeb API.

    Args:
        limit (int): Number of reports to fetch.

    Returns:
        dict or None: JSON response from the API or None if the request fails.
    """
    url = "https://api.reliefweb.int/v1/reports"
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

    # Button to fetch data
    if st.button("Fetch Reports"):
        with st.spinner("Fetching reports..."):
            data = fetch_reliefweb_data(num_reports)

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
    else:
        st.info("Use the slider and button above to fetch the latest reports.")
