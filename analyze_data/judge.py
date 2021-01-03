
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
        self.case_len = 'case_length'

        self.pending_date = 'disposition_date_days_pending'
        self.primary_flag_init = 'primary_charge_flag_init'

        self.cleaner = Cleaner()

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

        df1 = df[[self.disp_date, self.case_len]]
        df1 = df1[(df1[self.disp_date].notnull())].copy()
        df1 = df1[(df1[self.case_len] > 0 )].copy()

        counts = df1.value_counts()

        df1 = counts.to_frame().reset_index()
        df1.rename(columns={0: 'count'}, inplace=True)

        # print(df1)
        # https://pbpython.com/pandas-grouper-agg.html
        df1 = df1.groupby([self.case_len, pd.Grouper(key=self.disp_date, freq='M')])['count'].sum()
        df1 = df1.to_frame().reset_index()
        df1 = df1.sort_values(self.disp_date)
        # print(df1)

        df2 = df[[self.disp_date, self.disp_class]].value_counts()
        df2 = df2.to_frame().reset_index()
        df2.rename(columns={0: 'count'}, inplace=True)
        # https://pbpython.com/pandas-grouper-agg.html
        df2 = df2.groupby([self.disp_class, pd.Grouper(key=self.disp_date, freq='M')])['count'].sum()

        df2 = df2.to_frame().reset_index()



        n = 15
        stats = df[[self.judge, self.disp_class]].stb.freq([self.disp_class], cum_cols=False)[:n]

        ordered_charges = ['M', 'X', '1', '2', '3', '4', 'A', 'B', 'C', 'O', 'P', 'Z']
        ordered_charges.reverse()

        # print(stats)

        stats[self.disp_class] = stats[self.disp_class].astype('category')
        subset_charges = list(stats[self.disp_class].unique())
        ordered_subset = [i for i in ordered_charges if i in subset_charges]

        stats[self.disp_class] = stats[self.disp_class].cat.as_ordered()
        stats[self.disp_class] = stats[self.disp_class].cat.reorder_categories(ordered_subset, ordered=True)


        # stats['colors'] = stats[self.disp_class].cat.codes
        # color_scale = Colors().make_scales()
        # print(color_scale)
        # color_cats = df2['colors'].unique()
        # color_cats.sort()
        # # print(color_cats)
        # color_map = dict(zip(color_cats, color_scale))
        #
        # df2['colors'] = df2['colors'].map(color_map)

        # print(stats)



        fig = make_subplots(
            rows=2, cols=2
            , column_widths=[0.6, 0.4]
            , row_heights=[0.4, 0.6]
            , specs=[[{"type": "scatter"}, {"type": "bar"}],
                     [{"type": "scatter", 'colspan': 2}, None]]
            , subplot_titles=(
            "Case Length (Days)", "Disposition Hearings by Charge Class", "Hearings by Charge Class")
        )

        fig.add_trace(
            go.Scatter(
                x=df1[self.disp_date]
                , y=df1[self.case_len]
                , name='Days'
                # , mode='markers'
                # # , name=str('Class ' + name)
                # # ,
            ),
            row=1, col=1
        )

        df2 = df2.groupby(self.disp_class)
        for name, group in df2:
            fig.add_trace(
                go.Scatter(x=group[self.disp_date]
                           , y=group['count']
                           , name=str('Class ' + name)
                           ,
                           ),
                row=2, col=1
            )

        color = list(stats[self.disp_class].cat.codes)
        color.sort()

        fig.add_trace(
            go.Bar(x=stats[self.disp_class]
                   , y=stats['count']
                   , marker=dict(color=color)

                   , name="Class"
                   ),
            row=1, col=2
        )

        fig.update_yaxes(title_text=None, showgrid=False, zeroline=False
                         , row=2, col=1)
        fig.update_yaxes(title_text=None, showgrid=False, zeroline=False
                         , row=1, col=1)
        fig.update_xaxes(title_text="Year", showgrid=False, zeroline=False
                         , row=2, col=1)
        fig.update_xaxes(title_text="Year", showgrid=False, zeroline=False
                         , row=1, col=1)

        fig.update_yaxes(showticklabels=False)

        fig.update_layout(title=dict(text="Court Data by Judge", x=0.5)
                          , showlegend=False
                          # , paper_bgcolor='rgba(0,0,0,0)'
                          # , plot_bgcolor='rgba(0,0,0,0)'
                          )

        return fig


