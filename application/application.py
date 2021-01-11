import streamlit as st

from analyze_data.judge import Judge
from analyze_data.charts import Charts
from application.ov1 import OV_1
from do_data.getter import Reader

ov1 = OV_1()

class Application():
    def __init__(self):
        self.st = st
        self.df = None
        self.judge_names = Reader().to_df('judges.pickle', preview=False, echo=False, classify=False)
        self.n_samples = None
        self.judge = 'judge'
        """
        https://discuss.streamlit.io/t/how-to-render-chart-faster/6237
        https://discuss.streamlit.io/t/this-app-has-gone-over-its-resource-limits/7334/4
        """

    def run_app(self):
        # if df is not None:
        #     self.df = df
        #     self.sample_size()

        self.frame()
        self.overview()
        self.data_disclaimer()

    def frame(self):
        self.st.title('Analyze Cook County Court Data')
        self.st.markdown('An Interactive Dashboard by @justinhchae for Chicago Appleseed *[Alpha Version]*')

    def overview(self):
        self.object_overview()

    # @st.cache(hash_funcs={dict: lambda _: None}, max_entries=10, ttl=3600)
    def overview_data(self):
        # s = time.time()
        cached_dict = {'f1': Charts().overview_figures()}
        # e = time.time()
        # print('Get Subplot or narrative from Function', e - s)
        return cached_dict

    def object_overview(self):

        self.st.write('Cook county is the largest county in the United States by population and has millions of court records available for analysis.',
                      'In addition to size, Cook County is also the home county for Chicago and surrounding areas. The availability of this data, at scale, provides interesting analytical opportunities.'
                      )

        self.st.write('The court system is comprised of at least five phases that include Intake, Initiation, Dispositions, Sentencing, Diversions.',
                      'Out of the five phases, this dashboard currently processes Initiation, Disposition, and Sentencing phases.')

        self.st.plotly_chart(ov1.court_initiation())

        self.st.markdown('All source code, and cleaned data available in a [GitHub Respository](https://github.com/justinhchae/app_courts/tree/main/data)')

        self.st.write('Across all phases, cases are uniquely identified by Case IDs. In each case, there may be one or more individuals that are party to the case, given by Case Participant ID.',
                      'To provide high-level insights into court volumes, this dataset is filtered to identify aggregated measures of unique cases and individuals.',
                      'For instance, for what might be considered a sigular event, a person may be charged with multiple allegations and multiple counts of a given crime.',
                      'Although the severity of such circumstances is not taken lightly, counting each of these instances may overstate a characterization of court volumes.',
                      'As a result, to avoid double-counting, this analysis filters Initiation and Disposition records in two key ways.')

        self.st.write('For Initiation Events, the original source table of approximately 1 million records is reudce to about 350k records where the Primary Charge Flag == True.',
                      'For Disposition Hearings, the original source table of approximately 700k reocrds is reduced to about 350k records by the most severe charge in the case.',
                      'For example, in Initiation Events, the most severe criminal charge or allegation is usually the most severe charge if there are multiple counts and multiple charges.',
                      'In another example for Disposition Hearings, the most severe charge may not be the primary charge due to pleadings and other intricacies of the court system.',
                      )

    def frame_objects(self):
        self.object_overview()
        self.by_judge()
        # self.by_initiation()
        # self.by_disposition()
        # self.by_court()

    # @st.cache(hash_funcs={dict: lambda _: None}, max_entries=10, ttl=3600)
    @st.cache(max_entries=10, ttl=3600)
    def judge_data(self):
        # s = time.time()
        # cached_dict = {'figure1': Judge().overview(col=self.judge)}
        # e = time.time()
        # print('Get Overview Figure From Function', e - s)
        fig = Judge().overview(col=self.judge)
        return fig #cached_dict

    def by_judge(self):
        # cached = self.judge_data()

        if self.st.sidebar.checkbox(label="Show Analysis by Judge"
                                 , value=False
                                 , key=self.judge):

            self.st.markdown('Judge Narrative - High Level')

            # s = time.time()
            # self.st.plotly_chart(cached['figure1'])
            self.st.plotly_chart(self.judge_data())
            # e = time.time()
            # print('Get Overview Figure from Cache', e - s)

            sidebar_picklist = self.judge_names[self.judge]

            sidebar_selection = self.st.sidebar.selectbox('Select a Judge', sidebar_picklist)

            if sidebar_selection:
                self.st.markdown('Judge Narrative - Detail Level')
                self.st.write(sidebar_selection)
                self.st.plotly_chart(Judge().detail(col=sidebar_selection))

                # TODO Update Cached figures from sidebar selection
                # if sidebar_selection in cached:
                #     # s = time.time()
                #     self.st.plotly_chart(cached[sidebar_selection])
                #     # e = time.time()
                #     # print('Get Sidebar Selection from Cache', e - s)
                # else:
                #     # s = time.time()
                #     figure = Judge().detail(col=sidebar_selection)
                #     # e = time.time()
                #     # print('Get Sidebar Selection from Function', e - s)
                #     self.st.plotly_chart(figure)
                #     cached.update({sidebar_selection:figure})

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

        # s = time.time()
        data_fixer()
        # e = time.time()
        # print('Fix Data', e - s)

    def data_disclaimer(self):
        self.st.write('This site is under construction and active analysis. Please stop by again for future updates!')
        self.st.markdown('[Cook County Data Source](https://datacatalog.cookcountyil.gov/browse?category=Courts)')
        self.st.markdown('"This site provides applications using data that has been modified for use from its original source, www.cityofchicago.org, the official website of the City of Chicago.  The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site.  The data provided at this site is subject to change at any time.  It is understood that the data provided at this site is being used at one’s own risk."')
