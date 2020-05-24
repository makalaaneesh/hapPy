
from logging import info, warning
from bot.airflow_helpers.db_helper import insert_docs, delete_docs, get_docs, get_collection_count, get_all_docs
from bot.airflow_helpers.quotes import get_uplifting_quote, get_follow_up_response
from bot.airflow_helpers.twitter_helper import send_tweet, does_status_exist, get_tweets, user_has_liked_tweet


MONGODB_DB = "happy"
MONGODB_COLLECTION_TWEETS_SOURCE = "tweets"
MONGODB_COLLECTION_TWEETS_DESTINATION = "tweet_replies"

MONGODB_COLLECTION_TWEET_REPLIES_SOURCE = "tweet_replies"


def _get_top_depressed_tweets(n):
    """

    :param n: numberr
    :return: from all the tweets that were categorized as depressed, pick
            the top n tweets.
            "Top" here refers to the probabilistic confidence of th models
            classification.
    """
    docs_to_retrieve = n
    depressed_tweets = []
    visited_depressed_tweet_ids = set()
    non_existent_doc_ids = []

    while len(depressed_tweets) < n:
        collection_count = get_collection_count(MONGODB_DB,
                                                MONGODB_COLLECTION_TWEETS_SOURCE)
        if docs_to_retrieve > collection_count:
            raise ValueError("Collection has only %s documents. Cannot query for more (%s)"
                             % (collection_count, docs_to_retrieve))
            break
        print("Retrieving %s tweets" %(docs_to_retrieve,))
        aggregate_query = [
            {'$sort': {"prob": -1}},
            {'$limit': docs_to_retrieve}
        ]
        docs =  get_docs(MONGODB_DB,
                         MONGODB_COLLECTION_TWEETS_SOURCE,
                         aggregate_query)
        for doc in docs:
            doc_id = str(doc['_id'])
            if doc_id not in visited_depressed_tweet_ids:
                visited_depressed_tweet_ids.add(doc_id)
                # if tweet is deleted since, then we ignore it.
                # We pick only those tweets to which we can reply.
                if does_status_exist(doc_id):
                    depressed_tweets.append(doc)
                else:
                    non_existent_doc_ids.append(doc_id)

        # exponential increase in docs to fetch
        docs_to_retrieve = docs_to_retrieve + (docs_to_retrieve*2)

    # deleting the docs corresponding to the tweets that were deleted.
    delete_docs(MONGODB_DB, MONGODB_COLLECTION_TWEETS_SOURCE, non_existent_doc_ids)
    return depressed_tweets[:n]


def _tweet_reply(docs):
    """
    Send reply to the tweet.
    """
    tweet_doc = docs['tweet_doc']
    reply_doc = docs['reply_doc']

    reply_text = "@{user_mention} {text}".format(user_mention=tweet_doc['author'], text=reply_doc['text'])
    in_reply_to_status_id = tweet_doc['_id']

    print("Replying to ", tweet_doc['text'], "with", reply_doc["text"])
    if hasattr(tweet_doc, 'prob'):
        print(tweet_doc['prob'])
    # print(reply_doc['text'])
    print()
    tweet_reponse = send_tweet(reply_text, in_reply_to_status_id=in_reply_to_status_id)
    reply_doc['_id'] = tweet_reponse.id_str


def send_replies(n):
    tweet_docs = _get_top_depressed_tweets(n)
    reply_documents = []
    for tweet_doc in tweet_docs:
        uplifting_quote = get_uplifting_quote(tweet_doc['text'])
        docs = {
            'tweet_doc': tweet_doc,
            'reply_doc': {'text': uplifting_quote}
        }

        # send reply
        _tweet_reply(docs)

        reply_documents.append(docs)

    # inserting them in a different collection
    insert_docs(MONGODB_DB, MONGODB_COLLECTION_TWEETS_DESTINATION, reply_documents)

    # removing them from the old collection
    # TODO: ideally I could have just updated the existing docs in the same collection.
    delete_docs(MONGODB_DB, MONGODB_COLLECTION_TWEETS_SOURCE, [doc['tweet_doc']['_id'] for doc in reply_documents])


def should_follow_up(tweet_obj, author):
    # if favorite count has increased
        # if person has actually liked
            # true
    if tweet_obj.favorite_count > 0:
        if user_has_liked_tweet(author, tweet_obj.id_str):
            return True
    return False


def follow_up_with_replies():
    # get all documents
    tweet_with_reply_docs = get_all_docs(MONGODB_DB, MONGODB_COLLECTION_TWEET_REPLIES_SOURCE)

    reply_tweet_dict = {doc['reply_doc']['_id']: doc for doc in tweet_with_reply_docs}

    reply_tweet_objs = get_tweets(reply_tweet_dict.keys())

    doc_ids_to_delete = []

    for reply_tweet_obj in reply_tweet_objs:
        reply_tweet_id = reply_tweet_obj.id_str
        reply_tweet_doc = reply_tweet_dict[reply_tweet_id]
        if should_follow_up(reply_tweet_obj, reply_tweet_doc['tweet_doc']['author']):
            # follow up
            tweet_doc = {
                "_id": reply_tweet_id,
                "author": reply_tweet_doc['tweet_doc']['author'],
                "text" : reply_tweet_doc['reply_doc']['text']
            }

            reply_doc = {
                "text" : get_follow_up_response(tweet_doc)
            }

            _tweet_reply({
                "tweet_doc" : tweet_doc,
                "reply_doc" : reply_doc
            })

            # delete as we don't need to follow up any mor
            doc_ids_to_delete.append(str(reply_tweet_dict[reply_tweet_id]['_id']))


    # deleting docs
    delete_docs(MONGODB_DB, MONGODB_COLLECTION_TWEET_REPLIES_SOURCE, doc_ids_to_delete)

    # iterate
    #   if should followup
    #       followup
    #       delete
    #   else
    #       continue #separate job will work on deleting older tweets.
    #

    pass


if __name__ == "__main__":
    send_replies(1)
