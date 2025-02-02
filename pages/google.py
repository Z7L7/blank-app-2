# google_search.py

import pandas as pd
import requests
import streamlit as st
import json
from modules.charts import bar_chart, word_cloud_image
from modules.agent import run_expert_agent
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import matplotlib.pyplot as plt

# Ensure necessary NLTK resources are downloaded
nltk.download('vader_lexicon')

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

    # Display SERPER Data with Sentiment
    if st.session_state['serper_data'] is not None and st.session_state['sentiment_data'] is not None:
        st.header("Google Search Results Data with Sentiment")
        combined_df = pd.concat([st.session_state['serper_data'], st.session_state['sentiment_data']], axis=1)
        combined_df['Sentiment'] = combined_df['compound'].apply(categorize_sentiment)
        combined_df['Sentiment Indicator'] = combined_df['Sentiment'].apply(get_sentiment_indicator)
        # Reorder columns to move 'Sentiment Indicator' to the front
        combined_df = combined_df[['Sentiment Indicator', 'Sentiment', 'title', 'link', 'snippet']]
        # Rename columns for clarity
        combined_df.rename(columns={
            'snippet': 'Snippet',
            'title': 'Title',
            'link': 'Link'
        }, inplace=True)
        st.dataframe(combined_df)

    # Display Word Cloud
    if st.session_state.get('word_cloud'):
        st.header("Word Cloud of Article Snippets")
        word_cloud_image(st.session_state['word_cloud'])

    acaps_data_json = None

    # LLM Agent Analysis
    if st.session_state['serper_data'] is not None:
        st.header("LLM Agent Analysis")
        if st.button("Generate Expert Context and Prediction"):
            with st.spinner("Generating context and prediction..."):
                serper_data_json = st.session_state['serper_data'].to_json(orient='records')
                result = run_expert_agent(
                    acaps_data_json=None,
                    serper_data_json=serper_data_json,
                    start_date=None,  # Optional: Modify if you have date filters
                    end_date=None
                )
                st.session_state['expert_result'] = result


def fetch_serper_results(query, num_results=10):
    """
    Fetches Google search results using the SERPER API.

    Args:
        query (str): The search query.
        num_results (int): Number of search results to retrieve.

    Returns:
        dict: JSON response from SERPER API containing search results.
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

    Args:
        results (dict): JSON response from SERPER API.

    Returns:
        pd.DataFrame: DataFrame containing search results.
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

    Args:
        df (pd.DataFrame): DataFrame containing search results.

    Returns:
        pd.DataFrame: DataFrame with sentiment scores.
    """
    sia = SentimentIntensityAnalyzer()
    sentiments = df['snippet'].apply(lambda x: sia.polarity_scores(x) if isinstance(x, str) else {})
    sentiment_df = pd.json_normalize(sentiments)
    return sentiment_df

def categorize_sentiment(compound_score):
    """
    Categorizes sentiment based on compound score.

    Args:
        compound_score (float): Compound sentiment score.

    Returns:
        str: Sentiment category ('Negative', 'Neutral', 'Positive').
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

    Args:
        sentiment (str): Sentiment category.

    Returns:
        str: Emoji representing the sentiment.
    """
    if sentiment == 'Positive':
        return '🟢'
    elif sentiment == 'Negative':
        return '🔴'
    else:
        return '🟡'

def display_sentiment_analysis(sentiment_df):
    """
    Displays sentiment analysis results.

    Args:
        sentiment_df (pd.DataFrame): DataFrame containing sentiment scores.
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
