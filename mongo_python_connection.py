#======================================Mongo_Python_connector code=========================================================
from pymongo import MongoClient
import pandas as pd

class MongoPythonConnection:
    #creating MongoClient object to run mongod instance
    # connecting on host-localhost and port-27017
    client = MongoClient('mongodb://34.72.28.214:27017')
    # client = MongoClient()


    #fetching all records
    def get_all_records(self,db_name,collection_name):
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        data=col.find()
        return data

    # inserting all records (use to insert a dataframe from python code)
    def insert_many_records(self,db_name,collection_name,df):
        db = MongoPythonConnection.client[db_name]
        col=db[collection_name]
        status=col.insert_many(df.to_dict("records"))
        return status

    def get_records_by_condition(self ,db_name, collection_name , attribute , value) :
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        data=col.find({ attribute : value })
        return data

    def insert_one_record(self,db_name,collection_name,record):
        db = MongoPythonConnection.client[db_name]
        col=db[collection_name]
        status= col.insert_one(record)
        return status

    def delete_all_records(self,db_name,collection_name):
        db = MongoPythonConnection.client[db_name]
        col=db[collection_name]
        status=col.delete_many({})
        return status

    def get_records_by_less_then_volume(self,db_name,collection_name,value):
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        cursor = col.find({ "volume" : { "$lt" : value } })


    def get_records_by_greater_then_volume(self ,db_name, collection_name , value) :
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        data = col.find({ "volume" : { "$gt" : value } })


