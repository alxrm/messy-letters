import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib


class LetterClassifier:
    def __init__(self, gamma=1e-3, auto_save=True):
        self._auto_save = auto_save
        self.classifier = SVC(gamma=gamma)

    @staticmethod
    def _transform(images):
        return [np.array(img, dtype='float') for img in images]

    def load(self, dump_filename='clf.pkl'):
        self.classifier = joblib.load(dump_filename)

    def save(self, dump_filename='clf.pkl'):
        joblib.dump(self.classifier, dump_filename)

    def fit(self, images, labels):
        assert(len(images) == len(labels), 'Images list should be of the same size as labels')

        vectorized = self._transform(images)

        self.classifier.fit(vectorized, labels)

        if self._auto_save:
            self.save()

    def predict(self, images):
        vectorized = self._transform(images)

        return self.classifier.predict(vectorized)
