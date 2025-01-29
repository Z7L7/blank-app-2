import streamlit as st
from modules.actors import gdelt_wrapper
import pandas as pd
from modules.actors import crisis_cameo_codes, country_code  # Import dictionaries correctly

def app():
    st.title("Finding Hope")
    st.write("Welcome to the Humanitarian Aid Website!")

    st.header("How to Use This Website")
    st.write("Choose which country you wish to do a deep dive on, and select a keyword for the GDELT Dataset to use in the below dropdown boxes")
     
    # Initialize session state variables if they don't exist
    if 'homepage_country' not in st.session_state:
        st.session_state.homepage_country = 'Afghanistan'  # Default country

    if 'homepage_keyword' not in st.session_state:
        st.session_state.homepage_keyword = 'earthquake'  # Default keyword

    # Get the list of countries and keywords
    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())
    cola, colb = st.columns(2)

    # Dropdown for countries
    with cola:
        country = st.selectbox("Select a Country", countries)

    # Dropdown for keywords
    with colb:
        keyword = st.selectbox("Select a Keyword", keywords)

    # Update session state if selections change
    if country != st.session_state.homepage_country or keyword != st.session_state.homepage_keyword:
        st.session_state.homepage_country = country
        st.session_state.homepage_keyword = keyword


    # - - - Columns with images - - -
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://i.pinimg.com/474x/91/58/87/9158873487dc0d6fdad74b0dd1aed074.jpg", caption="")

    with col2:
        st.header("What is Humanitarian Aid?")
        st.write("Humanitarian aid is an important subject to many across the world. It is defined as the assistance provided to those in need using both logistic and material assistance. There are many humanitarian aid organizations such as UNICEF and Doctors Without Boarders")

    # - - - Text - - -
    coli3, coli4 = st.columns(2)
    with coli3:
        st.image("https://i.pinimg.com/474x/b8/19/79/b819799f9ab52866a70218fd23499519.jpg", caption="")

    with coli4:
        st.image("https://i.pinimg.com/474x/93/1d/62/931d62501c149f08ec1643592081754e.jpg", caption="")

    # - - - Text - - -
    coli5, coli6 = st.columns(2)
    with coli5:
        st.header("Why Does Humanitarian Aid Matter?")
        st.write("Humanitarian aid is an important subject to many across the world. It is defined as the assistance provided to those in need using both logistic and material assistance. There are many humanitarian aid organizations such as UNICEF and Doctors Without Boarders")

    with coli6:
        st.header("How to Contribute to Humanitarian Aid")
        st.write("Humanitarian aid is an important subject to many across the world. It is defined as the assistance provided to those in need using both logistic and material assistance. There are many humanitarian aid organizations such as UNICEF and Doctors Without Boarders")


