import streamlit as st

def main():
    # Sidebar for Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Homepage", "All Data", "News"])

    # Navigation logic
    if page == "Homepage":
        from pages import homepage
        homepage.app()

    elif page == "All Data":
        from pages import acaps_api
        acaps_api.app()

    elif page == "News":
        from pages import gdlt
        gdlt.app()

    # Footer
    st.sidebar.text("Humanitarian Aid Website By:\nAsiyah Adetunji")

if __name__ == "__main__":
    main()