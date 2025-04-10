# google.py

import nltk
nltk.download('vader_lexicon')
import pandas as pd
import requests
import streamlit as st
import json
from modules.agent import run_expert_agent  # Make sure this matches your file name
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from modules.charts import bar_chart, word_cloud_image

def app():
    st.title("Google Search Analysis")
    st.write("Welcome to the Google Search Data Analysis Page!")

    # Initialize session state
    if 'query' not in st.session_state:
        st.session_state['query'] = ""
    if 'serper_data' not in st.session_state:
        st.session_state['serper_data'] = None
    if 'expert_result' not in st.session_state:
        st.session_state['expert_result'] = None
    if 'sentiment_data' not in st.session_state:
        st.session_state['sentiment_data'] = None
    if 'word_cloud' not in st.session_state:
        st.session_state['word_cloud'] = ""

    # User Input: Search Query
    st.header("Search Query")
    query = st.text_input("Enter your search query:", value=st.session_state['query'])

    if st.button("Fetch Google Search Results"):
        if query.strip() == "":
            st.error("Please enter a valid search query.")
        else:
            with st.spinner("Fetching search results..."):
                results = fetch_serper_results(query)
                if results:
                    # Convert results to DataFrame
                    serper_df = parse_serper_results(results)
                    st.session_state['serper_data'] = serper_df
                    st.session_state['query'] = query

                    # Perform Sentiment Analysis on Snippets
                    sentiments = perform_sentiment_analysis(serper_df)
                    st.session_state['sentiment_data'] = sentiments

                    # Generate Word Cloud
                    combined_text = " ".join(serper_df['snippet'].dropna().tolist())
                    st.session_state['word_cloud'] = combined_text

                    # Clear out any old LLM result because we have new data
                    st.session_state['expert_result'] = None

                    st.success("Search results fetched and stored successfully!")


    # Display SERPER Data + Sentiment if present in session
    if st.session_state['serper_data'] is not None and st.session_state['sentiment_data'] is not None:
        st.header("Google Search Results Data with Sentiment")

        combined_df = pd.concat([
            st.session_state['serper_data'],
            st.session_state['sentiment_data']
        ], axis=1)

        combined_df['Sentiment'] = combined_df['compound'].apply(categorize_sentiment)
        combined_df['Sentiment Indicator'] = combined_df['Sentiment'].apply(get_sentiment_indicator)

        # Reorder columns
        combined_df = combined_df[['Sentiment Indicator', 'Sentiment', 'title', 'link', 'snippet']]
        combined_df.rename(columns={
            'snippet': 'Snippet',
            'title': 'Title',
            'link': 'Link'
        }, inplace=True)

        st.dataframe(combined_df)

    # Display Word Cloud if we have text
    if st.session_state.get('word_cloud'):
        st.header("Word Cloud of Article Snippets")
        word_cloud_image(st.session_state['word_cloud'])

    # LLM Agent Analysis: either show old results or allow new analysis
    st.header("LLM Agent Analysis")

    # If we already have an existing LLM result in session, show it:
    if st.session_state['expert_result'] is not None:
        st.write("### Previously Generated Analysis")
        # The run_expert_agent returns a dict with 'rendered_markdown' or other keys
        prev_result = st.session_state['expert_result']

        # If you stored raw HTML or markdown, display it here:
        if 'rendered_markdown' in prev_result:
            for block in prev_result['rendered_markdown']:
                st.markdown(block, unsafe_allow_html=True)
        else:
            # Fallback if you only have judge_content or expert_responses
            st.write(prev_result)

        # Optionally, let the user re-run the agent if they want:
        if st.button("Re-run LLM Agent with current data"):
            with st.spinner("Generating context and prediction..."):
                rerun_result = run_llm_analysis()
                if rerun_result:
                    st.session_state['expert_result'] = rerun_result
                    st.success("Analysis re-generated successfully!")
                    #st.stop()

    else:
        # If there's no existing result, check if we have any Serper data to analyze
        if st.session_state['serper_data'] is None:
            st.warning("Serper data not available. Please ensure data is loaded before proceeding.")
        else:
            # Show button to generate brand new LLM analysis
            if st.button("Generate Expert Context and Prediction"):
                with st.spinner("Generating context and prediction..."):
                    new_result = run_llm_analysis()
                    if new_result:
                        st.session_state['expert_result'] = new_result
                        st.success("New analysis generated successfully!")
                        #st.stop()


def run_llm_analysis():
    """ Helper function to call run_expert_agent with the current serper_data from session state. Returns the result dict."""
    serper_data_json = st.session_state['serper_data'].to_json(orient='records')
    try:
        result = run_expert_agent(
            acaps_data_json=None,
            serper_data_json=serper_data_json,
            start_date=None,  # Modify if you have date filters
            end_date=None
        )
        return result
    except Exception as e:
        st.error(f"Error running LLM agent: {e}")
        return None


def fetch_serper_results(query, num_results=10):
    """
    Fetches Google search results using the SERPER API.
    """
    serper_api_key = st.secrets["SERPER_API_KEY"]
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": num_results
    }
    response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching SERPER results: {response.status_code} - {response.text}")
        return None


def parse_serper_results(results):
    """
    Parses SERPER API results into a pandas DataFrame.
    """
    if "organic" not in results:
        st.error("No organic results found.")
        return pd.DataFrame()

    data = []
    for item in results["organic"]:
        data.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet", "")
        })
    df = pd.DataFrame(data)
    return df


def perform_sentiment_analysis(df):
    """
    Performs sentiment analysis on the article snippets.
    """
    sia = SentimentIntensityAnalyzer()
    sentiments = df['snippet'].apply(lambda x: sia.polarity_scores(x) if isinstance(x, str) else {})
    sentiment_df = pd.json_normalize(sentiments)
    return sentiment_df


def categorize_sentiment(compound_score):
    """
    Categorizes sentiment based on compound score.
    """
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


def get_sentiment_indicator(sentiment):
    """
    Returns a traffic light emoji based on sentiment.
    """
    if sentiment == 'Positive':
        return '🟢'
    elif sentiment == 'Negative':
        return '🔴'
    else:
        return '🟡'


def display_sentiment_analysis(sentiment_df):
    """
    Displays sentiment analysis results (example function).
    """
    if sentiment_df.empty:
        st.write("No sentiment data to display.")
        return

    st.subheader("Sentiment Scores")
    st.dataframe(sentiment_df)

    # Plotting Sentiment Distribution
    st.subheader("Sentiment Distribution")
    fig, ax = plt.subplots()
    sentiment_df[['neg', 'neu', 'pos']].plot(kind='hist', alpha=0.5, ax=ax, bins=20)
    plt.xlabel("Sentiment Score")
    plt.ylabel("Frequency")
    plt.title("Sentiment Distribution of Article Snippets")
    st.pyplot(fig)


if __name__ == "__main__":
    app()
