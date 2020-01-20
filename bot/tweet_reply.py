from airflow.contrib.hooks.mongo_hook import MongoHook
from logging import info, warning


def _get_mongo_hook():
    return MongoHook()


def _get_top_depressed_tweets(mongo_hook, n):
    cursor = mongo_hook.aggregate(mongo_db="happy",
                                  mongo_collection="tweets",
                                  aggregate_query=[
                                      {'$sort': {"prob": -1}},
                                      {'$limit': n}
                                  ])
    return cursor
    # client = MongoClient()
    # db = client.happy
    # tweet_docs = db.tweets.find().sort("prob", -1).limit(n)
    # return tweet_docs


def _delete_tweets(mongo_hook, doc_ids):
    info("deleting tweets from tweets collection")
    delete_result = mongo_hook.delete_many(mongo_db="happy",
                                           mongo_collection="tweets",
                                           filter_doc={'_id': {"$in": doc_ids}})

    if delete_result.deleted_count != len(doc_ids):
        import pdb; pdb.set_trace()
        raise ValueError("Could not delete all %s docs from collection. "
                         "Only %s were deleted" %(len(doc_ids),
                                                  delete_result.deleted_count))

    info("Succesfully deleted %s docs" %(delete_result.deleted_count))


def _insert_replies(mongo_hook, reply_docs):
    if not reply_docs:
        return
    info("Inserting replies in tweet_replies collection")
    mongo_hook.insert_many(mongo_db="happy",
                           mongo_collection="tweet_replies",
                           docs=reply_docs)


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
    mongo_hook = _get_mongo_hook()
    tweet_docs = _get_top_depressed_tweets(mongo_hook, n)
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
    _insert_replies(mongo_hook, reply_documents)

    # removing them from the old collection
    _delete_tweets(mongo_hook, [doc['tweet_doc']['_id'] for doc in reply_documents])


if __name__ == "__main__":
    send_replies(1)
