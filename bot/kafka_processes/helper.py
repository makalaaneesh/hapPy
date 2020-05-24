from kafka import KafkaProducer, KafkaConsumer
from cached_property import cached_property
import json
from termcolor import colored


def serializer(k_or_v):
    return json.dumps(k_or_v).encode('utf-8')


def deserializer(k_or_v):
    return json.loads(k_or_v.decode('utf-8'))


class MyKafkaClient():
    def __init__(self,
                 bootstrap_servers=['localhost:9092'],
                 api_version=(0,10)
                 ):
        self.bootstrap_servers = bootstrap_servers
        self.api_version = api_version


class MyKafkaProducer(MyKafkaClient):
    @cached_property
    def producer(self):
        # http://blog.adnansiddiqi.me/getting-started-with-apache-kafka-in-python/
        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                      api_version=self.api_version,
                                      value_serializer=serializer)
        except Exception as ex:
            print(colored('Exception while connecting Kafka', 'red'))
            print(colored(str(ex),'red'))
        finally:
            return _producer

    def publish_message(self, topic_name, value, key=None):
        try:
            self.producer.send(topic_name, value=value, key=key)
            self.producer.flush()
            print(colored('Message published successfully:', 'green'), value)
        except Exception as ex:
            print(colored('Could not publish message', 'red'))
            print(colored(str(ex), 'red'))


class MyKafkaConsumer(MyKafkaClient):
    def __init__(self,
                 *args,
                 **kwargs):
        self.topic_sub = kwargs.pop('topic_sub')
        self.group_id = kwargs.pop('group_id')
        super(MyKafkaConsumer, self).__init__(*args, **kwargs)

    @cached_property
    def consumer(self):
        return KafkaConsumer(self.topic_sub,
                             bootstrap_servers=self.bootstrap_servers,
                             api_version=self.api_version,
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id=self.group_id,
                             value_deserializer=deserializer)

    def produce(self, msg):
        """
        In this method, Subclasses should implement the logic
        for loading(ETL) the consumed and transformed message elsewhere.
        """
        raise NotImplementedError()

    def transform(self, msg):
        """
        In this method, subclasses should implement the logic
        to transform(ETL) the consumed message.
        """
        raise NotImplementedError()

    def run(self):
        while True:
            for msg in self.consumer:
                print(colored("Consumed message succesfully:",'green'), msg.value)
                msg_value = msg.value
                transformed_msg = self.transform(msg_value)
                self.produce(transformed_msg)


class MyKafkaConsumerProducer(MyKafkaConsumer, MyKafkaProducer):
    def __init__(self,
                 *args,
                 **kwargs):
        self.topic_pub = kwargs.pop('topic_pub')
        super(MyKafkaConsumerProducer, self).__init__(*args, **kwargs)

    def produce(self, msg):
        if not msg:
            return
        self.publish_message(self.topic_pub, msg)







