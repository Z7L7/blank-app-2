import streamlit as st

def main():
    # Sidebar for Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Homepage", "Acaps", "GDELT"])

    # Navigation logic
    if page == "Homepage":
        from pages import homepage
        homepage.app()

    elif page == "Acaps":
        from pages import acaps_api
        acaps_api.app()

    elif page == "GDELT":
        from pages import gdlt
        gdlt.app()

    # Footer
    st.sidebar.text("Humanitarian Aid Website By:\nAsiyah Adetunji")

if __name__ == "__main__":
    main()