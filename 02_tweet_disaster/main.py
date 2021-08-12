import pandas as pd
from tweet_disaster.transform import transform
from tweet_disaster.vocabulary import Vocabulary
import numpy as np
import kmapper as km
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import LabelEncoder


def run():
    df = pd.read_csv('../data/tweet_disaster.csv')
    df = transform(df)

    vocabulary = Vocabulary()
    df.TEXT = df.TEXT.apply(vocabulary.remove_unknown)
    df = df[df.TEXT.str.strip() != '']

    keyword_encoder = LabelEncoder()
    location_encoder = LabelEncoder()
    df['KEYWORD_index'] = keyword_encoder.fit_transform(df.KEYWORD)
    df['LOCATION_index'] = location_encoder.fit_transform(df.LOCATION)

    X = np.stack([vocabulary.average(sentence) for sentence in df.TEXT])

    mapper = km.KeplerMapper(verbose=1)
    lens = mapper.fit_transform(X, projection=TSNE(random_state=42))
    graph = mapper.map(lens, X,
                       clusterer=DBSCAN(eps=2.2),
                       cover=km.Cover(n_cubes=14, perc_overlap=0.5))

    mapper.visualize(
        graph,
        title="Tweet Disaster Mapper",
        path_html="output/tweet_disaster.html",
        color_values=df[['TARGET', 'KEYWORD_index', 'LOCATION_index']],
        color_function_name=['disaster', 'keyword', 'location'],
        custom_tooltips=np.array(
            [f'<p>[target={val[0]}, keyword={val[1]}, location={val[2]}]</p>' for val
             in df[['TARGET', 'KEYWORD', 'LOCATION']].values]),

    )


if __name__ == '__main__':
    run()
