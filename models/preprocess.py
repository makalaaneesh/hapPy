import string
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import numpy as np
import emoji


def stem(sentence):
    sno = SnowballStemmer('english')
    filtered_sentence = []

    def is_valid_word(w):
        return w.isalpha()

    for w in sentence.split():
        if is_valid_word(w):
            word_stem = sno.stem(w)
            filtered_sentence.append(word_stem)
        else:
            filtered_sentence.append(w)

    return " ".join(filtered_sentence)


def give_emoji_free_text(text):
    # https: // stackoverflow.com / a / 50602709 / 4434664
    text = text if isinstance(text, str) else text.decode('utf8')
    return emoji.get_emoji_regexp().sub(r'', text)


def preprocess_text(text, is_stem=True, remove_stopwords=False, min_len=25, max_len=400):
    """
    TODO:
    - expand contractions
    """
    if not text:
        return text
    if not isinstance(text, str):
        print(text, type(text))
        if np.isnan(text):
            return None

    # Removing \n
    text = text.replace("\n", "")

    # Removing deleted and removed submissions
    if text in ["[deleted]", "[removed]"]:
        return None

    # removing emoji
    text = give_emoji_free_text(text)

    # Retaining posts between a threshold
    if len(text) > max_len:
        return None
    if len(text) < min_len:
        return None

    # removing punctuation
    translate_table = str.maketrans('', '', string.punctuation)
    text = text.translate(translate_table)

    # lowercase
    text = text.lower()

    text_split = text.split()

    # removing stopwords
    if remove_stopwords:
        english_stopwords = stopwords.words('english')
        text_split = [w for w in text_split
                      if w not in english_stopwords]

    # remove @mentions
    text_split = [w for w in text_split
                  if not w.startswith("@")]

    # remove hypertext links
    text_split = [w for w in text_split
                  if not w.startswith("http")
                  and not w.startswith("www")]

    text = " ".join(text_split)

    # stemming
    if is_stem:
        text = stem(text)

    if not text:
        return None

    return text