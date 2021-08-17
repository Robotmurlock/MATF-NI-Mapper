import pandas as pd
from transform import transform
from vocabulary import Vocabulary
import numpy as np
import kmapper as km
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA


def kmapper_create_visualization(
        mapper: km.KeplerMapper,
        graph: dict,
        df: pd.DataFrame,
        filename: str
        ) -> None:

    def create_tooltip(val) -> str:
        return f'<p>Info: target={val[0]}, keyword={val[1]}<br> Text: {val[2]}</p>'

    mapper.visualize(
        graph,
        title='Tweet Disaster Mapper',
        path_html=f'output/{filename}.html',
        color_values=df[['TARGET', 'KEYWORD_index']],
        color_function_name=['disaster', 'keyword'],
        custom_tooltips=np.array([create_tooltip(val) for val in df[['TARGET', 'KEYWORD', 'TEXT']].values]),
    )


def kmapper_create_from_configuration(df: pd.DataFrame, mapper: km.KeplerMapper, configuration: dict) -> None:
    lens = mapper.fit_transform(configuration['X'], **configuration['lens_args'])
    graph = mapper.map(lens, configuration['X'], **configuration['map_args'])
    kmapper_create_visualization(mapper, graph, df, configuration['name'])


def run():
    df = pd.read_csv('../data/tweet_disaster.csv')
    df = transform(df)

    vocabulary = Vocabulary()
    df.TEXT = df.TEXT.apply(vocabulary.remove_unknown)
    df = df[df.TEXT.str.strip() != '']

    keyword_encoder = LabelEncoder()
    df['KEYWORD_index'] = keyword_encoder.fit_transform(df.KEYWORD)

    mapper = km.KeplerMapper(verbose=1)
    X_glove_maximum = np.stack([vocabulary.maximum(sentence) for sentence in df.TEXT])
    X_glove_average = np.stack([vocabulary.average(sentence) for sentence in df.TEXT])
    X_tfidf = TfidfVectorizer(min_df=3).fit_transform(df.TEXT).toarray()

    configurations = [
        {
            'name': 'kmapper_maximum_of_token_vectors',
            'X': X_glove_maximum,
            'lens_args': {
                'projection': TSNE(random_state=42),
            },
            'map_args': {
                'clusterer': DBSCAN(eps=3.5),
                'cover': km.Cover(n_cubes=14, perc_overlap=0.5)
            }
        },
        {
            'name': 'kmapper_averaged_token_vectors',
            'X': X_glove_average,
            'lens_args': {
                'projection': TSNE(random_state=42),
            },
            'map_args': {
                'clusterer': DBSCAN(eps=2.2),
                'cover': km.Cover(n_cubes=14, perc_overlap=0.5)
            }
        },
        {
            'name': 'kmapper_tfidf_pca_projection',
            'X': X_tfidf,
            'lens_args': {
                'projection': PCA(n_components=2, random_state=42),
            },
            'map_args': {
                'clusterer': DBSCAN(eps=2.0),
                'cover': km.Cover(n_cubes=10, perc_overlap=0.4)
            }
        },
        {
            'name': 'kmapper_tfidf_pca_projection_with_cosine_distance_and_dbscan_clustering',
            'X': X_tfidf,
            'lens_args': {
                'projection': PCA(n_components=2, random_state=42),
                'scaler': None
            },
            'map_args': {
                'clusterer': DBSCAN(eps=0.55, metric='cosine'),
                'cover': km.Cover(n_cubes=8, perc_overlap=0.5),
                'remove_duplicate_nodes': True
            }
        },
        {
            'name': 'kmapper_tfidf_pca_projection_kmeans',
            'X': X_tfidf,
            'lens_args': {
                'projection': PCA(n_components=2, random_state=42),
                'scaler': None
            },
            'map_args': {
                'clusterer': KMeans(n_clusters=3),
                'cover': km.Cover(n_cubes=8, perc_overlap=0.5),
            }
        }
    ]

    for configuration in configurations:
        kmapper_create_from_configuration(df, mapper, configuration)


if __name__ == '__main__':
    run()
