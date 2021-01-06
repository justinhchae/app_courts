import streamlit as st
import numpy as np
import pandas as pd

from analyze_data.judge import Judge
from analyze_data.charts import Charts

class App():
    def __init__(self):
        self.st = st
        self.df = None
        self.df_sample = None

        self.judge = 'judge'
        """
        https://discuss.streamlit.io/t/how-to-render-chart-faster/6237
        """

    def run_app(self, df=None):
        if df is not None:
            self.df = df
            self.data()
        self.frame()
        self.frame_objects()
        self.data_disclaimer()

    def frame(self):
        self.st.title('Analyze Cook County Court Data')
        self.st.markdown('An Interactive Dashboard by @justinhchae for Chicago Appleseed *[Alpha Version]*')
        self.st.markdown('[Data Source](https://datacatalog.cookcountyil.gov/browse?category=Courts)')


    def object_overview(self):

        @st.cache(hash_funcs={dict: lambda _: None})
        def get_cached():
            print('got figs overview')
            cached_dict = {'figure1': Charts().overview_figures(self.df)
                        ,'narrative1': Charts().overview(self.df)}
            return cached_dict

        cached = get_cached()

        narrative = cached['narrative1']

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

        self.st.plotly_chart(cached['figure1'])

    def frame_objects(self):
        self.object_overview()
        self.by_judge()
        self.by_initiation()
        self.by_disposition()
        self.by_court()


    def by_judge(self):

        @st.cache(hash_funcs={dict: lambda _: None})
        def get_cached():
            cached_dict = {'figure1': Judge().overview(df=self.df, col=self.judge)}
            return cached_dict

        cached = get_cached()

        if self.st.sidebar.checkbox(label="Show Analysis by Judge"
                                 , value=False
                                 , key=self.judge):

            self.st.markdown('Judge Narrative - High Level')

            self.st.plotly_chart(cached['figure1'])

            sidebar_picklist = self.df[self.judge].dropna(how='any').unique()

            sidebar_selection = self.st.sidebar.selectbox('Select a Judge', sidebar_picklist)

            if sidebar_selection:
                self.st.markdown('Judge Narrative - Detail Level')
                self.st.write(sidebar_selection)

                if sidebar_selection in cached:
                    self.st.plotly_chart(cached[sidebar_selection])
                else:
                    figure = Judge().detail(df=self.df, col=sidebar_selection)
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

    
    def data(self):

        @st.cache
        def data_fixer():

            col_types = self.df.dtypes.to_frame()
            col_types = col_types.rename_axis('col_name').reset_index().rename(columns={0: 'dtype'})

            col_types = col_types[(col_types['dtype'] == 'category')]
            col_list = col_types['col_name'].to_list()

            self.df[col_list] = self.df[col_list].astype('object')

        data_fixer()

    def data_disclaimer(self):
        self.st.markdown('"This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago.  The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site.  The data provided at this site is subject to change at any time.  It is understood that the data provided at this site is being used at one’s own risk."')




