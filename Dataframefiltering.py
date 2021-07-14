import pandas as pd
from mongo_python_connection import MongoPythonConnection

def getAllRecordsFromDB():
    #==============================to get from db==================================================================
    connection_obj = MongoPythonConnection()
    db=connection_obj["StockMarket_db"]
    col=connection_obj["new_stocks"]
    myquery={'time_stamp':{"$gt":"2020-07-14 02:46:00"}}
    mydoc=col.find(myquery)
    df = pd.DataFrame(list(mydoc))
    df.drop('_id', axis=1, inplace=True)
    df.sort_values(by=['time_stamp'], inplace=True, ascending=False)
    df_new = df.drop_duplicates()
    df_new.rename(columns={ "time_stamp" : "date" } , inplace=True)
    return df_new

#===============================================================================================================================================

