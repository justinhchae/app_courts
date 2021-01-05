
import pandas as pd
import numpy as np

# import matplotlib.pyplot as plt
# import seaborn as sns

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from clean_data.cleaner import Cleaner

import os
import json
from pandas.io.json import json_normalize

import sidetable
import geopandas

from collections import deque
from collections import defaultdict

class Judge():
    def __init__(self):
        self.overview_stats = None
        self.judge = 'judge'
        self.received_date = 'received_date'
        self.district_courts = 'disposition_court_name'
        self.court_fac = 'disposition_court_facility'
        self.initiation_events = 'event'
        self.disposition_types = 'charge_disposition'
        self.cpi = 'case_participant_id'
        self.case_id = 'case_id'
        self.disp_date = 'disposition_date'
        self.disp_class = 'disposition_charged_class'
        self.charged_class = 'class'
        self.case_len = 'case_length'
        self.pending_date = 'disposition_date_days_pending'
        self.primary_flag_init = 'primary_charge_flag_init'

        self.ordered_charges = ['M', 'X', '1', '2', '3', '4', 'A', 'B', 'C', 'O', 'P', 'Z']
        self.ordered_charges.reverse()

        self.cleaner = Cleaner()
        self.fig = None

        self.transparent = 'rgba(0,0,0,0)'

    def overview(self, df, col):
        title = str('Overview of Court Data by ' + col.title())

        summary_stats = df.stb.freq([col], cum_cols=False)
        graph = px.bar(summary_stats
                       , x=col
                       , y='count'
                       , title=title)

        graph.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell'))

        return graph

    def detail(self, df, col):

        df = df[(df[self.judge]==col)].copy()
        center = 0.5

        self.fig = make_subplots(
            rows=2, cols=2
            , column_widths=[0.6, 0.4]
            , row_heights=[0.4, 0.6]
            , specs=[[{"type": "scatter"}, {"type": "bar"}],
                     [{"type": "scatter", 'colspan': 2}, None]]
            , subplot_titles=(
                "Case Length", "Disposition Hearings by Charge Class", "Hearings by Charge Class")
        )

        self._ts_case_len(df, row=1, col=1)
        self._ts_charge_class(df, row=2, col=1)
        self._bar_charge_class(df, row=1, col=2)

        self.fig.update_yaxes(showticklabels=False)
        self.fig.update_layout(title=dict(text="Court Data by Judge", x=center)
                          , showlegend=False
                          , paper_bgcolor=None
                          , plot_bgcolor=None
                          )
        #

        return self.fig

    def _ts_case_len(self, df, row, col):
        """
        https://pbpython.com/pandas-grouper-agg.html
        """
        df = df[[self.disp_date, self.case_len]]
        df = df[(df[self.disp_date].notnull())].copy()
        df = df[(df[self.case_len] > 0 )].copy()

        counts = df.value_counts()

        df = counts.to_frame().reset_index()
        df.rename(columns={0: 'count'}, inplace=True)

        df = df.groupby([self.case_len, pd.Grouper(key=self.disp_date, freq='M')])['count'].sum()
        df = df.to_frame().reset_index()
        df = df.sort_values(self.disp_date)

        self.fig.add_trace(
            go.Scatter(
                x=df[self.disp_date]
                , y=df[self.case_len]
                , name='Days'
                # , mode='markers'
                # # , name=str('Class ' + name)
                # # ,
            ),
            row=row, col=col
        )

        self.fig.update_yaxes(title_text=None, showgrid=False, zeroline=False
                              , row=row, col=col)
        self.fig.update_xaxes(title_text="Year", showgrid=False, zeroline=False
                              , row=row, col=col)

    def _ts_charge_class(self, df, row, col):
        """
        :param df:
        :return:

        references: https://pbpython.com/pandas-grouper-agg.html
        """
        df = df[[self.disp_date, self.charged_class]].value_counts()
        df = df.to_frame().reset_index()
        df.rename(columns={0: 'count'}, inplace=True)

        df = df.groupby([self.charged_class, pd.Grouper(key=self.disp_date, freq='M')])['count'].sum()

        df = df.to_frame().reset_index()

        test = df.groupby(self.charged_class, as_index=False).agg({'count': sum})
        # print(test[self.charged_class].dtype)

        df = df.groupby(self.charged_class)
        
        for name, group in df:
            self.fig.add_trace(
                go.Scatter(x=group[self.disp_date]
                           , y=group['count']
                           , name=str('Class ' + name)
                           ,
                           ),
                row=row, col=col
            )

        self.fig.update_yaxes(title_text=None, showgrid=False, zeroline=False
                              , row=row, col=col)
        self.fig.update_xaxes(title_text="Year", showgrid=False, zeroline=False
                              , row=row, col=col)

    def _bar_charge_class(self, df, row, col):
        n = 15
        df = df[[self.judge, self.charged_class]].stb.freq([self.charged_class], cum_cols=False)[:n]

        df[self.charged_class] = df[self.charged_class].astype('category')
        subset_charges = list(df[self.charged_class].unique())
        ordered_subset = [i for i in self.ordered_charges if i in subset_charges]

        df[self.charged_class] = df[self.charged_class].cat.as_ordered()
        df[self.charged_class] = df[self.charged_class].cat.reorder_categories(ordered_subset, ordered=True)

        color = list(df[self.charged_class].cat.codes)
        color.sort()

        self.fig.add_trace(
            go.Bar(x=df[self.charged_class]
                   , y=df['count']
                   , marker=dict(color=color)
                   , name="Class"
                   ),
            row=row, col=col
        )


