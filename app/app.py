import streamlit as st
import numpy as np
import pandas as pd

import time

from analyze_data.judge import Judge
from analyze_data.charts import Charts

import sys

class App():
    def __init__(self):
        self.st = st
        self.df = None
        self.n_samples = None
        self.judge = 'judge'
        """
        https://discuss.streamlit.io/t/how-to-render-chart-faster/6237
        """

    def run_app(self, df=None):
        if df is not None:
            self.df = df
            self.sample_size()

        self.frame()
        self.frame_objects()
        self.data_disclaimer()

    def sample_size(self):
        n_samples = len(self.df) // 2
        self.n_samples = n_samples

    def frame(self):
        self.st.title('Analyze Cook County Court Data')
        self.st.markdown('An Interactive Dashboard by @justinhchae for Chicago Appleseed *[Alpha Version]*')
        self.st.markdown('[Data Source](https://datacatalog.cookcountyil.gov/browse?category=Courts)')

    def object_overview(self):

        @st.cache(hash_funcs={dict: lambda _: None})
        def get_cached():
            # s = time.time()
            cached_dict = {'n1': Charts().overview(self.df)
                           , 'f1': Charts().overview_figures(self.df, self.n_samples)}
            # e = time.time()
            # print('Get Subplot or narrative from Function', e - s)

            return cached_dict

        cached = get_cached()

        narrative = cached['n1']

        self.st.write('There are a total of',  narrative['total_count']
                      , ' court records based on Initiation and Disposition Court data. '
                      , 'The data spans', narrative['span'], 'years from', narrative['start_date'], 'to', narrative['end_date'] +'.'
                      , 'Court records include data for', narrative['judge_count'], 'judges,'
                      , narrative['initiation_count'], 'types of initiation events,'
                      , narrative['disposition_count'], 'types of disposition events,'
                      , 'approximately ', narrative['cpi'], 'individuals (by case participant id),'
                      , 'and approximately', narrative['case_id'], 'unique cases (by case id)'
                      , 'across', narrative['district_count'], ' primary districts in Cook County.'
                      )

        self.st.plotly_chart(cached['f1'])

    def frame_objects(self):
        self.object_overview()
        # self.by_judge()
        # self.by_initiation()
        # self.by_disposition()
        # self.by_court()

    def by_judge(self):

        @st.cache(hash_funcs={dict: lambda _: None})
        def get_cached():
            s = time.time()
            cached_dict = {'figure1': Judge().overview(df=self.df, col=self.judge)}
            e = time.time()
            # print('Get Overview Figure From Function', e - s)
            return cached_dict

        cached = get_cached()

        if self.st.sidebar.checkbox(label="Show Analysis by Judge"
                                 , value=False
                                 , key=self.judge):

            self.st.markdown('Judge Narrative - High Level')

            s = time.time()
            self.st.plotly_chart(cached['figure1'])
            e = time.time()
            # print('Get Overview Figure from Cache', e - s)

            sidebar_picklist = self.df[self.judge].dropna(how='any').unique()

            sidebar_selection = self.st.sidebar.selectbox('Select a Judge', sidebar_picklist)

            if sidebar_selection:
                self.st.markdown('Judge Narrative - Detail Level')
                self.st.write(sidebar_selection)

                if sidebar_selection in cached:
                    s = time.time()
                    self.st.plotly_chart(cached[sidebar_selection])
                    e = time.time()
                    # print('Get Sidebar Selection from Cache', e - s)
                else:
                    s = time.time()
                    figure = Judge().detail(df=self.df, col=sidebar_selection)
                    e = time.time()
                    # print('Get Sidebar Selection from Function', e - s)
                    self.st.plotly_chart(figure)
                    cached.update({sidebar_selection:figure})

    def by_initiation(self):
        #TODO
        # if self.st.sidebar.checkbox(label="Show Analysis by Initiation"
        #         , value=True
        #         , key='event'):
        #     self.st.write(self.df['event'].dropna(how='any').unique())
        pass

    def by_disposition(self):
        # TODO
        pass

    def by_court(self):
        # TODO
        pass

    @st.cache
    def data(self):
        """
        Converts all categorical columns to object types.
        Only use if writing dataframe to page. Otherwise avoid usage due to memory problems when converting from cat to obj.
        """

        @st.cache
        def data_fixer():

            col_types = self.df.dtypes.to_frame()
            col_types = col_types.rename_axis('col_name').reset_index().rename(columns={0: 'dtype'})

            col_types = col_types[(col_types['dtype'] == 'category')]
            col_list = col_types['col_name'].to_list()

            self.df[col_list] = self.df[col_list].astype('object')

        s = time.time()
        data_fixer()
        e = time.time()
        # print('Fix Data', e - s)

    def data_disclaimer(self):
        self.st.markdown('"This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago.  The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site.  The data provided at this site is subject to change at any time.  It is understood that the data provided at this site is being used at one’s own risk."')
