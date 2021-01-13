import streamlit as st


class Footer():
    def __init__(self):
        pass

    def data_disclaimer(self):

        st.markdown(
            'All source code, and cleaned data available in a [GitHub Respository](https://github.com/justinhchae/app_courts/tree/main/data)')

        st.markdown(
            '_This site is under construction and active analysis._')
        # self.st.write('This site is under construction and active analysis. Please stop by again for future updates!')
        st.markdown('[Cook County Data Source](https://datacatalog.cookcountyil.gov/browse?category=Courts)')
        st.markdown(
            '"This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago.  The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site.  The data provided at this site is subject to change at any time.  It is understood that the data provided at this site is being used at one’s own risk."')
