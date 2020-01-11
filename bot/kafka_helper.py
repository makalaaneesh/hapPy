from kafka import KafkaProducer, KafkaConsumer
from cached_property import cached_property


class KafkaClient():
    def __init__(self,
                 bootstrap_servers=['localhost:9092'],
                 api_version=(0,10)
                 ):
        self.bootstrap_servers = bootstrap_servers
        self.api_version = api_version

    @cached_property
    def producer(self):
        # http://blog.adnansiddiqi.me/getting-started-with-apache-kafka-in-python/
        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                      api_version=self.api_version)
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        finally:
            return _producer


    def publish_message(self, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            self.producer.send(topic_name, key=key_bytes, value=value_bytes)
            self.producer.flush()
            print('Message published successfully.')
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))
