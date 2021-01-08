import gc

import pandas as pd

from application.application import Application
from clean_data.maker import Maker
from do_data.config import Columns
from do_data.getter import Reader
from do_data.joiner import Joiner
from do_data.writer import Writer
from do_data.config import Columns

# from analyze_data.eda import EDA


reader = Reader()
writer = Writer()
joiner = Joiner()
maker = Maker()
app = Application()
c = Columns()
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

        judges = pd.DataFrame(main[c.judge].dropna(how='any').unique(), columns=[c.judge])
        writer.to_package(judges, c.judge, compression=False)

        del initiation
        del disposition
        del main
        del sample
        del judges
        gc.collect()

read_source(from_source=True)
