from abc import ABC, abstractmethod
import pandas as pd
from sklearn.decomposition import PCA


class Lens(ABC):
    @abstractmethod
    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        return df


class PCALens(Lens):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        pca = PCA()
        df = pca.fit_transform(df)
        return df[:, 0]
