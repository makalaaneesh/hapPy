import tweepy
from passwords import *
from kafka_helper import MyKafkaProducer

TOPIC_PUB = "raw_tweets"


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        super(MyStreamListener, self).__init__(*args, **kwargs)
        self.kafka_producer = MyKafkaProducer()

    def on_status(self, status):
        #         raise ValueError()
        if status.lang == 'en' and not status.text.startswith("RT"):
            print(status.text)
            status_info = {
                'id': status.id_str,
                'text': status.text
            }
            self.kafka_producer.publish_message(TOPIC_PUB, value=status_info)


    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False
#         import pdb; pdb.set_trace()


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_token,
                               consumer_secret)

    auth.set_access_token(access_token,
                          access_secret)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=auth,
                             listener=myStreamListener)

    myStream.filter(track=['life'])
