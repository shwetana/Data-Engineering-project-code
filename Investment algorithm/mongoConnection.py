from pymongo import MongoClient
import pandas as pd
from collections import OrderedDict

class MongoPythonConnection:
    client = MongoClient('34.72.28.214:27017')

    def get_latet_record(self, db_name, collection_name):
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        doc = col.find().sort("_id", -1)
        latest_doc = doc[0]     
        return latest_doc  

    def get_all_records(self, db_name, collection_name):
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        data=col.find()
        for document in data :
           print(document)
        return data

    def get_records_by_condition(self ,db_name, collection_name , attribute , value) :
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        data=col.find({ attribute : value })
        for document in data :
            print(document)
        return data

    def insert_many_records(self, db_name, collection_name, df):
        db = MongoPythonConnection.client[db_name]
        col=db[collection_name]
        status=col.insert_many(df.to_dict("records"))
        return status

    def insert_one_record(self, db_name, collection_name, record):
        db = MongoPythonConnection.client[db_name]
        col=db[collection_name]
        status= col.insert_one(record)
        return status

    def delete_all_records(self, db_name, collection_name):
        db = MongoPythonConnection.client[db_name]
        col=db[collection_name]
        status=col.delete_many({})
        return status

    def get_records_by_less_then_volume(self, db_name, collection_name, value):
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        cursor = col.find({ "volume" : { "$lt" : value } })
        for document in cursor:
            print(document)

    def get_records_by_greater_then_volume(self, db_name, collection_name, value) :
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        data = col.find({ "volume" : { "$gt" : value } })
        for document in data :
            print(document)

    def count(self, db_name, collection_name):
        db = MongoPythonConnection.client[db_name]
        col = db[collection_name]
        data = col.count()    
        return data

    # def delete_many_records_by_condition(self,collection_name,attribute,value):
    #     col=MongoPythonConnection.db[collection_name]
    #     status=col.delete_many({ attribute : value })
    #     return status
    #
    # def delete_one_records_by_condition(self ,collection_name, attribute , value) :
    #     col =MongoPythonConnection.db[collection_name]
    #     status=col.delete_one({ attribute : value })
    #     return status

#creating instance of pymongoclient
#connection_obj=MongoPythonConnection()
# print('reading file')
#df=pd.read_csv("C:\\Users\\Hp\\Downloads\\intraday_5min_IBM_24-06-20.csv")
# #inserting df into mongodb
# connection_obj.insert_many_records("IBM_5min_Data",df)
#
#to read all document in collection
#connection_obj.get_all_records("StockMarket_db","stock_daily")

# delobj = MongoPythonConnection()
# delobj.delete_all_records('stockmarkets', 'StocksDaily_14072020')

# getObj = MongoPythonConnection()
# getObj.get_all_records("stockmarkets", "StocksDaily_14072020")

# list_cmp = ["AAPL", "ADBE", "ADI", "ADP", "ALGN", "ALXN", "AMAT", "AMD", "AMGN", "AMZN", "ASML", "ATVI", "AVGO", "BIIB", "BMRN", "CDNS", "CERN", "CHKP", "CMCSA", "COST", "CSCO", "CSX", "CTAS", "CTSH", "CTXS", "EBAY", "EXPE", "FAST", "FB", "FISV", "FOX", "GILD", "GOOG", "GOOGL", "IDXX", "ILMN", "INCY", "INTC", "INTU", "ISRG", "JD", "LBTYA", "LBTYK", "LRCX", "MAR", "MCHP", "MELI", "MSFT", "MXIM"]
# for cmp in list_cmp:
#     df = pd.read_csv(f"F:\\SRH Academics\\Data Engineering\\Project\\Data\\5yrs historical data\\{cmp}.csv")
#     #inserting df into mongodb
#     connection_obj=MongoPythonConnection()
#     connection_obj.insert_many_records("StockMarket_db","stocks",df)

countObj = MongoPythonConnection()
countObj.count("StockMarket_db", "StocksDaily_14072020")






