from __future__ import absolute_import

from data_pipeline.constants import DEFAULT_LOGGING_LEVEL
import logging
import sys

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format, level=logging.INFO)

class Logger(object):

    @classmethod
    def get_logger(cls, name, threshold_level=DEFAULT_LOGGING_LEVEL):
    	"""
    	:param name: name of logger
    	:param threshold_level: minimum level to be log
    	:return: logging.Logger object
    	"""
        logger = logging.getLogger(name)
        logger.setLevel = threshold_level
        return logger