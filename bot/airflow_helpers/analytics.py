from airflow.contrib.hooks.mongo_hook import MongoHook
from airflow.hooks.mysql_hook import MySqlHook
from wordcloud import STOPWORDS
from collections import defaultdict
from models.preprocess import preprocess_text
import unidecode

from bot.airflow_helpers.db_helper import get_all_docs

MONGODB_DB = "happy"
MONGODB_COLLECTION_SOURCE = "tweet_replies"
MYSQL_DB = "happy"
MYSQL_TABLE_DESTINATION = "tweet_analytics_wordcount"


def _get_mysql_hook():
    return MySqlHook(schema=MYSQL_DB)


def _count(word_counter, text):
    text = preprocess_text(text, is_stem=False)
    words = text.split()
    for word in words:
        # to remove accented unicode chars
        word = unidecode.unidecode_expect_ascii(word)
        if word in STOPWORDS:
            continue
        word_counter[word] = word_counter[word]+1
    print(word_counter)


def _get_word_count_depressed_tweets_replied():
    replied_tweet_docs = get_all_docs(MONGODB_DB, MONGODB_COLLECTION_SOURCE)

    word_counter = defaultdict(lambda: 0)
    for tweet_doc_info in replied_tweet_docs:
        tweet_doc_text = tweet_doc_info['tweet_doc']['text']
        _count(word_counter, tweet_doc_text)

    return word_counter


def _insert_word_count_to_mysql(mysql_hook, word_counts):
    # deleting first
    table_name = MYSQL_TABLE_DESTINATION
    delete_sql = "delete from {table_name};".format(table_name=table_name)
    mysql_hook.run(delete_sql)

    # reset autoincrement
    auto_increment_sql = "ALTER TABLE {table_name} AUTO_INCREMENT = 1;".format(table_name=table_name)
    mysql_hook.run(auto_increment_sql)

    word_count_rows = [(word, count) for word, count in word_counts.items()]

    #inserting
    mysql_hook.insert_rows(table_name, word_count_rows,
                           target_fields=('word', 'count'))


def perform_analytics():
    word_counts = _get_word_count_depressed_tweets_replied()
    mysql_hook = _get_mysql_hook()
    _insert_word_count_to_mysql(mysql_hook, word_counts)





