
import pandas as pd
import gc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from clean_data.cleaner import Cleaner
from do_data.getter import Reader
from do_data.config import Columns

class Judge():
    def __init__(self):
        self.overview_stats = None
        self.c = Columns()

        self.ordered_charges = ['M', 'X', '1', '2', '3', '4', 'A', 'B', 'C', 'O', 'P', 'Z']
        self.ordered_charges.reverse()

        self.cleaner = Cleaner()
        self.fig = None

        self.transparent = 'rgba(0,0,0,0)'
        self.reader = Reader()

        self.df = self.reader.to_df('subset.bz2'
                                    , preview=False
                                    , echo=False
                                    , classify=False
                                    )

    def overview(self, col):

        title = str('Overview of Court Data by ' + col.title())

        df = self.df.stb.freq([col], cum_cols=False)
        graph = px.bar(df
                       , x=col
                       , y='count'
                       , title=title)

        graph.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell'))
        del df
        gc.collect()

        return graph

    def detail(self, col):

        df = self.df[(self.df[self.c.judge]==col)]
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
        del df
        gc.collect()

        return self.fig

    def _ts_case_len(self, df, row, col):
        """
        https://pbpython.com/pandas-grouper-agg.html
        """
        df = df[[self.c.disposition_date, self.c.case_length]]
        df = df[(df[self.c.disposition_date].notnull())].copy()
        df = df[(df[self.c.case_length] > 0 )].copy()

        counts = df.value_counts()

        df = counts.to_frame().reset_index()
        df.rename(columns={0: 'count'}, inplace=True)

        df = df.groupby([self.c.case_length, pd.Grouper(key=self.c.disposition_date, freq='M')])['count'].sum()
        df = df.to_frame().reset_index()
        df = df.sort_values(self.c.disposition_date)

        self.fig.add_trace(
            go.Scatter(
                x=df[self.c.disposition_date]
                , y=df[self.c.case_length]
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
        df = df[[self.c.disposition_date, self.c.charge_class]].value_counts()
        df = df.to_frame().reset_index()
        df.rename(columns={0: 'count'}, inplace=True)

        df = df.groupby([self.c.charge_class, pd.Grouper(key=self.c.disposition_date, freq='M')])['count'].sum()

        df = df.to_frame().reset_index()

        df = df.groupby(self.c.charge_class)
        
        for name, group in df:
            self.fig.add_trace(
                go.Scatter(x=group[self.c.disposition_date]
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
        df = df[[self.c.judge, self.c.charge_class]].stb.freq([self.c.charge_class], cum_cols=False)[:n]

        # print(df[self.charged_class].dtypes)

        # df[self.charged_class] = df[self.charged_class].astype('category')
        # subset_charges = list(df[self.charged_class].unique())
        # ordered_subset = [i for i in self.ordered_charges if i in subset_charges]
        #
        # df[self.charged_class] = df[self.charged_class].cat.as_ordered()
        # df[self.charged_class] = df[self.charged_class].cat.reorder_categories(ordered_subset, ordered=True)

        color = list(df[self.c.charge_class].cat.codes)
        color.sort()

        self.fig.add_trace(
            go.Bar(x=df[self.c.charge_class]
                   , y=df['count']
                   , marker=dict(color=color)
                   , name="Class"
                   ),
            row=row, col=col
        )

