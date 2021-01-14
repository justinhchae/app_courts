import streamlit as st

from analyze_data.metrics import Metrics
from do_data.getter import Reader

class DV_1():
    def __init__(self):
        pass

    def bond_tree(self, year):
        return Metrics().dv1_bond(year)

    def bond_timeseries(self):
        return Metrics().dv1_bond_timeseries()