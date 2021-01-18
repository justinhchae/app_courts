import streamlit as st

from application.bond_data import BondData
from application.footer import Footer
from application.featured import Featured
from application.ov1 import OV_1
from application.dv1 import DV_1

class Application():
    def __init__(self):
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
        if self.sidebar_selection == 'Sentencing Data':
            self.st.write('')
            self.st.plotly_chart(DV_1().sentencing_network())
            self.st.markdown('_What does the court system look like? As a network of judges, courts, and sentencing decisions, one way to visualize the courts is as a network graph._')
            self.st.markdown('_This network graph depicts the path of a case starting with a judge (gray circles), the sentencing type (lines), the associated courts (large nodes) and outcomes (squares)._')
            self.st.markdown('_Larger icons indicate higher percentage of cases and bolder lines indicate longer sentences as measured by commitment days._')

        if self.sidebar_selection == 'Bond Data':
            BondData().frame()

        if self.sidebar_selection == 'Court Volume':
            self.st.write('')
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
