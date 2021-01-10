import pandas as pd
import numpy as np
import os
from do_data.config import Columns
name = Columns()
from do_data.writer import Writer
from clean_data.cleaner import Cleaner
import math

from dateutil.relativedelta import relativedelta

class Maker():
    def __init__(self):
        self.days = np.timedelta64(1, 'D')
        self.year = 365.25
        self.month = 30
        self.week = 7
        self.max_est_life = 124
        self.writer = Writer()
        self.join_cols = ['case_id'
                        , 'case_participant_id'
                        , 'received_date'
                        , 'offense_category'
                        , 'charge_id'
                        , 'charge_version_id'
                        , 'charge_count']
        self.cleaner = Cleaner()
        self.today = pd.Timestamp.now()

    def make_caselen(self, df, col1=None, col2=None):
        df['case_length'] = (df[col2] - df[col1]) / self.days
        return df

    def make_commitment(self, df):
        # https://stackoverflow.com/questions/41719259/how-to-remove-numbers-from-string-terms-in-a-pandas-dataframe
        # https://stackoverflow.com/questions/35376387/extract-int-from-string-in-pandas
        # https://stackoverflow.com/questions/34507883/how-would-i-convert-decimal-years-in-to-years-and-days
        # cols = ['commitment_type'
        #        , 'commitment_term'
        #        , 'commitment_unit'
        #        , 'commitment_dollars'
        #        , 'commitment_weight'
        #        ,  'commitment_days']

        df['commitment_term'] = df['commitment_term'].str.extract('(\d+)').astype('float32')
        df['commitment_unit'] = np.where(df['commitment_type'] == 'Natural Life', 'Natural Life', df['commitment_unit'])

        def from_days(x):
            # tdelta = pd.to_timedelta(x['commitment_term'], unit='d')
            return x['commitment_term']

        def from_years(x):
            try:
                relative_delta = relativedelta(years=x['commitment_term'])
                est_sentence_end = x['sentence_date'] + relative_delta
                est_delta = est_sentence_end - x['sentence_date']
                days = est_delta / self.days
                return days

            except:
                days = x['commitment_term'] * self.year
                return days

        def from_months(x):
            try:
                relative_delta = relativedelta(months=x['commitment_term'])
                est_sentence_end = x['sentence_date'] + relative_delta
                est_delta = est_sentence_end - x['sentence_date']
                days = est_delta / self.days
                return days

            except:
                days = x['commitment_term'] * self.month
                return days

        def from_weeks(x):
            try:
                days =  x['commitment_term'] * self.week
                return days
            except:
                print('error', x['commitment_term'])
                return x['commitment_term']

        def from_hours(x):
            try:
                # years = pd.to_timedelta(x['commitment_term'], unit='Y')
                days =  x['commitment_term'] / 24
                return days
                # diff = relativedelta(years=x)
            except:
                return x['commitment_term']

        def from_lifeterm(x):

            try:
                relative_delta = relativedelta(years=x['age_at_incident'])
                est_born_date = x['sentence_date'] - relative_delta
                est_age_at_sentencing = (x['sentence_date'] - est_born_date) / np.timedelta64(1, 'Y')
                est_life_term_months, est_life_term_years = math.modf(self.max_est_life - est_age_at_sentencing)
                est_life_term_days = round(est_life_term_months * self.year)
                relative_delta = relativedelta(years=int(est_life_term_years), days=est_life_term_days)
                est_sentence_end = x['sentence_date'] + relative_delta
                est_delta = est_sentence_end - x['sentence_date']
                days = est_delta / self.days
                return days
            except:

                return x['commitment_term']

        def from_term(x):
            try:
                relative_delta = relativedelta(months=int(x['commitment_term']))
                est_sentence_end = x['sentence_date'] + relative_delta
                est_delta = est_sentence_end - x['sentence_date']
                days = est_delta / self.days
                return days

            except:
                print('error', x['commitment_term'])
                days = x['commitment_term'] * self.month
                return days

        impute_time = lambda x: \
            from_days(x) if x['commitment_unit'] == 'Days' else \
            from_years(x) if x['commitment_unit'] == 'Year(s)' else \
            from_months(x) if x['commitment_unit'] == 'Months' else \
            from_weeks(x) if x['commitment_unit'] == 'Weeks' else \
            from_hours(x) if x['commitment_unit'] == 'Hours' else \
            from_lifeterm(x) if x['commitment_unit'] == 'Natural Life' else \
            from_term(x) if x['commitment_unit'] == 'Term' else np.nan

        df['commitment_days'] = df.apply(impute_time, axis=1).astype('float32')

        impute_dollars = lambda x: x['commitment_term'] if x['commitment_unit'] == 'Dollars' else np.nan

        df['commitment_dollars'] =  df.apply(impute_dollars, axis=1).astype('float32')

        weight_cols = ['Pounds' 'Ounces' 'Kilos']
        impute_weight = lambda x: x['commitment_term'] if any(i in [x['commitment_unit']] for i in weight_cols) else np.nan

        df['commitment_weight'] = df.apply(impute_weight, axis=1).astype('float32')
        df['life_term'] = np.where(df['commitment_unit'] == 'Natural Life', True, False)
        df['commitment_unit'] = np.where(df['commitment_days'].notnull(), 'Days', df['commitment_unit'])

        # patch when type is Probation but Days are null and units == Year(s)
        df['commitment_unit'] = np.where((df['commitment_type'] == 'Probation') & (df['commitment_days'].isnull()), 'Days', df['commitment_unit'])

        return df

    def make_disposition_cats(self, df, col1=None):

        cat_col = str(col1 + '_cat')

        # col_vals = sorted(df[col1].dropna().tolist())
        # print(set(col_vals))

        key = {'Finding Guilty': 'Finding Guilty'
            , 'Charge Vacated': 'Charge Vacated'
            , 'Case Dismissed': 'Case Dismissed'
            , 'Verdict Guilty - Amended Charge': 'Verdict Guilty'
            , 'Verdict Guilty - Lesser Included': 'Verdict Guilty'
            , 'Nolle Prosecution': 'Nolle Prosecution'
            , 'Finding Guilty But Mentally Ill': 'Finding Guilty'
            , 'FNG': 'Finding Not Guilty'
            , 'Death Suggested-Cause Abated': 'Cause Abated'
            , 'BFW': 'BFW'
            , 'Charge Rejected': 'Charge Rejected'
            , 'Verdict Guilty': 'Verdict Guilty'
            , 'FNPC': 'FNPC'
            , 'Plea Of Guilty': 'Plea of Guilty'
            , 'SOL': 'SOL'
            , 'Nolle On Remand': 'Nolle On Remand'
            , 'Finding Guilty - Amended Charge': 'Finding Guilty'
            , 'Plea of Guilty But Mentally Ill': 'Plea of Guilty'
            , 'Sexually Dangerous Person':'Sexually Dangerous Person'
            , 'Verdict-Not Guilty': 'Verdict Not Guilty'
            , 'Plea of Guilty - Amended Charge': 'Plea of Guilty'
            , 'FNG Reason Insanity': 'Finding Not Guilty'
            , 'Charge Reversed':'Charge Reversed'
            , 'Transferred - Misd Crt':'Transferred - Misd Crt'
            , 'Superseded by Indictment':'Superseded by Indictment'
            , 'Plea of Guilty - Lesser Included': 'Plea of Guilty'
            , 'Finding Not Not Guilty': 'Finding Not Guilty'
            , 'Mistrial Declared': 'Mistrial Declared'
            , 'Verdict Guilty But Mentally Ill': 'Verdict Guilty'
            , 'Hold Pending Interlocutory': 'Hold Pending Interlocutory'
            , 'Finding Guilty - Lesser Included': 'Finding Guilty'
            , 'Withdrawn': 'Withdrawn'
            , 'WOWI': 'WOWI'
            , 'SOLW':'SOLW'
            , np.nan: np.nan
        }

        df[cat_col] = df[col1].map(key)
        df[cat_col] = df[cat_col].astype('category')
        # print(df[cat_col].cat.categories)

        print('------ Mapped Categories for', col1)

        return df

    def make_disposition_pending(self, df1, df2, source=None, target=None):
        new_col = str(target +'_days_pending')
        today = pd.Timestamp.now()

        cols = self.join_cols

        df2_cols = cols.copy()
        df2_cols.append(target)

        df = pd.merge(left=df1, right=df2[df2_cols], how='left', left_on=cols, right_on=cols)

        cols = [name.offense_category, name.charge_offense_title]
        df[cols] = df[cols].astype('category')

        def diff(x):
            s = (today - df[x]) / self.days
            return s

        df[new_col] = np.where(df[target].isna(), diff(source), np.nan)

        change_log = df[['case_id', 'case_participant_id', source, target, new_col]].copy()
        change_log = change_log[(change_log[new_col].notnull())].copy()

        filename = str('change_log_' + new_col)
        self.writer.to_csv(change_log, filename)

        print('------ Calculated Days Pending for', target)

        df.drop(columns=[target], inplace=True)

        df = self.cleaner.reduce_num_precision(df, new_col)
        return df

    def make_class_diff(self, df1, df2, col1, col2, diff_name='charged_class_difference'):

        cols = self.join_cols

        df2_cols = cols.copy()
        df2_cols.append(col2)

        df = pd.merge(left=df1, right=df2[df2_cols], how='left', left_on=cols, right_on=cols)

        temp1 = str(col1 + '_cat_val')
        temp2 = str(col2 + '_cat_val')

        df[temp1] = df[col1].cat.codes
        df[temp2] = df[col2].cat.codes

        df[diff_name] = np.where(df[col2].notnull(), df[temp1] - df[temp2], np.nan)

        change_log = df[[col1, temp1, col2, temp2, diff_name]].copy()

        filename = str('change_log_' + diff_name)

        self.writer.to_csv(change_log, filename)

        print('------ Calculated Charged Class Differential from', str(col2 + ' to ' + col1))

        df = df.drop(columns=[temp1, temp2])
        new_col2 = str('initial_charged_' + col2)
        df.rename(columns={col2:new_col2}, inplace=True)
        
        df = self.cleaner.reduce_num_precision(df, 'charged_class_difference')

        return df



