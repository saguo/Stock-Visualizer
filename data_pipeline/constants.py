from __future__ import absolute_import

import logging

SOURCE = 'source'
SYMBOLS = 'symbols'
KAFKA_BROKER = 'broker'
KAFKA_TOPIC = 'topic'
KAFKA_OUTPUT_TOPIC = 'output_topic'
CASSANDRA_CONTACT_POINTS = 'contact_points'
REDIS_CHANNEL = 'redis_channel'
REDIS_HOST = 'redis_host'
REDIS_PORT = 'redis_port'

DEFAULT_SYMBOL = 'AAPL'
DEFAULT_KAFKA_BROKER = '127.0.0.1:9092'
DEFAULT_KAFKA_TOPIC = 'data-analyzer'
DEFAULT_KAFKA_OUTPUT_TOPIC = 'data-analyzer-output'
DEFAULT_CASSANDRA_CONTACT_POINTS = '192.168.99.101'
DEFAULT_REDIS_CHANNEL = 'average-stock-price'
DEFAULT_REDIS_HOST = '192.168.99.100'
DEFAULT_REDIS_PORT = '6379'

DEFAULT_LOGGING_LEVEL = logging.DEBUG

SOURCE_GOOGLE_FINANCE = 'google_finance'
VALID_SOURCES = [SOURCE_GOOGLE_FINANCE]