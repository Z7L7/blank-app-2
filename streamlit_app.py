import streamlit as st
import pandas as pd
import numpy as np
from modules.actors import crisis_cameo_codes, country_code
from modules.charts import time_series_chart, bar_chart, word_cloud_image
from datetime import datetime
import requests
import time


def main():
# Initialize session state with page-specific values
    if 'global_country' not in st.session_state:
        st.session_state['global_country'] = 'Afghanistan'
    if 'global_keyword' not in st.session_state:
        st.session_state['global_keyword'] = 'biological threat'

    # Initialize page-specific values if they don't exist
    if 'page_values' not in st.session_state:
        st.session_state['page_values'] = {}

    # Sidebar controls
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Homepage", "Acaps", "GDELT", "Relief Web", "Google"])

    # Global selections in sidebar
    st.sidebar.title("Global Selections")
    st.session_state['global_country'] = st.sidebar.selectbox(
        "Default Country",
        sorted(country_code.keys()),
        key='global_country_select'
    )
    st.session_state['global_keyword'] = st.sidebar.selectbox(
        "Default Keyword",
        sorted(crisis_cameo_codes.keys()),
        key='global_keyword_select'
    )

    # Navigation logic
    if page == "Homepage":
        from pages import homepage
        homepage.app()

    elif page == "Acaps":
        from pages import acaps_api
        acaps_api.app()

    elif page == "GDELT":
        from pages import gdelt
        gdelt.app()

    elif page == "Relief Web":
        from pages import news
        news.app()

    elif page == "Google":
        from pages import google
        google.app()

    # Footer
    st.sidebar.text("Humanitarian Aid Website By:\nAsiyah Adetunji")

if __name__ == "__main__":
    main()