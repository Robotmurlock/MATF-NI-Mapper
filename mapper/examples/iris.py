import pandas as pd
from mapper.lens import PCALens
from mapper.mapper import Mapper
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import entropy


def most_common(lst):
    return max(set(lst), key=lst.count)


def run():
    df = pd.read_csv('../../data/Iris.csv')
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

    node_info = []
    for name, data in graph.nodes.data():
        instances = data['instances']
        instance_classes = y[instances]
        node_info.append([name, instance_classes])

    mode_colors = {
        'Iris-setosa': 'red',
        'Iris-virginica': 'blue',
        'Iris-versicolor': 'green'
    }

    pos = nx.spring_layout(graph)
    fig, axs = plt.subplots(figsize=(14, 8), ncols=2)

    axs[0].set_title('Graph colored by class mode')
    cs = set()
    for c in ['Iris-setosa', 'Iris-virginica', 'Iris-versicolor']:
        for ni in node_info:
            if ni[1].mode()[0] != c:
                continue
            nx.draw_networkx_nodes(graph, pos,
                ax=axs[0],
                node_color=mode_colors[c],
                nodelist=[ni[0]],
                node_size=10*ni[1].shape[0],
                label=c if c not in cs else None)
            cs.add(c)
    nx.draw_networkx_edges(graph, pos=pos, ax=axs[0])
    nx.draw_networkx_labels(graph, pos, ax=axs[0])
    axs[0].legend(scatterpoints=1)

    entropy_colors = {
        0.0: 'beige',
        0.1: 'yellow',
        0.2: 'orange',
        0.3: 'darkorange',
        0.4: 'coral',
        1.0: 'red'
    }
    axs[1].set_title('Graph colored by node entropy')
    used_nodes = set()
    threshold_labels = set()
    for treshold, color in entropy_colors.items():
        for ni in node_info:
            e = entropy(ni[1].value_counts() / ni[1].shape[0])
            if ni[0] in used_nodes or e > treshold:
                continue
            used_nodes.add(ni[0])
            nx.draw_networkx_nodes(graph, pos,
                ax=axs[1],
                node_color=color,
                nodelist=[ni[0]],
                node_size=10 * ni[1].shape[0],
                label=f'<= {treshold}' if treshold not in threshold_labels else None)
            threshold_labels.add(treshold)
    nx.draw_networkx_edges(graph, pos=pos, ax=axs[1])
    nx.draw_networkx_labels(graph, pos, ax=axs[1])
    axs[1].legend(scatterpoints=1)

    fig.savefig('../../docs/images/iris.png')


if __name__ == '__main__':
    run()
