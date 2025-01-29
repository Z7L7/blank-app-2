import pandas as pd
import requests
from datetime import datetime
import time
import streamlit as st
import numpy as np
import pickle
from modules.actors import crisis_cameo_codes, country_code  # Import dictionaries correctly

def app():

    st.title("GDELT Data Viewer")
    st.write("Welcome to the Humanitarian Aid Website!")

    countries = sorted(country_code.keys())
    #keywords = sorted(crisis_cameo_codes.keys())

    # Dropdown for countries
    country = st.selectbox("Select a Country", countries)

    credentials = {
        "username": "asiyah.adetunji.workplace@gmail.com", # Replace with your email address
        "password": "sPAcA317&2" # Replace with your password
    }
    auth_token_response = requests.post("https://api.acaps.org/api/v1/token-auth/", credentials)
    auth_token = auth_token_response.json()['token']

    # Pull data from ACAPS API, loop through the pages, and append to a pandas DataFrame
    df = pd.DataFrame()
    request_url = ("https://api.acaps.org/api/v1/risk-list/?country=") # Replace with the URL of the dataset you want to access
    last_request_time = datetime.now()
    while True:

        # Wait to avoid throttling
        while (datetime.now()-last_request_time).total_seconds() < 1:
            time.sleep(0.1)

        # Make the request
        response = requests.get(request_url, headers={"Authorization": "Token %s" % auth_token})
        last_request_time = datetime.now()
        response = response.json()
        print(response)

        # Append to a pandas DataFrame
        df = df._append(pd.DataFrame(response["results"]))

        # Loop to the next page; if we are on the last page, break the loop
        if ("next" in response.keys()) and (response["next"] != None):
            request_url = response["next"]
        else: break

    # st.dataframe(df) 
    with st.expander('Data'):
        st.write("Raw data")
        st.dataframe(df)

        st.write("X Variables")
        X = df.drop(columns="risk_level", axis=1)
        st.dataframe(X)

        st.write("Y Variables")
        y = df.risk_level
        st.dataframe(y)

        rows = {

        }

    # Graphs
    with st.expander('Data Visualiser'):
        st.bar_chart(data=df, x="risk_level", y="risk_type", color="impact")

    # # Data preferation
    # with st.sidebar:
    #     st.header('Input Features')
    #     count = st.selectbox('country', ('Syria','Chad'))
    #     geolevel = st.selectbox('geographic_level', ('Regional','Subnational', 'National'))

