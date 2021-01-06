import pandas as pd
import os
import re

from clean_data.cleaner import Cleaner
from clean_data.maker import Maker
from do_data.joiner import Joiner
import geopandas




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
                    df = self.cleaner.parse_ids(df, ['case_id', 'case_participant_id'])
                    date_cols = self.cleaner.get_date_cols(df)
                    df = self.cleaner.parse_dates(df, date_cols=date_cols)
                    df = self.cleaner.parse_conversions(df, col_name='offense_category')
                    df = self.cleaner.parse_subset(df, type='initiation')

                    df = self.cleaner.impute_dates(df, col1='event_date', col2='received_date', date_type='initiation')
                    df = self.cleaner.impute_dates(df, col1='felony_review_date', col2='received_date', date_type='initiation')
                    df = self.cleaner.impute_dates(df, col1='arraignment_date', col2='received_date', date_type='initiation')
                    df = self.cleaner.parse_duplicates(df)

                    if classify:
                        df = self.cleaner.classer(df, 'class')
                        df = self.cleaner.classer(df, 'race')
                        df = self.cleaner.classer(df, 'gender')
                        df = self.cleaner.classer(df, 'offense_category')
                        df = self.cleaner.classer(df, 'updated_offense_category')
                        df = self.cleaner.classer(df,
                                                  [ 'charge_id', 'charge_version_id'
                                                  , 'chapter', 'act', 'section', 'aoic'
                                                  , 'event'
                                                  , 'bond_type_initial', 'bond_type_current'
                                                  , 'incident_city'
                                                  , 'law_enforcement_agency', 'law_enforcement_unit'
                                                  , 'felony_review_result'])

                if clean_disposition:
                    df = self.cleaner.parse_cols(df)
                    df = self.cleaner.parse_ids(df, ['case_id', 'case_participant_id'])
                    date_cols = self.cleaner.get_date_cols(df)
                    df = self.cleaner.parse_dates(df, date_cols=date_cols)
                    df = self.cleaner.parse_conversions(df, col_name='offense_category')
                    df = self.cleaner.parse_conversions(df, col_name='disposition_court_name')
                    df = self.cleaner.parse_conversions(df, col_name='disposition_court_facility')
                    df = self.cleaner.parse_subset(df, type='disposition')
                    df = self.cleaner.impute_dates(df, col1='disposition_date', col2='received_date', date_type='disposition')
                    df = self.maker.make_disposition_cats(df, 'charge_disposition')
                    df = self.cleaner.parse_duplicates(df)

                    if classify:
                        df = self.cleaner.classer(df, 'disposition_charged_class')
                        df = self.cleaner.classer(df, 'disposition_court_name')
                        df = self.cleaner.classer(df, 'judge')
                        df = self.cleaner.classer(df, 'offense_category')
                        df = self.cleaner.classer(df, 'updated_offense_category')
                        df = self.cleaner.classer(df,
                                                  [ 'charge_id', 'charge_version_id'
                                                  , 'disposition_charged_chapter', 'disposition_charged_act'
                                                  , 'disposition_charged_section', 'disposition_charged_aoic'
                                                  , 'charge_disposition', 'charge_disposition_reason'
                                                  , 'race', 'gender', 'incident_city'
                                                  , 'law_enforcement_agency', 'law_enforcement_unit'
                                                  , 'felony_review_result'])

                    if derive_data:
                        df = self.maker.make_caselen(df, 'received_date', 'disposition_date')

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

                return df

    def from_pickle(self, filename=None):
        pd.set_option('display.max_columns', None)
        path = os.sep.join([self.root, filename])
        df = pd.read_pickle(path)

        return df