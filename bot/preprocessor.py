from bot.kafka_helper import MyKafkaConsumerProducer
from models.preprocess import preprocess_text


GROUP = "preprocessor"
TOPIC_SUB = "raw_tweets"
TOPIC_PUB = "preprocessed_tweets"


class PreprocessConsumerProducer(MyKafkaConsumerProducer):
    def transform(self, msg):
        msg['preprocessed_text'] = preprocess_text(msg['text'])
        # print(msg)
        # print()
        return msg


if __name__ == "__main__":
    PreprocessConsumerProducer(group_id=GROUP,
                               topic_sub=TOPIC_SUB,
                               topic_pub=TOPIC_PUB).run()

