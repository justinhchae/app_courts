import numpy as np
import pandas as pd

from functools import reduce

from clean_data.cleaner import Cleaner
from clean_data.maker import Maker

from do_data.config import Columns

name = Columns()


class Joiner():
    def __init__(self):
        self.cleaner = Cleaner()
        self.maker = Maker()
        self.join_cols = [
              name.case_id
            , name.case_participant_id
            , name.received_date
            , name.offense_category
            , name.charge_id
            , name.charge_version_id
            , name.charge_count
            , name.arraignment_date
            ]

    def make_main(self, df):
        # https://stackoverflow.com/questions/23668427/pandas-three-way-joining-multiple-dataframes-on-columns
        def get_mem(df):
            total_mem = df.memory_usage().sum() / (1024 ** 2)
            print(total_mem)

        sentencing_cols = self.join_cols.copy()
        keep_cols = [
                     name.updated_offense_category
                    , 'sentence_phase'
                    , 'sentence_judge'
                    , 'sentence_court_name'
                    , 'sentence_court_facility'
                    , 'sentence_date'
                    , 'sentence_type'
                    , 'current_sentence_flag'
                    , 'commitment_type'
                    , 'commitment_unit'
                    , 'commitment_days'
                    , 'commitment_dollars'
                    , 'life_term'
                    , name.case_length]
        sentencing_cols.extend(keep_cols)

        df1 = self.initiation_disposition(df[0], df[1], how='inner')

        merged = pd.merge(left=df1, right=df[2][sentencing_cols], how='inner', left_on=self.join_cols, right_on=self.join_cols
                      , suffixes=('_main', '_sent')
                      )

        # merged = reduce(lambda left, right: pd.merge(left, right, how='inner', on=self.join_cols), frames)

        return merged

    def initiation_disposition(self, df1, df2, how='left'):

        cols = self.join_cols

        df1_cols = [name.gender]
        df2_cols = [name.age_at_incident
                    , name.race
                    , name.incident_city, name.incident_begin_date
                    , name.incident_end_date, name.law_enforcement_agency, name.law_enforcement_unit
                    , name.arrest_date, name.felony_review_date, name.felony_review_result]

        df1 = df1.drop(columns=df1_cols)
        df2 = df2.drop(columns=df2_cols)


        df = pd.merge(left=df1, right=df2, how=how, left_on=cols, right_on=cols
                      , suffixes=('_init', '_disp')
                      )

        initiation_charge_cols = [name.act, name.section, name.charge_class, name.aoic, name.chapter]
        disposition_charge_cols = [name.disposition_charged_act
                                    , name.disposition_charged_section
                                    , name.disposition_charged_class
                                    , name.disposition_charged_aoic
                                    , name.disposition_charged_chapter
                                   ]

        charge_cols = tuple(zip(initiation_charge_cols, disposition_charge_cols))

        for col in charge_cols:
            df[col[0]] = np.where(df[col[1]].notnull(), df[col[1]], df[col[0]])

        df = df.drop(columns=disposition_charge_cols)

        df[name.offense_category] = np.where(df['updated_offense_category_disp'].notnull(), df['updated_offense_category_disp']
                                          , np.where(df['updated_offense_category_init'].notnull(), df['updated_offense_category_init'], df[name.offense_category]))

        df = df.drop(columns=['updated_offense_category_disp', 'updated_offense_category_init'])

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

        df = self.cleaner.classer(df, name.offense_category)
        df = self.cleaner.classer(df,
                                  [
                                  name.charge_id
                                  , name.charge_version_id
                                  , name.charge_offense_title
                                  , name.chapter
                                  , name.act
                                  , name.section
                                  , name.charge_class
                                  , name.aoic
                                  , name.event
                                  , name.bond_type_initial
                                  , name.bond_type_current
                                  , name.incident_city
                                  , name.law_enforcement_agency
                                  , name.law_enforcement_unit
                                  , name.felony_review_result
                                  , name.disposition_court_facility
                                   ])

        # df['primary_charge_flag_disp'] = df['primary_charge_flag_disp'].astype('bool')

        # print(df.dtypes)

        # workaround for memory problems, usecols subset

        return df





