
from logging import info, warning
from bot.airflow_helpers.db_helper import insert_docs, delete_docs, get_docs
from bot.airflow_helpers.quotes import get_uplifting_quote
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


def _tweet_reply(reply_doc):
    # print(reply_doc)

    text = "@{user_mention} {text}".format(user_mention=reply_doc['tweet_doc']['author'], text=reply_doc['reply'])
    in_reply_to_status_id = reply_doc['tweet_doc']['_id']


    # from datetime import datetime
    # text = "@hapybot test again" + str(datetime.now())
    # in_reply_to_status_id="1219607118698831872"

    print(text, in_reply_to_status_id)
    send_tweet(text, in_reply_to_status_id=in_reply_to_status_id)


def send_replies(n):
    tweet_docs = _get_top_depressed_tweets(n)
    reply_documents = []
    for tweet_doc in tweet_docs:
        uplifting_quote = get_uplifting_quote(tweet_doc['text'])
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
