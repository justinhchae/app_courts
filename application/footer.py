import streamlit as st


class Footer():
    def __init__(self):
        pass

    def data_disclaimer(self):

        st.markdown(
            'All source code, data, and methodology available in a [GitHub Respository](https://github.com/justinhchae/app_courts/tree/main/data)')

        st.markdown(
            '_This site is under construction and active analysis._')

        st.markdown('[Cook County Data Source](https://datacatalog.cookcountyil.gov/browse?category=Courts)')
        
