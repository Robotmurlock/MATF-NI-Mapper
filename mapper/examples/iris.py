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
        modes.append(instance_classes.mode()[0])
        entropies.append(entropy(instance_classes.value_counts() / instance_classes.shape[0]))

    mode_colors = {
        'Iris-setosa': 'red',
        'Iris-virginica': 'blue',
        'Iris-versicolor': 'green'
    }
    mode_color_map = [mode_colors[m] for m in modes]

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, node_color=mode_color_map, with_labels=True)
    plt.show()

    entropy_colors = {
        0.0: 'beige',
        0.1: 'yellow',
        0.2: 'orange',
        0.3: 'darkorange',
        0.4: 'coral',
        1.0: 'red'
    }
    entropy_color_map = []
    for e in entropies:
        for treshold, color in entropy_colors.items():
            if e <= treshold:
                entropy_color_map.append(color)
                break

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, node_color=entropy_color_map, with_labels=True)
    plt.show()


if __name__ == '__main__':
    run()
