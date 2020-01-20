import tweepy
import sys
from multiprocessing import Process
from bot.passwords import *
from bot.kafka_helper import MyKafkaProducer

TOPIC_PUB = "raw_tweets"


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        self.num_tweets = kwargs.pop('num_tweets')
        self.current_num_tweets = 0
        super(MyStreamListener, self).__init__(*args, **kwargs)
        self.kafka_producer = MyKafkaProducer()

    def on_status(self, status):
        if self.current_num_tweets >= self.num_tweets:
            # Limiting to a number.
            return False
            # sys.exit(0)

        if status.lang == 'en' and not status.text.startswith("RT"):
            print(status.text)
            status_info = {
                'id': status.id_str,
                'text': status.text
            }
            print(status_info)
            self.kafka_producer.publish_message(TOPIC_PUB, value=status_info)
            self.current_num_tweets = self.current_num_tweets + 1

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def read_stream_of_tweets(n):
    auth = tweepy.OAuthHandler(consumer_token,
                               consumer_secret)

    auth.set_access_token(access_token,
                          access_secret)

    myStreamListener = MyStreamListener(num_tweets=n)
    myStream = tweepy.Stream(auth=auth,
                             listener=myStreamListener)

    myStream.filter(track=['life'], languages=['en'])


if __name__ == "__main__":
    read_stream_of_tweets(1000)
