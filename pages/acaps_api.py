import pandas as pd
import requests
from datetime import datetime
import time
import streamlit as st
import numpy as np
import pickle
from modules.actors import crisis_cameo_codes, country_code  # Import dictionaries correctly
from modules.charts import time_series_chart, bar_chart, word_cloud_image
from modules.agent import run_expert_agent
import json

def app():
    st.title("Acaps")
    st.write("Welcome to the Humanitarian Aid Website!")

    # Get the list of countries and keywords
    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())

    # Use session state to persist country, keyword, and fetched data
    if 'country' not in st.session_state:
        st.session_state['country'] = countries[0]  # Default to the first country

    if 'keyword' not in st.session_state:
        st.session_state['keyword'] = keywords[0]  # Default to the first keyword

    if 'acaps_data' not in st.session_state:
        st.session_state['acaps_data'] = None  # Initialize ACAPS data as None

    if 'acaps_expert_result' not in st.session_state:
        st.session_state['acaps_expert_result'] = None  # Initialize LLM Expert as None

    # Dropdown for countries
    country = st.selectbox("Select a Country", countries, index=countries.index(st.session_state['country']))

    # Dropdown for keywords (if needed)
    # keyword = st.selectbox("Select a Keyword", keywords, index=keywords.index(st.session_state['keyword']))

    # Update session state with the new selections
    st.session_state['country'] = country
    # st.session_state['keyword'] = keyword  # Uncomment if you want to use the keyword

    # Fetch ACAPS data only if the country changes or data is not already fetched
    if st.session_state['acaps_data'] is None or st.session_state['country'] != country:
        # Post credentials to get an authentication token
        credentials = {
            "username": "asiyah.adetunji.workplace@gmail.com",  # Replace with your email address
            "password": "sPAcA317&2"  # Replace with your password
        }
        auth_token_response = requests.post("https://api.acaps.org/api/v1/token-auth/", credentials)
        auth_token = auth_token_response.json()['token']

        # Pull data from ACAPS API, loop through the pages, and append to a pandas DataFrame
        df = pd.DataFrame()
        request_url = ("https://api.acaps.org/api/v1/risk-list/?country=%s" % st.session_state['country'])  # Use session state for country
        last_request_time = datetime.now()
        while True:
            # Wait to avoid throttling
            while (datetime.now() - last_request_time).total_seconds() < 1:
                time.sleep(0.1)

            # Make the request
            response = requests.get(request_url, headers={"Authorization": "Token %s" % auth_token})
            last_request_time = datetime.now()
            response = response.json()
            print(response)

            # Append to a pandas DataFrame
            df = df._append(pd.DataFrame(response["results"]))

            # Loop to the next page; if we are on the last page, break the loop
            if ("next" in response.keys()) and (response["next"] is not None):
                request_url = response["next"]
            else:
                break

        # Store the fetched data in session state
        st.session_state['acaps_data'] = df

    # Use the fetched data from session state
    df = st.session_state['acaps_data']

    # - - - Front End - - -
    st.header("Data")
    st.dataframe(df)
    url = "https://www.acaps.org/en/"
    st.write("This is the Risk List dataset from [ACAPS.org](%s) a nonprofit, nongovernmental website." % url)

    container = st.container(border=True)
    df2 = df[df['rationale'] != '[-]']
    container.header("Rationale")
    container.write(df2.to_string(columns=['rationale'], header=True, index=True))

    st.header("Analysis")

     # Bar chart
    st.subheader("Sources Comparison")
    bar_chart(df, 'country', 'intensity')

    # Word cloud by source (side by side)
    st.subheader("Word Clouds by Source")
    sources = df['risk_type'].unique()

    # Display two word clouds per row
    for i in range(0, len(sources), 2):
        row_sources = sources[i:i+2]
        columns = st.columns(len(row_sources))
        for idx, source in enumerate(row_sources):
            with columns[idx]:
                st.write(f"**{source}**")
                subset = df[df['risk_type'] == source]
                combined_text = " ".join(subset['rationale'].tolist())
                word_cloud_image(combined_text, max_width=400, max_height=300)

    st.header("LLM Agent Analysis")

    # If we have all required data, show the "Generate Expert Context and Prediction" button
    if ('acaps_data' in st.session_state and country and keywords):

        acaps_data_json = st.session_state['acaps_data'].to_json(orient='records')
        # serper_query = f"{country} {keywords} crisis after:{start_date.strftime('%Y-%m-%d')} before:{end_date.strftime('%Y-%m-%d')}"

        if st.button("Generate Expert Context and Prediction"):
            with st.spinner("Generating context and prediction..."):
                result = run_expert_agent(
                    acaps_data_json,
                    # serper_query,
                    # start_date.strftime("%Y-%m-%d"),  # Convert start_date to string format
                    # end_date.strftime("%Y-%m-%d")     # Convert end_date to string format
                )
                st.session_state['acaps_expert_result'] = result

                # Ensure result is a string
                if isinstance(result, dict):
                    result = json.dumps(result)







    