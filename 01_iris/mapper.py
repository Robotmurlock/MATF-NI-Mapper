import pandas as pd
from typing import Any, List, Tuple
from lens import Lens
import networkx as nx


class Mapper:
    def __init__(self, verbosity: int = 1):
        """
        Tracing level for `trace function`. All traces with level
        lower or equal than `self.verbostity` are shown.
        :param verbosity: verbosity level
        """
        self.verbosity = verbosity

    def _trace(self, msg: str, verbosity: int = 0, *args, **kwargs) -> None:
        """
        Tracing function for proper verbosity level.
        :param msg: Tracing message.
        :param verbosity: Verbosity level of trace
        """
        if verbosity <= self.verbosity:
            print(f'[Mapper]: {msg}', *args, **kwargs)

    def map(self,
            df: pd.DataFrame,
            lens: Lens,
            clusterer: Any,
            n_intervals: int = 10,
            overlap_perc: float = 0.2
            ) -> nx.Graph:
        self._trace('Creating copy if initial dataframe...', verbosity=1)
        df_local = df.copy().reset_index(drop=True).reset_index()

        self._trace('Applying lens function...', verbosity=1)
        df_local['lens'] = lens(df_local.drop('index', axis=1))

        min_lens, max_lens = df_local.lens.min(), df_local.lens.max()
        self._trace(f'Filter function image: [{min_lens:.2f}, {max_lens:.2f}].', verbosity=2)
        intervals = self._form_intervals(min_lens, max_lens, n_intervals=n_intervals, overlap_perc=overlap_perc)

        us = self._cluster_subsets(intervals, df_local, clusterer)
        return self._form_graph(us)

    def _form_intervals(self,
                        min_lens: float,
                        max_lens: float,
                        n_intervals: int,
                        overlap_perc: float
                        ) -> List[Tuple[float, float]]:
        """
        Given minimum and maximum filter (lens) function values, number of intervals and
        percentage of overlappings, creates list of intervals [start, end]
        Example:
            min_lens := 1
            max_lens := 5
            n_intervals := 5
            overlap_perc := 0.1
            => [(1, 1.1), (0.9, 2.1), (1.9, 3.1), (2.9, 4.1), (3.9, 5)]

        :param min_lens: Minimum filter (lens) function value.
        :param max_lens: Maximum filter (lens) function value.
        :param n_intervals: Number of intervals.
        :param overlap_perc: Interval overlap percentage
        :return: Intervals.
        """
        self._trace('Creating intervals...', verbosity=1)
        interval_size = (max_lens - min_lens) / n_intervals
        intervals = []
        for i in range(n_intervals):
            start = max(min_lens, min_lens + (i-overlap_perc)*interval_size)
            end = min(max_lens, min_lens + (i+1+overlap_perc)*interval_size)
            self._trace(f'Interval {i}: ({start}, {end})', verbosity=2)
            intervals.append((start, end))
        return intervals

    def _form_graph(self, df_us: pd.DataFrame) -> nx.Graph:
        """
        Forms graph from list of clusters using these rules:
        1. Every cluster becomes a node.
        2. Two nodes are connected with an edge if they share a point.

        :param df_us: Dataframe with points and clusters (possible duplicate points)
        :return: Graph
        """
        self._trace('Forming graph...')
        us_grps = df_us.groupby('index')
        graph = nx.Graph()

        for _, df_grp in us_grps:
            for i, (i_index, row_i) in enumerate(df_grp.iterrows()):
                node_i = f'C[{row_i["interval"]}, {row_i["cluster"]}]'
                if node_i not in graph.nodes:
                    graph.add_node(node_i, instances=[])
                if 'instances' not in graph.nodes[node_i]:
                    graph.nodes[node_i]['instances'] = []
                graph.nodes[node_i]['instances'].append(i_index)

                if row_i['cluster'] == -1:
                    continue
                for j, (j_index, row_j) in enumerate(df_grp.iterrows()):
                    if i == j:
                        continue
                    node_j = f'C[{row_j["interval"]}, {row_j["cluster"]}]'
                    graph.add_edge(node_i, node_j)

        return graph

    def _cluster_subsets(self, intervals: List[Tuple[float, float]],
                         df: pd.DataFrame,
                         clusterer: Any
                         ) -> pd.DataFrame:
        """
        This function clusters subset of data points f^-1(I) for each interval I in set of
        lens intervals.

        :param intervals: List of intervals.
        :param df: Data.
        :param clusterer: Clustering algorithm.
        :return: Dataframe with points and clusters (possible duplicate points)
        """
        self._trace('Clustering subsets...', verbosity=1)
        us = []
        for i, interval in enumerate(intervals):
            df_u = df[(df.lens >= interval[0])
                      & (df.lens <= interval[1])]\
                .copy()\
                .drop('lens', axis=1)

            df_u['interval'] = i
            if df_u.shape[0] == 0:
                # Skipping empty intervals
                continue

            clusterer.fit(df_u.drop(['index', 'interval'], axis=1))
            df_u['cluster'] = clusterer.labels_
            self._trace(f'Number of cluster for interval {i}: {df_u.cluster.nunique()}', verbosity=2)
            us.append(df_u[['index', 'cluster', 'interval']])

        return pd.concat(us)
