import numpy as np
from sklearn.svm import SVC


class LetterClassifier:
    def __init__(self, gamma=1e-3):
        self.classifier = SVC(gamma=gamma)

    @staticmethod
    def _transform(images):
        return [np.array(img, dtype='float') for img in images]

    def load(self):
        pass

    def save(self):
        pass

    def fit(self, images, labels):
        vectorized = self._transform(images)

        assert(len(vectorized) == len(labels), 'Images list should be of the same size as labels')

        self.classifier.fit(vectorized, labels)

    def predict(self, images):
        vectorized = self._transform(images)

        return self.classifier.predict(vectorized)
