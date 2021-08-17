import pandas as pd
from lens import PCALens
from mapper import Mapper
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import entropy
from typing import List, Tuple
import os


def create_node_info(graph: nx.Graph, classes: pd.Series) -> List[Tuple[str, pd.Series]]:
    """
    For each node information (result is list of infos for each node) is collected as
    list of pairs:
        - first: Node name
        - second: Classes (target) contained node

    :param graph: Graph (mapper result)
    :param classes: classes (target) of whole dataset
    :return: Information for each node as a list
    """
    node_info = []
    for name, data in graph.nodes.data():
        instances = data['instances']
        instance_classes = classes[instances]
        node_info.append((name, instance_classes))

    return node_info


def plot_mode_graph(
        graph: nx.Graph,
        node_info: List[Tuple[str, pd.Series]],
        pos: dict,
        ax: plt.Axes
        ) -> None:
    """
    Plots graph where each node is colored by most frequent class (mode).
    Node sizes are correlated to number of instances in that node.

    :param graph: Mapper graph
    :param node_info: Node informations
    :param pos: Graph layout
    :param ax: Plot axes
    :return: None
    """
    mode_colors = {
        'Iris-setosa': 'red',
        'Iris-virginica': 'blue',
        'Iris-versicolor': 'green'
    }

    ax.set_title('Graph colored by class mode')
    cs = set()
    for c in ['Iris-setosa', 'Iris-virginica', 'Iris-versicolor']:
        for ni in node_info:
            if ni[1].mode()[0] != c:
                continue
            nx.draw_networkx_nodes(graph, pos,
                                   ax=ax,
                                   node_color=mode_colors[c],
                                   nodelist=[ni[0]],
                                   node_size=10 * ni[1].shape[0],
                                   label=c if c not in cs else None)
            cs.add(c)
    nx.draw_networkx_edges(graph, pos=pos, ax=ax)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=10)
    ax.legend(scatterpoints=1)


def plot_entropy_graph(
        graph: nx.Graph,
        node_info: List[Tuple[str, pd.Series]],
        pos: dict,
        ax: plt.Axes
        ) -> None:
    """
    Plots graph where each node is colored by node classes entropy.
    Node sizes are correlated to number of instances in that node.

    :param graph: Mapper graph
    :param node_info: Node informations
    :param pos: Graph layout
    :param ax: Plot axes
    :return: None
    """
    entropy_colors = {
        0.0: 'lightgray',
        0.1: 'yellow',
        0.2: 'orange',
        0.3: 'darkorange',
        0.4: 'coral',
        1.0: 'red'
    }
    ax.set_title('Graph colored by node entropy')
    used_nodes = set()
    threshold_labels = set()
    for treshold, color in entropy_colors.items():
        for ni in node_info:
            e = entropy(ni[1].value_counts() / ni[1].shape[0])
            if ni[0] in used_nodes or e > treshold:
                continue
            used_nodes.add(ni[0])
            nx.draw_networkx_nodes(graph, pos,
                ax=ax,
                node_color=color,
                nodelist=[ni[0]],
                node_size=10 * ni[1].shape[0],
                label=f'<= {treshold}' if treshold not in threshold_labels else None)
            threshold_labels.add(treshold)
    nx.draw_networkx_edges(graph, pos=pos, ax=ax)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=10)
    ax.legend(scatterpoints=1)


def run():
    df = pd.read_csv('../data/Iris.csv')
    features = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
    target = 'Species'
    X, y = df[features], df[target]

    scaler = StandardScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=features)

    mapper = Mapper(verbosity=2)
    graph = mapper.map(
        df=X,
        lens=PCALens(),
        clusterer=DBSCAN(eps=1.5),
        n_intervals=10,
        overlap_perc=0.5)

    node_info = create_node_info(graph, y)

    pos = nx.spring_layout(graph)
    fig, axs = plt.subplots(figsize=(14, 8), ncols=2)
    plot_mode_graph(graph, node_info, pos, axs[0])
    plot_entropy_graph(graph, node_info, pos, axs[1])

    if not os.path.exists('output'):
        os.mkdir('output')
    fig.savefig('output/iris.png')


if __name__ == '__main__':
    run()
