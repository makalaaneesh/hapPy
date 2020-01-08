import pandas as pd
import text_embeddings
import preprocess

def is_text_depressed(model, text, **kwargs):
    text = preprocess.preprocess_text(text)

    x_df = pd.DataFrame(columns=['text'])
    x_df.loc[0] = text

    model_id = kwargs['model_id']
    if model_id == "NB":
        vectorizer = kwargs['vectorizer']
        x_test_features = vectorizer.transform(x_df['text'].values.astype(str))
        return model.predict(x_test_features)[0]


