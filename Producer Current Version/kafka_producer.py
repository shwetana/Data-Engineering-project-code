from kafka import KafkaProducer
import json
import config as conf
from logging import log

#Producer class:
class MyKafka:

    #Create Kafka Producer Properties:
    def __init__(self, kafka_brokers):
        self.producer = KafkaProducer(
            key_serializer=lambda key: json.dumps(key).encode('utf-8'), #convert key = symbol into str
            value_serializer=lambda value: json.dumps(value).encode('utf-8'), #convert value = json_data into str
            bootstrap_servers= conf.kafka_broker)

    #New method which sends data to our topic:
    def send_data(self, topic, json_data, symbol, partition):
        future = self.producer.send(topic, partition = partition, key = symbol, value = json_data)
        self.producer.flush()
        record_metadata = future.get(timeout=10)
        #Successful result returns assigned partition and offset
        print (symbol,"TOPIC :== ", record_metadata.topic)
        print (symbol, "PARTITION :== ", record_metadata.partition)
        print (symbol, "OFFSET:==", record_metadata.offset)




