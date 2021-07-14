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

list_cmp = ["AAPL", "ADBE", "ADI", "ADP", "ALGN", "ALXN", "AMAT", "AMD", "AMGN", "AMZN", "ASML", "ATVI", "AVGO", "BIIB", "BMRN", "CDNS", "CERN", "CHKP", "CMCSA", "COST", "CSCO", "CSX", "CTAS", "CTSH", "CTXS", "EBAY", "EXPE", "FAST", "FB", "FISV", "FOX", "GILD", "GOOG", "GOOGL", "IDXX", "ILMN", "INCY", "INTC", "INTU", "ISRG", "JD", "LBTYA", "LBTYK", "LRCX", "MAR", "MCHP", "MELI", "MSFT", "MXIM", "SAP"]

############ Read data from MongoDB into respective dataframes ##################
def get_all_records(db_name, collection_name):
    client = MongoClient("mongodb://34.72.28.214:27017")
    db = client[db_name]
    col = db[collection_name]
    data=col.find()
    return data

cursor = get_all_records("StockMarket_db", "StocksDaily_14072020")

def naming(company_name):
    for eachValue in cursor:
        metadata1 = eachValue['Time Series (Daily)']
        metadata2 = eachValue["Meta Data"]["2. Symbol"]
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
        print(df.columns)
        return df

company_dict = []
for cmp in list_cmp:
    df_new = naming(cmp)
    company_dict.append(df_new)

od = OrderedDict()
for name, i in zip(list_cmp, range(len(company_dict))):
    od[name] = company_dict[i]

############################ Function to calculate Rank, Stock eligibiliy ####################################
list_reg_slope = []
list_r2 = []
list_annualized_exp_slope = []
list_adjusted_slope = []
list_current_stock_price = []
list_sma = []
list_atr20 =[]
list_eligible = []

thisweek = '15072020'
lastweek = '01072020'

for i in range(len(company_dict)):
    df_last_100_records = od[list_cmp[i]][-100:]
    df_last_100_records.reset_index(drop = True, inplace = True)
    x = np.array(range(0,90))
    y = np.array(df_last_100_records['close'][10:100])
    sma = statistics.mean(df_last_100_records['close'][0:100])
    list_sma.append(sma)
    curr_stock_price = df_last_100_records['close'][99]
    list_current_stock_price.append(curr_stock_price)
    fluctuations =[]
    for n in range(1,90):
        next_day_open_price = df_last_100_records['open'][n]
        previous_day_close_price = df_last_100_records['close'][n-1]
        fluctuation = ((next_day_open_price - previous_day_close_price)/previous_day_close_price)*100
        fluctuations.append(fluctuation)
    filter = (max(fluctuations) < 15) & (curr_stock_price > sma)
    if(filter):
        p = 'ELIGIBLE'
        list_eligible.append(p)
    else:
        p = 'NON_ELIGIBLE'
        list_eligible.append(p)
    list_tr = []
    for m in range(80, 100):
        previous_day_close_price = df_last_100_records['close'][m-1]
        today_high_price = df_last_100_records['high'][m]
        today_low_price = df_last_100_records['low'][m]
        tr20 = max((today_high_price - today_low_price), abs(today_low_price - previous_day_close_price), abs(today_high_price - previous_day_close_price))
        list_tr.append(tr20)
    atr20 = statistics.mean(list_tr)
    list_atr20.append(atr20)
    log_y = []
    for k in range(len(y)):
        y_log = math.log(y[k])
        log_y.append(y_log)
    log_y = np.array(log_y)
    ################# Performing Linear regression #######################
    slope, intercept, r_value, p_value, std_err = linregress(x, log_y)
    list_reg_slope.append(slope)
    r2 = r_value**2
    annualized_exp_slope = np.subtract(pow(np.exp(slope), 250), 1)
    adjusted_slope = r2 * annualized_exp_slope
    list_adjusted_slope.append(adjusted_slope)
    def fittingline(b):
        y_fit = intercept + slope * b
        return y_fit
    line = fittingline(x)  

################### Ranking Table ########################
df_rank = pd.DataFrame(list(zip(list_cmp, list_adjusted_slope, list_atr20, list_eligible, list_current_stock_price)), columns = ['Company', 'AdjustedSlope', 'ATR', 'Eligibility', 'CurrentPrice'])
df_rank = df_rank.sort_values(by = 'AdjustedSlope',ascending=False)
df_rank.reset_index(drop = True, inplace = True)

################# Account value and Risk factor ################
account_value = 1090.12
risk_factor = 0.0025

