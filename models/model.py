from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from cached_property import cached_property
from logging import warning

import pandas as pd
import pickle
import os
import bz2

from models import helper
from models import preprocess
from models import performance
from models import text_embeddings
from models.constants import BOW, TFIDF, TEXT



MODEL_PATH = "{basepath}/etc/model_{model_id}.pkl"
BASE_PATH = os.environ['HAPPY_HOME']

def dump_model(model):
    path = MODEL_PATH.format(basepath=BASE_PATH,
                             model_id=model.id)
    with bz2.BZ2File(path, 'wb') as f:
    # with open(path, "wb") as f:
        pickle.dump(model, f)


def load_model():
    path = MODEL_PATH.format(basepath=BASE_PATH,
                             model_id="final")
    try:
        with bz2.BZ2File(path, 'rb') as f:
        # with open(path, "rb") as f:
            final_model = pickle.load(f)
    except:
        with open(path, "rb") as f:
            final_model = pickle.load(f)

    return final_model


class Model:
    def __init__(self,
                 model_class,
                 model_params,
                 text_embedder,
                 text_embedder_params,
                 id=""):
        self.id = id
        self.model_class = model_class
        self.model_params = model_params
        self.model = self.model_class(**self.model_params)

        self.x = None
        self.y = None

        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

        default_vectorizer_params = {
            'min_df': 10,
            'ngram_range': (1, 2)
        }
        text_embedder_method = {
            BOW: (text_embeddings.CountVectorizer, default_vectorizer_params),
            TFIDF: (text_embeddings.TfidfVectorizer, default_vectorizer_params)
        }

        self.text_embedder, self.text_embedder_params = text_embedder_method[text_embedder]
        self.text_embedder_params.update(text_embedder_params)
        self.vectorizer = self.text_embedder(**self.text_embedder_params)


    def set_params(self, **new_params):
        _params = self.model_params.copy()
        _params.update(new_params)
        self.model = self.model_class(**_params)

    def _load_data(self):
        self.x, self.y = helper.load_data()

    def _split_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = helper.split_data(self.x, self.y)

    def _fit_vectorizer(self):
        self.vectorizer.fit(self.x_train[TEXT].values.astype(str))

    def _transform(self, x):
        return self.vectorizer.transform(x[TEXT].values.astype(str))

    def _preprocess_text(self, text):
        return preprocess.preprocess_text(text, min_len=0)

    @property
    def final_x_train(self):
        return self._transform(self.x_train)

    @property
    def final_x_test(self):
        return self._transform(self.x_test)

    @property
    def final_y_train(self):
        return self.y_train

    @property
    def final_y_test(self):
        return self.y_test

    def initialize(self):
        """
        1. Loads the data
        2. Splits the data into training and test data.
        3. Creates features by using a vectorizer
        """
        self._load_data()
        self._split_data()
        self._fit_vectorizer()

    def search_hyperparameter(self, params_to_search, scoring='accuracy', cv=5):
        search = GridSearchCV(self.model,
                              params_to_search,
                              cv=cv,
                              scoring=scoring,
                              return_train_score=True)

        search.fit(self.final_x_train, self.final_y_train)
        results = pd.DataFrame.from_dict(search.cv_results_)
        results = results.sort_values(['param_alpha'])
        results['mean_train_score-mean_test_score'] = results['mean_train_score'] - results['mean_test_score']
        return results[['param_alpha', 'mean_train_score', 'mean_test_score', 'mean_train_score-mean_test_score']]

    def fit(self):
        self.model.fit(self.final_x_train, self.final_y_train)

    def predict(self, text):
        prediction = {}

        preprocessed_text = self._preprocess_text(text)
        x_df = pd.DataFrame(columns=['text'])
        x_df.loc[0] = preprocessed_text

        x_test_features = self.vectorizer.transform(x_df['text'].values.astype(str))
        prediction['class'] = int(self.model.predict(x_test_features)[0])
        try:
            prediction['prob'] = float(self.model.predict_proba(x_test_features)[0][1])
        except Exception as e:
            warning(e)
            prediction['prob'] = None

        return prediction

    def get_performance_measures(self):
        return performance.get_performance_measures(self.model, self.final_x_test, self.final_y_test)








