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

    def about(self):
        def expander(key):
            st.subheader('About This Data')
            self.overview()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("About Bond Data in Cook County (Click to Expand)", expanded=True)
        with my_expander:
            clicked = expander("first")

    def frame(self):
        st.markdown("<h2 style='text-align: center; color: black;'> * * * </h2>", unsafe_allow_html=True)
        self.st.title('A Visual Brief on Bond in Chicagoland')
        self.data()

    def overview(self):
        st.write('Based on Cook County Open Court Data, this page provides a count of bond types and amounts over the years.',
                 'Top - a Timeline of bond with recent legislative milestones. Total monthly bond amounts are indicated by line height on the y-axis.',
                 'The size of each dot represents a dollar total of bond dollars in a given month.',
                 'Bottom - A Treemap of bond types by race, and hearing type.')

        st.markdown('[Chicago Appleseed Center for Fair Courts](http://www.chicagoappleseed.org/)')

    # @st.cache(max_entries=10, ttl=3600, hash_funcs={dict: lambda _: None})
    # def cache_fig(self):
    #     afig = dv1.bond_timeseries()
    #     cached_dict = {'bond_timeseries': afig}
    #     return cached_dict

    def data(self):
        self.narrative_time()
        st.plotly_chart(dv1.bond_timeseries())
        st.markdown("<h2 style='text-align: center; color: black;'> * * * </h2>", unsafe_allow_html=True)
        self.about()
        self.narrative_tree()
        st.plotly_chart(dv1.bond_tree())
        dv1.bond_tree_header()

    def narrative_time(self):
        self.st.markdown(
            '_Over the years, how big has bond been in Cook County?_')
        self.st.markdown(
            '_This timeline displays monthly bond amounts by bond type._')

    def narrative_tree(self):
        st.markdown("<h2 style='text-align: center; color: black;'> * * * </h2>", unsafe_allow_html=True)
        self.st.markdown(
            '_Where did bond dollars come from? How much money and for what types of court events?_')
        self.st.markdown(
            '_This treemap displays the relative proportion of bond amounts paid by race and court event with filters for time_')

    def footer(self):
        def expander(key):
            # st.subheader('Disclaimer and Notices')
            # self.data_disclaimer()
            Footer().data_disclaimer()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("Disclaimer and Notices", expanded=False)
        with my_expander:
            clicked = expander("second")



