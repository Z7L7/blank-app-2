import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def time_series_chart(df, date_col, value_col):
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(x=date_col, y=value_col)
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

def bar_chart(df, category_col, value_col):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(x=category_col, y=value_col)
        .properties(width='container')
    )
    st.altair_chart(chart, use_container_width=True)

def word_cloud_image(text_data, max_width=400, max_height=300):
    wordcloud = WordCloud(background_color="white", width=800, height=400).generate(text_data)
    fig, ax = plt.subplots(figsize=(max_width/100, max_height/100))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)