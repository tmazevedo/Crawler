from kafka import KafkaConsumer
import time
import logging
import json

class KafkaConsumer:
    def __init__(self, topic, bootstrap_servers, auto_offset, auto_commit, group_id):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset=auto_offset,
            enable_auto_commit=auto_commit,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    def execute(self):
        return self.consumer.message.value
