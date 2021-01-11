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

    def ov1_initiation(self):
        df = Reader().to_df('initiation_modified.bz2', preview=False)
        df = df[df[name.primary_charge_flag]==True]
        cols = [name.case_id, name.case_participant_id, name.primary_charge_flag, name.disposition_date_days_pending, name.bond_type_current]
        df = df[cols]
        Writer().to_pickle(df=df, filename='ov1_initiation', compression=False)

    def ov1_disposition(self):
        """
        return the most severe allegation for a given case (not always the primary charge
        https://stackoverflow.com/questions/15705630/get-the-rows-which-have-the-max-count-in-groups-using-groupby
        """
        df = Reader().to_df('disposition_modified.bz2', preview=False)

        cols = [name.case_id, name.case_participant_id, name.received_date, name.updated_offense_category, name.disposition_charged_class]
        df1 = df[cols].copy()
        df1[self.charged_class_code] = df1[name.disposition_charged_class].cat.codes

        cols = [name.case_id, name.case_participant_id, name.received_date, name.updated_offense_category]
        idx = df1.groupby(cols, sort=False)[self.charged_class_code].transform(max) == df1[self.charged_class_code]
        df = df[idx].drop_duplicates(subset=cols)

        cols = [name.case_id
            , name.case_participant_id
            , name.received_date
            , name.updated_offense_category
            , name.disposition_charged_class
            , name.charge_disposition_cat
                ]

        df = df[cols]

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
            , name.commitment_days
            , name.sentence_type
                ]
        df = df[cols]
        Writer().to_pickle(df=df, filename='ov1_sentencing', compression=False)

