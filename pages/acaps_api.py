import pandas as pd
import requests
from datetime import datetime
import time
import streamlit as st
import numpy as np
import pickle
from modules.actors import crisis_cameo_codes, country_code
from modules.charts import time_series_chart, bar_chart, word_cloud_image
from modules.agent import run_expert_agent
import json
import networkx as nx
import matplotlib.pyplot as plt

def app():
    st.title("Acaps")
    st.write("Welcome to the ACAPS Data Analysis Page")

    # Get the list of countries and keywords
    countries = sorted(country_code.keys())
    keywords = sorted(crisis_cameo_codes.keys())

    # Initialize session state for ACAPS data if not exists
    if 'acaps_data' not in st.session_state:
        st.session_state['acaps_data'] = None
    if 'acaps_expert_result' not in st.session_state:
        st.session_state['acaps_expert_result'] = None
    if 'last_fetched_country' not in st.session_state:
        st.session_state['last_fetched_country'] = None

    # Display current selections from sidebar
    current_country = st.session_state.get('global_country', countries[0])
    current_keyword = st.session_state.get('global_keyword', keywords[0])

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Current Country:** {current_country}")
    with col2:
        st.write(f"**Current Keyword:** {current_keyword}")

    # Add Fetch Data button
    if st.button("Fetch ACAPS Data"):
        with st.spinner(f"Fetching data for {current_country}..."):
            credentials = {
                "username": "asiyah.adetunji.workplace@gmail.com",
                "password": "sPAcA317&2"
            }
            auth_token_response = requests.post("https://api.acaps.org/api/v1/token-auth/", credentials)
            auth_token = auth_token_response.json()['token']

            df = pd.DataFrame()
            request_url = f"https://api.acaps.org/api/v1/risk-list/?country={current_country}"
            last_request_time = datetime.now()

            while True:
                while (datetime.now() - last_request_time).total_seconds() < 1:
                    time.sleep(0.1)
                response = requests.get(request_url, headers={"Authorization": f"Token {auth_token}"})
                last_request_time = datetime.now()
                response_json = response.json()
                print(response_json)

                df = pd.concat([df, pd.DataFrame(response_json["results"])])

                if response_json.get("next"):
                    request_url = response_json["next"]
                else:
                    break

            st.session_state['acaps_data'] = df
            st.session_state['last_fetched_country'] = current_country
            st.success("Data fetched successfully!")

    # Only show the rest if we have data
    if st.session_state['acaps_data'] is not None:
        df = st.session_state['acaps_data']

        # - - - Front End - - -
        st.header("Data")
        st.dataframe(df)
        url = "https://www.acaps.org/en/"
        st.write(f"This is the Risk List dataset from [ACAPS.org]({url}) a nonprofit, nongovernmental website.")

        df2 = df[df['rationale'] != '[-]']
        with st.expander("View Rationale"):
            if not df2.empty:
                for idx, row in df2.iterrows():
                    st.markdown(f"**Entry {idx+1}:**")
                    st.markdown(row['rationale'])
                    st.markdown("---")
            else:
                st.write("No rationale available.")

        # st.header("Analysis")
        # st.subheader("Sources Comparison")
        # bar_chart(df, 'impact', 'risk_type')

        st.subheader("Word Clouds by Source")
        sources = df['risk_type'].unique()
        for i in range(0, len(sources), 2):
            row_sources = sources[i:i+2]
            columns = st.columns(len(row_sources))
            for idx, source in enumerate(row_sources):
                with columns[idx]:
                    st.write(f"**{source}**")
                    subset = df[df['risk_type'] == source]
                    combined_text = " ".join(subset['rationale'].tolist())
                    word_cloud_image(combined_text, max_width=400, max_height=300)

        # --------------- Knowledge Graph Section ---------------
        st.header("Knowledge Graph")

        # --- 1) Build a graph from Country -> Risk Types, plus cameo-code keywords from rationale ---
        def parse_cameo_codes(text, cameo_dict):
            found_codes = []
            text_lower = text.lower()
            for cameo_keyword in cameo_dict:
                if cameo_keyword.lower() in text_lower:
                    found_codes.append(cameo_keyword)
            return found_codes

        G = nx.Graph()
        G.add_node(current_country)  # The main country node

        risk_counts = df['risk_type'].value_counts().to_dict()
        max_count = max(risk_counts.values()) if risk_counts else 1

        cameo_counts = {}
        cameo_counts_by_risk = {}

        for idx, row in df.iterrows():
            risk = row['risk_type']
            rationale_text = str(row.get('rationale', ''))
            cameo_found = parse_cameo_codes(rationale_text, crisis_cameo_codes)

            if risk not in cameo_counts_by_risk:
                cameo_counts_by_risk[risk] = {}

            for code in cameo_found:
                cameo_counts[code] = cameo_counts.get(code, 0) + 1
                cameo_counts_by_risk[risk][code] = cameo_counts_by_risk[risk].get(code, 0) + 1

        for risk, count in risk_counts.items():
            if not G.has_node(risk):
                G.add_node(risk)
            G.add_edge(current_country, risk, weight=count)

        for risk, cameo_dict in cameo_counts_by_risk.items():
            for code, freq in cameo_dict.items():
                if not G.has_node(code):
                    G.add_node(code)
                G.add_edge(risk, code, weight=freq)

        # --- 2) Color and size nodes ---
        node_colors = {}
        node_sizes = {}

        node_colors[current_country] = 'red'
        node_sizes[current_country] = 3000

        for r, rc in risk_counts.items():
            node_colors[r] = 'blue'
            node_sizes[r] = 1000 + 300 * (rc / max_count)

        cameo_max = max(cameo_counts.values()) if cameo_counts else 1
        for code, cc in cameo_counts.items():
            node_colors[code] = 'green'
            node_sizes[code] = 500 + 300 * (cc / cameo_max)

        # --- 3) Draw the graph ---
        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42, k=0.5)

        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=[node_sizes[n] for n in G.nodes()],
            node_color=[node_colors[n] for n in G.nodes()],
            alpha=0.8,
            ax=ax
        )

        edges = G.edges(data=True)
        nx.draw_networkx_edges(
            G, pos,
            edgelist=edges,
            width=[d['weight'] for (_, _, d) in edges],
            alpha=0.6,
            ax=ax
        )

        for node, (x, y) in pos.items():
            ax.text(x + 0.02, y, s=node, color='black', fontsize=9, fontweight='bold')

        ax.axis('off')
        st.pyplot(fig)

        # --------------- LLM Agent Analysis ---------------
        st.header("LLM Agent Analysis")
        acaps_data_json = df.to_json(orient='records')

        if st.button("Generate Expert Context and Prediction"):
            with st.spinner("Generating context and prediction..."):
                result = run_expert_agent(acaps_data_json)
                st.session_state['acaps_expert_result'] = result
                if isinstance(result, dict):
                    result = json.dumps(result, indent=2)
                st.text_area("Expert Analysis", value=result, height=300)