import streamlit as st

from application.dv1 import DV_1
from application.footer import Footer

dv1 = DV_1()

class BondTime():
    def __init__(self):
        self.st = st

    def run_app(self):
        self.frame()

        def footer(key):
            # st.subheader('Disclaimer and Notices')
            # self.data_disclaimer()
            Footer().data_disclaimer()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("Disclaimer and Notices", expanded=False)
        with my_expander:
            clicked = footer("second")

    def frame(self):
        # self.st.title('Analysis of Cook County Bond Data')
        # self.st.title('An Interactive Visualization by @justinhchae for Chicago Appleseed Center for Fair Courts')
        def header(key):
            st.subheader('About This Data')
            self.overview()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("About Bond Data Treemap in Cook County (Click to Expand)", expanded=False)
        with my_expander:
            clicked = header("first")

        self.data()

    def overview(self):
        #TODO: write narrative and overview
        st.write('Bond Time Overview: PENDING')

    def data(self):
        #TODO: create graphs in metrics
        st.write('Bond Time Data: PENDING')
        dv1.bond_timeseries()


