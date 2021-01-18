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
        def expander(key):
            st.subheader('About This Data')
            self.overview()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("About Bond Data in Cook County (Click to Expand)", expanded=True)
        with my_expander:
            clicked = expander("first")

    def frame(self):
        self.st.title('A Visual Brief on Bond in Chicagoland')
        self.data()

    def overview(self):
        st.write('Based on Cook County Open Court Data, this page provides a count of bond types and amounts over the years.',
                 'Top - a Timeline of bond with recent legislative milestones. Monthly bond volumes are indicated by line height on the y-axis.',
                 'The size of each dot represents a dollar total of bond dollars in a given month.',
                 'Bottom - A Treemap of bond types by race, and hearing type.')

        st.markdown('[Chicago Appleseed Center for Fair Courts](http://www.chicagoappleseed.org/)')

    # @st.cache(max_entries=10, ttl=3600, hash_funcs={dict: lambda _: None})
    # def cache_fig(self):
    #     afig = dv1.bond_timeseries()
    #     cached_dict = {'bond_timeseries': afig}
    #     return cached_dict

    def data(self):
        self.header()
        st.plotly_chart(dv1.bond_timeseries())
        st.plotly_chart(dv1.bond_tree())
        dv1.bond_tree_header()

    def footer(self):
        def expander(key):
            # st.subheader('Disclaimer and Notices')
            # self.data_disclaimer()
            Footer().data_disclaimer()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("Disclaimer and Notices", expanded=False)
        with my_expander:
            clicked = expander("second")



