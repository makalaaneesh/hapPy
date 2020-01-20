from airflow.contrib.hooks.mongo_hook import MongoHook
from wordcloud import STOPWORDS
from collections import defaultdict
from models.preprocess import preprocess_text


def _get_mongo_hook():
    return MongoHook()


def _count(word_counter, text):

    text = preprocess_text(text, is_stem=False)
    words = text.split()
    for word in words:
        word_counter[word] = word_counter[word]+1


def _get_word_count_depressed_tweets_replied(mongo_hook):
    replied_tweet_docs = mongo_hook.find(mongo_db="happy",
                                         mongo_collection="tweet_replies",
                                         query={})

    word_counter = defaultdict(lambda: 0)
    for tweet_doc_info in replied_tweet_docs:
        tweet_doc_text = tweet_doc_info['tweet_doc']['text']
        _count(word_counter, tweet_doc_text)

    return word_counter


def _insert_word_count_to_mongo(mongo_hook, word_counts):
    # deleting first
    mongo_hook.delete_many(mongo_db="happy",
                           mongo_collection="word_count",
                           filter_doc={})

    word_count_docs = [{"_id": word, "count": count} for word, count in word_counts.items()]

    #inserting
    mongo_hook.insert_many(mongo_db="happy",
                           mongo_collection="word_count",
                           docs=word_count_docs)


def perform_analytics():
    mongo_hook = _get_mongo_hook()
    word_counts = _get_word_count_depressed_tweets_replied(mongo_hook)
    _insert_word_count_to_mongo(mongo_hook, word_counts)





