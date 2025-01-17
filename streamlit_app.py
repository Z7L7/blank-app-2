import streamlit as st

st.title("Humanitarian Aid")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

homepage = st.Page(
    page="views/homepage.py",
    title="Homepage",
    icon=":material/home:",
    default=True,
)

data = st.Page(
    page="views/acaps_api.py",
    title="All Data",
    icon=":material/laptop_mac:",
)

gdlt = st.Page(
    page="views/gdlt.py",
    title="News",
    icon=":material/laptop_mac:",
)
# project_1_page = st.Page(
#     page="views/chatbot.py",
#     title="Chatbot",
#     icon=":material/laptop_mac:",
# )

# syria = st.Page(
#     page="views/syria.py",
#     title="Syria",
#     icon=":material/laptop_mac:",
# )

# yemen = st.Page(
#     page="views/yemen.py",
#     title="Yemen",
#     icon=":material/laptop_mac:",
# )



# - - - Navigation Setup [WITHOUT SECTIONS] - - -
# pg = st.navigation(pages=[homepage, project_1_page])

# - - - Navigation Setup [WITH SECTIONS] - - -
pg = st.navigation(
    {
        "Info": [homepage],
        "Projects": [data, gdlt],
    }
)

# - - - Shared on All Pages - - -
st.sidebar.text("Humanitarian Aid Website By: \n Asiyah Adetunji")

# - - - Run Navigation - - -
pg.run()