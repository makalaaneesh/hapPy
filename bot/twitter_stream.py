import tweepy
from passwords import *
from kafka_helper import KafkaClient


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        #         raise ValueError()
        if status.lang == 'en' and not status.text.startswith("RT"):
            print(status.text)
            kafkac = KafkaClient()
            kafkac.publish_message("raw_tweets", status.id_str, status.text)


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
