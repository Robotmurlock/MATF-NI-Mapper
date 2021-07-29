import pandas as pd
from mapper.lens import PCALens
from mapper.mapper import Mapper
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import networkx as nx


def most_common(lst):
    return max(set(lst), key=lst.count)


def run():
    df = pd.read_csv('../../data/Iris.csv')
    features = ['SepalLengthCm', 'SepalWidthCm' , 'PetalLengthCm', 'PetalWidthCm']
    target = 'Species'
    X, y = df[features], df[target]

    scaler = StandardScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=features)

    lens = PCALens()
    mapper = Mapper()
    graph = mapper.map(X, lens=lens, clusterer=DBSCAN(eps=1.5), n_intervals=10, overlap_perc=0.3)

    modes = []
    for name, data in graph.nodes.data():
        instances = data['instances']
        modes.append(y[instances].mode()[0])

    colors = {
        'Iris-setosa': 'red',
        'Iris-virginica': 'blue',
        'Iris-versicolor': 'green'
    }
    color_map = [colors[m] for m in modes]

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, node_color=color_map, with_labels=True)
    plt.show()


if __name__ == '__main__':
    run()
