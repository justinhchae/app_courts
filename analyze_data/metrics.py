import numpy as np
import pandas as pd
import sidetable

import plotly.graph_objects as go
import plotly_express as px
from plotly.subplots import make_subplots

import matplotlib.pyplot as plt
import seaborn as sns

from clean_data.cleaner import Cleaner
from do_data.getter import Reader
from do_data.writer import Writer
from do_data.config import Columns
name = Columns()

# from pandasgui import show
from analyze_data.colors import Colors
from scipy import stats

colors = Colors()

class Metrics():
    def __init__(self):
        self.today = pd.Timestamp.now()
        self.transparent = 'rgba(0,0,0,0)'
        self.charged_class_code = 'charged_class_category'
        self.years = 365.25

        self.common_cols = [
            name.case_id
            , name.case_participant_id
            , name.received_date
            , name.updated_offense_category
            , name.charge_id
            , name.charge_version_id
            , name.charge_count
        ]

        ## https://community.plotly.com/t/plotly-colours-list/11730/3
        self.blue = '#1f77b4'  # muted blue
        self.orange = '#ff7f0e'  # safety orange
        self.green = '#2ca02c'  # cooked asparagus green
        self.red = '#d62728'  # brick red
        self.purple = '#9467bd'  # muted purple
        self.brown = '#8c564b'  # chestnut brown
        self.pink = '#e377c2'  # raspberry yogurt pink
        self.gray = '#7f7f7f'  # middle gray
        self.yellow_green='#bcbd22'  # curry yellow-green
        self.teal = '#17becf'  # blue-teal
        self.df = None
        self.fig = None

    def ov1(self, year="All Time"):
        self.fig = make_subplots(
            rows=1, cols=3
            , specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
            , subplot_titles=("Initiation"
                              , "Disposition"
                              , "Sentencing")
        )

        self.ov1_initiation(row=1, col=1, year=year)
        self.ov1_disposition(row=1, col=2, year=year)
        self.ov1_sentencing(row=1, col=3, year=year)

        self.fig.update_layout(showlegend=False
                          , title_text=str('Court Data for ' + str(year))
                          , paper_bgcolor=self.transparent
                          , plot_bgcolor=self.transparent)

        self.fig.update_xaxes(tickangle=45)

        return self.fig

    def ov1_initiation(self, row, col, year=None):
        df = Reader().to_df('ov1_initiation.pickle', preview=False, classify=False, echo=False)

        if year !='All Time':
            df = df[(df['year']==year)]

        total_case_id = len(df[name.case_id].unique())
        total_cpi = len(df[name.case_participant_id].unique())

        bond_types = df.stb.freq([name.bond_type_current], cum_cols=False).drop(columns='percent')
        bond_types = pd.melt(bond_types, id_vars=['count'], value_vars=[name.bond_type_current])
        bond_types = bond_types.sort_values(by=['count'], ascending=False)

        event_types = df.stb.freq([name.event], cum_cols=False).drop(columns='percent')
        event_types = pd.melt(event_types, id_vars=['count'], value_vars=[name.event])
        event_types = event_types.sort_values(by=['count'], ascending=False)

        df = pd.DataFrame({'count': [total_case_id, total_cpi],
                           'variable': ['case_id', name.case_participant_id],
                           'value': ['Cases', 'Individuals'],
                           'Color': [np.nan, np.nan]})

        df = df.append(bond_types)
        df = df.append(event_types)

        df['Color'] = df['variable'].map({name.case_id: 'blues',
                                          name.case_participant_id: 'ylgn',
                                          name.event: 'sunset',
                                          name.bond_type_current: 'sunset',
                                          })

        df['variable'] = df['variable'].map({name.case_id: '1 - Cases',
                                             name.case_participant_id: '2 - Individuals',
                                             name.event: '3 - Hearing Type',
                                             name.bond_type_current: '4 - Bond Type'
                                             })
        df['Width'] = 1

        df = df.groupby('variable')

        for x, y in df:
            self.fig.add_trace(
                go.Bar(
                    x=y['variable']
                    , y=y['count']  # , color=df_plot['value']
                    , marker=dict(color=y['count'], colorscale=y['Color'].iloc[0])
                    , text=y['value']
                    , width=y['Width']
                ),
                row=row, col=col
            )

    def ov1_disposition(self, row, col, year=None):
        """
        return the most severe allegation for a given case (not always the primary charge
        https://stackoverflow.com/questions/15705630/get-the-rows-which-have-the-max-count-in-groups-using-groupby
        """
        df = Reader().to_df('ov1_disposition.pickle', preview=False, classify=False, echo=False)

        if year !='All Time':
            df = df[(df['year']==year)]

        disp_cats = df.stb.freq([name.charge_disposition_cat], cum_cols=False).drop(columns='percent')
        disp_cats = pd.melt(disp_cats, id_vars=['count'], value_vars=[name.charge_disposition_cat])
        disp_cats = disp_cats.sort_values(by=['count'], ascending=False)

        charge_cats = df.stb.freq([name.disposition_charged_class], cum_cols=False).drop(columns='percent')
        charge_cats = pd.melt(charge_cats, id_vars=['count'], value_vars=[name.disposition_charged_class])
        charge_cats = charge_cats.sort_values(by=['count'], ascending=False)

        total_case_id = len(df[name.case_id].unique())
        total_cpi = len(df[name.case_participant_id].unique())

        df = pd.DataFrame({'count': [total_case_id, total_cpi],
                           'variable': ['case_id', name.case_participant_id],
                           'value': ['Cases', 'Individuals'],
                           'Color': [np.nan, np.nan]})

        df = df.append(disp_cats)
        df = df.append(charge_cats)

        df['Color'] = df['variable'].map({name.case_id: 'blues',
                                          name.case_participant_id: 'ylgn',
                                          name.charge_disposition_cat: 'sunset',
                                          name.disposition_charged_class: 'sunset'
                                          })

        df['Width'] = 1

        df['variable'] = df['variable'].map({name.case_id: '1 - Cases',
                                          name.case_participant_id: '2 - Individuals',
                                          name.charge_disposition_cat: '3 - Charge Category',
                                          name.disposition_charged_class: '4 - Charge Class'
                                          })

        df = df.groupby('variable')

        for x, y in df:
            self.fig.add_trace(
                go.Bar(
                    x=y['variable']
                    , y=y['count']  # , color=df_plot['value']
                    , marker=dict(color=y['count'], colorscale=y['Color'].iloc[0])
                    , text=y['value']
                    , width=y['Width']
                ),
                row=row, col=col
            )

    def ov1_sentencing(self, row, col, year=None):
        df = Reader().to_df('ov1_sentencing.pickle', preview=False)

        if year !='All Time':
            df = df[(df['year']==year)]

        cols = [
              name.case_id
            , name.case_participant_id
            , name.received_date
            , name.updated_offense_category
            , name.disposition_charged_class
            , name.sentence_judge
            , name.commitment_days
            , name.sentence_type
                ]

        df1 = df[cols].copy()
        df1[self.charged_class_code] = df1[name.disposition_charged_class].cat.codes

        cols = [name.case_id, name.case_participant_id, name.received_date, name.updated_offense_category]
        idx = df1.groupby(cols, sort=False)[self.charged_class_code].transform(max) == df1[self.charged_class_code]
        df = df[idx].drop_duplicates(subset=cols)

        total_cpi = len(df[name.case_participant_id].unique())

        judges = df.stb.freq([name.sentence_judge], cum_cols=False).drop(columns='percent')
        judges = pd.melt(judges, id_vars=['count'], value_vars=[name.sentence_judge])
        judges = judges.sort_values(by=['count'], ascending=False)

        sentence = df.stb.freq([name.sentence_type], cum_cols=False).drop(columns='percent')
        sentence = pd.melt(sentence, id_vars=['count'], value_vars=[name.sentence_type])
        sentence = sentence.sort_values(by=['count'], ascending=False)

        commitment = df.stb.freq([name.commitment_days], cum_cols=False).drop(columns='percent')
        commitment = pd.melt(commitment, id_vars=['count'], value_vars=[name.commitment_days])
        commitment = commitment.sort_values(by=['count'], ascending=False)
        commitment['value'] = (commitment['value'] / self.years).round(1)
        commitment['value'] = commitment['value'].astype(str) + ' Years'


        df = pd.DataFrame({'count':[total_cpi],
                           'variable':[name.case_participant_id],
                           'value':['Individuals'],
                           'Color': [self.green]})

        df = df.append(judges)
        df = df.append(sentence)
        df = df.append(commitment)

        df['Color'] = df['variable'].map({name.case_participant_id:'ylgn',
                                       name.sentence_judge:'sunset',
                                       name.sentence_type:'sunset',
                                       name.commitment_days:'sunset'})

        df['Width'] = 1

        df['variable'] = df['variable'].map({name.case_participant_id: '1 - Individuals',
                                             name.sentence_judge: '2 - Sentence Judge',
                                             name.sentence_type: '3 - Sentence Type',
                                             name.commitment_days: '4 - Sentence Years'
                                             })

        df = df.groupby('variable')

        for x, y in df:
            self.fig.add_trace(
                go.Bar(
                      x=y['variable']
                    , y=y['count']  # , color=df_plot['value']
                    , marker=dict(color=y['count'], colorscale=y['Color'].iloc[0])
                    , text=y['value']
                    , width=y['Width']
                ),
                row=row, col=col
            )


    def ov1_timeseries(self):
        df = Reader().to_df('ov1_initiation.pickle', preview=False, classify=False, echo=False)

        initiation = df[[name.case_participant_id, 'year']].groupby('year', as_index=False).agg('count')
        initiation['type'] = 'initiation'
        df = Reader().to_df('ov1_disposition.pickle', preview=False, classify=False, echo=False)
        disposition = df[[name.case_participant_id, 'year']].groupby('year', as_index=False).agg('count')
        disposition['type'] = 'disposition'
        df = Reader().to_df('ov1_sentencing.pickle', preview=False, classify=False, echo=False)
        sentencing = df[[name.case_participant_id, 'year']].groupby('year', as_index=False).agg('count')
        sentencing['type'] = 'sentencing'

        df = initiation.append(disposition)
        df = df.append(sentencing)

        df = df.rename(columns={name.case_participant_id: '#Cases'})

        df = df[df['year'] > 2010]

        fig = px.area(df, x='year', y='#Cases', color='type')
        # https://towardsdatascience.com/line-chart-animation-with-plotly-on-jupyter-e19c738dc882

        fig.update_yaxes(title='Case Volume')
        fig.update_xaxes(title='Year')

        fig.update_layout(
            hovermode='x unified',
            showlegend=False
            # , title_text=str('Court Data for ' + str(year))
            , paper_bgcolor=self.transparent
            , plot_bgcolor=self.transparent
            , title='Court Volume Over Time - The COVID Court Cliff'
        )

        self.ov1_regression()

        return fig

    def ov1_regression(self):
        # from sklearn.linear_model import LinearRegression
        # from plotly.graph_objs.scatter.marker import Line
        frequency = 'M'

        df = Reader().to_df('ov1_initiation.pickle', preview=False, classify=False, echo=False)

        df = df[df['year'] > 2010]
        df = df[df['year'] < 2021]

        initiation = df[[name.event_date, name.event]].groupby([pd.Grouper(key=name.event_date, freq=frequency)]).agg('count').reset_index()
        initiation = initiation.sort_values(name.event_date)
        initiation['type'] = 'initiation'
        initiation = initiation.rename(columns={name.event:'count'})
        # counts = df.value_counts()
        # df = counts.to_frame().reset_index()
        # df.rename(columns={0: 'count'}, inplace=True)
        #
        # df = df.groupby([pd.Grouper(key=name.event_date, freq=frequency)])['count'].sum().to_frame().reset_index()
        # initiation = df.sort_values(name.event_date).dropna(subset=['count'])
        # initiation['type'] = 'initiation'
        #
        # print(initiation)

        del df

        df = Reader().to_df('ov1_disposition.pickle', preview=False, classify=False, echo=False)
        df = df[df['year'] > 2010]
        df = df[df['year'] < 2021]

        df = df[[name.disposition_date, name.charge_disposition_cat]].groupby([pd.Grouper(key=name.disposition_date, freq=frequency)]).agg('count').reset_index()
        disposition = df.sort_values(name.disposition_date)
        disposition['type'] = 'disposition'
        disposition = disposition.rename(columns={name.charge_disposition_cat: 'count'})

        del df

        df = Reader().to_df('ov1_sentencing.pickle', preview=False, classify=False, echo=False)
        df = df[df['year'] > 2010]
        df = df[df['year'] < 2021]

        df = df[[name.sentence_date, name.sentence_type]].groupby([pd.Grouper(key=name.sentence_date, freq=frequency)]).agg('count').reset_index()
        sentencing = df.sort_values(name.sentence_date)
        sentencing['type'] = 'sentencing'
        sentencing = sentencing.rename(columns={name.sentence_type: 'count'})

        del df

        initiation = initiation.rename(columns={name.event_date:'date'})
        disposition = disposition.rename(columns={name.disposition_date:'date'})
        sentencing = sentencing.rename(columns={name.sentence_date:'date'})

        df = initiation.append(disposition)
        df = df.append(sentencing).reset_index(drop=True)

        g = df.groupby('type')
        fig = go.Figure()

        for group, df in g:
            # https://stackoverflow.com/questions/60204175/plotly-how-to-add-trendline-to-a-bar-chart

            fig.add_trace(go.Scatter(x=df['date'], y=df['count'], name=group, fill='tozeroy'))

            help_fig = px.scatter(df, x=df['date'], y=df['count'], trendline="lowess")
            x_trend = help_fig["data"][1]['x']
            y_trend = help_fig["data"][1]['y']

            fig.add_trace(go.Scatter(x=x_trend, y=y_trend, name=str(group + ' trend')))

        # # https://towardsdatascience.com/line-chart-animation-with-plotly-on-jupyter-e19c738dc882

        fig.update_yaxes(title='Case Volume')
        fig.update_xaxes(title='Year')

        fig.update_layout(
            hovermode='x',
            showlegend=False
            # , title_text=str('Court Data for ' + str(year))
            , paper_bgcolor=self.transparent
            , plot_bgcolor=self.transparent
            , title='Monthly Court Volume Over Time'
        )

        return fig










