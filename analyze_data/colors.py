
import pandas as pd
import numpy as np

# import matplotlib.pyplot as plt
# import seaborn as sns

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import os

from do_data.getter import Reader
from do_data.writer import Writer
from clean_data.cleaner import Cleaner

from textwrap import wrap

class Colors():
    def __init__(self):
        pass

    def make_scales(self):
        # https: // plotly.com / python / builtin - colorscales /
        scales = px.colors.named_colorscales()
        # print("\n".join(wrap("".join('{:<12}'.format(c) for c in scales), 96)))


        return px.colors.cyclical.Edge


