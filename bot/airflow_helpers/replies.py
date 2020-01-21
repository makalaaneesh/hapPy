
from logging import info, warning
from bot.airflow_helpers.db_helper import insert_docs, delete_docs, get_docs
from bot.airflow_helpers.twitter_helper import send_tweet


MONGODB_DB = "happy"
MONGODB_COLLECTION_SOURCE = "tweets"
MONGODB_COLLECTION_DESTINATION = "tweet_replies"


def _get_top_depressed_tweets(n):
    aggregate_query = [
                          {'$sort': {"prob": -1}},
                          {'$limit': n}
                      ]
    return get_docs(MONGODB_DB,
                    MONGODB_COLLECTION_SOURCE,
                    aggregate_query)


def _get_uplifting_quote(tweet):
    text = "Sometimes, life will kick you around, but sooner or later, you realize you’re not just a survivor." \
           " You’re a warrior, and you’re stronger than anything life throws your way. - " \
           "Brooke Davis"
    reply_text = "{0} #MentalHealth #MentalHealthAwareness".format(text)
    return reply_text


def _tweet_reply(reply_doc):
    print(reply_doc)

    pass


def send_replies(n):
    tweet_docs = _get_top_depressed_tweets(n)
    reply_documents = []
    for tweet_doc in tweet_docs:
        uplifting_quote = _get_uplifting_quote(tweet_doc['text'])
        reply_doc = {
            'tweet_doc' : tweet_doc,
            'reply' : uplifting_quote,

        }

        # send reply
        _tweet_reply(reply_doc)

        reply_documents.append(reply_doc)

    # inserting them in a different collection
    # _insert_replies(mongo_hook, reply_documents)
    insert_docs(MONGODB_DB, MONGODB_COLLECTION_DESTINATION, reply_documents)


    # removing them from the old collection
    # _delete_tweets(mongo_hook, [doc['tweet_doc']['_id'] for doc in reply_documents])
    delete_docs(MONGODB_DB, MONGODB_COLLECTION_SOURCE, [doc['tweet_doc']['_id'] for doc in reply_documents])


if __name__ == "__main__":
    send_replies(1)
