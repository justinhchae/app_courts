import numpy as np
import pandas as pd
import sidetable

import matplotlib.pyplot as plt
import seaborn as sns

from clean_data.cleaner import Cleaner
from do_data.getter import Reader
from do_data.writer import Writer
from do_data.config import Columns
name = Columns()

# from pandasgui import show

class Utilities():
    def __init__(self):
        self.today = pd.Timestamp.now()
        self.transparent = 'rgba(0,0,0,0)'
        self.charged_class_code = 'charged_class_category'

        self.common_cols = [
              name.case_id
            , name.case_participant_id
            , name.received_date
            , name.updated_offense_category
            , name.charge_id
            , name.charge_version_id
            , name.charge_count
        ]

    def max_disp_charge(self, df):
        cols = [name.case_id, name.case_participant_id, name.received_date, name.updated_offense_category,
                name.disposition_charged_class]
        df1 = df[cols].copy()
        df1[self.charged_class_code] = df1[name.disposition_charged_class].cat.codes

        cols = [name.case_id, name.case_participant_id, name.received_date, name.updated_offense_category]
        idx = df1.groupby(cols, sort=False)[self.charged_class_code].transform(max) == df1[self.charged_class_code]
        df = df[idx].drop_duplicates(subset=cols)

        return df

    def ov1_initiation(self):
        df = Reader().to_df('initiation_modified.bz2', preview=False)
        df = df[df[name.primary_charge_flag]==True].reset_index(drop=True)

        cols = [
            name.case_id
            , name.received_date
            , name.event_date
            , name.case_participant_id
            , name.event
            , name.primary_charge_flag
            , name.disposition_date_days_pending
            , name.bond_type_current
        ]

        df = df[cols]

        df['year'] = df[name.event_date].dt.year.astype('float32').fillna(value=0)
        df['year'] = df.apply(lambda x: x[name.received_date].year if x['year'] == 0 else x['year'], axis=1)
        df['year'] = df['year'].astype('int16')
        Writer().to_pickle(df=df, filename='ov1_initiation', compression=False)

    def ov1_disposition(self):
        """
        return the most severe allegation for a given case (not always the primary charge
        https://stackoverflow.com/questions/15705630/get-the-rows-which-have-the-max-count-in-groups-using-groupby
        """
        df = Reader().to_df('disposition_modified.bz2', preview=False)

        df = self.max_disp_charge(df)

        cols = [
              name.case_id
            , name.case_participant_id
            , name.received_date
            , name.disposition_date
            , name.updated_offense_category
            , name.disposition_charged_class
            , name.charge_disposition_cat
                ]

        df = df[cols]

        df['year'] = df[name.disposition_date].dt.year.astype('float32').fillna(value=0)
        df['year'] = df.apply(lambda x: x[name.received_date].year if x['year'] == 0 else x['year'], axis=1)
        df['year'] = df['year'].astype('int16')

        Writer().to_pickle(df=df, filename='ov1_disposition', compression=False)

    def ov1_sentencing(self):
        df = Reader().to_df('sentencing_modified.bz2', preview=False)

        cols = [
              name.case_id
            , name.case_participant_id
            , name.received_date
            , name.updated_offense_category
            , name.disposition_charged_class
            , name.sentence_judge
            , name.sentence_date
            , name.disposition_date
            , name.commitment_days
            , name.sentence_type
            , name.charge_disposition_cat
            , name.sentence_court_name
            , name.sentence_court_facility
                ]
        df = df[cols]

        df['year'] = df[name.sentence_date].dt.year.astype('float32').fillna(value=0)
        df['year'] = df.apply(lambda x: x[name.disposition_date].year if x['year'] == 0 else x['year'], axis=1)
        df['year'] = df.apply(lambda x: x[name.received_date].year if x['year'] == 0 else x['year'], axis=1)
        df['year'] = df['year'].astype('int16')
        Writer().to_pickle(df=df, filename='ov1_sentencing', compression=False)

    def dv1_bond(self):
        initiation = Reader().to_df('initiation_modified.bz2', preview=False)

        initiation = initiation[initiation[name.primary_charge_flag] == True].reset_index(drop=True)

        cols = [
              name.case_id
            , name.case_participant_id
            , name.received_date
            , name.charge_class
            , name.event
            , name.disposition_date_days_pending
            , name.bond_type_initial
            , name.bond_type_current
            , name.bond_date_initial
            , name.bond_date_current
            , name.bond_amount_initial
            , name.bond_amount_current
            , name.bond_electronic_monitor_flag_initial
            , name.bond_electroinic_monitor_flag_current
            , name.age_at_incident
            , name.race
            , name.gender
                ]

        initiation = initiation[cols]
        initiation = initiation[initiation[name.bond_amount_current].notnull()].reset_index(drop=True)
        initiation['year'] = initiation[name.bond_date_current].dt.year.astype('float32').fillna(value=0)
        # initiation['year'] = initiation.apply(lambda x: x[name.bond_date_current].year if x['year'] == 0 else x['year'], axis=1)
        initiation['year'] = initiation.apply(lambda x: x[name.received_date].year if x['year'] == 0 else x['year'], axis=1)
        initiation['year'] = initiation['year'].astype('int16')
        initiation = initiation[initiation['year'] > 2010]
        initiation = initiation[initiation['year'] < 2021]

        # print(initiation)

        Writer().to_pickle(initiation, 'dv1_bond', compression=False)
        # gui = show(initiation)

        # gui = show(initiation)

        # print(type(initiation))
        # print(initiation.head())

        # test = initiation[[name.bond_type_current, name.bond_type_initial]]


        # disposition = Reader().to_df('disposition_modified.bz2', preview=False)
        #
        # disposition = self.max_disp_charge(disposition)
        #
        # cols = [
        #       name.case_id
        #     , name.case_participant_id
        #     , name.received_date
        #     , name.disposition_date
        #     , name.initial_charged_class
        #     , name.disposition_charged_class
        #     , name.charged_class_difference
        #     , name.charge_disposition_cat
        #     , name.judge
        #     , name.disposition_court_name
        #     , name.disposition_court_facility
        #     , name.incident_city
        #     , name.felony_review_date
        #     , name.felony_review_result
        #     , name.case_length
        #     , name.age_at_incident
        #     , name.race
        #     , name.gender
        # ]
        #
        # disposition = disposition[cols]
        # print(disposition.head())
        # print(disposition.dtypes)

        # sentencing = Reader().to_df('sentencing_modified.bz2', preview=False)

        cols = [
              name.case_id
            , name.case_participant_id
            , name.received_date
            , name.disposition_date
            , name.disposition_charged_class
            , name.charge_disposition_cat
            , name.sentence_judge
            , name.sentence_court_name
            , name.sentence_court_facility
            , name.sentence_phase
            , name.sentence_date
            , name.sentence_type
            , name.current_sentence_flag
            , name.commitment_type
            , name.commitment_days
            , name.incident_city
            , name.felony_review_date
            , name.felony_review_result
            , name.life_term
            , name.case_length
            , name.age_at_incident
            , name.race
            , name.gender
        ]

        # print(sentencing[cols].head())

        # df[name.bond_electronic_monitor_flag_initial] = df[name.bond_electronic_monitor_flag_initial].fillna(0)
        # print(df[name.bond_electronic_monitor_flag_initial].unique())
        # df = Reader().to_df('disposition_modified.bz2', preview=False)
        # df = Reader().to_df('initiation_modified.bz2', preview=False)


