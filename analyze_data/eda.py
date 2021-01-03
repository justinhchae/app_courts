
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
import os
import json
import sidetable


from collections import deque
from collections import defaultdict
from pandas.io.json import json_normalize
import geopandas

from do_data.writer import Writer


class EDA():
    def __init__(self):
        self.filename = 'figure'
        self.folder = 'figures'
        self.path = os.environ['PWD'] + os.sep + os.sep.join([self.folder, self.filename])
        self.p_cutoff = pd.to_datetime('2015-01-01')
        self.f_cutoff = pd.to_datetime('2020-02-01')
        self.writer = Writer()

    def s8(self, df):
        theme = 'Change from Original Charged Class\nto Disposition Charged Class'
        cat0 = 'event_date'
        cat1 = 'class_diff'
        cat2 = 'class'
        cat3 = 'disposition_court_name'
        cat4 = 'disposition_charged_class'

        # df = df[(df[cat3] == True)]
        df = df[(df[cat0] > self.p_cutoff)]

        # df = df.sample(250000, random_state=0)

        n_samples = len(df)

        df1 = df[[cat0, cat1, cat2, cat3, cat4]].copy()

        # print(df1.head(2))
        #
        cols = df1.columns.tolist()
        counts = df1[cols].value_counts()

        df2 = counts.to_frame().reset_index()
        df2.rename(columns={0: 'count'}, inplace=True)

        print(df2.head(2))

        # print(df2)

        # cat_names = df1[cat2].cat.categories.tolist()
        # print(cat_names)

        # df1[cat2] = df1[cat2].cat.codes
        # cat_vals = list(df1[cat2].unique())
        # cat_vals.sort()
        # print(cat_vals)

        df2 = df2.sample(10000, random_state=0)

        plt.figure()

        sns.displot(data=df2
                    , x='count'
                    # , y=cat1
                    , hue=cat2
                    # , size='count'
                    # , rug=True
                    , palette='RdBu_r'
                    # , kde=True
                    # , multiple='stack'
                    # , kind='hist'

                    )

        # cat_vals, labels = plt.yticks()
        # cat_vals = cat_vals[1:-1]
        # plt.yticks(cat_vals, cat_names)

        # title = str(theme + ' n=' + str(n_samples))
        # plt.legend(ncol=2, loc='upper right', fontsize='x-small')
        # plt.gca().invert_yaxis()
        # plt.title(title)
        # plt.tight_layout()
        plt.show()

    def s7(self, df):
        theme = 'Differential in Charged Class and Disposition Class'
        cat0 = 'disposition_date'
        cat1 = 'class_diff'
        cat2 = 'class'
        cat3 = 'primary_charge_flag_init'

        # df = df[(df[cat3] == True)]

        # df = df.sample(250000, random_state=0)

        n_samples = len(df)

        df1 = df[[cat0, cat1, cat2]].copy()

        plt.figure()

        sns.scatterplot(data=df1
                        , x=cat0
                        , y=cat1
                        , hue=cat2
                        # , rug = True
                        , alpha=.5
                        , palette='tab10')

        title = str(theme + ' n=' + str(n_samples))
        plt.legend(ncol=4, loc='upper left', fontsize='x-small')
        plt.title(title)
        plt.tight_layout()
        plt.show()

    def s6(self, df):
        theme = 'Pending Hearings'
        date_col = 'received_date'
        cat0 = 'disposition_date'
        cat1 = 'disposition_date_days_pending'
        cat2 = 'class'

        df = df[(df[date_col] > self.p_cutoff)]
        # df = df[(df[date_col] < self.f_cutoff)]
        # df = df[(df[cat0] == True)]

        df1 = df[[date_col, cat1, cat2]]
        cols = df1.columns.tolist()
        counts = df1[cols].value_counts()

        df2 = counts.to_frame().reset_index()
        df2.rename(columns={0: 'count'}, inplace=True)

        print(df2)

        fig = plt.figure(figsize=(10, 10))

        sns.scatterplot(data=df2
                        , x=date_col
                        , y='count'
                        , hue=cat2
                        , size=cat1
                        , palette='coolwarm'
                        # , legend=False
                        )

        title = str(theme + ' by ' + date_col + ' n=' + str(len(df1)))
        plt.title(title)
        plt.tight_layout()
        plt.legend(ncol=3)
        # plt.legend(loc="lower center", bbox_to_anchor=(0.5, -.2), ncol=4)
        fig.subplots_adjust(bottom=.25)
        self.filename = str(theme)
        self.folder = 'figures'
        self.path = os.environ['PWD'] + os.sep + os.sep.join([self.folder, self.filename])
        plt.savefig(self.path)
        plt.show()

    def s5(self, df):
        theme = 'Judges in Cook County'
        date_col = 'disposition_date'
        cat0 = 'primary_charge_flag_disp'
        cat1 = 'judge'
        cat2 = 'case_length'
        cats = []
        df = df[(df[date_col] > self.p_cutoff)]
        df = df[(df[date_col] < self.f_cutoff)]
        # df = df[(df[cat0] == True)]

        df1 = df.groupby(cat1)
        print(df1.get_group('Paula M Daleo'))

    def s4(self, df):
        theme = 'Hearing Types'
        date_col = 'disposition_date'
        cat0 = 'primary_charge_flag_disp'
        cat1 = 'charge_disposition_cat'
        cat2 = 'case_length'

        df = df[(df[date_col] > self.p_cutoff)]
        # df = df[(df[date_col] < self.f_cutoff)]
        # df = df[(df[cat0] == True)]

        df1 = df[[date_col, cat1]]
        cols = df1.columns.tolist()
        counts = df1[cols].value_counts()
        df2 = counts.to_frame().reset_index()
        df2.rename(columns={0: 'count'}, inplace=True)

        print(df2.head(3))

        fig = plt.figure(figsize=(10,10))

        sns.scatterplot(data=df2
                     , x=date_col
                     , y='count'
                     , hue=cat1
                     # , size=cat2
                     , palette='viridis'
                     # , legend=False
                     )


        title = str(theme + ' by ' + date_col + ' n=' +str(len(df1)))
        plt.title(title)
        plt.tight_layout()
        plt.legend(loc="lower center", bbox_to_anchor=(0.5, -.28), ncol=4)
        fig.subplots_adjust(bottom=.25)
        self.filename = str(theme + ' By Disposition')
        self.folder = 'figures'
        self.path = os.environ['PWD'] + os.sep + os.sep.join([self.folder, self.filename])
        plt.savefig(self.path)
        plt.show()

    def s3(self, df):
        theme = 'Hearing Types'
        date_col = 'event_date'
        cat0 = 'primary_charge_flag_init'
        cat1 = 'event'
        cat2 = 'class'

        df = df[(df[date_col] > self.p_cutoff)]
        # df = df[(df[date_col] < self.f_cutoff)]
        df = df[(df[cat0] == True)]

        df1 = df[[date_col, cat1]]
        cols = df1.columns.tolist()
        counts = df1[cols].value_counts()
        df2 = counts.to_frame().reset_index()
        df2.rename(columns={0: 'count'}, inplace=True)

        print(df2.head(3))

        fig = plt.figure(figsize=(10,10))

        # colors = [
        # 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r'
        # , 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r'
        # , 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r'
        # , 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r'
        # , 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r'
        # , 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn'
        # , 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r'
        # , 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r'
        # , 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r'
        # , 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3'
        # , 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn'
        # , 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd'
        # , 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary'
        # , 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r'
        # , 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r'
        # , 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r'
        # , 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r'
        # , 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar'
        # , 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern'
        # , 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2'
        # , 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv'
        # , 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r'
        # , 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r'
        # , 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism'
        # , 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic'
        # , 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r'
        # , 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain'
        # , 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted'
        # , 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter'
        # , 'winter_r']

        # for c in colors:
        sns.scatterplot(data=df2
                     , x=date_col
                     , y='count'
                     , hue=cat1
                     , palette='Pastel1'
                     )


        title = str(theme + ' by ' + date_col + ' n=' +str(len(df1)))
        plt.title(title)

        plt.legend()
        self.filename = theme
        self.folder = 'figures'
        self.path = os.environ['PWD'] + os.sep + os.sep.join([self.folder, self.filename])
        plt.tight_layout()
        plt.savefig(self.path)
        plt.show()

    def s2(self, df):
        theme = 'Disposition Hearings by Case Length'
        date_col = 'disposition_date'
        cat0 = 'case_length'
        cat1 = 'disposition_court_name'
        # cat2 = 'class'

        df = df[(df[date_col] > self.p_cutoff)]
        # df = df[(df[date_col] < self.f_cutoff)]
        # df = df[(df[cat0] == True)]

        df1 = df[[cat0, cat1]]
        cols = df1.columns.tolist()
        counts = df1[cols].value_counts()
        df2 = counts.to_frame().reset_index()
        df2.rename(columns={0: 'count'}, inplace=True)

        print(df2.head(3))

        fig = plt.figure(figsize=(10,10))

        # colors = [
        # 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r'
        # , 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r'
        # , 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r'
        # , 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r'
        # , 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r'
        # , 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn'
        # , 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r'
        # , 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r'
        # , 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r'
        # , 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3'
        # , 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn'
        # , 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd'
        # , 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary'
        # , 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r'
        # , 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r'
        # , 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r'
        # , 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r'
        # , 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar'
        # , 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern'
        # , 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2'
        # , 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv'
        # , 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r'
        # , 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r'
        # , 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism'
        # , 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic'
        # , 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r'
        # , 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain'
        # , 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted'
        # , 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter'
        # , 'winter_r']

        # for c in colors:
        sns.displot(data=df2
                     , x=cat0
                     # , y='count'
                     , hue=cat1
                     , multiple='stack'
                     , palette='tab20'
                     , legend=True
                     # , label=
                     )
        # g.despine(left=True)

        title = str(theme + ' n=' +str(len(df1)))
        plt.title(title)
        plt.tight_layout()
        self.filename = theme
        self.folder = 'figures'
        self.path = os.environ['PWD'] + os.sep + os.sep.join([self.folder, self.filename])
        plt.savefig(self.path)
        plt.show()

    def s1(self, df):
        theme = 'Case Length by Charge Class'
        date_col = 'disposition_date'
        class_col = 'disposition_charged_class'

        df = df[(df[date_col] > self.p_cutoff)]

        df1 = df[[class_col, date_col, 'case_length']]

        df1 = df1.groupby([date_col, class_col])['case_length'].mean().reset_index()
        df1['class_code'] = df1[class_col].cat.codes

        print(df1)
        # df1 = df1.dropna(subset=['received_date'])
        # df1 = df1.set_index('received_date').drop_duplicates()
        # df1 = df1.reset_index().groupby(['received_date','class'])['received_date'].count().reset_index(name='count')
        # test = df1.set_index('received_date')

        # print(test.head(3))
        # self.writer.to_csv(test, 'test.csv')

        fig = plt.figure(figsize=(10,10))

        sns.displot(data=df1
                    , x='case_length'
                    , hue=class_col
                    , multiple='stack'
                    , palette='nipy_spectral'
                    )

        title = str(theme + ' ' + date_col + ' n=' +str(len(df1)))
        plt.title(title)
        plt.tight_layout()

        self.filename = theme
        self.folder = 'figures'
        self.path = os.environ['PWD'] + os.sep + os.sep.join([self.folder, self.filename])
        plt.savefig(self.path)
        plt.show()
