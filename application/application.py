import streamlit as st

from application.bond_data import BondData
from application.sentencing_data import SentencingData
from application.footer import Footer
from application.featured import Featured
from application.ov1 import OV_1
from application.dv1 import DV_1

class Application():
    def __init__(self):
        st.set_page_config(page_title='Fair Courts')
        self.st = st
        self.sidebar_picklist = ['Sentencing Data', 'Court Volume','Bond Data']
        self.sidebar_selection = self.st.sidebar.selectbox('Select Analysis', self.sidebar_picklist)

        """
        https://discuss.streamlit.io/t/how-to-render-chart-faster/6237
        https://discuss.streamlit.io/t/this-app-has-gone-over-its-resource-limits/7334/4
        """

    def run_app(self):
        self.frame()

    def frame(self):
        self.st.title('Analysis of Cook County Court Data')
        self.st.markdown('An Interactive Visualization by @justinhchae for [Chicago Appleseed Center for Fair Courts](http://www.chicagoappleseed.org/)')

        self.header()
        self.menu_options()
        st.markdown("<h2 style='text-align: center; color: black;'> * * * </h2>", unsafe_allow_html=True)
        self.footer()

    def header(self):
        def expander(key):
            st.subheader('About This Data')
            self.overview()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("Data Overview", expanded=False)
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
        if self.sidebar_selection == 'Sentencing Data':
            SentencingData().frame()

        if self.sidebar_selection == 'Bond Data':
            BondData().frame()

        if self.sidebar_selection == 'Court Volume':
            Featured().narrative()

        #TODO
        # if self.sidebar_selection == 'Electronic Monitoring':
        #     pass

    def footer(self):
        def expander(key):
            Footer().data_disclaimer()

        my_expander = st.beta_expander("Disclaimer and Notices", expanded=False)
        with my_expander:
            clicked = expander("second")
