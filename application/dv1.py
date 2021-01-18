import streamlit as st

from analyze_data.metrics import Metrics
from do_data.getter import Reader

class DV_1():
    def __init__(self):
        pass

    def bond_tree(self):
        year = st.select_slider('Slide to Filter data by Year',
                                     options=['All Time', 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011],
                                key='bond_treemap_slider'
                                )

        return Metrics().dv1_bond(year)

    def bond_tree_overview(self):
        st.write(
            'In this bond data tree map, the size of the box indicates the relative percentage of each category.',
            'For example, for all Initiation events where a bond is granted, the tree map breaks down charges by race, hearing type, and bond type.',
            'Bigger boxes indiciate more counts of that combination of data and red colors indicate higher dollar amounts.')

    def bond_tree_header(self):
        def expander(key):
            st.subheader('About This Data')
            self.bond_tree_overview()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("About Bond Data Treemap in Cook County (Click to Expand)", expanded=False)
        with my_expander:
            clicked = expander("first")

    def bond_timeseries(self):
        return Metrics().dv1_bond_timeseries()

    def sentencing_network(self, disp_edges=True, disp_nodes=True):
        return Metrics().dv1_sentencing_network(disp_edges=disp_edges, disp_nodes=disp_nodes)
