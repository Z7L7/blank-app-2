import streamlit as st
import pandas as pd
import numpy as np
from modules.actors import crisis_cameo_codes, country_code
from modules.charts import time_series_chart, bar_chart, word_cloud_image
from datetime import datetime
import requests
import time

def app():
    st.title("Full Analysis Page")
    st.write("Welcome to the Humanitarian Aid Website!")

    # Example DataFrame (replace with real data)
    # data = {
    #     'date': pd.date_range("2023-01-01", periods=10, freq='D'),
    #     'article_count': np.random.randint(5, 50, 10),
    #     'source': ["ReliefWeb"]*5 + ["ACAPS"]*5,
    #     'text_data': [
    #         "Relief text example one example one example",
    #         "Relief text example two example two example",
    #         "Relief text example three example three",
    #         "Relief text four example",
    #         "Relief text five example",
    #         "ACAPS text example one example",
    #         "ACAPS text example two example",
    #         "ACAPS text example three example",
    #         "ACAPS text four example",
    #         "ACAPS text five example"
    #     ]
    # }
    # df = pd.DataFrame(data)

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

    # Time-series chart
    # st.subheader("Time-Series of Articles")
    # time_series_chart(df, 'date', 'article_count')

