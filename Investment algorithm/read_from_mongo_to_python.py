import pymongo 
import numpy as np
import pandas as pd
from scipy.stats import linregress
import json
from matplotlib import pyplot as plt
import statistics
import math
from pymongo import MongoClient
import requests
from collections import OrderedDict
import datetime

list_cmp = ["AAPL", "ADBE", "ADI", "ADP", "ALGN", "ALXN", "AMAT", "AMD", "AMGN", "AMZN", "ASML", "ATVI", "AVGO", "BIIB", "BMRN", "CDNS", "CERN", "CHKP", "CMCSA", "COST", "CSCO", "CSX", "CTAS", "CTSH", "CTXS", "EBAY", "EXPE", "FAST", "FB", "FISV", "FOX", "GILD", "GOOG", "GOOGL", "IDXX", "ILMN", "INCY", "INTC", "INTU", "ISRG", "JD", "LBTYA", "LBTYK", "LRCX", "MAR", "MCHP", "MELI", "MSFT", "MXIM"]

############ Read data from MongoDB into respective dataframes ##################
def dict_to_dataframe(collection_name):
    # this df is for the first key in dict json
    client = MongoClient()
    db = client["stockmarkets"]
    col = db[collection_name]
    list_cmps = []
    list_symbols = []
    list_metadata_full = []
    list_metadata_dates = []
    cursor = col.find({}).sort("_id", 1)
    #print(cursor[0])
    for eachValue in cursor:
        metadata1 = eachValue['Time Series (Daily)']
        metadata2 = eachValue["Meta Data"]["2. Symbol"]
        #print(metadata2)
        df = pd.DataFrame.from_dict(metadata1, orient='index')
        df['date'] = df.index.values
        list_names = []
        for i in range(100):
            list_names.append(metadata2)
        df['symbol'] = list_names
        df = df.rename(index=str, columns={"1. open":"open", "2. high":"high", "3. low":"low", "4. close":"close", "5. volume":"volume"})
        df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']]
        df = df.sort_values(by='date', ascending=True)
        df.reset_index(drop = True, inplace = True)
        df.open = df.open.astype(float)
        df.close = df.close.astype(float)
        df.high = df.high.astype(float)
        df.low = df.low.astype(float)
        df.volume = df.volume.astype(int)
        print(df)


dict_to_dataframe("StocksDaily")

