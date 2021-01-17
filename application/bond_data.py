import streamlit as st

from application.dv1 import DV_1
from application.footer import Footer

dv1 = DV_1()

class BondData():
    def __init__(self):
        self.st = st

    def run_app(self):
        self.frame()
        self.footer()

    def header(self):
        def header_section(key):
            st.subheader('About This Data')
            self.overview()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("About Bond Data in Cook County (Click to Expand)", expanded=True)
        with my_expander:
            clicked = header_section("first")

    def frame(self):
        self.st.title('Analysis of Cook County Court Data')
        self.st.markdown('An Interactive Visualization by @justinhchae for Chicago Appleseed Center for Fair Courts')
        self.data()

    def overview(self):
        #TODO: write narrative and overview
        st.write('Based on Cook County Open Court Data, this page provides a count of bond types and amounts over the years.',
                 'Top - a Timeline of bond with recent legislative milestones. Bottom - A Treemap of bond types by race, and hearing type.')

    def data(self):
        self.header()
        st.plotly_chart(dv1.bond_timeseries())
        st.plotly_chart(dv1.bond_tree())
        dv1.bond_tree_header()

    def footer(self):
        def footer_section(key):
            # st.subheader('Disclaimer and Notices')
            # self.data_disclaimer()
            Footer().data_disclaimer()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("Disclaimer and Notices", expanded=False)
        with my_expander:
            clicked = footer_section("second")



