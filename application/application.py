import streamlit as st

from application.bond_tree import BondTree
from application.bond_time import BondTime
from application.footer import Footer
from application.featured import Featured
from application.ov1 import OV_1


class Application():
    def __init__(self):
        self.st = st
        self.sidebar_picklist = ['Featured: COVID Cliff','Bond Treemap', 'Bond Timeseries']
        self.sidebar_selection = self.st.sidebar.selectbox('Select Analysis', self.sidebar_picklist)

        """
        https://discuss.streamlit.io/t/how-to-render-chart-faster/6237
        https://discuss.streamlit.io/t/this-app-has-gone-over-its-resource-limits/7334/4
        """

    def run_app(self):
        self.frame()

    def frame(self):
        self.st.title('Analysis of Cook County Court Data')
        self.st.markdown('Interactive Visualization by @justinhchae for Chicago Appleseed Center for Fair Courts')

        self.header()
        self.menu_options()
        self.footer()

    def header(self):
        def expander(key):
            st.subheader('About This Data')
            self.overview()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("Data Overview (Click to Expand)", expanded=False)
        with my_expander:
            clicked = expander("first")

    def overview(self):

        self.st.markdown('**Data Overview**')
        self.st.markdown('**Initiation - Disposition - Sentencing**')

        self.st.write(
            'The court system is comprised of at least five phases that include Intake, Initiation, Dispositions, Sentencing, Diversions.',
            'Out of the five phases, this dashboard currently processes Initiation, Disposition, and Sentencing phases.',
            )

        year = self.st.select_slider('Slide to Filter data by Year', options=['All Time', 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011])
        self.st.plotly_chart(OV_1().court_counts(year))

    def menu_options(self):
        if self.sidebar_selection == 'Bond Treemap':
            BondTree().data()

        if self.sidebar_selection == 'Featured: COVID Cliff':
            self.st.write('')
            Featured().narrative()

        if self.sidebar_selection == 'Bond Timeseries':
            BondTime().data()

        #TODO
        # if self.sidebar_selection == 'Electronic Monitoring':
        #     pass

    def footer(self):
        def footer(key):
            Footer().data_disclaimer()

        my_expander = st.beta_expander("Disclaimer and Notices", expanded=False)
        with my_expander:
            clicked = footer("second")
