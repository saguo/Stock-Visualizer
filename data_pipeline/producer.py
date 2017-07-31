from __future__ import absolute_import

from data_pipeline.logger import Logger
from kafka import KafkaProducer
import time
import ujson

logger = Logger.get_logger('data_analyzer.producer')

class Producer(object):
    """ Connect to a kafka broker and send messages
    """

    def __init__(self, broker, topic):
        """ Instantiate a producer given broker and topic
        :param broker: ip and port number of broker, e.g. 127.0.0.1:9092
        :param topic: name of the topic
        :return: None
        """
        self.producer = KafkaProducer(bootstrap_servers=broker, value_serializer=lambda v: ujson.dumps(v).encode('utf-8'))
        self.topic = topic
        logger.info("Setup kafka producer at {} with topic {}".format(broker, topic))

    def send(self, message):
        """ Produce a message
        :param message: the message being produced
        :return: None
        """
        # skip None value
        if message is None:
            return

        self.producer.send(topic=self.topic, value=message, timestamp_ms=time.time())

    def shut_down(self):
        self.producer.flush()
        self.producer.close()