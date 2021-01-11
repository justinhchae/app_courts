import streamlit as st

from analyze_data.metrics import Metrics
from do_data.getter import Reader

class OV_1():
    def __init__(self):
        pass

    def court_counts(self, year=None):
        return Metrics().ov1(year)
        # self.st.plotly_chart(Metrics().ov1_initiation())

