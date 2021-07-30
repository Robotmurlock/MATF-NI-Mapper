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
    features = ['SepalLengthCm', 'SepalWidthCm' , 'PetalLengthCm', 'PetalWidthCm']
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
        overlap_perc=0.3)

    modes = []
    entropies = []
    for name, data in graph.nodes.data():
        instances = data['instances']
        instance_classes = y[instances]
        modes.append([name, instance_classes.mode()[0]])
        entropies.append([name, entropy(instance_classes.value_counts() / instance_classes.shape[0])])

    mode_colors = {
        'Iris-setosa': 'red',
        'Iris-virginica': 'blue',
        'Iris-versicolor': 'green'
    }

    pos = nx.spring_layout(graph)
    fig, axs = plt.subplots(figsize=(14, 8), ncols=2)

    axs[0].set_title('Graph colored by class mode')
    for c in ['Iris-setosa', 'Iris-virginica', 'Iris-versicolor']:
        nx.draw_networkx_nodes(graph, pos,
            ax=axs[0],
            node_color=mode_colors[c],
            nodelist=[m[0] for m in modes if m[1] == c],
            label=c)
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
    used_nodes = []
    for treshold, color in entropy_colors.items():
        nodelist = [e[0] for e in entropies if e[1] <= treshold and e[0] not in used_nodes]
        used_nodes = used_nodes + nodelist
        nx.draw_networkx_nodes(graph, pos,
            ax=axs[1],
            node_color=color,
            nodelist=nodelist,
            label=f'<= {treshold}')
    nx.draw_networkx_edges(graph, pos=pos, ax=axs[1])
    nx.draw_networkx_labels(graph, pos, ax=axs[1])
    axs[1].legend(scatterpoints=1)

    fig.savefig('../../docs/images/iris.png')


if __name__ == '__main__':
    run()
