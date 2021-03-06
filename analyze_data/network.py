import numpy as np
import pandas as pd
import sidetable

import plotly.graph_objects as go
import plotly_express as px
from plotly.subplots import make_subplots

import matplotlib.pyplot as plt
import seaborn as sns

from clean_data.cleaner import Cleaner
from do_data.getter import Reader
from do_data.writer import Writer
from do_data.config import Columns
name = Columns()

# from pandasgui import show
from analyze_data.colors import Colors
from scipy import stats

import networkx as nx

from collections import Counter
import math
from sklearn import preprocessing

colors = Colors()

class Network():
    def __init__(self):
        self.G = nx.DiGraph()
        self.hubs = None
        self.blue = '#1f77b4'  # muted blue
        self.orange = '#ff7f0e'  # safety orange
        self.green = '#2ca02c'  # cooked asparagus green
        self.red = '#d62728'  # brick red
        self.purple = '#9467bd'  # muted purple
        self.brown = '#8c564b'  # chestnut brown
        self.pink = '#e377c2'  # raspberry yogurt pink
        self.gray = '#7f7f7f'  # middle gray
        self.yellow_green = '#bcbd22'  # curry yellow-green
        self.teal = '#17becf'

        self.sentence_color = {
              'Prison': self.red
            , 'Conversion': self.blue
            , 'Probation': self.blue
            , 'Jail': self.red
            , 'Conditional Discharge': self.green
            , 'Supervision': self.blue
            , 'Cook County Boot Camp': self.green
            , 'Probation Terminated Satisfactorily': self.green
            , 'Inpatient Mental Health Services': self.blue
            , 'Death': self.red
            , 'Conditional Release': self.green
            , 'Probation Terminated Instanter': self.orange
            , 'Probation Terminated Unsatisfactorily': self.orange
            , '2nd Chance Probation': self.orange
        }

    def ingest_df(self, df, filename):
        self.G.clear()
        judge_df = df.groupby(name.sentence_judge)
        edges = []
        counter = 0
        # df['sentence_color'] = df[name.sentence_type].apply(lambda x: self.sentence_color[x])
        df['sentence_color'] = df[name.sentence_type].cat.codes
        scaler = preprocessing.MinMaxScaler(feature_range=(.5, 15.))

        # https://towardsdatascience.com/data-normalization-with-pandas-and-scikit-learn-7c1cc6ed6475
        df['scaled_commitment_days'] = pd.DataFrame(scaler.fit_transform(df[[name.commitment_days]]))

        self.hubs = list(df[name.sentence_court_name].unique())
        sentence_types = list(df[name.sentence_type].unique())
        sentence_facs = list(df[name.sentence_court_facility].unique())
        mean_scaled_commitment_days = []
        self.hubs.extend(sentence_types)
        self.hubs.extend(sentence_facs)
        self.hubs = list(set(self.hubs))
        self.hubs.remove(np.nan)
        self.hubs.sort()

        for df1_name, df1 in judge_df:
            counter +=1

            if len(df1) > 0:
                n_cases = len(df1)
                node_record = tuple((df1_name, {'n_cases':n_cases}))
                self.G.add_nodes_from([node_record])
                court_df = df1.groupby(name.sentence_court_name)

                for df2_name, df2 in court_df:
                    df2[name.sentence_court_facility] = df2[name.sentence_court_facility].cat.remove_unused_categories()

                    if len(df2) > 0:
                        n_cases = len(df2)
                        node_record = tuple((df2_name, {'n_cases': n_cases}))
                        self.G.add_nodes_from([node_record])
                        fac_df = df2.groupby(name.sentence_court_facility)

                        for df3_name, df3 in fac_df:
                            df3[name.sentence_court_name] = df2[name.sentence_court_name].cat.remove_unused_categories()

                            if len(df3) > 0:
                                # nx.add_path(self.G, [df1_name, df3_name, df2_name])
                                sentence_df = df3.groupby(name.sentence_type)
                                n_cases = len(df3)
                                node_record = tuple((df3_name, {'n_cases': n_cases}))
                                self.G.add_nodes_from([node_record])

                                for df4_name, df4 in sentence_df:
                                    df4[name.sentence_type] = df4[name.sentence_type].cat.remove_unused_categories()

                                    if len(df4) > 0:
                                        n_cases = len(df4)
                                        node_record = tuple((df4_name, {'n_cases': n_cases}))
                                        self.G.add_nodes_from([node_record])
                                        color = df4['sentence_color'].unique()[0]
                                        msc_day = df4['scaled_commitment_days'].fillna(0).median()
                                        n_cases = len(df4)
                                        nx.add_path(self.G, [df1_name, df3_name, df2_name, df4_name]
                                                    , color=color
                                                    , label=df4_name
                                                    , msc_day=msc_day
                                                    , judge=df1_name
                                                    , n_cases=n_cases
                                                    )

        if filename:
            saved_name = str('data/'+filename+'.gpickle')
            nx.write_gpickle(self.G, saved_name, protocol=2)

    def graph_network(self, df=None, filename=None):

        if filename:
            read_name = str('data/'+filename+'.gpickle')
            self.G = nx.read_gpickle(read_name)

        if df is not None:
            self.hubs = list(df[name.sentence_court_name].unique())
            self.types = list(set(df[name.sentence_type].unique()))
            sentence_facs = list(df[name.sentence_court_facility].unique())
            mean_scaled_commitment_days = []
            # self.hubs.extend(sentence_types)
            # self.hubs.extend(sentence_facs)
            self.hubs = list(set(self.hubs))
            self.hubs.remove(np.nan)
            self.hubs.sort()
            self.judges = list(set(df[name.sentence_judge].unique()))
            self.judges.remove(np.nan)

        d = dict(self.G.degree)
        pos = nx.spring_layout(self.G, k=5 / math.sqrt(self.G.order()), seed=0)

        node_values = np.array([v for v in d.values()]).reshape(-1, 1)
        scaler = preprocessing.MinMaxScaler(feature_range=(5, 30))
        scaled_node_values = scaler.fit_transform(node_values)
        vmin = min(scaled_node_values)
        vmax = max(scaled_node_values)

        # colors = [self.G[u][v]['color'] for u, v in self.G.edges()]
        edge_values = [self.G[n1][n2]['color'] for n1, n2 in self.G.edges()]
        edge_vmin = min(edge_values)
        edge_vmax = max(edge_values)

        plt.figure(figsize=(10, 10))

        labels = {}
        for node in self.G.nodes():
            if node in self.hubs:
                labels[node] = node

        nx.draw_networkx_nodes(self.G
                               , cmap=plt.get_cmap('coolwarm')
                               , node_color=scaled_node_values
                               , pos=pos
                               , vmin=vmin
                               , vmax=vmax
                               , node_size=scaled_node_values
                               , label=False
                               )

        edge_widths=[self.G[n1][n2]['msc_day'] for n1, n2 in self.G.edges()]

        nx.draw_networkx_edges(self.G
                               , edge_cmap=plt.get_cmap('tab20')
                               , pos=pos
                               , width=edge_widths
                               , alpha =.8
                               , edge_vmin=edge_vmin
                               , edge_vmax=edge_vmax
                               , edge_color=edge_values
                               )

        edge_labels = nx.get_edge_attributes(self.G, 'label')

        # nx.draw_networkx_edge_labels(self.G
        #                              , pos=pos
        #                              , edge_labels=edge_labels
        #                              , font_size=4
        #                              )

        nx.draw_networkx_labels(self.G
                                , pos=pos
                                , labels=labels
                                , font_size=8
                                , font_color='black'
                                , font_weight='medium'
                                )
        # plt.show()

        return self.G, pos, edge_widths, scaled_node_values, self.hubs, self.judges, self.types


    def make_network(self):
        # neo 4 j

        # https://stackoverflow.com/questions/44611449/cannot-create-a-directed-graph-using-from-pandas-dataframe-from-networkx
        # types https://networkx.org/documentation/stable//reference/drawing.html
        """
        https://stackoverflow.com/questions/45350222/select-nodes-and-edges-form-networkx-graph-with-attributes
        selected_nodes = [n for n, v in G.nodes(data=True) if v['ej_status'] == 'EM']
        print(selected_nodes)

        https://stackoverflow.com/questions/13517614/draw-different-color-for-nodes-in-networkx-based-on-their-node-value

        """

        G = nx.DiGraph()
        H = nx.DiGraph()

        df = pd.read_csv('data/testing.csv', index_col=0)
        df = df[df['ir'] != 'NOT ASSIGNED.']
        df = df.dropna(subset=['ir'])

        df = df[(df['detainee_status_date']=='2020-07-15') | (df['detainee_status_date']=='2020-06-30')]
        df['detainee_status_date'] = pd.to_datetime(df['detainee_status_date'])

        df = df.groupby('ir')

        attrs = {}
        nodes = []
        seen_nodes = []
        edges = []
        node = []
        weight = 0
        person_records = []
        path_records = []

        counter = 0

        for ir, node_df in df:
            counter +=1

            person_record = tuple((ir, node_df))
            G.add_nodes_from([person_record])

            edge_df = node_df.groupby('detainee_status_date')

            for detainee_status_date, status_df in edge_df:

                status_record = tuple(zip(status_df['ej_status'], status_df['detainee_status']))[0]
                edges.append(status_record)

                if 'Jail' in status_record[0]:
                    G.add_edge(ir, status_record, color='tomato')
                elif 'Out' in status_record[0]:
                    G.add_edge(ir, status_record, color='mediumseagreen')
                elif 'EM' in status_record[0]:
                    G.add_edge(ir, status_record, color='gold')
                else:
                    G.add_edge(ir, status_record, color='gray')

            if counter == 1000:
                break

        test_time = np.datetime64('2020-07-15')
        # selected_edges = [(u,v) for u,v,e in G.edges(data=True) if e['status_date'] == test_time]
        # print(selected_edges)

        # test = G.nodes(data=True)['1000878']

        # print(G.nodes['1000878'])

        # test_nodes = [(x, y) for x, y in G.nodes(data=True)]
        # print(test_nodes)


        d = dict(G.degree)
        hubs = list(set(edges))
        # pos = nx.circular_layout(G)
        # https://stackoverflow.com/questions/34630621/how-do-i-draw-non-overlapping-edge-labels-in-networkx
        pos = nx.spring_layout(G, k=7/math.sqrt(G.order()), seed=42)

        # plt.figure(figsize=(10, 10))
        # nx.draw(G, pos=pos, with_labels=True)
        # plt.tight_layout()
        # plt.show()

        values = np.array([v for v in d.values()]).reshape(-1,1)
        scaler = preprocessing.MinMaxScaler(feature_range=(5, 1000))
        # https://towardsdatascience.com/data-normalization-with-pandas-and-scikit-learn-7c1cc6ed6475
        scaled_values = scaler.fit_transform(values)
        # print(test.ravel())

        colors = [G[u][v]['color'] for u, v in G.edges()]

        plt.figure(figsize=(10, 10))
        # https://stackoverflow.com/questions/14665767/networkx-specific-nodes-labeling
        labels = {}
        for node in G.nodes():
            if node in hubs:
                # set the node name as the key and the label as its value
                labels[node] = node
        # set the argument 'with labels' to False so you have unlabeled graph
        nx.draw(G, with_labels=False, pos=pos
                , node_size=scaled_values
                , edge_color=colors)
        # Now only add labels to the nodes you require (the hubs in my case)
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='black')
        plt.show()

        G.clear()


        # G.add_nodes_from(person_records)

        # G.add_edge('1000878', tuple(('Jail', 'Penitentiary Hold')))

        # print(G.edges())

        # print(G.nodes['1000878']['detainee_status'])



        # for df1_name, df1 in df:
        #     df2 = df1.groupby('ej_status')
        #
        #     for df2_name, df3 in df2:
        #         df4 = df3.groupby('detainee_status')
        #
        #         for df4_name, df4 in df4:
        #             df5 = df4.groupby('ir')
        #
        #             for node_id, df6 in df5:
        #                 # node_name = str('n'+ node_id)
        #
        #                 records = df6[['detainee_status_date', 'ej_status', 'detainee_status']].to_dict('records')
        #
        #                 if node_id in seen_nodes:
        #                     for i in nodes:
        #                         if node_id == i[0]:
        #
        #                             ## working with dicts
        #                             # p1 = [x for x in i[1][node_id]][0]['ej_status']
        #                             # p1_status = [x for x in i[1][node_id]][0]['detainee_status']
        #                             # p2 = records[0]['ej_status']
        #                             # p2_date = records[0]['detainee_status_date']
        #                             # p2_status = records[0]['detainee_status']
        #
        #                             ## working with dfs
        #
        #                             # if p1 == 'Out' and p2 == 'Out':
        #                             #     path = tuple((p1, p2))
        #                             #
        #                             # elif p1 == 'Out':
        #                             #     path = tuple((p1, (p2, p2_status)))
        #                             #
        #                             # elif p2 == 'Out':
        #                             #     path = tuple(((p1, p1_status), p2))
        #                             #
        #                             # else:
        #                             #     path = tuple(((p1, p1_status), (p2, p2_status)))
        #                             #
        #                             # edges.append(path)
        #
        #                             try:
        #                                 i[1][node_id].append(df6)
        #                                 print(i[1][node_id])
        #                             except:
        #                                 print('error', node_id, df6)
        #
        #                 else:
        #                     ## working with dicts
        #                     # node = tuple((node_id, {node_id: records}))
        #
        #                     ## working with dfs
        #
        #                     node = tuple((node_id, {node_id: df6}))
        #                     nodes.append(node)
        #                     seen_nodes.append(node_id)
        #             # break
        #         # break
        #     # break

        # G.add_nodes_from(nodes)

        # print(G.nodes['1170077'])

        # weighted_edges = list(Counter(edges).items())

        # weighted_edges = [tuple((lis[0][0], lis[0][1], lis[1])) for lis in weighted_edges]

        # H.add_weighted_edges_from(weighted_edges)

        # for i in nodes:
        #     print(i)

        # print(G.edges())

        # selected_nodes = [n for n, v in G.nodes(data=True)]
        # print(len(selected_nodes))
        # print(nodes[0])

        # new = {'detainee_status': 'Something Else', 'detainee_status_date': '2020-06-30', 'ej_status': 'Jail'}

        # print([i['n1163614']['1163614'] for i in nodes if 'n1163614' in i][0])

        # for i in nodes:
        #     if 'n1163614' in i:
        #         old = i['n1163614']['1163614']
        #         old.append(new)
        #         i.update({'n1163614':old})

        # d = dict(H.degree)

        # values = [d.get(node, 0.25) for node in H.nodes()]

        # pos=nx.circular_layout(H)
        # pos=nx.spring_layout(H, k=5.)
        # cmap=plt.get_cmap('nipy_spectral')



        # vmin = min(values)
        # vmax = max(values)
        #
        # for edge in G.edges():
        #     # print(H.nodes[0])
        #     print(G.nodes[edge[0]])
        #
        #     break

        # plt.figure(figsize=(10, 8))
        # plt.title('Prototype Model EM-Jail Flow (2021-01-15)\nGiven a Roster of EM and Jail Populations by IR, Date, and Detainee Status')
        # nx.draw(H
        #         , with_labels=True
        #         , pos=pos
        #         , node_size=[v * 100 for v in d.values()]
        #         , cmap=cmap
        #         , node_color=values
        #         )
        #
        # # https://stackoverflow.com/questions/26739248/how-to-add-a-simple-colorbar-to-a-network-graph-plot-in-python
        # # https://stackoverflow.com/questions/33737427/top-label-for-matplotlib-colorbars/33740567
        # sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        # sm._A = []
        # cbar = plt.colorbar(sm)
        # cbar.ax.set_ylabel('Normalized Count of Population Movement Destinations')
        #
        # plt.savefig('figures/em_jail_flow.png')
        # plt.show()

        # edge_x = []
        # edge_y = []
        # for edge in H.edges():
        #     x0, y0 = H.nodes[edge[0]]['pos']
        #     x1, y1 = H.nodes[edge[1]]['pos']
        #     edge_x.append(x0)
        #     edge_x.append(x1)
        #     edge_x.append(None)
        #     edge_y.append(y0)
        #     edge_y.append(y1)
        #     edge_y.append(None)
        #
        # edge_trace = go.Scatter(
        #     x=edge_x, y=edge_y,
        #     line=dict(width=0.5, color='#888'),
        #     hoverinfo='none',
        #     mode='lines')
        #
        # node_x = []
        # node_y = []
        # for node in H.nodes():
        #     x, y = H.nodes[node]['pos']
        #     node_x.append(x)
        #     node_y.append(y)
        #
        # node_trace = go.Scatter(
        #     x=node_x, y=node_y,
        #     mode='markers',
        #     hoverinfo='text',
        #     marker=dict(
        #         showscale=True,
        #         # colorscale options
        #         # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #         # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #         # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        #         colorscale='YlGnBu',
        #         reversescale=True,
        #         color=[],
        #         size=10,
        #         colorbar=dict(
        #             thickness=15,
        #             title='Node Connections',
        #             xanchor='left',
        #             titleside='right'
        #         ),
        #         line_width=2))

        # https://stackoverflow.com/questions/16566871/node-size-dependent-on-the-node-degree-on-networkx

        # plt.figure(figsize=(10, 8))
        # nx.draw(H, nodelist=d.keys(), node_size=[v * 100 for v in d.values()])
        # plt.show()

        # print(G.nodes())

        import gc
        del G
        del H
        gc.collect()




        # G = nx.Graph()
        # time1 = pd.to_datetime('2020-05-13')
        # time2 = pd.to_datetime('2020-06-30')

        # print(df)

        # G = nx.from_pandas_edgelist(df, 'ir', 'ej_status', create_using=nx.DiGraph())
        #
        # plt.figure(figsize=(10, 8))
        # nx.draw(G, with_labels=True, pos=nx.spring_layout(G))
        # plt.show()
        # print(G.edges())

        # edges = pd.DataFrame({'source': [0, 1],
        #                       'target': [1, 2],
        #                       'weight': [100, 50]})
        #
        # nodes = pd.DataFrame({'node': [0, 1, 2],
        #                       'name': ['Foo', 'Bar', 'Baz'],
        #                       'gender': ['M', 'F', 'M']})
        #
        # G = nx.from_(edges, 'source', 'target', 'weight')


    def organize(self):
        df = pd.read_csv('data/em_testing.csv')

        df = df[df['ir'] != 'NOT ASSIGNED.']
        df = df.dropna(subset=['ir'])

        df['detainee_status'] = df['detainee_status'].str.title()
        cols = ['ir', 'detainee_status', 'ej_status']
        df[cols] = df[cols].astype('category')
        df['detainee_status_date'] = pd.to_datetime(df['detainee_status_date'])

        status_col = df[['detainee_status', 'detainee_status_date', 'ir']].copy()

        df = df.pivot(index=['ir'], columns=['detainee_status_date'], values=['ej_status'])
        df.columns = df.columns.get_level_values(1)
        df = df.fillna(value='Out')

        df = df.unstack().reset_index(name='ej_status')

        df = pd.merge(df, status_col, how='left', on=['ir', 'detainee_status_date'])

        df['detainee_status'].cat.add_categories(['None'], inplace=True)
        df['detainee_status'].fillna('None', inplace=True)
        df['detainee_status'].cat.remove_categories(np.nan, inplace=True)

        df = df[['ir', 'detainee_status', 'detainee_status_date', 'ej_status']]

        df = df.sort_values(by=['detainee_status_date'])

        df = df.reset_index(drop=True)

        df = self.length_of_stay(df)

        self.df = df

        self.df.to_csv('data/testing.csv')

    def length_of_stay(self, df):

        grouped = df.groupby('ir')

        frames = []

        for ir, df1 in grouped:
            df1['status_length'] = (
                        df1['detainee_status_date'] - df1['detainee_status_date'].shift()).fillna(
                pd.Timedelta(seconds=0))

            frames.append(df1)

        df = pd.concat(frames)

        return df

