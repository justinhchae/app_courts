import streamlit as st

from application.dv1 import DV_1
from do_data.getter import Reader

dv1 = DV_1()

class BondApp():
    def __init__(self):
        self.st = st

        """ References
        https://discuss.streamlit.io/t/how-to-render-chart-faster/6237
        https://discuss.streamlit.io/t/this-app-has-gone-over-its-resource-limits/7334/4
        """

    def run_app(self):
        self.frame()
        self.data_disclaimer()

    def frame(self):
        self.st.title('Analysis of Cook County Bond Data')
        self.st.markdown('An Interactive Visualization by @justinhchae for Chicago Appleseed')
        self.bond_data()

    def bond_data(self):

        self.st.markdown('**Bond Data Tree Map**')
        self.st.write(
            'In this bond data tree map, the size of the box indicates the relative percentage of each category.',
            'For example, for all Initiation events where a bond is granted, the tree map breaks down charges by race, hearing type, and bond type.',
            'Bigger boxes indiciate more counts of that combination of data and red colors indicate higher dollar amounts.')

        year = self.st.select_slider('Slide to Filter data by Year',
                                     options=['All Time', 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012,
                                              2011],
                                     key='bond_slider')

        self.st.write('Bond Data for', str(year))
        self.st.plotly_chart(dv1.bond_tree(year))

    def data_disclaimer(self):
        self.st.markdown('**Disclaimer and Notices**')
        self.st.markdown(
            'All source code, and cleaned data available in a [GitHub Respository](https://github.com/justinhchae/app_courts/tree/main/data)')

        self.st.markdown(
            '_This site is under construction and active analysis. Please stop by again for future updates!_')
        # self.st.write('This site is under construction and active analysis. Please stop by again for future updates!')
        self.st.markdown('[Cook County Data Source](https://datacatalog.cookcountyil.gov/browse?category=Courts)')
        self.st.markdown(
            '"This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago.  The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site.  The data provided at this site is subject to change at any time.  It is understood that the data provided at this site is being used at one’s own risk."')
