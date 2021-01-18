import streamlit as st

from application.dv1 import DV_1
from application.footer import Footer

dv1 = DV_1()

class SentencingData():
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

        my_expander = st.beta_expander("About Sentencing Data in Cook County", expanded=True)
        with my_expander:
            clicked = expander("first")

    def frame(self):
        st.markdown("<h2 style='text-align: center; color: black;'> * * * </h2>", unsafe_allow_html=True)
        self.st.title('The Court System as a Network')
        self.filters()
        self.data()
        self.about()

    def overview(self):
        self.st.markdown(
            '_What does the court system look like? As a network of judges, courts, and sentencing decisions, one way to visualize the courts is as a network graph._')
        self.st.markdown(
            '_This network graph depicts the path of a case starting with a judge (gray circles), the sentencing type (lines), the associated courts (large nodes) and outcomes (squares)._')
        self.st.markdown(
            '_Larger icons indicate higher percentage of cases and bolder lines indicate longer sentences as measured by commitment days._')

        st.markdown('[Chicago Appleseed Center for Fair Courts](http://www.chicagoappleseed.org/)')

    def data(self):
        st.plotly_chart(dv1.sentencing_network(disp_edges=self.disp_edges, disp_nodes=self.disp_nodes))

    def filters(self):

        def options():
            col1, col2 = st.beta_columns(2)
            with col1:
                self.disp_nodes = st.checkbox('Display Nodes', value=True, key='1')
            with col2:
                self.disp_edges = st.checkbox('Display Edges', value=True, key='2')

        def expander(key):
            options()

        my_expander = st.beta_expander("Filter Data", expanded=False)
        with my_expander:
            clicked = expander("filter")

    def footer(self):
        def expander(key):
            Footer().data_disclaimer()

        my_expander = st.beta_expander("Disclaimer and Notices", expanded=False)
        with my_expander:
            clicked = expander("second")



