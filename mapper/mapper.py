import pandas as pd
from typing import Any, List, Tuple
from mapper.lens import Lens
import networkx as nx


class Mapper:
    def __init__(self, verbosity: int = 1):
        self.verbosity = verbosity

    def _trace(self, verbosity: int = 0, *args, **kwargs):
        if verbosity <= self.verbosity:
            print(*args, **kwargs)

    def map(self,
            df: pd.DataFrame,
            lens: Lens,
            clusterer: Any,
            n_intervals: int = 10,
            overlap_perc: float = 0.2
            ) -> nx.Graph:

        df_local = df.copy().reset_index(drop=True).reset_index()
        df_local['lens'] = lens(df_local.drop('index', axis=1))

        min_lens, max_lens = df_local.lens.min(), df_local.lens.max()
        intervals = self._form_intervals(min_lens, max_lens, n_intervals=n_intervals, overlap_perc=overlap_perc)

        us = []
        for i, interval in enumerate(intervals):
            df_u = df_local[(df_local.lens >= interval[0]) & (df_local.lens <= interval[1])].copy().drop('lens', axis=1)
            df_u['interval'] = i
            if df_u.shape[0] == 0:
                continue
            clusterer.fit(df_u.drop(['index', 'interval'], axis=1))
            df_u['cluster'] = clusterer.labels_
            df_u = df_u[['index', 'cluster', 'interval']]
            us.append(df_u)
        return self._form_graph(us)

    def _form_intervals(self, min_lens, max_lens, n_intervals, overlap_perc) -> List[Tuple[float, float]]:
        interval_size = (max_lens - min_lens) / n_intervals
        intervals = []
        for i in range(n_intervals):
            start = max(min_lens, min_lens + (i-overlap_perc)*interval_size)
            end = min(max_lens, min_lens + (i+1+overlap_perc)*interval_size)
            intervals.append((start, end))
        return intervals

    def _form_graph(self, us: List[pd.DataFrame]) -> nx.Graph:
        df_us = pd.concat(us)
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