################### Calculate Stock size ##################
def stock_size_calculation():
    list_stock_size =[]
    for i in range(len(df_rank)):
        stock_size = math.floor((account_value * risk_factor)/df_rank.ATR[i])
        list_stock_size.append(stock_size)
    df_rank['StockSize'] = list_stock_size
    return df_rank
#print(df_rank) 

################## Calculating eligible and non eligible stocks ################
stock_size = stock_size_calculation()
df_eligible = df_rank[df_rank.Eligibility.str.match('ELIGIBLE')]
df_eligible.reset_index(drop = True, inplace = True)
df_noneligible = df_rank[df_rank.Eligibility.str.match('NON_ELIGIBLE')]
df_noneligible.reset_index(drop = True, inplace = True)

################ Buying strategy ##################
top = 12
def buy_stocks():
    balance = account_value
    amount = 0
    list_stock_count = []
    list_balance_after_purchase =[]
    for i in range(top):
        stock_count = 0
        for stsz in range(df_eligible['StockSize'][i]): 
            amount = df_eligible['CurrentPrice'][i] 
            if amount <= balance: 
                balance -= amount          
                stock_count += 1
        list_stock_count.append(stock_count)
        list_balance_after_purchase.append(round(balance,2))
    df_stocks_bought = pd.DataFrame(list(zip(df_eligible['Company'], list_stock_count, list_balance_after_purchase)), columns = ['Company', 'StocksPurchased', 'Balance'])
    return df_stocks_bought

############## Selling Strategy ###############
def sell_stocks():
    ######## Check if this week's non eligible stock is present in last week's file ##########
    df_last_week_data = pd.read_excel(f"C:\\Users\\Hp\\Downloads\\ranking_list_{lastweek}.xlsx", sheet_name='Stocks Purchased')
    list_sold_stock = []
    list_sold_names = []
    list_curr_price = []
    list_stock_available = []
    sell_stock_amount = 0
    balance = 0
    for i in range(len(df_noneligible)):
        for j in range(len(df_last_week_data)):
            if df_noneligible['Company'][i] == df_last_week_data['Company'][j]:
                sell_stock_amount = df_last_week_data['StocksPurchased'][j] * df_noneligible['CurrentPrice'][i]
                balance += sell_stock_amount
                list_sold_names.append(df_noneligible['Company'][i])
                list_sold_stock.append(balance)
                list_curr_price.append(df_noneligible['CurrentPrice'][i])
                list_stock_available.append(df_last_week_data['StocksPurchased'][j])
    df_sold = pd.DataFrame(list(zip(list_sold_names, list_curr_price, list_stock_available, list_sold_stock)), columns = ['Company', 'CurrentPrice', 'StocksSold', 'Total Amount'])
    return df_sold
    
df_stocks_bought = buy_stocks()
updated_account_balance = df_stocks_bought['Balance'][11]
df_eligible[['StocksPurchased', 'Balance']] = df_stocks_bought[['StocksPurchased', 'Balance']]

df_sold = sell_stocks()
with pd.ExcelWriter(f"C:\\Users\\Hp\\Downloads\\ranking_list_{thisweek}.xlsx") as writer:
    df_rank.to_excel(writer, index = False, sheet_name = 'Ranking List')
    df_eligible[0:12].to_excel(writer, index = False, sheet_name = 'Stocks Purchased')
    df_sold.to_excel(writer, index = False, sheet_name = 'Stocks Sold')

################### Calculate percentage allocation of stocks #################
list_percentage_allocation = []
for i in range(len(df_eligible)):
    stocksize = df_eligible['StockSize'][i]
    currentprice = df_eligible['CurrentPrice'][i]
    percent_allocation = round((stocksize * currentprice)/account_value,2)
    list_percentage_allocation.append(percent_allocation)
df_eligible['PercentageAllocation'] = list_percentage_allocation
df_eligible_column_name=df_eligible.columns
df_pie=pd.DataFrame(df_eligible[df_eligible['PercentageAllocation'] != 0].values)
df_pie.set_axis(df_eligible_column_name, axis=1, inplace=True)

############### Linear Regression ##################
def linearregression(company_name):
    x = np.array(range(0,90))
    y = np.array(od[company_name]['close'][10:100])
    log_y = []
    for k in range(len(y)):
        y_log = math.log(y[k])
        log_y.append(y_log)
    log_y = np.array(log_y)
    slope, intercept, r_value, p_value, std_err = linregress(x, log_y)
    y_fit = intercept + slope * x
    return x,log_y,y_fit
