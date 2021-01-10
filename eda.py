import gc

import pandas as pd
from pandasgui import show


from application.application import Application
from clean_data.maker import Maker
from do_data.config import Columns
from do_data.getter import Reader
from do_data.joiner import Joiner
from do_data.writer import Writer
from do_data.config import Columns


reader = Reader()
writer = Writer()
joiner = Joiner()
maker = Maker()
app = Application()
name = Columns()


# initiation = reader.to_df('Initiation.zip'
#                                   , clean_initiation=True
#                                   , preview=False
#                                   , classify=True
#                                   )
#
# disposition = reader.to_df('Dispositions.zip'
#                            , clean_disposition=True
#                            , preview=False
#                            , classify=True
#                            )
#
# initiation = maker.make_disposition_pending(df1=initiation
#                                             , df2=disposition
#                                             , source='received_date'
#                                             , target='disposition_date')
#
# disposition = maker.make_class_diff(df1=disposition
#                                     , df2=initiation
#                                     , col1='disposition_charged_class'
#                                     , col2='class')
#
# main = joiner.initiation_disposition(initiation, disposition)

df = reader.to_df('Sentencing.zip', preview=False, clean_sentencing=True)

cols = ['commitment_type'
       , 'commitment_days'
       , 'commitment_unit'
       , 'commitment_dollars'
       , 'commitment_weight'
       , 'life_term'
       # , 'commitment_unit_new'
        ]
gui = show(df)

