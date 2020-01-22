from logging import info, warn
from airflow.contrib.hooks.mongo_hook import MongoHook


def get_mongo_hook():
    return MongoHook()


def delete_docs(db, collection, doc_ids):
    mongo_hook = get_mongo_hook()
    info("deleting tweets from tweets collection")
    delete_result = mongo_hook.delete_many(mongo_db=db,
                                           mongo_collection=collection,
                                           filter_doc={'_id': {"$in": doc_ids}})

    if delete_result.deleted_count != len(doc_ids):
        raise ValueError("Could not delete all %s docs from collection. "
                         "Only %s were deleted" %(len(doc_ids),
                                                  delete_result.deleted_count))

    info("Succesfully deleted %s docs" %(delete_result.deleted_count))


def insert_docs(db, collection, docs):
    mongo_hook = get_mongo_hook()
    if not docs:
        return
    info("Inserting replies in tweet_replies collection")
    mongo_hook.insert_many(mongo_db=db,
                           mongo_collection=collection,
                           docs=docs)


def get_all_docs(db, collection):
    mongo_hook = get_mongo_hook()
    return mongo_hook.find(mongo_db=db,
                            mongo_collection=collection,
                            query={})


def get_docs(db, collection, agg_query):
    mongo_hook = get_mongo_hook()
    cursor = mongo_hook.aggregate(mongo_db=db,
                                  mongo_collection=collection,
                                  aggregate_query=agg_query)
    return cursor


def get_collection_count(db, collection):
    mongo_hook = get_mongo_hook()
    coll = mongo_hook.get_collection(mongo_collection=collection,
                                     mongo_db=db)

    coll_count = coll.count_documents({})
    return coll_count
