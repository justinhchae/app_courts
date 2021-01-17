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
from analyze_data.metrics import Metrics
from analyze_data.network import Network

reader = Reader()
writer = Writer()
joiner = Joiner()
maker = Maker()
app = Application()
name = Columns()
utils = Utilities()
metrics = Metrics()
tracker = Network()


# tracker.organize()
# tracker.create_membership_table()
# tracker.make_network()

# utils.ov1_initiation()
# utils.ov1_disposition()
# utils.ov1_sentencing()
# utils.dv1_bond()

# metrics.ov1_timeseries()
# metrics.dv1_bond()
metrics.dv1_bond_timeseries()

def parse_em_data():
    cols = ['ir', 'detainee_status', 'detainee_status_date', 'ej_status']
    may_em = reader.to_df('EM_513.csv', clean_em=True, preview=False)
    may_em = maker.make_status_date(may_em, '2020-05-13')
    may_em = maker.make_status(may_em, 'EM')
    may_em = may_em[cols].drop_duplicates()


    may_jail = reader.to_df('Jail_513.csv', clean_jail=True, preview=False)
    may_jail = maker.make_status_date(may_jail, '2020-5-13')
    may_jail = maker.make_status(may_jail, 'Jail')
    may_jail = may_jail[cols].drop_duplicates()

    june_em = reader.to_df('EM_630.csv', clean_em=True, preview=False)
    june_em = maker.make_status_date(june_em, '2020-06-30')
    june_em = maker.make_status(june_em, 'EM')
    june_em = june_em[cols].drop_duplicates()

    june_jail = reader.to_df('Jail_630.csv', clean_jail=True, preview=False)
    june_jail = maker.make_status_date(june_jail, '2020-06-30')
    june_jail = maker.make_status(june_jail, 'Jail')
    june_jail = june_jail[cols].drop_duplicates()

    df = pd.concat([may_em, may_jail, june_em, june_jail])
    df.reset_index(drop=True)

    df.to_csv('data/em_testing.csv', index=False)

# parse_em_data()

# initiation = reader.to_df('Initiation.zip'
#                                   , clean_initiation=True
#                                   , preview=False
#                                   , classify=True
#                                   )


# initiation = reader.to_df('initiation_modified.bz2'
#                                   , preview=False)

# sentencing = reader.to_df('sentencing_modified.bz2'
#                                    , preview=False)
# gui = show(initiation)



