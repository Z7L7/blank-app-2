import streamlit as st
from modules.actors import gdelt_wrapper, crisis_cameo_codes, country_code  # Import dictionaries correctly

def app():
    st.title("Fews Net")
    st.write("Welcome to the Humanitarian Aid Website!")
