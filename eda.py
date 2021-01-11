import gc

import pandas as pd
# from pandasgui import show


from application.application import Application
from clean_data.maker import Maker
from do_data.config import Columns
from do_data.getter import Reader
from do_data.joiner import Joiner
from do_data.writer import Writer
from do_data.config import Columns
from analyze_data.utils import Utilities
from analyze_data.metrics import Metrics

reader = Reader()
writer = Writer()
joiner = Joiner()
maker = Maker()
app = Application()
name = Columns()
utils = Utilities()
metrics = Metrics()

# utils.ov1_initiation()
# utils.ov1_disposition()
# utils.ov1_sentencing()

metrics.ov1_timeseries()


# initiation = reader.to_df('Initiation.zip'
#                                   , clean_initiation=True
#                                   , preview=False
#                                   , classify=True
#                                   )



# initiation = reader.to_df('initiation_modified.bz2'
#                                   , preview=False)
# disposition = reader.to_df('disposition_modified.bz2'
#                                    , preview=False)
# sentencing = reader.to_df('sentencing_modified.bz2'
#                                    , preview=False)
# gui = show(initiation)




