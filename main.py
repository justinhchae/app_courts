from do_data.getter import Reader
from do_data.writer import Writer
from do_data.joiner import Joiner

from clean_data.maker import Maker
# from analyze_data.eda import EDA

from app.app import App

import numpy as np

if __name__ == '__main__':
    reader = Reader()
    writer = Writer()
    joiner = Joiner()
    maker = Maker()
    app = App()
    # eda = EDA()

    def read_source(from_source=False):

        if from_source:
            initiation = reader.to_df('Initiation.zip'
                                      , clean_initiation=True
                                      , preview=False
                                      , classify=True
                                      )
            disposition = reader.to_df('Dispositions.zip'
                                       , clean_disposition=True
                                       , preview=False
                                       , classify=True
                                       )

            initiation = maker.make_disposition_pending(df1=initiation
                                                        , df2=disposition
                                                        , source='received_date'
                                                        , target='disposition_date')

            disposition = maker.make_class_diff(df1=disposition
                                                , df2=initiation
                                                , col1='disposition_charged_class'
                                                , col2='class')

            writer.to_package(initiation, 'initiation_modified')
            writer.to_package(disposition, 'disposition_modified')

        else:

            initiation = reader.to_df('initiation_modified.bz2'
                                      , preview=False)
            disposition = reader.to_df('disposition_modified.bz2'
                                       , preview=False)

            main = joiner.initiation_disposition(initiation, disposition)
            writer.to_package(main, 'main')
            sample = main.sample(n=250000, random_state=0)
            writer.to_package(sample, 'sample')

    # read_source(from_source=False)

    def run_app():
        df = reader.to_df('main.bz2'
                          , preview=False
                          , echo=False
                          , classify=False
                          )

        # FIXME: move memory patches to cleaning routines

        def get_mem(df):
            total_mem = df.memory_usage().sum() / (1024**2)
            # origin total: 272.2295866012573
            # with float32: 246.7372808456421
            # change one col to category: 265.85659408569336
            # + with float 32: 244.00604629516602
            # offense cat as cat: 237.63601398468018
            # after in16: 232.17337703704834
            # categorize charge data: 202.27989768981934
            # with disp court fac: 195.907546043396
            # after disp charged title: 190.4935998916626
            # resolve bool flag: 178.70780563354492

            # int16 is -32768 to +32767
            print(total_mem)


        cols = [ 'bond_amount_initial'
                , 'bond_amount_current', 'age_at_incident'
                , 'disposition_date_days_pending', 'case_length', 'charged_class_difference']

        df['finding_no_probable_cause'] = df['finding_no_probable_cause'].astype('category')

        df[cols] = df[cols].astype('float32')

        cols = ['received_date', 'event_date', 'arraignment_date', 'bond_date_initial'
                ,'bond_date_current', 'incident_begin_date', 'incident_end_date'
                ,'felony_review_date', 'disposition_date']

        # df[cols] = df[cols].astype('datetime64[D]')

        df['offense_category'] = df['offense_category'].astype('category')
        df['charge_count'] = df['charge_count'].astype('int16')

        cols = ['chapter', 'act', 'section', 'class', 'aoic'
              , 'disposition_court_facility', 'disposition_charged_offense_title'
              , 'charge_offense_title'
              ]

        df[cols] = df[cols].astype('category')

        key = {'False': False,
               'True': True,
               'nan': np.nan}

        df['primary_charge_flag_disp'] = df['primary_charge_flag_disp'].map(key)
        df['primary_charge_flag_disp'] = df['primary_charge_flag_disp'].astype('bool')

        # print(df['case_participant_id'].value_counts().size)

        # get_mem(df)

        app.run_app(df)
        #TODO manage large data table, loading entire set creats slow app

    run_app()

    # eda.s3(df)



