import gc

import pandas as pd

from application.application import Application
from clean_data.maker import Maker
from do_data.config import Columns
from do_data.getter import Reader
from do_data.joiner import Joiner
from do_data.writer import Writer
from do_data.config import Columns
from analyze_data.utils import Utilities

reader = Reader()
writer = Writer()
joiner = Joiner()
maker = Maker()
app = Application()
name = Columns()
sub_utils = Utilities()


def read_source(from_source=False, write=True, process_subsets=True):

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

        sentencing = reader.to_df('Sentencing.zip', preview=False, clean_sentencing=True)

        if write:
            writer.to_package(disposition, 'disposition_modified')
            writer.to_package(initiation, 'initiation_modified')
            writer.to_package(sentencing, 'sentencing_modified')

            if process_subsets:
                sub_utils.ov1_initiation()
                sub_utils.ov1_disposition()
                sub_utils.ov1_sentencing()
                sub_utils.dv1_bond()

        del initiation
        del disposition
        del sentencing
        gc.collect()

    else:

        initiation = reader.to_df('initiation_modified.bz2'
                                  , preview=False)
        disposition = reader.to_df('disposition_modified.bz2'
                                   , preview=False)
        sentencing = reader.to_df('sentencing_modified.bz2'
                                   , preview=False)

        main = joiner.initiation_disposition(initiation, disposition)
        main_new = joiner.make_main(df=[initiation, disposition, sentencing])

        if write:
            writer.to_package(main, 'main')
            sample = main.sample(250000, random_state=0)
            writer.to_package(sample, 'sample')
            writer.to_package(main_new, 'main_new')

        judges = pd.DataFrame(main[name.judge].dropna(how='any').unique(), columns=[name.judge])

        if write:
            writer.to_package(judges, name.judge, compression=False)

        usecols = ['case_id'
                    , 'case_participant_id'
                    , 'primary_charge_flag_init'
                    , 'class'
                    , 'received_date'
                    , 'event'
                    , 'judge'
                    , 'disposition_court_name'
                    , 'disposition_court_facility'
                    , 'charge_disposition'
                    , 'case_length'
                    , 'disposition_date'
                    , 'disposition_date_days_pending']

        subset = main[usecols]

        if write:
            writer.to_package(subset, 'subset')

        # print(main.dtypes)

        del main
        del main_new
        gc.collect()

read_source(from_source=True, write=True, process_subsets=True)
