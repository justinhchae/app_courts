import streamlit as st

from analyze_data.judge import Judge
from analyze_data.charts import Charts
from application.ov1 import OV_1
from application.bond_tree import BondTree
from application.footer import Footer
from do_data.getter import Reader

ov1 = OV_1()

class Application():
    def __init__(self):
        self.st = st
        self.sidebar_picklist = ['Featured: COVID Cliff','Bond Data']

        self.sidebar_selection = self.st.sidebar.selectbox('Select Analysis', self.sidebar_picklist)

        # self.bond_box = self.st.sidebar.checkbox(label="Bond Data"
        #                          , value=False
        #                          , key='bond_tree')
        #
        # self.featured = self.st.sidebar.checkbox(label="Featured Analysis"
        #                          , value=True
        #                          , key='covid_cliff')
        self.df = None
        self.judge_names = Reader().to_df('judges.pickle', preview=False, echo=False, classify=False)
        self.n_samples = None
        self.judge = 'judge'
        """
        https://discuss.streamlit.io/t/how-to-render-chart-faster/6237
        https://discuss.streamlit.io/t/this-app-has-gone-over-its-resource-limits/7334/4
        """

    def run_app(self):

        self.frame()

        def footer(key):
            # st.subheader('Disclaimer and Notices')
            # self.data_disclaimer()
            Footer().data_disclaimer()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("Disclaimer and Notices", expanded=False)
        with my_expander:
            clicked = footer("second")

    def frame(self):
        self.st.title('Analysis of Cook County Court Data')
        self.st.markdown('Interactive Visualization by @justinhchae for Chicago Appleseed Center for Fair Courts')

        def header(key):
            st.subheader('About This Data')
            self.overview()
            # clicked = st.button("Click me " + key)

        my_expander = st.beta_expander("About Data Overview (Click to Expand)", expanded=False)
        with my_expander:
            clicked = header("first")

        self.bond_data()

        if self.sidebar_selection == 'Featured: COVID Cliff':
            self.st.write(
                'In 2020, the COVID-19 Pandemic brought the world to a grinding halt across all sectors of business and government.',
                'Similarly, court systems reduced their availability and services while doing their part to support public health measures.',
                'However, unlike schools and businesses, some court systems have struggled to resume operations.',
                'The result, so far, has been a growing backlog of cases as individuals wait on the courts.')

            self.st.markdown('**The COVID Court Cliff**')

            self.st.write('Exactly how many cases are in the backlog? It depends on which phase of the court system you are investigating.',
                          'On a monthly basis over the past 10 years; however, the backlog may be the difference between the projected trend (given by a logistic regression) and an actual count of cases.',
                          )

            self.st.plotly_chart(ov1.timeseries())

            self.st.write('As one example of court volume and backlog over time, Cook County courts has seen a severe drop-off in cases across multiple phases of the system.',
                          'In 2020, Cook County managed to process about half as many cases in prior years (at best).',
                          'For instance, monthly court volumes are down as much as 90% on a monthly basis.')

            self.st.markdown('**The Issue**')

            self.st.write('Given the opportunity for alternative remote hearings (i.e. "Zoom Courts"), at issue is whether courts are not meeting their obligation to process cases during the Pandemic.',
                          'As just one example of the impact of delayed court proceedings, individuals, who have yet to be convicted of any crime, remain in limbo while waiting on the courts.',
                          'In some cases, people are in some form of incarceration (Jail or Electronic Monitoring) or are anxiously waiting for their day in court.',
                          'This dashboard might answer questions regarding the operation of the courts over time.'
                          )
            # self.st.sidebar.checkbox('Bond Data', value=False)

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

        self.st.markdown('**Data Overview**')

        self.st.write('Cook county is the largest county in the United States by population and has millions of court records available for analysis.',
                      'In addition to size, Cook County is also the home county for Chicago and surrounding areas.',
                      'The availability of this data, at scale, provides interesting analytical opportunities to support public awareness of the court system.',
                      'Although the source data is publicly available, the raw data is split into different sections and is difficult to interpret without significant engineering.',
                      'This dashboard represents the results of a processed and ready-to-analyze dataset about the courts.'
                      )

        if self.sidebar_selection != 'Bond Data':
            self.st.markdown('**Initiation - Disposition - Sentencing**')

            self.st.write(
                'The court system is comprised of at least five phases that include Intake, Initiation, Dispositions, Sentencing, Diversions.',
                'Out of the five phases, this dashboard currently processes Initiation, Disposition, and Sentencing phases.',
                )

            year = self.st.select_slider('Slide to Filter data by Year', options=['All Time', 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011])
            self.st.plotly_chart(ov1.court_counts(year))

    # @st.cache(hash_funcs={dict: lambda _: None}, max_entries=10, ttl=3600)
    @st.cache(max_entries=10, ttl=3600)
    def judge_data(self):
        # s = time.time()
        # cached_dict = {'figure1': Judge().overview(col=self.judge)}
        # e = time.time()
        # print('Get Overview Figure From Function', e - s)
        fig = Judge().overview(col=self.judge)
        return fig #cached_dict

    def bond_data(self):

        if self.sidebar_selection == 'Bond Data':
            BondTree().bond_data()

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