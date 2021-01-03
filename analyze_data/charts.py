
import pandas as pd
import numpy as np

# import matplotlib.pyplot as plt
# import seaborn as sns

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import os
import json
from pandas.io.json import json_normalize

import sidetable
import geopandas

from do_data.getter import Reader
from do_data.writer import Writer
from clean_data.cleaner import Cleaner
from analyze_data.colors import Colors

import locale
locale.setlocale(locale.LC_ALL, 'en_US')

class Charts():
    def __init__(self):
        self.today = pd.Timestamp.now()
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

        self.pending_date = 'disposition_date_days_pending'
        self.primary_flag_init = 'primary_charge_flag_init'

        self.key_district = {  1: 'District 1 - Chicago'
                             , 2: 'District 2 - Skokie'
                             , 3: 'District 3 - Rolling Meadows'
                             , 4: 'District 4 - Maywood'
                             , 5: 'District 5 - Bridgeview'
                             , 6: 'District 6 - Markham'}

        # https://loumeza.com/cook-county-branch-court-locations/

        self.key_facname = { '26Th Street' : 'Criminal Courts (26th/California)'
                           , 'Markham Courthouse' : 'Markham Courthouse (6th District)'
                           , 'Skokie Courthouse': 'Skokie Courthouse (2nd District)'
                           , 'Rolling Meadows Courthouse' : 'Rolling Meadows Courthouse (3rd District)'
                           , np.nan : np.nan
                           , 'Maywood Courthouse' : 'Maywood Courthouse (4th District)'
                           , 'Bridgeview Courthouse' : 'Bridgeview Courthouse (5th District)'
                           , 'Dv Courthouse' : 'Domestic Violence Courthouse'
                           , 'Dnu_3605 W. Fillmore St (Rjcc)' : 'RJCC'
                           , 'Daley Center' : 'Daley Center'
                           , '3605 W. Fillmore (Rjcc)' : 'RJCC'
                           , 'Grand & Central (Area 5)' : 'Circuit Court Branch 23/50'
                           , 'Harrison & Kedzie (Area 4)' : 'Circuit Court Branch 43/44'
                           , '51St & Wentworth (Area 1)' : 'Circuit Court Branch 34/38'
                           , 'Belmont & Western (Area 3)' : 'Circuit Court Branch 29/42'
                           , '727 E. 111Th Street (Area 2)' : 'Circuit Court Branch 35/38'
                            }

        self.timedelta = np.timedelta64(1, 'Y')

        self.reader = Reader()
        self.writer = Writer()
        self.cleaner = Cleaner()

        self.geo_districts = self.reader.to_geo('districts.geojson')
        self.geo_facilities = self.reader.to_geo('facilities.geojson')

    def overview(self, df):

        title = str('Overview of Court Data')

        # total_count = locale.format_string("%d", len(df), grouping=True)

        total_count = len(df)
        judge_count = str(len(df[self.judge].dropna(how='any').unique()))
        start_date = min(df[self.received_date])
        end_date = max(df[self.received_date])
        span = str(np.round((end_date - start_date) / self.timedelta, decimals=2))
        districts = list(df[self.district_courts].dropna(how='any').unique())
        initiations = list(df[self.initiation_events].dropna(how='any').unique())
        dispositions = list(df[self.disposition_types].dropna(how='any').unique())
        # cpi = locale.format_string("%d", len(df[self.cpi].dropna(how='any').unique()), grouping=True)
        cpi = len(df[self.cpi].dropna(how='any').unique())
        # case_id = locale.format_string("%d", len(df[self.case_id].dropna(how='any').unique()), grouping=True)
        case_id = len(df[self.case_id].dropna(how='any').unique())

        narrative = {'total_count': f"{total_count:,d}"
                ,'start_date':start_date.strftime('%B %Y')
                ,'end_date':end_date.strftime('%B %Y')
                , 'span': span
                , 'judge_count': judge_count
                , 'initiation_count': str(len(initiations))
                , 'disposition_count': str(len(dispositions))
                , 'district_count': str(len(districts))
                , 'cpi': f"{cpi:,d}"
                , 'case_id': f"{case_id:,d}"
                }

        return narrative

    def overview_figures(self, df):
        # https://towardsdatascience.com/how-to-create-maps-in-plotly-with-non-us-locations-ca974c3bc997

        court_key = 'Fac_Name'
        df[court_key] = df[self.court_fac].map(self.key_facname, na_action='ignore')

        df1 = df[[court_key, self.case_id]].groupby([court_key], as_index=False)[self.case_id].agg('count')
        count_col = str(self.case_id + '_count')
        df1.rename(columns={self.case_id: count_col}, inplace=True)

        courts = self.geo_facilities[(self.geo_facilities['SubType'] == 'Court')]

        courts = courts[[court_key, 'Muni','geometry']]

        geo_df = pd.merge(left=courts, right=df1
                          , how='left'
                          , left_on=court_key
                          , right_on=court_key
                          ).dropna(subset=[count_col])


        geojson = geo_df.__geo_interface__

        geo_df['lon'] = geo_df.geometry.x
        geo_df['lat'] = geo_df.geometry.y

        center = geo_df[(geo_df[court_key] =='Circuit Court Branch 43/44')].geometry

        fig = make_subplots(
            rows=2, cols=2
            , column_widths=[0.6, 0.4]
            , row_heights=[0.4, 0.6]
            , specs=[[{"type": "scatter"}, {"type": "bar"}],
                     [{"type": "scatter", 'colspan':2}, None]]
            , subplot_titles=("Length of Pending Cases", "Top 15 Judges by Case Load", "Count of Disposition Hearings by Charge Class")
        )

        df3 = df[[self.primary_flag_init, self.received_date, self.pending_date]]
        df3 = df3[(df3[self.pending_date].notnull() & df3[self.primary_flag_init] == True)].copy()
        df3 = df3.drop(columns=[self.primary_flag_init])

        counts = df3.value_counts()

        df3 = counts.to_frame().reset_index()
        df3.rename(columns={0: 'count'}, inplace=True)
        # https://pbpython.com/pandas-grouper-agg.html
        df3 = df3.groupby([self.pending_date, pd.Grouper(key=self.received_date, freq='M')])['count'].sum()

        df3 = df3.to_frame().reset_index()

        fig.add_trace(
            go.Scatter(
                       x=df3[self.received_date]
                       , y=df3['count']
                       , name='Primary Charge'
                       # , mode='markers'
                       # # , name=str('Class ' + name)
                       # # ,
                       ),
            row=1, col=1
        )

        # fig.update_geos(fitbounds='locations'
        #                 , scope='usa'
        #                 , lakecolor='LightBlue'
        #                 , center=dict(lon=int(center.x), lat=int(center.y))
        #                 )


        col = 'judge'
        n = 15
        stats = df.stb.freq([col], cum_cols=False)[:n]
        # print(stats)

        fig.add_trace(
            go.Bar( x=stats['count'][:n]
                   , y=stats[col][:n]
                   , orientation='h'
                   , name=self.judge
                   ),
            row=1, col=2
        )

        # fig.update_xaxes(ticklabelposition="outside right",
        #                  row=1, col=2)

        cols = [self.disp_date, self.disp_class]

        counts = df[cols].value_counts()

        df2 = counts.to_frame().reset_index()
        df2.rename(columns={0: 'count'}, inplace=True)
        # https://pbpython.com/pandas-grouper-agg.html
        df2 = df2.groupby([self.disp_class, pd.Grouper(key=self.disp_date, freq='M')])['count'].sum()

        df2 = df2.to_frame().reset_index()
        df2 = self.cleaner.classer(df=df2, col_name=self.disp_class)
        # df2 = df2.set_index(self.disp_date)
        # print(df2)

        # df2['colors'] = df2[self.disp_class].cat.codes
        # color_scale = Colors().make_scales()
        # print(color_scale)
        # color_cats = df2['colors'].unique()
        # color_cats.sort()
        # # print(color_cats)
        # color_map = dict(zip(color_cats, color_scale))
        #
        # df2['colors'] = df2['colors'].map(color_map)

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
        fig.update_yaxes(title_text=None, showgrid=False, zeroline=False
                         , row=2, col=1)
        fig.update_xaxes(title_text="Year", showgrid=False, zeroline=False
                         , row=2, col=1)

        fig.update_yaxes(showticklabels=False)

        fig.update_layout(title=dict(text="Visual Data Summary of Court Data", x=0.5)
                          , showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)' )

        return fig

