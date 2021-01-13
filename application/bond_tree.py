import streamlit as st

from application.dv1 import DV_1
from application.footer import Footer
from do_data.getter import Reader

dv1 = DV_1()

class BondTree():
    def __init__(self):
        self.st = st

        """ References
        https://discuss.streamlit.io/t/how-to-render-chart-faster/6237
        https://discuss.streamlit.io/t/this-app-has-gone-over-its-resource-limits/7334/4
        """

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

        self.bond_data()

    def overview(self):
        self.st.write(
            'In this bond data tree map, the size of the box indicates the relative percentage of each category.',
            'For example, for all Initiation events where a bond is granted, the tree map breaks down charges by race, hearing type, and bond type.',
            'Bigger boxes indiciate more counts of that combination of data and red colors indicate higher dollar amounts.')

        self.st.write('An Interactive Visualization by @justinhchae for Chicago Appleseed Center for Fair Courts')

    def bond_data(self):

        year = self.slider_year()
        self.st.plotly_chart(dv1.bond_tree(year))

    def slider_year(self):
        return self.st.select_slider('Slide to Filter data by Year',
                                     options=['All Time', 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012,
                                              2011],
                                     key='bond_slider')
