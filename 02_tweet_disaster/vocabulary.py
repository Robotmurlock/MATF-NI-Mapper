import numpy as np
import os


class Vocabulary:
    """
    Mini framework for Glove embeddings which can translate words to vectors using Glove vector representation
    When creating an instance of Vocabulary, file 'glove.6B.100d.txt' is loaded from '../data' path.
    """
    def __init__(self):
        glove_path = '../data/glove.6B.100d.txt'
        assert os.path.exists(glove_path), 'Please download "glove.6B.100d.txt" from '\
                                           '"https://www-nlp.stanford.edu/projects/glove/" '\
                                           'and store it in "data/glove.6B.100d.txt"'

        self.embed = {}
        with open(glove_path) as f:
            for line in f:
                values = line.split(' ')
                token = values[0]
                embedding = np.asarray(values[1:], 'float32')
                self.embed[token] = embedding

    def remove_unknown(self, sentence: str) -> str:
        """
        Removes words from sentence that can't be found in loaded glove file.

        :param sentence: Text with words separeted by spaces ' '.
        :return: Text with removed words that can't be founf in vocabulary.
        """
        return ' '.join([token for token in sentence.split() if token in self.embed])

    def average(self, sentence: str) -> np.array:
        """
        Transforms words in sentence into list of vectors and returns the average of all vectors.

        :param sentence: Text with words separeted by spaces ' '.
        :return: Numpy array that represents averaged vector.
        """
        return np.mean([self.embed[token] for token in sentence.split()], axis=0)

    def maximum(self, sentence: str) -> np.array:
        """
        Transforms words in sentence into list of vectors and returns the maximum of all vectors.

        :param sentence: Text with words separeted by spaces ' '.
        :return: Numpy array that represents maximum vector.
        """
        return np.max([self.embed[token] for token in sentence.split()], axis=0)

