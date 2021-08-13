import numpy as np
import pandas as pd


class Vocabulary:
    def __init__(self):
        self.embed = {}
        with open('../data/glove.6B.100d.txt') as f:
            for line in f:
                values = line.split(' ')
                token = values[0]
                embedding = np.asarray(values[1:], 'float32')
                self.embed[token] = embedding

    def remove_unknown(self, sentence: str) -> str:
        return ' '.join([token for token in sentence.split() if token in self.embed])

    def average(self, sentence: str) -> np.array:
        return np.mean([self.embed[token] for token in sentence.split()], axis=0)

    def maximum(self, sentence: str) -> np.array:
        return np.max([self.embed[token] for token in sentence.split()], axis=0)

