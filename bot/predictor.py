import sys
import os
sys.path.insert(0, os.path.abspath("../models/"))


from kafka_helper import MyKafkaConsumerProducer
import models


GROUP = "predictor"
TOPIC_SUB = "preprocessed_tweets"
TOPIC_PUB = "depression_tweets"


class PredictorConsumerProducer(MyKafkaConsumerProducer):
    def __init__(self, *args, **kwargs):
        super(PredictorConsumerProducer, self).__init__(*args, **kwargs)
        self.model = models.load_model()

    def transform(self, msg):
        prediction_info = self.model.predict(msg['text'])
        # print(type(msg['text']))
        # print(msg)
        # print(prediction_info)
        # print()
        if prediction_info['class'] == 1:
            msg.update(prediction_info)
            return msg
        return None


if __name__ == "__main__":
    PredictorConsumerProducer(group_id=GROUP,
                               topic_sub=TOPIC_SUB,
                               topic_pub=TOPIC_PUB).run()

