import pandas as pd
import numpy as np
import os

from do_data.writer import Writer

class Maker():
    def __init__(self):
        self.days = np.timedelta64(1, 'D')
        self.writer = Writer()
        self.join_cols = ['case_id'
                        , 'case_participant_id'
                        , 'received_date'
                        , 'offense_category'
                        , 'charge_id'
                        , 'charge_version_id'
                        , 'charge_count']

    def make_caselen(self, df, col1=None, col2=None):

        df['case_length'] = (df[col2] - df[col1]) / self.days

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

        return df



