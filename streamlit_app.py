import streamlit as st

def main():
    # Sidebar for Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Homepage", "Acaps", "GDELT", "Relief Web", "Analysis", "Fewsnet", "Google"])

    # Navigation logic
    if page == "Homepage":
        from pages import homepage
        homepage.app()

    elif page == "Acaps":
        from pages import acaps_api
        acaps_api.app()

    elif page == "GDELT":
        from pages import gdelt
        gdelt.app()
    
    elif page == "Relief Web":
        from pages import news
        news.app()

    elif page == "Fewsnet":
        from pages import fewsnet
        fewsnet.app()

    elif page == "Google":
        from pages import google
        google.app()

    elif page == "Analysis":
        from pages import analysis
        analysis.app()




    # Footer
    st.sidebar.text("Humanitarian Aid Website By:\nAsiyah Adetunji")

if __name__ == "__main__":
    main()