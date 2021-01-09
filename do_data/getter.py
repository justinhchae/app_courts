import pandas as pd
import os
import re

from clean_data.cleaner import Cleaner
from clean_data.maker import Maker
from do_data.joiner import Joiner
from do_data.config import Columns

name = Columns()

import geopandas

# import ray
# ray.init()
# import modin.pandas as md

# test branch

class Reader():
    def __init__(self, folder='data', display_all_cols=True):
        self.root = folder

        self.cleaner = Cleaner()
        self.maker = Maker()
        self.joiner = Joiner()

        if display_all_cols:
            pd.set_option('display.max_columns', None)

    def to_geo(self, filename, folder='map_data'):
        path = os.sep.join([self.root, folder, filename])
        df = geopandas.read_file(path)

        return df

    def to_df(self
              , filename=None
              , index_col=None
              , usecols=None
              , dtype=None
              , clean_initiation=False
              , clean_disposition=False
              , preview=True
              , classify=True
              , echo=True
              , derive_data=True
              ):

        if not isinstance(filename, str):
            return "Filename should be a string"

        if filename:
            csv = '.csv'
            pickle = '.pickle'
            bz = '.bz2'
            zip = '.zip'

            if csv in filename or zip in filename:
                path = os.sep.join([self.root, filename])

                if echo:
                    print('Reading From:', path)
                    print()

                df = pd.read_csv(path
                                 , index_col=index_col
                                 , usecols=usecols
                                 , dtype=dtype
                                 , low_memory=False
                                 )

                if echo:
                    print('Read dataframe', filename,'of length', len(df))
                    print()

                if preview:
                    print(df.head(2))
                    print()

                if not clean_disposition and not clean_initiation:
                    return "Please indicate type"

                if clean_initiation:
                    df = self.cleaner.parse_cols(df)
                    df = self.cleaner.parse_ids(df, [name.case_id, name.case_participant_id])
                    date_cols = self.cleaner.get_date_cols(df)
                    df = self.cleaner.parse_dates(df, date_cols=date_cols)
                    df = self.cleaner.parse_conversions(df, col_name=name.offense_category)
                    # df = self.cleaner.parse_subset(df, type='initiation')

                    df = self.cleaner.impute_dates(df, col1=name.event_date, col2=name.received_date, date_type='initiation')
                    df = self.cleaner.impute_dates(df, col1=name.felony_review_date, col2=name.received_date, date_type='initiation')
                    df = self.cleaner.impute_dates(df, col1=name.arraignment_date, col2=name.received_date, date_type='initiation')

                    if classify:
                        df = self.cleaner.classer(df, name.charge_class)
                        df = self.cleaner.classer(df, name.race)
                        df = self.cleaner.classer(df, name.gender)

                        df = self.cleaner.classer(df, name.offense_category)
                        df = self.cleaner.classer(df, name.updated_offense_category)

                        df = self.cleaner.classer(df,
                                                  [ name.charge_id
                                                  , name.charge_version_id
                                                  , name.chapter
                                                  , name.act
                                                  , name.section
                                                  , name.aoic
                                                  , name.event
                                                  , name.bond_type_initial
                                                  , name.bond_type_current
                                                  , name.incident_city
                                                  , name.law_enforcement_agency
                                                  , name.law_enforcement_unit
                                                  , name.felony_review_result])

                    df = self.cleaner.reduce_bool_precision(df)
                    df = self.cleaner.reduce_num_precision(df)
                    df = self.cleaner.reduce_nans(df)
                    df = self.cleaner.parse_duplicates(df)

                if clean_disposition:
                    df = self.cleaner.parse_cols(df)
                    df = self.cleaner.parse_ids(df, [name.case_id, name.case_participant_id])
                    date_cols = self.cleaner.get_date_cols(df)
                    df = self.cleaner.parse_dates(df, date_cols=date_cols)

                    df = self.cleaner.parse_conversions(df, col_name=name.offense_category)

                    df = self.cleaner.parse_conversions(df, col_name=name.disposition_court_name)
                    df = self.cleaner.parse_conversions(df, col_name=name.disposition_court_facility)
                    # df = self.cleaner.parse_subset(df, type='disposition')
                    df = self.cleaner.impute_dates(df, col1=name.disposition_date, col2=name.received_date, date_type='disposition')
                    df = self.maker.make_disposition_cats(df, name.charge_disposition)

                    if classify:
                        df = self.cleaner.classer(df, name.disposition_charged_class)
                        df = self.cleaner.classer(df, name.disposition_court_name)
                        df = self.cleaner.classer(df, name.judge)
                        df = self.cleaner.classer(df, name.offense_category)
                        df = self.cleaner.classer(df, name.updated_offense_category)
                        df = self.cleaner.classer(df,
                                                  [ name.charge_id
                                                  , name.charge_version_id
                                                  , name.disposition_charged_chapter
                                                  , name.disposition_charged_act
                                                  , name.disposition_charged_section
                                                  , name.disposition_charged_aoic
                                                  , name.disposition_charged_offense_title
                                                  , name.charge_disposition
                                                  , name.charge_disposition_reason
                                                  , name.race
                                                  , name.gender
                                                  , name.incident_city
                                                  , name.law_enforcement_agency
                                                  , name.law_enforcement_unit
                                                  , name.felony_review_result])

                    if derive_data:
                        df = self.maker.make_caselen(df, name.received_date, name.disposition_date)

                    df = self.cleaner.reduce_bool_precision(df)
                    df = self.cleaner.reduce_num_precision(df)
                    df = self.cleaner.reduce_nans(df)
                    df = self.cleaner.parse_duplicates(df)

                return df

            if pickle in filename or bz in filename:
                path = os.sep.join([self.root, filename])

                if echo:
                    print('Reading From:', path)
                    print()

                df = pd.read_pickle(path)

                if echo:
                    print('Read dataframe of length', len(df))
                    print()

                if preview:
                    print('------ Displaying DataFrame Head')
                    print(df.head(2))
                    print()

                # df = md.DataFrame(df)

                return df

    def from_pickle(self, filename=None):
        pd.set_option('display.max_columns', None)
        path = os.sep.join([self.root, filename])
        df = pd.read_pickle(path)

        return df
