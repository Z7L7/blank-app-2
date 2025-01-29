import streamlit as st
import pandas as pd
import numpy as np
from modules.actors import crisis_cameo_codes, country_code
from modules.charts import time_series_chart, bar_chart, word_cloud_image

def app():
    st.title("GDELT Data Viewer")
    st.write("Welcome to the Humanitarian Aid Website!")

    # Example DataFrame (replace with real data)
    data = {
        'date': pd.date_range("2023-01-01", periods=10, freq='D'),
        'article_count': np.random.randint(5, 50, 10),
        'source': ["ReliefWeb"]*5 + ["ACAPS"]*5,
        'text_data': [
            "Relief text example one example one example",
            "Relief text example two example two example",
            "Relief text example three example three",
            "Relief text four example",
            "Relief text five example",
            "ACAPS text example one example",
            "ACAPS text example two example",
            "ACAPS text example three example",
            "ACAPS text four example",
            "ACAPS text five example"
        ]
    }
    df = pd.DataFrame(data)

    # Time-series chart
    st.subheader("Time-Series of Articles")
    time_series_chart(df, 'date', 'article_count')

    # Bar chart
    st.subheader("Sources Comparison")
    bar_chart(df, 'source', 'article_count')

    # Word cloud by source (side by side)
    st.subheader("Word Clouds by Source")
    sources = df['source'].unique()

    # Display two word clouds per row
    for i in range(0, len(sources), 2):
        row_sources = sources[i:i+2]
        columns = st.columns(len(row_sources))
        for idx, source in enumerate(row_sources):
            with columns[idx]:
                st.write(f"**{source}**")
                subset = df[df['source'] == source]
                combined_text = " ".join(subset['text_data'].tolist())
                word_cloud_image(combined_text, max_width=400, max_height=300)
