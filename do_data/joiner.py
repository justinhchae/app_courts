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

    def joiner(self, df1, df2):
        cols = ['case_id', 'case_participant_id', 'received_date', 'offense_category', 'charge_id']

        df = pd.merge(left=df1, right=df2, how='left', left_on=cols, right_on=cols
                      , suffixes=('_init', '_disp')
                      )

        df = self.maker.make_caselen(df, 'received_date', 'disposition_date')
        df = self.maker.make_disposition_pending(df, 'received_date', 'disposition_date')
        df = self.maker.make_class_diff(df, 'class', 'disposition_charged_class')

        # TODO: re-write logic for joining and column hierarchy

        # df['offense_category'] = np.where(df['updated_offense_category_y'].notna(),
        #                                   df['updated_offense_category_y'], df['updated_offense_category_x'])
        #
        # df['aoic'] = np.where(df['disposition_charged_aoic'].notna(),
        #                       df['disposition_charged_aoic'],
        #                                   df['aoic'])
        #
        # df['charge_class'] = np.where(df['disposition_charged_class'].notna(),
        #                       df['disposition_charged_class'],
        #                       df['class'])

        # df = df.drop(columns=[
        #       'updated_offense_category_y'
        #     , 'updated_offense_category_x'
        #     , 'disposition_charged_aoic'
        #     # , 'primary_charge_flag_x'
        #     # , 'primary_charge_flag_y'
        #     , 'disposition_charged_class'
        #     , 'class'
        # ])

        print('Merged DataFrames to:', len(df))
        # print('Classified Data:')
        # print(df.dtypes)

        return df





