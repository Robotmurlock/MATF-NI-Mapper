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


def kmapper_maximum_of_token_vectors(df: pd.DataFrame, vocabulary: Vocabulary) -> None:
    X = np.stack([vocabulary.maximum(sentence) for sentence in df.TEXT])
    mapper = km.KeplerMapper(verbose=1)
    lens = mapper.fit_transform(X, projection=TSNE(random_state=42))
    graph = mapper.map(lens, X,
                       clusterer=DBSCAN(eps=3.5),
                       cover=km.Cover(n_cubes=14, perc_overlap=0.5))

    kmapper_create_visualization(mapper, graph, df, 'maximum_of_token_vectors')


def kmapper_averaged_token_vectors(df: pd.DataFrame, vocabulary: Vocabulary) -> None:
    X = np.stack([vocabulary.average(sentence) for sentence in df.TEXT])
    mapper = km.KeplerMapper(verbose=1)
    lens = mapper.fit_transform(X, projection=TSNE(random_state=42))
    graph = mapper.map(lens, X,
                       clusterer=DBSCAN(eps=2.2),
                       cover=km.Cover(n_cubes=14, perc_overlap=0.5))

    kmapper_create_visualization(mapper, graph, df, 'averaged_token_vectors')


def kmapper_tfidf_pca_projection(df: pd.DataFrame) -> None:
    X = TfidfVectorizer().fit_transform(df.TEXT).toarray()
    mapper = km.KeplerMapper(verbose=1)
    lens = mapper.fit_transform(X, projection=PCA(n_components=2, random_state=42))
    graph = mapper.map(lens, X,
                       clusterer=DBSCAN(eps=2.0),
                       cover=km.Cover(n_cubes=10, perc_overlap=0.4))

    kmapper_create_visualization(mapper, graph, df, 'tfidf_pca_dbscan')


def kmapper_tfidf_pca_projection_with_cosine_distance_and_dbscan_clustering(df: pd.DataFrame) -> None:
    X = TfidfVectorizer(min_df=3).fit_transform(df.TEXT).toarray()

    mapper = km.KeplerMapper(verbose=1)
    lens = mapper.fit_transform(X, projection=PCA(n_components=2, random_state=42), scaler=None)
    graph = mapper.map(lens, X,
                       clusterer=DBSCAN(eps=0.55, metric='cosine'),
                       cover=km.Cover(n_cubes=8, perc_overlap=0.5),
                       remove_duplicate_nodes=True)

    kmapper_create_visualization(mapper, graph, df, 'tfidf_pca_cosine_dbscan')


def kmapper_tfidf_pca_projection_kmeans(df: pd.DataFrame) -> None:
    X = TfidfVectorizer().fit_transform(df.TEXT).toarray()

    mapper = km.KeplerMapper(verbose=1)
    lens = mapper.fit_transform(X, projection=PCA(n_components=2, random_state=42),
                                scaler=None)
    graph = mapper.map(lens, X,
                       clusterer=KMeans(n_clusters=3),
                       cover=km.Cover(n_cubes=10, perc_overlap=0.4))

    kmapper_create_visualization(mapper, graph, df, f'tfidf_pca_kmeans')


def run():
    df = pd.read_csv('../data/tweet_disaster.csv')
    df = transform(df)

    vocabulary = Vocabulary()
    df.TEXT = df.TEXT.apply(vocabulary.remove_unknown)
    df = df[df.TEXT.str.strip() != '']

    keyword_encoder = LabelEncoder()
    df['KEYWORD_index'] = keyword_encoder.fit_transform(df.KEYWORD)

    kmapper_averaged_token_vectors(df, vocabulary)
    kmapper_maximum_of_token_vectors(df, vocabulary)
    kmapper_tfidf_pca_projection(df)
    kmapper_tfidf_pca_projection_with_cosine_distance_and_dbscan_clustering(df)
    kmapper_tfidf_pca_projection_kmeans(df)


if __name__ == '__main__':
    run()
