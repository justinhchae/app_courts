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
from analyze_data.network import Network
name = Columns()
network = Network()

# from pandasgui import show
from analyze_data.colors import Colors
from scipy import stats

from sklearn import preprocessing

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

    def ov1_regression(self, frequency='M', annotation = 'By @justinhchae for Chicago Appleseed Center for Fair Courts'):
        df = Reader().to_df('ov1_initiation.pickle', preview=False, classify=False, echo=False)

        df = df[df['year'] > 2010]
        df = df[df['year'] < 2021]

        initiation = df[[name.event_date, name.event]].groupby([pd.Grouper(key=name.event_date, freq=frequency)]).agg('count').reset_index()
        initiation = initiation.sort_values(name.event_date)
        initiation['type'] = 'initiation'
        initiation['color'] = self.purple
        initiation = initiation.rename(columns={name.event:'count'})

        del df

        df = Reader().to_df('ov1_disposition.pickle', preview=False, classify=False, echo=False)
        df = df[df['year'] > 2010]
        df = df[df['year'] < 2021]

        df = df[[name.disposition_date, name.charge_disposition_cat]].groupby([pd.Grouper(key=name.disposition_date, freq=frequency)]).agg('count').reset_index()
        disposition = df.sort_values(name.disposition_date)
        disposition['type'] = 'disposition'
        disposition['color'] = self.orange
        disposition = disposition.rename(columns={name.charge_disposition_cat: 'count'})

        del df

        df = Reader().to_df('ov1_sentencing.pickle', preview=False, classify=False, echo=False)
        df = df[df['year'] > 2010]
        df = df[df['year'] < 2021]

        df = df[[name.sentence_date, name.sentence_type]].groupby([pd.Grouper(key=name.sentence_date, freq=frequency)]).agg('count').reset_index()
        sentencing = df.sort_values(name.sentence_date)
        sentencing['type'] = 'sentencing'
        sentencing['color'] = self.teal
        sentencing = sentencing.rename(columns={name.sentence_type: 'count'})

        del df

        initiation = initiation.rename(columns={name.event_date:'date'})
        disposition = disposition.rename(columns={name.disposition_date:'date'})
        sentencing = sentencing.rename(columns={name.sentence_date:'date'})

        df = sentencing.append(disposition)
        df = df.append(initiation).reset_index(drop=True)

        g = df.groupby('type')
        fig = go.Figure()

        for group, df in g:
            # https://stackoverflow.com/questions/60204175/plotly-how-to-add-trendline-to-a-bar-chart

            fig.add_trace(go.Scatter(x=df['date'], y=df['count'], name=group, fill='tozeroy', marker=dict(color=df['color'].iloc[0])))

            help_fig = px.scatter(df, x=df['date'], y=df['count'], trendline="lowess")
            x_trend = help_fig["data"][1]['x']
            y_trend = help_fig["data"][1]['y']

            fig.add_trace(go.Scatter(x=x_trend, y=y_trend, name='trend', line = dict(color=df['color'].iloc[0], width=4, dash='dash')))

        # # https://towardsdatascience.com/line-chart-animation-with-plotly-on-jupyter-e19c738dc882

        fig.update_yaxes(title='Case Volume')
        fig.update_xaxes(title=annotation)

        fig.update_layout(
            hovermode='x',
            showlegend=False
            # , title_text=str('Court Data for ' + str(year))
            , paper_bgcolor=self.transparent
            , plot_bgcolor=self.transparent
            , title='Monthly Court Volume Over Time'
        )

        return fig

    def dv1_bond(self, year=2020, annotation = 'By @justinhchae for Chicago Appleseed Center for Fair Courts'):

        df = Reader().to_df('dv1_bond.pickle', preview=False)

        if year !='All Time':
            df = df[(df['year']==year)]

        df[name.race].cat.add_categories(['None'], inplace=True)
        df[name.race].fillna('None', inplace=True)
        df[name.race].cat.remove_categories(np.nan, inplace=True)

        df[name.bond_type_current].cat.add_categories(['None'], inplace=True)
        df[name.bond_type_current].fillna('None', inplace=True)
        df[name.bond_type_current].cat.remove_categories(np.nan, inplace=True)

        df[name.event].cat.add_categories(['None'], inplace=True)
        df[name.event].fillna('None', inplace=True)
        df[name.event].cat.remove_categories(np.nan, inplace=True)

        df['root'] = 'initiation event'
        df['weights'] = df[name.event].cat.codes
        df.rename(columns={name.bond_amount_current:'Bond Amount'}, inplace=True)


        fig = px.treemap(df
                         , path=['root', name.race, name.event, name.bond_type_current]
                         , values='Bond Amount'
                         , hover_data=['race']
                         , color='Bond Amount'
                         , color_continuous_scale='RdBu_r'

                         , title='Bond Data by Race for ' + str(year)
                         )

        fig.add_annotation(x=.1, y=-.1,
                           text=annotation,
                           showarrow=False,
                           )

        return fig

    def dv1_bond_timeseries(self, frequency='M', year=2020, annotation = 'By @justinhchae for Chicago Appleseed Center for Fair Courts'):

        df = Reader().to_df('dv1_bond.pickle', preview=False)
        df = df[df['year'] > 2010]
        df = df[df['year'] < 2021]

        df = df[[name.bond_date_current, name.bond_type_current, name.bond_amount_current]]

        aggies = ['count', 'sum', 'mean', 'min', 'max']
        df = df.groupby([name.bond_type_current, pd.Grouper(key=name.bond_date_current, freq=frequency)])[name.bond_amount_current].agg(aggies).reset_index()
        df[aggies] = df[aggies].fillna(0)

        scaler = preprocessing.MinMaxScaler(feature_range=(5, 35))

        # https://towardsdatascience.com/data-normalization-with-pandas-and-scikit-learn-7c1cc6ed6475
        df['scaled'] = pd.DataFrame(scaler.fit_transform(df[['mean']]))

        key = {
                'C Bond': self.purple
              , 'D Bond': self.blue
              , 'I Bond': self.green
              , 'No Bond': self.gray
               }
        
        df['color'] = df[name.bond_type_current].map(key, na_action='ignore')

        grouped = df.groupby(name.bond_type_current)

        fig = go.Figure()

        annotation_y = []

        for group, df in grouped:
            # https://stackoverflow.com/questions/60204175/plotly-how-to-add-trendline-to-a-bar-chart
            # fig.add_trace(go.Scatter(x=df[name.bond_date_current], y=df['sum'], name=group))
            # print(df[''])

            y_val = np.max(df['sum'])
            annotation_y.append(y_val)

            fig.add_trace(go.Scatter(x=df[name.bond_date_current], y=df['sum']
                                     , name=group
                                     , mode='markers'
                                     , marker=dict(size=df['scaled'], color=df['color'])
                                     , showlegend=False
                                     , hoverinfo='skip'
                                     ))

            fig.add_trace(go.Scatter(x=df[name.bond_date_current], y=df['sum']
                                     , name=group
                                     , mode='lines'
                                     , line=dict(color=df['color'].iloc[0])
                                     ))

        a1_date = pd.to_datetime('2017-02-13')

        a2_date = pd.to_datetime('2021-01-14')

        maxv = np.max(annotation_y)
        minv = np.mean(annotation_y)

        # fig.add_shape(x0=[a1_date], y0=[test], text=['poo'], type='line')

        fig.add_shape(type="line",
                      x0=a1_date, y0=0, x1=a1_date, y1=maxv*.7,
                      line=dict(color=self.red, width=2)
                      )

        fig.add_trace(go.Scatter(
            x=[a1_date], y=[maxv*.7]
            , text='<b>Bail Reform Act 2017</b>'
            , mode='text'
            , showlegend=False
            , hoverinfo='skip'
        ))

        fig.add_shape( type="line",
                       x0=a2_date, y0=0, x1=a2_date, y1=minv*1.3
                      , line=dict(color=self.red, width=2)
                      )

        fig.add_trace(go.Scatter(
            x=[a2_date], y=[minv*1.3]
            , text='<b>Pre-Trial Fairness Act 2021</b>'
            , mode='text'
            , showlegend=False
            , hoverinfo='skip'
        ))


        a3_date = pd.to_datetime('2020-09-30')

        fig.add_shape(type="line",
                      x0=a3_date, y0=0, x1=a3_date, y1=minv*.5
                      , line=dict(color=self.gray, width=1)
                      )

        fig.add_trace(go.Scatter(
            x=[a3_date], y=[minv*.5]
            , text='Last Data Point'
            , mode='text'
            , showlegend=False
            , hoverinfo='skip'
        ))

        # fig.update_layout(uniformtext_minsize=20, uniformtext_mode='hide')

        fig.update_traces(textposition='top left')

        fig.update_layout(
            hovermode='x',
            showlegend=True
            # , title_text=str('Court Data for ' + str(year))
            , paper_bgcolor=self.transparent
            , plot_bgcolor=self.transparent
            , title='Cook County Bond History (Monthly Totals by Type) | Legislation'
            , xaxis_title = annotation
        )

        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
        ))

        return fig

    def dv1_sentencing_network(self, ingest_df=False, generate_graph=True, annotation = 'By @justinhchae for Chicago Appleseed Center for Fair Courts'):
        df = Reader().to_df('ov1_sentencing.pickle', preview=False)
        # df = df[df['year'] > 2010]
        # df = df[df['year'] < 2021]
        # df = df[df[name.bond_electroinic_monitor_flag_current].notnull()]

        if ingest_df:
            network.ingest_df(df, filename='nx_sentencing')

        if generate_graph:
            G, pos_, edge_widths, scaled_node_values, hubs, judges, sentence_types = network.graph_network(df, filename='nx_sentencing')
            edge_trace = []

            fig = go.Figure()

            for i, node in enumerate(G.nodes()):
                x, y = pos_[node]

                # print(G.nodes(data=True)[node])

                # [x for x in cols if any(i in x for i in bool_types)]

                if node in hubs:
                    fig.add_trace(go.Scatter(
                        x=tuple([x]), y=tuple([y])
                        , name=node
                        , mode='markers'
                        , marker=dict(size=scaled_node_values[i])
                        # , text=node
                        , text=str('Cases ' + str(G.nodes(data=True)[node]['n_cases']))
                        , hoverinfo=['name']
                    ))

                elif node in judges:
                    fig.add_trace(go.Scatter(
                        x=tuple([x]), y=tuple([y])
                        , name=node
                        , mode='markers'
                        , marker=dict(size=scaled_node_values[i], color=self.gray)
                        , text=str('Cases ' + str(G.nodes(data=True)[node]['n_cases']))
                        , hoverinfo=['name+text']
                        , showlegend=False
                    ))


                elif node in sentence_types:

                    fig.add_trace(go.Scatter(

                        x=tuple([x]), y=tuple([y])
                        , name=node
                        , mode='markers'
                        , marker=dict(size=scaled_node_values[i], color=self.blue, line=dict(color='black'), symbol=1)
                        , text=node
                        , hoverinfo=['name+text']
                        , showlegend=False
                        , textposition='top center'

                    ))

                else:
                    fig.add_trace(go.Scatter(
                        x=tuple([x]), y=tuple([y])
                        , name=node
                        , mode='markers'
                        , marker=dict(size=scaled_node_values[i])
                        , text=str('Cases ' + str(G.nodes(data=True)[node]['n_cases']))
                        , hoverinfo=['name']
                        , showlegend=False
                    ))

            #TODO: Add a ghost trace to add judge icon to legend icons

            for i, edge in enumerate(G.edges()):
                n1 = edge[0]
                n2 = edge[1]
                x0, y0 = pos_[n1]
                x1, y1 = pos_[n2]

                fig.add_trace(go.Scatter(
                    x=tuple((x0, x1)),y=tuple((y0, y1))
                    , name=G.edges()[edge]['label']
                    , mode='lines'
                    , line=dict(width=edge_widths[i])
                    , hoverinfo=['name']
                    , showlegend=False

                ))

            fig.update_yaxes(showticklabels=False)
            fig.update_xaxes(showticklabels=False)

            # fig.update_layout(legend=dict(
            #     yanchor="top",
            #     y=0.99,
            #     xanchor="right",
            #     x=0.99,
            # ))

            fig.update_layout(
                showlegend=False
                # , title_text=str('Court Data for ' + str(year))
                , paper_bgcolor=self.transparent
                , plot_bgcolor=self.transparent
                , title='Cook County Courts as a Network of Judges, Courts, and Sentencing Types'
                , xaxis_title=annotation

            )


            return fig








