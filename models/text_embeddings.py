from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def _encode_text(xtrain, xtest, col_name, vectorizer):
    """
    Given vectorizer, it will train xtrain[col_name] and transform xtrain[col_name] and xtest[col_name]

    @param vectorizer: sklearn.feature_extraction.text.{CountVectorizer, TfIdfVectorizer}
    """
    vectorizer.fit(xtrain[col_name].values.astype(str))
    train_features = vectorizer.transform(xtrain[col_name].values.astype(str))
    test_features = vectorizer.transform(xtest[col_name].values.astype(str))

    x_train_features = {}
    x_test_features = {}

    x_train_features[col_name] = {
        'data': train_features,
        'names': vectorizer.get_feature_names()
    }
    x_test_features[col_name] = {
        'data': test_features,
        'names': vectorizer.get_feature_names()
    }
    return x_train_features, x_test_features, vectorizer


def encode_bag_of_words(xtrain, xtest, col_name, max_ngram=2):
    essay_bow_vectorizer = CountVectorizer(ngram_range=(1, max_ngram),
                                           min_df=10)
    x_train_features, x_test_features, vectorizer = _encode_text(xtrain, xtest, col_name, essay_bow_vectorizer)

    return x_train_features, x_test_features, vectorizer


def encode_tdfif(xtrain, xtest, col_name, max_ngram=2):
    essay_tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, max_ngram), min_df=10)
    x_train_features, x_test_features, vectorizer = _encode_text(xtrain, xtest, col_name, essay_tfidf_vectorizer)

    return x_train_features, x_test_features, vectorizer

