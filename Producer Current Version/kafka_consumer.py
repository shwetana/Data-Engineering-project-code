import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads

# class MongoConnection():
#     client = MongoClient()
#     def insert_many_records(self, db_name, collection_name):
#         self.db = MongoConnection.client[db_name]
#         self.col=db[collection_name]

# mymongo = MongoConnection()
# mymongo.insert_many_records("StockMarket", "StocksDaily")         
# consumer = KafkaConsumer('col')
# for data in consumer:
#     json_dailydata = json.loads(data.value)
#     mymongo.col.insert_many(json_dailydata)   
  
consumer = KafkaConsumer(
    'numtest',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

client = MongoClient('localhost:27017')
collection = client.numtest.numtest

for message in consumer:
    message = message.value
    collection.insert_one(message)
    print('{} added to {}'.format(message, collection))