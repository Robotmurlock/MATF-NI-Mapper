import pandas as pd
from tweet_disaster.transform import transform
from tweet_disaster.vocabulary import Vocabulary
import numpy as np
import kmapper as km
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN


def run():
    df = pd.read_csv('../data/tweet_disaster.csv')
    df = transform(df)

    vocabulary = Vocabulary()
    df.TEXT = df.TEXT.apply(vocabulary.remove_unknown)
    df = df[df.TEXT.str.strip() != '']

    X = np.stack([vocabulary.average(sentence) for sentence in df.TEXT])
    y = df.TARGET.values

    mapper = km.KeplerMapper(verbose=1)
    lens = mapper.fit_transform(X, projection=PCA(n_components=5), scaler=None)
    graph = mapper.map(lens, X, clusterer=DBSCAN(eps=1.0), cover=km.Cover(n_cubes=4, perc_overlap=0.3))

    mapper.visualize(
        graph,
        title="Tweet Disaster Mapper",
        path_html="output/tweet_disaster.html",
        custom_tooltips=y,
    )


if __name__ == '__main__':
    run()
