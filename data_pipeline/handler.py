from __future__ import absolute_import

from data_pipeline.constants import *
from data_pipeline.consumer import Consumer
from data_pipeline.logger import Logger
from data_pipeline.processor import Processor
from data_pipeline.producer import Producer
from data_pipeline.scheduler import Scheduler
from data_pipeline.api import Api
import atexit
import redis
import threading
import ujson

logger = Logger.get_logger('data_pipeline.handler')

class Handler(object):
    """ Putting everything together:
        produce or consume stock messages
    """

    @classmethod
    def produce_messages(cls, **kwargs):
        def job(producer_, source_, symbol_):
            if source_ == SOURCE_GOOGLE_FINANCE:
                message = Api.get_google_finance_quotes(symbol_)
            else:
                # should never reach here
                return

            producer_.send(message)

        def shut_down(producer_):
            producer_.shut_down()

        source = kwargs.get(SOURCE)

        if source not in VALID_SOURCES:
            raise Exception('source {} is not valid'.format(source))

        # get producer
        symbols = kwargs.get(SYMBOLS).split(',') or [DEFAULT_SYMBOL]
        kafka_broker = kwargs.get(KAFKA_BROKER) or DEFAULT_KAFKA_BROKER
        kafka_topic = kwargs.get(KAFKA_TOPIC) or DEFAULT_KAFKA_TOPIC

        threads = []
        for symbol in symbols:
            producer = Producer(kafka_broker, kafka_topic)
            atexit.register(shut_down, producer)
            scheduler = Scheduler(3, job, producer, source, symbol)
            threads.append(threading.Thread(target=scheduler.run))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    @classmethod
    def process_messages(cls, **kwargs):

        kafka_broker = kwargs.get(KAFKA_BROKER) or DEFAULT_KAFKA_BROKER
        source_topic = kwargs.get(KAFKA_TOPIC) or DEFAULT_KAFKA_TOPIC
        desitination_topic = kwargs.get(KAFKA_OUTPUT_TOPIC) or DEFAULT_KAFKA_OUTPUT_TOPIC

        processor = Processor('StockAveragePrice', kafka_broker, source_topic, desitination_topic)
        processor.process()

    @classmethod
    def consume_messages(cls, **kwargs):
        def job(consumer_, redis_client_, redis_channel_):
            for msg in consumer_.poll():
                message = msg.value
                logger.info(ujson.loads(message))
                redis_client_.publish(redis_channel_, message)

        def shut_down(consumer_):
            consumer_.shut_down()

        # get consumer
        kafka_broker = kwargs.get(KAFKA_BROKER) or DEFAULT_KAFKA_BROKER
        kafka_topic = kwargs.get(KAFKA_OUTPUT_TOPIC) or DEFAULT_KAFKA_OUTPUT_TOPIC
        consumer = Consumer(kafka_broker, kafka_topic)

        # get redis
        redis_channel = kwargs.get(REDIS_CHANNEL) or DEFAULT_REDIS_CHANNEL
        redis_host = kwargs.get(REDIS_HOST) or DEFAULT_REDIS_HOST
        redis_port = kwargs.get(REDIS_PORT) or DEFAULT_REDIS_PORT
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

        atexit.register(shut_down, consumer)

        scheduler = Scheduler(1, job, consumer, redis_client, redis_channel)
        scheduler.run()