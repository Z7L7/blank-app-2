import streamlit as st

def app():
    st.title("Homepage")
    st.write("Welcome to the Humanitarian Aid Website!")

# - - - Columns with images - - -
col1, col2 = st.columns(2)

with col1:
    st.image("https://i.pinimg.com/474x/91/58/87/9158873487dc0d6fdad74b0dd1aed074.jpg", caption="")

with col2:
    st.header("What is Humanitarian Aid?")
    st.write("Humanitarian aid is an important subject to many across the world. It is defined as the assitance provided to those in need using both logistic and material assistance. There are many humanitarian aid organizations such as UNICEF and Doctors Without Boarders")

# - - - Text - - -
coli3, coli4 = st.columns(2)
with coli3:
    st.image("https://i.pinimg.com/474x/b8/19/79/b819799f9ab52866a70218fd23499519.jpg", caption="")

with coli4:
    st.image("https://i.pinimg.com/474x/93/1d/62/931d62501c149f08ec1643592081754e.jpg", caption="")
