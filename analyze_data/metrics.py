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

    def ov1(self):
        self.fig = make_subplots(
            rows=1, cols=3
            # , column_widths=[0.6, 0.4]
            # , row_heights=[0.4, 0.6]
            , specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
            , subplot_titles=("Initiation"
                              , "Disposition"
                              , "Sentencing")
        )

        self.ov1_initiation(row=1, col=1)
        self.ov1_disposition(row=1, col=2)
        self.ov1_sentencing(row=1, col=3)

        self.fig.update_layout(showlegend=False
                          , paper_bgcolor=self.transparent
                          , plot_bgcolor=self.transparent)

        self.fig.update_xaxes(tickangle=45)

        return self.fig

    def ov1_initiation(self, row, col):
        df = Reader().to_df('ov1_initiation.pickle', preview=False, classify=False, echo=False)

        df = df[df[name.primary_charge_flag]==True]
        total_case_id = len(df[name.case_id].unique())
        total_cpi = len(df[name.case_participant_id].unique())
        cases_pending = len(df[df[name.disposition_date_days_pending].notnull()])
        # cpi_bond = df[[name.case_id, name.case_participant_id, name.bond_type_current]][df[name.bond_type_current].notnull()].drop_duplicates()
        cases_bond = len(df[(df[name.bond_type_current] != 'No Bond') & (df[name.bond_type_current].notnull())])

        df = pd.DataFrame({'count': [total_case_id, total_cpi, cases_bond, cases_pending],
                           'variable': [name.case_id, name.case_participant_id, name.bond_type_current, name.disposition_date_days_pending],
                           'value': ['1 - Cases', '2 - Individuals', '3 - Current Bond', '4 - Disposition Pending Days'],
                           'Color': [np.nan, np.nan, np.nan, np.nan]})

        df['Width'] = .8

        df['Color'] = df['variable'].map({name.case_id: 'blues',
                                          name.case_participant_id: 'ylgn',
                                          name.disposition_date_days_pending: 'sunset',
                                          name.bond_type_current: 'sunset',
                                          })

        df = df.groupby('value')

        for x, y in df:
            self.fig.add_trace(
                go.Bar(
                      x=y['value']
                    , y=y['count']
                    , marker=dict(color=y['count'], colorscale=y['Color'].iloc[0])
                    , text=x
                    , width=y['Width']
                ),
                row=row, col=col
            )


    def ov1_disposition(self, row, col):
        """
        return the most severe allegation for a given case (not always the primary charge
        https://stackoverflow.com/questions/15705630/get-the-rows-which-have-the-max-count-in-groups-using-groupby
        """
        df = Reader().to_df('ov1_disposition.pickle', preview=False, classify=False, echo=False)

        disp_cats = df.stb.freq([name.charge_disposition_cat], cum_cols=False).drop(columns='percent')
        disp_cats = pd.melt(disp_cats, id_vars=['count'], value_vars=[name.charge_disposition_cat])
        disp_cats = disp_cats.sort_values(by=['count'])

        total_case_id = len(df[name.case_id].unique())
        total_cpi = len(df[name.case_participant_id].unique())

        df = pd.DataFrame({'count': [total_case_id, total_cpi],
                           'variable': ['case_id', name.case_participant_id],
                           'value': ['Cases', 'Individuals'],
                           'Color': [np.nan, np.nan]})

        df = df.append(disp_cats)

        df['Color'] = df['variable'].map({name.case_id: 'blues',
                                          name.case_participant_id: 'ylgn',
                                          name.charge_disposition_cat: 'sunset_r',
                                          })

        df['Width'] = 1

        df['variable'] = df['variable'].map({name.case_id: '1 - Cases',
                                          name.case_participant_id: '2 - Individuals',
                                          name.charge_disposition_cat: '3 - Charge Category',
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


    def ov1_sentencing(self, row, col):
        df = Reader().to_df('ov1_sentencing.pickle', preview=False)

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
        # print(total_cpi)

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

        # colors.make_scales()

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




