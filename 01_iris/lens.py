from abc import ABC, abstractmethod
import pandas as pd
from sklearn.decomposition import PCA


class Lens(ABC):
    """
    Abstraction for 1d filter function.
    """
    @abstractmethod
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        :param df: Input data for filter function
        :return: Range of filter function
        """
        pass


class PCALens(Lens):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        :param df: Input data for filter function
        :return: Main component of PCA decomposition
        """
        pca = PCA()
        df = pca.fit_transform(df)
        return df[:, 0]
