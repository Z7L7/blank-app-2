import streamlit as st
import pandas as pd
import numpy as np
from modules.actors import crisis_cameo_codes, country_code
from modules.charts import time_series_chart, bar_chart, word_cloud_image
from datetime import datetime
import requests
import time


def main():
    # Sidebar for Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Homepage", "Acaps", "GDELT", "Relief Web", "Google"])

    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())

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

    # elif page == "Fewsnet":
    #     from pages import fewsnet
    #     fewsnet.app()

    elif page == "Google":
        from pages import google
        google.app()

    # elif page == "Analysis":
    #     from pages import analysis
    #     analysis.app()

    # elif page == "Chatbot":
    #     from pages import chatbot
    #     chatbot.app()

    # countries = sorted(country_code.keys())
    # keywords = sorted(crisis_cameo_codes.keys())
    # country = st.selectbox("Select a Country", countries, index=countries.index(st.session_state['country']))
    # st.sidebar.country




    # Footer
    st.sidebar.text("Humanitarian Aid Website By:\nAsiyah Adetunji")

if __name__ == "__main__":
    main()