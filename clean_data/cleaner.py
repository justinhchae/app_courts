import pandas as pd
import numpy as np
import re
import string

import os

# import matplotlib.pyplot as plt

import time

from do_data.writer import Writer

class Cleaner():
    def __init__(self):
        self.timedelta = np.timedelta64(1, 'h')
        self.writer = Writer()
        # self.filename = os.sep.join(['data', 'file.csv'])
        # self.path = os.environ['PWD'] + os.sep + self.filename
        self.log = []

    def parse_geo(self, df, type):
        pass

    def parse_duplicates(self, df, cols=None):

        start = len(df)
        df = df.drop_duplicates(subset=cols, ignore_index=True)
        end = len(df)
        count = start-end

        print('------ Dropped Duplicate Records:', count)

        return df

    def get_date_cols(self, df):
        date_pattern = r'_date'
        date_cols = [c for c in df.columns if re.search(date_pattern, c)]
        return date_cols

    def classer(self, df, col_name, echo=False):
        if echo:
            print('------ Classifying to Categorical:', col_name)

        def reverse(lst):
            lst.reverse()
            return lst

        if col_name == 'offense_category' or col_name == 'updated_offense_category':
            df[col_name] = df[col_name].str.strip()
            df[col_name] = df[col_name].str.upper()
            df[col_name] = df[col_name].astype('category')

        if col_name == 'charge_class' or col_name == 'class' or col_name == 'disposition_charged_class':
            ordered_charges = ['M', 'X', '1', '2', '3', '4', 'A', 'B', 'C', 'O', 'P', 'Z']
            ordered_charges.reverse()

            df[col_name] = df[col_name].str.strip()

            start = len(df)
            df = df[~(df[col_name] == 'U')].copy()
            end = len(df)

            diff = start-end
            if echo:
                print('------ Dropped Records with U:', str(diff))

            df[col_name] = df[col_name].astype('category')
            df[col_name] = df[col_name].cat.as_ordered()
            df[col_name] = df[col_name].cat.reorder_categories(ordered_charges, ordered=True)

        if col_name == 'disposition_court_name':
            df[col_name] = df[col_name].str.strip()
            df[col_name] = df[col_name].str.title()
            # df = df[df[col_name] != 'Traffic']
            # df = df[~(df[col_name] == 'Traffic')].copy()
            # print('------ Dropped Records with Traffic Court Category')
            # df[col_name] = df[col_name].fillna(value='Court Not Specified')

            df[col_name] = df[col_name].astype('category')

        if col_name == 'race':
            df[col_name] = df[col_name].str.strip()
            df[col_name] = df[col_name].str.title()
            # df[col_name] = df[col_name].fillna(value='None')
            df[col_name] = df[col_name].astype('category')

        if col_name == 'gender':
            key = {'Unknown Gender': 'Unknown'}
            df[col_name] = df[col_name].str.strip()
            df[col_name] = df[col_name].str.title()
            df[col_name] = df[col_name].map(key)
            df[col_name] = df[col_name].astype('category')

        if col_name == 'judge':
            # df[col_name] = df[col_name].fillna(value='Judge Not Specified')
            df[col_name] = df[col_name].str.strip()
            df[col_name] = df[col_name].str.replace('\.', '')
            df[col_name] = df[col_name].str.replace('\s+', ' ')
            df[col_name] = df[col_name].str.title()

            df['temp'] = df[col_name].str.contains(',', na=False)
            df['names'] = np.where(df['temp'] == True, df[col_name].str.split(','), df[col_name])

            temp = df[(df['temp'] == True)]
            names = temp['names'].tolist()

            backwards = [list(x) for x in set(tuple(x) for x in names)]
            x1 = [', '.join(str(c).strip() for c in s) for s in backwards]

            forwards = [reverse(x) for x in backwards]
            x2 = [' '.join(str(c).strip() for c in s) for s in forwards]

            key = {x1[i]: x2[i] for i in range(len(x1))}

            df['judge'] = np.where(df['temp'] == True, df['judge'].map(key, na_action='ignore'), df['judge'])
            df['judge'] = df['judge'].astype('category')

            df = df.drop(columns=['names', 'temp'])

        if isinstance(col_name, list):
            for col in col_name:
                if not isinstance(df[col], str):
                    df[col] = df[col].astype(str)

                df[col] = df[col].str.strip()
                # df[col] = df[col].fillna(value='None')
                df[col] = df[col].astype('category')

        return df

    def parse_conversions(self, df, col_name):

        start = len(df)

        df[col_name] = df[col_name].str.title()

        cond1 = df[col_name] != 'Promis Conversion'
        df = df[cond1]

        cond2 = df[col_name] != 'Promis'
        df = df[cond2]

        end = len(df)
        count = str(start-end)

        print('------ Filtered PROMIS Conversions: ', len(df))
        print('--------- Removed', count, 'records')


        return df

    def parse_primary_charge(self, df):
        df = df[~(df['primary_charge_flag'] == False)]
        print('------ Filtered primary charges: ', len(df))
        return df

    def parse_cols(self, df):
        print('------ Parsing columns text with lower string and underscores')
        df.columns = map(str.lower, df.columns)
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('-', '_')
        return df

    def parse_subset(self, df, cols=None, type='initiation'):

        columns = list(df.columns)

        if type == 'initiation':
            columns = [
                'case_id'
                , 'case_participant_id'
                , 'received_date'
                , 'offense_category'
                , 'primary_charge_flag'
                , 'charge_id'
                , 'charge_version_id'
                , 'charge_offense_title'
                , 'charge_count'
                , 'chapter'
                , 'act'
                , 'section'
                , 'class'
                , 'aoic'
                , 'event'
                , 'event_date'
                , 'finding_no_probable_cause'
                , 'arraignment_date'
                , 'bond_date_initial'
                , 'bond_date_current'
                , 'bond_type_initial'
                , 'bond_type_current'
                , 'bond_amount_initial'
                , 'bond_amount_current'
                , 'bond_electronic_monitor_flag_initial'
                , 'bond_electroinic_monitor_flag_current'
                , 'age_at_incident'
                , 'race'
                , 'gender'
                , 'incident_city'
                , 'incident_begin_date'
                , 'incident_end_date'
                , 'law_enforcement_agency'
                , 'law_enforcement_unit'
                , 'arrest_date'
                , 'felony_review_date'
                , 'felony_review_result'
                , 'updated_offense_category'
            ]

        if type == 'disposition':
            columns = [
                'case_id'
                , 'case_participant_id'
                , 'received_date'
                , 'offense_category'
                , 'primary_charge_flag'
                , 'charge_id'
                , 'charge_version_id'
                , 'disposition_charged_offense_title'
                , 'charge_count'
                , 'disposition_date'
                , 'disposition_charged_chapter'
                , 'disposition_charged_act'
                , 'disposition_charged_section'
                , 'disposition_charged_class'
                , 'disposition_charged_aoic'
                , 'charge_disposition'
                , 'charge_disposition_reason'
                , 'judge'
                , 'disposition_court_name'
                , 'disposition_court_facility'
                , 'age_at_incident'
                , 'race'
                , 'gender'
                , 'incident_city'
                , 'incident_begin_date'
                , 'incident_end_date'
                , 'law_enforcement_agency'
                , 'law_enforcement_unit'
                , 'arrest_date'
                , 'felony_review_date'
                , 'felony_review_result'
                , 'arraignment_date'
                , 'updated_offense_category'
            ]

        df = df[columns]
        return df

    def impute_dates(self, df, col1=None, col2=None, date_type=None):
        """
        assumptions:
        1. if event date greater than this year + 1, it is a mistake and the year should be the same year as received
        2. if event date less than 2011, it is a mistake and should be same as received year
        3.
        """
        today = pd.Timestamp.now()
        curr_year = today.year
        past_year = 2010
        change_log = []
        col_new = str(col1 + '_new')

        if date_type == 'initiation':

            if col1 == 'event_date' or col1 == 'felony_review_date' or col1 == 'arraignment_date':

                impute = lambda x: x[col1].replace(year=x[col2].year) if x[col1].year > curr_year \
                        else x[col1].replace(year=x[col2].year) if x[col1].year < past_year \
                        else x[col1]

                df[col_new] = df.apply(impute, axis=1)

                change_log = df[(df[col1].dt.year > curr_year)]

                filename = str('change_log_' + col1 + '_dates')
                self.writer.to_csv(df=change_log, filename=filename)

                print('------ Impute Dates for', col1, 'given', col2, ' ', len(df))

                df[col1] = df[col_new]

                df = df.drop(columns=col_new)

        if date_type == 'disposition':

            if col1 == 'disposition_date':

                df['diff'] = (df[col1] - df[col2]) / self.timedelta
                df['diff'] = df['diff'].rolling(100, min_periods=1).median()

                def new(x):
                    new = x[col2] + pd.to_timedelta(x['diff'], unit='h')
                    return new

                impute = lambda x: new(x) if x[col1] > today else x[col1]
                df[col_new] = df.apply(impute, axis=1)

                change_log = df[(df[col1].dt.year > curr_year)]
                filename = str('change_log_' + col1 + '_dates')
                self.writer.to_csv(df=change_log, filename=filename)

                print('------ Impute Dates:', col1, ' ', len(df))

                df[col1] = df[col_new]

                df = df.drop(columns=[col_new, 'diff'])

        return df

    def parse_dates(self, df, date_cols, timedelta=None, parse_dates=None):
        # filter erroneous dates where arrest date < received in lock up < released from lockup
        print('------ Parsing dates columns')

        if date_cols is None:
            return 'Need Date Cols'

        # if timedelta is None:
        #     timedelta = self.timedelta

        for col in date_cols:
            print('--------', col)

            df[col] = pd.to_datetime(df[col],
                                     errors='coerce',
                                     infer_datetime_format=False)

        return df

    def parse_ids(self, df, cols):
        df[cols] = df[cols].astype('str')
        return df

