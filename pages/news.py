import streamlit as st
from modules.actors import crisis_cameo_codes, country_code  # Import dictionaries correctly

def app():
    st.title("News")
    st.write("Welcome to the Humanitarian Aid Website!")

    # Get the list of countries and keywords
    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())

    # Dropdown for countries
    country = st.selectbox("Select a Country", countries)

    # Dropdown for keywords
    keyword = st.selectbox("Select a Keyword", keywords)

