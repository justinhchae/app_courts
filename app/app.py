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

        narrative = Charts().overview(self.df)
        self.st.write('There are a total of',  narrative['total_count']
                      , ' court records that have both an Initiation Event and a Disposition Hearing record. '
                      , 'The data spans', narrative['span'], 'years from', narrative['start_date'], 'to', narrative['end_date'] +'.'
                      , 'Court records include data for', narrative['judge_count'], 'judges,'
                      , narrative['initiation_count'], 'types of initiation events,'
                      , narrative['disposition_count'], 'types of disposition events,'
                      , 'approximately ', narrative['cpi'], 'individuals (by case participant id),'
                      , 'and approximately', narrative['case_id'], 'unique cases (by case id)'
                      , 'across the', narrative['district_count'], 'districts in Cook County.'
                      )

        chart = Charts().overview_figures(self.df)

        self.st.plotly_chart(chart)

    def frame_objects(self):

        self.object_overview()

        if self.st.sidebar.checkbox(label="Show Analysis by Judge"
                                 , value=False
                                 , key=self.judge):

            self.st.plotly_chart(Judge().overview(df=self.df, col=self.judge))

            sidebar_picklist = self.df[self.judge].dropna(how='any').unique()

            sidebar_selection = self.st.sidebar.selectbox('Select a Judge', sidebar_picklist)

            if sidebar_selection:
                # self.st.markdown('Section Text or Title...')
                self.st.write(sidebar_selection)
                self.st.plotly_chart(Judge().detail(df=self.df, col=sidebar_selection))


            # self.st.write(picks)

        # if self.st.sidebar.checkbox(label="Show Analysis by Initiation"
        #         , value=True
        #         , key='event'):
        #     self.st.write(self.df['event'].dropna(how='any').unique())


    # @st.cache
    def data(self):

        def data_fixer():
            col_types = self.df.dtypes.to_frame()
            col_types = col_types.rename_axis('col_name').reset_index().rename(columns={0: 'dtype'})

            col_types = col_types[(col_types['dtype'] == 'category')]
            col_list = col_types['col_name'].to_list()

            self.df[col_list] = self.df[col_list].astype('object')

        # self.df = df
        # self.df = df.sample(1000, random_state=0)
        data_fixer()


    def data_disclaimer(self):
        self.st.markdown('"This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago.  The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site.  The data provided at this site is subject to change at any time.  It is understood that the data provided at this site is being used at one’s own risk."')




