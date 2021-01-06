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

        # print(df1['law_enforcement_unit'].cat.categories)
        # print(df2['law_enforcement_unit'].dtype)

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

        #FIXME supress categorical transformation with nan categories [law_enforcement_unit] and [charge_disposition_reason]
        # refactor in cleaner.py
        # Likely bug in cleaner when forcing type to str
        # TEMP WORK AROUND

        bad_cols = ['law_enforcement_unit', 'charge_disposition_reason', 'bond_type_initial', 'bond_type_current']

        df['law_enforcement_unit'] = np.where(df['law_enforcement_unit']=='nan', np.nan, df['law_enforcement_unit'])
        df['law_enforcement_unit'] = df['law_enforcement_unit'].astype('category')

        df['charge_disposition_reason'] = np.where(df['charge_disposition_reason'] == 'nan', np.nan, df['charge_disposition_reason'])
        df['charge_disposition_reason'] = df['charge_disposition_reason'].astype('category')

        df['bond_type_initial'] = np.where(df['bond_type_initial'] == 'nan', np.nan,
                                                   df['bond_type_initial'])
        df['bond_type_initial'] = df['bond_type_initial'].astype('category')

        df['bond_type_current'] = np.where(df['bond_type_current'] == 'nan', np.nan,
                                           df['bond_type_current'])
        df['bond_type_current'] = df['bond_type_current'].astype('category')

        # FIXME: move memory patches to cleaning routines

        def get_mem(df):
            total_mem = df.memory_usage().sum() / (1024 ** 2)
            # origin total: 272.2295866012573
            # with float32: 246.7372808456421
            # change one col to category: 265.85659408569336
            # + with float 32: 244.00604629516602
            # offense cat as cat: 237.63601398468018
            # after in16: 232.17337703704834
            # categorize charge data: 202.27989768981934
            # with disp court fac: 195.907546043396
            # after disp charged title: 190.4935998916626
            # resolve bool flag: 178.70780563354492
            # after more bools: 172.33464527130127
            # convert more bools: 165.96156883239746

            # int16 is -32768 to +32767
            print(total_mem)

        cols = ['bond_amount_initial'
            , 'bond_amount_current', 'age_at_incident'
            , 'disposition_date_days_pending', 'case_length', 'charged_class_difference']

        key = {'nan': np.nan,
               1.: True}

        df['finding_no_probable_cause'] = df['finding_no_probable_cause'].map(key)
        df['bond_electronic_monitor_flag_initial'] = df['bond_electronic_monitor_flag_initial'].map(key)
        df['bond_electroinic_monitor_flag_current'] = df['bond_electroinic_monitor_flag_current'].map(key)

        df['finding_no_probable_cause'] = df['finding_no_probable_cause'].astype('bool')
        df['bond_electronic_monitor_flag_initial'] = df['bond_electronic_monitor_flag_initial'].astype('bool')
        df['bond_electroinic_monitor_flag_current'] = df['bond_electroinic_monitor_flag_current'].astype('bool')

        df[cols] = df[cols].astype('float32')

        cols = ['received_date', 'event_date', 'arraignment_date', 'bond_date_initial'
            , 'bond_date_current', 'incident_begin_date', 'incident_end_date'
            , 'felony_review_date', 'disposition_date']

        # df[cols] = df[cols].astype('datetime64[D]')

        df['offense_category'] = df['offense_category'].astype('category')
        df['charge_count'] = df['charge_count'].astype('int16')

        cols = ['chapter', 'act', 'section', 'class', 'aoic'
            , 'disposition_court_facility', 'disposition_charged_offense_title'
            , 'charge_offense_title'
                ]

        df[cols] = df[cols].astype('category')

        key = {'False': False,
               'True': True,
               'nan': np.nan}

        df['primary_charge_flag_disp'] = df['primary_charge_flag_disp'].map(key)
        df['primary_charge_flag_disp'] = df['primary_charge_flag_disp'].astype('bool')

        # print(df['bond_electroinic_monitor_flag_current'].unique())
        # get_mem(df)


        return df





