import streamlit as st
from modules.actors import gdelt_wrapper
import pandas as pd
from modules.actors import crisis_cameo_codes, country_code

def app():
    st.title("Finding Hope")
    st.write("Welcome to the Humanitarian Aid Website!")

    st.divider()

    st.header("How to Use This Website")
    st.write("""
        Choose which country and keyword you wish to explore using the dropdown boxes
        in the sidebar. These selections will be used throughout the website.
    """)

    # - - - Columns with images - - -
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://i.pinimg.com/474x/91/58/87/9158873487dc0d6fdad74b0dd1aed074.jpg", caption="")

    with col2:
        st.header("What is Humanitarian Aid?")
        st.write("""
            Humanitarian aid is an important subject to many across the world. It is defined as the assistance
            provided to those in need using both logistic and material assistance. There are many humanitarian
            aid organizations such as UNICEF and Doctors Without Borders.
        """)

    # - - - Image columns - - -
    coli3, coli4 = st.columns(2)
    with coli3:
        st.image("https://i.pinimg.com/474x/b8/19/79/b819799f9ab52866a70218fd23499519.jpg", caption="")

    with coli4:
        st.image("https://i.pinimg.com/474x/93/1d/62/931d62501c149f08ec1643592081754e.jpg", caption="")

    # - - - Text columns - - -
    coli5, coli6 = st.columns(2)
    with coli5:
        st.header("Why Does Humanitarian Aid Matter?")
        st.write("""
            Humanitarian aid is crucial because it addresses the immediate needs of people affected by crises,
            such as natural disasters, conflicts, and health emergencies, ensuring their survival and well-being.
            It provides essential services like food, shelter, healthcare, and education, which are often
            disrupted in these situations.
        """)

    with coli6:
        st.header("How to Contribute to Humanitarian Aid")
        st.write("""
            Donating money, volunteering, and raising awareness are three key ways to contribute to humanitarian aid.
            Contributing can be something small, such as buying an extra can of food to donate. Or something big,
            such as volunteering to go on site.
        """)
