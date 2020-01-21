from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from termcolor import colored
from logging import error

from bot.kafka_processes.helper import MyKafkaConsumer


GROUP = "mongo_loader"
TOPIC_SUB = "depression_tweets"


class MongoLoader(MyKafkaConsumer):
    def __init__(self, *args, **kwargs):
        super(MongoLoader, self).__init__(*args, **kwargs)
        self.mongo = MongoClient()

    def transform(self, msg):
        return msg

    def produce(self, msg):
        db = self.mongo.happy

        # using mongo specific id
        msg["_id"] = msg["id"]
        del msg["id"]

        # inserting to mongo
        try:
            db.tweets.insert_one(msg)
            print(colored("Inserted msg into mongo: ", "green"), msg)
        except DuplicateKeyError as e:
            error(e)




if __name__ == "__main__":
    MongoLoader(group_id=GROUP,
                topic_sub=TOPIC_SUB).run()

