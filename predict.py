import pandas as pd
import text_embeddings
import preprocess
import json

def is_text_depressed(model, text, **kwargs):
    prediction = {}
    text = preprocess.preprocess_text(text)

    x_df = pd.DataFrame(columns=['text'])
    x_df.loc[0] = text

    model_id = kwargs['model_id']
    if model_id == "NB":
        vectorizer = kwargs['vectorizer']
        x_test_features = vectorizer.transform(x_df['text'].values.astype(str))
        prediction['class'] = model.predict(x_test_features)[0]
        prediction['prob'] = model.predict_proba(x_test_features)[0][1]

    if model_id == "SVM":
        vectorizer = kwargs['vectorizer']
        x_test_features = vectorizer.transform(x_df['text'].values.astype(str))
        prediction['class'] = model.predict(x_test_features)[0]


    return prediction


def manual_test(model, **kwargs):
    test_set = {
        "I love my life": 0,
        "I hate my life": 1,
        "Nothing ever goes right for me.":1,
        "Why does everything bad happen with me?": 1,
        "Today was such a good day!":0,
        "Wow. I had such an amazing time":0,
        "Loving how me and my lovely partner is talking about what we want." : 0,
        "Happy Thursday everyone. Thought today was Wednesday so super happy tomorrow is Friday yayyyyy" : 0,
        "It’s the little things that make me smile. Got our new car today and this arrived with it":0,
        "Lately I have been feeling unsure of myself as a person & an artist":1,
        "Feeling down":1,
        "Why bother?":1
    }

    records = []

    for test_text, expected_class in test_set.items():
        prediction = is_text_depressed(model, test_text, **kwargs)
        records.append((test_text, expected_class, prediction['class'], prediction.get('prob', None)))

    records_df = pd.DataFrame.from_records(records, columns=['Text', 'is_depressed(expected)',
                                                             'is_depressed(model output)',
                                                             'model output probability (if any)'])
    return records_df.sort_values('is_depressed(expected)')


def test_tweets_from_file(model, filepath, **kwargs):
    with open(filepath, 'r') as f:
        tweets = json.load(f)
    tweet_texts = list(tweets.values())
    records = []

    for test_text in tweet_texts:
        prediction = is_text_depressed(model, test_text, **kwargs)
        records.append((test_text, prediction['class'], prediction.get('prob', None)))

    records_df = pd.DataFrame.from_records(records, columns=['Text',
                                                             'is_depressed(model output)',
                                                             'model output probability (if any)'])
    return records_df.sort_values('is_depressed(model output)')






