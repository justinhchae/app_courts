import pandas as pd
import numpy as np
import os
import re

from clean_data.cleaner import Cleaner
from clean_data.maker import Maker

class Joiner():
    def __init__(self):
        self.cleaner = Cleaner()
        self.maker = Maker()
        self.join_cols = [
              'case_id'
            , 'case_participant_id'
            , 'received_date'
            , 'offense_category'
            , 'charge_id'
            , 'charge_version_id'
            , 'charge_count'
            , 'arraignment_date'
            , ]

    def initiation_disposition(self, df1, df2):
        cols = self.join_cols

        df1_cols = ['gender']
        df2_cols = ['age_at_incident'
                    , 'race'
                    , 'incident_city', 'incident_begin_date'
                    , 'incident_end_date', 'law_enforcement_agency', 'law_enforcement_unit'
                    , 'arrest_date', 'felony_review_date', 'felony_review_result']

        df1 = df1.drop(columns=df1_cols)
        df2 = df2.drop(columns=df2_cols)


        df = pd.merge(left=df1, right=df2, how='left', left_on=cols, right_on=cols
                      , suffixes=('_init', '_disp')
                      )

        initiation_charge_cols = ['act', 'section', 'class', 'aoic', 'chapter']
        disposition_charge_cols = ['disposition_charged_act', 'disposition_charged_section', 'disposition_charged_class', 'disposition_charged_aoic', 'disposition_charged_chapter']

        charge_cols = tuple(zip(initiation_charge_cols, disposition_charge_cols))

        for col in charge_cols:
            df[col[0]] = np.where(df[col[1]].notnull(), df[col[1]], df[col[0]])

        df = df.drop(columns=disposition_charge_cols)

        df['offense_category'] = np.where(df['updated_offense_category_disp'].notnull(), df['updated_offense_category_disp']
                                          , np.where(df['updated_offense_category_init'].notnull(), df['updated_offense_category_init'], df['offense_category']))

        df = df.drop(columns=['updated_offense_category_disp', 'updated_offense_category_init'])

        print('Merged DataFrames to:', len(df))

        return df





