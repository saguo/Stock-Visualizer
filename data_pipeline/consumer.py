from __future__ import absolute_import

from kafka import KafkaConsumer

class Consumer(object):

    def __init__(self, broker, topic):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=broker)

    def poll(self):
        raw_message = self.consumer.poll()
        messages = []
        for key in raw_message:
            messages.extend(raw_message[key])
        self.consumer.commit()
        return messages

    def shut_down(self):
        self.consumer.close()