
from logging import info, warning
from bot.airflow_helpers.db_helper import insert_docs, delete_docs, get_docs, get_collection_count
from bot.airflow_helpers.quotes import get_uplifting_quote
from bot.airflow_helpers.twitter_helper import send_tweet, does_status_exist


MONGODB_DB = "happy"
MONGODB_COLLECTION_SOURCE = "tweets"
MONGODB_COLLECTION_DESTINATION = "tweet_replies"


def _get_top_depressed_tweets(n):
    docs_to_retrieve = n
    depressed_tweets = []
    visited_depressed_tweet_ids = set()
    non_existent_doc_ids = []

    while len(depressed_tweets) < n:
        collection_count = get_collection_count(MONGODB_DB,
                                                MONGODB_COLLECTION_SOURCE)
        if docs_to_retrieve > collection_count:
            raise ValueError("Collection has only %s documents. Cannot query for more (%s)" %(collection_count, docs_to_retrieve))
            break
        print("Retrieving %s tweets" %(docs_to_retrieve,))
        aggregate_query = [
            {'$sort': {"prob": -1}},
            {'$limit': docs_to_retrieve}
        ]
        docs =  get_docs(MONGODB_DB,
                        MONGODB_COLLECTION_SOURCE,
                        aggregate_query)
        for doc in docs:
            doc_id = str(doc['_id'])
            if doc_id not in visited_depressed_tweet_ids:
                visited_depressed_tweet_ids.add(doc_id)
                if does_status_exist(doc_id):
                    depressed_tweets.append(doc)
                else:
                    non_existent_doc_ids.append(doc_id)

        # exponential increase in docs to fetch
        docs_to_retrieve = docs_to_retrieve + (docs_to_retrieve*2)

    delete_docs(MONGODB_DB, MONGODB_COLLECTION_SOURCE, non_existent_doc_ids)
    return depressed_tweets[:n]



def _tweet_reply(reply_doc):
    # print(reply_doc)

    reply_text = "@{user_mention} {text}".format(user_mention=reply_doc['tweet_doc']['author'], text=reply_doc['reply'])
    in_reply_to_status_id = reply_doc['tweet_doc']['_id']


    # from datetime import datetime
    # text = "@hapybot test again" + str(datetime.now())
    # in_reply_to_status_id="1219607118698831872"

    print(reply_doc['tweet_doc']['text'], reply_doc['tweet_doc']['prob'])
    print(reply_text)
    print()
    send_tweet(reply_text, in_reply_to_status_id=in_reply_to_status_id)


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
