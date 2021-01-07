
# import modin as md
import numpy as np
import pandas as pd
import sidetable
import geopandas
import gc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn import preprocessing

from clean_data.cleaner import Cleaner
from do_data.getter import Reader
from do_data.writer import Writer


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
        self.charged_class = 'class'
        self.pending_date = 'disposition_date_days_pending'
        self.primary_flag_init = 'primary_charge_flag_init'

        self.key_district = {  1: 'District 1 - Chicago'
                             , 2: 'District 2 - Skokie'
                             , 3: 'District 3 - Rolling Meadows'
                             , 4: 'District 4 - Maywood'
                             , 5: 'District 5 - Bridgeview'
                             , 6: 'District 6 - Markham'}

        # https://loumeza.com/cook-county-branch-court-locations/

        self.fac_name = 'Fac_Name'
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

        self.fig = None
        self.transparent = 'rgba(0,0,0,0)'

        self.n_samples = None
        self.df = self.reader.to_df('main.bz2'
                                    , preview=False
                                    , echo=False
                                    , classify=False
                                    )

    def chart_data(self):
        print('load data')

    def overview(self):
        self.df = self.reader.to_df('main.bz2'
                                    , preview=False
                                    , echo=False
                                    , classify=False
                                    )

        title = str('Overview of Court Data')

        total_count = len(self.df)
        judge_count = str(len(self.df[self.judge].dropna(how='any').unique()))
        start_date = min(self.df[self.received_date])
        end_date = max(self.df[self.received_date])
        span = str(np.round((end_date - start_date) / self.timedelta, decimals=2))
        districts = list(self.df[self.district_courts].dropna(how='any').unique())
        initiations = list(self.df[self.initiation_events].dropna(how='any').unique())
        dispositions = list(self.df[self.disposition_types].dropna(how='any').unique())
        # cpi = locale.format_string("%d", len(df[self.cpi].dropna(how='any').unique()), grouping=True)
        cpi = len(self.df[self.cpi].dropna(how='any').unique())
        # case_id = locale.format_string("%d", len(df[self.case_id].dropna(how='any').unique()), grouping=True)
        case_id = len(self.df[self.case_id].dropna(how='any').unique())

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

    def overview_figures(self, n_samples = None):

        self.n_samples = n_samples
        # https://towardsdatascience.com/how-to-create-maps-in-plotly-with-non-us-locations-ca974c3bc997
        center = 0.5

        self.fig = make_subplots(
            rows=2, cols=2
            , column_widths=[0.6, 0.4]
            , row_heights=[0.4, 0.6]
            , specs=[[{"type": "scatter"}, {"type": "bar"}],
                     [{"type": "scatter"}, {"type": "choropleth"}]]
            , subplot_titles=("Length of Pending Cases by Time"
                              , "Top 15 Judges by Case Volume"
                              , "Disposition Hearing Volume by Time"
                              , "Case Volume by Court Location")
        )

        self._ts_pending_case_len(self.df, row=1, col=1)
        self._ts_charge_class(self.df, row=2, col=1)
        self._bar_judge(self.df, row=1, col=2)
        self._geo_map(self.df, row=2, col=2)

        self.fig.update_yaxes(showticklabels=False)

        self.fig.update_layout(title=dict(text="Visual Data Summary of Court Data", x=center)
                          , showlegend=False, paper_bgcolor=self.transparent, plot_bgcolor=self.transparent )
        return self.fig

    def _ts_pending_case_len(self, df, row, col):

        if isinstance(self.n_samples, int):
            df = df.sample(self.n_samples, random_state=0)

        df = df[[self.primary_flag_init, self.received_date, self.pending_date]]
        df = df[(df[self.pending_date].notnull() & df[self.primary_flag_init] == True)].copy()
        df = df.drop(columns=[self.primary_flag_init])

        df = df.value_counts().to_frame('count').reset_index()

        # https://pbpython.com/pandas-grouper-agg.html
        df = df.groupby([self.pending_date, pd.Grouper(key=self.received_date, freq='M')])['count'].sum().to_frame().reset_index()

        self.fig.add_trace(
            go.Scatter(
                x=df[self.received_date]
                , y=df['count']
                , name='Primary Charge'
                # , mode='markers'
                # # , name=str('Class ' + name)
                # # ,
            ),
            row=row, col=col
        )

    def _ts_charge_class(self, df, row, col):

        if isinstance(self.n_samples, int):
            df = df.sample(self.n_samples, random_state=0)

        cols = [self.disp_date, self.charged_class]

        df = df[cols].value_counts().to_frame('count').reset_index()

        # https://pbpython.com/pandas-grouper-agg.html
        df = df.groupby([self.charged_class, pd.Grouper(key=self.disp_date, freq='M')])['count'].sum().to_frame().reset_index()

        df = self.cleaner.classer(df=df, col_name=self.charged_class).groupby(self.charged_class)
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

    def _bar_judge(self, df, row, col):
        if isinstance(self.n_samples, int):
            df = df.sample(self.n_samples, random_state=0)

        n = 15
        df = df.stb.freq([self.judge], cum_cols=False)[:n]

        self.fig.add_trace(
            go.Bar(x=df['count'][:n]
                   , y=df[self.judge][:n]
                   , orientation='h'
                   , name=self.judge
                   ),
            row=row, col=col
        )

    def _geo_map(self, df, row, col):
        if isinstance(self.n_samples, int):
            df = df.sample(self.n_samples, random_state=0)

        df[self.fac_name] = df[self.court_fac].map(self.key_facname, na_action='ignore')

        df = df[[self.fac_name, self.case_id]].groupby([self.fac_name], as_index=False)[self.case_id].agg('count')
        count_col = str(self.case_id + '_count')
        df.rename(columns={self.case_id: count_col}, inplace=True)

        courts = self.geo_facilities[(self.geo_facilities['SubType'] == 'Court')]
        courts = courts[[self.fac_name, 'Muni', 'geometry']]

        districts = self.geo_districts

        gdf = pd.merge(left=courts, right=df
                          , how='left'
                          , left_on=self.fac_name
                          , right_on=self.fac_name
                          ).dropna(subset=[self.fac_name])

        # geojson = districts.__geo_interface__

        mm_scaler = preprocessing.MinMaxScaler(feature_range=(10,40))

        # https://towardsdatascience.com/data-normalization-with-pandas-and-scikit-learn-7c1cc6ed6475
        gdf['scaled'] = pd.DataFrame(mm_scaler.fit_transform(gdf[[count_col]]))

        gdf = gdf.dropna(how='any')

        gdf['lon'] = gdf.geometry.x
        gdf['lat'] = gdf.geometry.y

        def human_format(num):
            # https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python
            magnitude = 0
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            # add more suffixes if you need them
            return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

        gdf[count_col] = gdf[count_col].apply(lambda x: human_format(x))

        gdf = gdf.groupby(self.fac_name)

        # COMEBACK: Map Plots
        # fig = px.choropleth(districts
        #                     , geojson=districts.geometry
        #                     , locations=districts.index
        #                     )

        for name, group in gdf:
            self.fig.add_trace(
                go.Scattergeo(lat=group['lat']
                              , lon=group['lon']
                              , name=name
                              , mode='markers'
                              , hoverinfo='text'
                              , text=group[[self.fac_name, count_col]]
                              , marker=dict(size=group['scaled']
                                            , opacity=0.5)
                              )
                ,row=row, col=col
            )

        self.fig.update_geos(
                            fitbounds='locations'
                            , scope='usa'
                            # , lataxis=dict(range=(-85, -86))
                            #,
                             )



