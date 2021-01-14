import streamlit as st

from analyze_data.metrics import Metrics
from do_data.getter import Reader

class OV_1():
    def __init__(self):
        pass

    def narrative(self):
        st.write(
            'Cook county is the largest county in the United States by population and has millions of court records available for analysis.',
            'In addition to size, Cook County is also the home county for Chicago and surrounding areas.',
            'The availability of this data, at scale, provides interesting analytical opportunities to support public awareness of the court system.',
            'Although the source data is publicly available, the raw data is split into different sections and is difficult to interpret without significant engineering.',
            'This dashboard represents the results of a processed and ready-to-analyze dataset about the courts.'
            )
        return

    def court_counts(self, year=2020):
        return Metrics().ov1(year)
        # self.st.plotly_chart(Metrics().ov1_initiation())

    def timeseries(self):
        return Metrics().ov1_regression()