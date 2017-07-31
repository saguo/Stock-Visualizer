from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from data_pipeline.logger import Logger
from data_pipeline.producer import Producer


import time
import ujson

logger = Logger.get_logger('data_pipeline.processor')

def process_stream(stream, producer):

    def send_to_kafka(rdd):
        results = rdd.collect()
        for r in results:
            data = ujson.dumps(
                {
                    'symbol': r[0],
                    'timestamp': time.time(),
                    'average': r[1]
                }
            )
            try:
                logger.info('Sending average price %s to kafka' % data)
                producer.send(data)
            except KafkaError as error:
                logger.warn('Failed to send average stock price to kafka, caused by: %s', error.message)

    def create_pair(data):
        record = ujson.loads(data[1].decode('utf-8'))[0]
        return record.get('StockSymbol'), (float(record.get('LastTradePrice')), 1)

    (stream.map(create_pair)
           .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
           .map(lambda (k, v): (k, v[0]/v[1]))
           .foreachRDD(send_to_kafka))

class Processor(object):

    def __init__(self, name, broker, source_topic, destination_topic):
        sc = SparkContext("local[2]", name)
        sc.setLogLevel('ERROR')
        self.ssc = StreamingContext(sc, 5)

        directKafkaStream = KafkaUtils.createDirectStream(
            self.ssc,
            [source_topic],
            {'metadata.broker.list': broker}
        )

        producer = Producer(broker, destination_topic)
        process_stream(directKafkaStream, producer)

    def process(self):
        self.ssc.start()
        self.ssc.awaitTermination()