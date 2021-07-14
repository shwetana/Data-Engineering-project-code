import pandas as pd 
import numpy as np
import Investment_algorithm as inv
import math

df_rank = inv.df_rank
#print(df_rank)
df_noneligible = df_rank[df_rank.Eligibility.str.match("NON_ELIGIBLE")]
df_noneligible.reset_index(drop = True, inplace = True)
#print(df_noneligible)
df_last_week_data = pd.read_csv("F:\\SRH Academics\\Data Engineering\\Project\\Data\\4-7-20\\ranking_list_p.csv")
df_this_week_data = pd.read_csv("F:\\SRH Academics\\Data Engineering\\Project\\Data\\6-7-20\\ranking_list.csv")


def sell_stock():
    ######## Check if this week's non eligible stock is present in last week's CSV ##########
    sell_stock_amount = 0
    for i in range(len(df_noneligible)):
        for j in range(len(df_last_week_data['StocksPurchased'])):
            if df_noneligible['Company'][i] == df_last_week_data['Company'][j]:
                sell_stock_amount += df_last_week_data['StocksPurchased'][j] * df_noneligible['CurrentPrice'][i]
    return sell_stock_amount

updated_balance = 2498.28
balance_after_selling = sell_stock() + updated_balance
print("balance_after_selling ", balance_after_selling)

# def cal_stock_size():
#     for i in range(len(df_last_week_data['StocksPurchased'])):
#         for j in range(len(inv.df_eligible['CurrentPrice'])):
#             if df_last_week_data['Company'][i] == inv.df_eligible['Company'][j]:
#                 stock_value = df_last_week_data['StocksPurchased'][i] * inv.df_eligible['CurrentPrice'][j]

def cal_stock_size(stock_size, current_price):
    stock_value = stock_size * current_price
    return stock_value

list_updated_stock = []
list_company_name =[]
list_cp =[]
list_updated_stock_size= []
for i in range(len(df_last_week_data['StocksPurchased'])):
    for j in range(len(inv.df_eligible['CurrentPrice'])):
        if df_last_week_data['Company'][i] == inv.df_eligible['Company'][j]:
            stock_size = cal_stock_size(df_last_week_data['StocksPurchased'][i], inv.df_eligible['CurrentPrice'][j])
            list_updated_stock_size.append(stock_size)
            list_company_name.append(inv.df_eligible['Company'][j])
            list_cp.append(inv.df_eligible['CurrentPrice'][j])
df_updated_stock = pd.DataFrame(list(zip(list_company_name, list_updated_stock_size, list_cp)), columns = ['Company', 'StockSize', 'CurrentPrice'])
print(df_updated_stock)

current_stock_value = 0
for i in range(len(df_updated_stock)):
    current_stock_value += df_updated_stock['StockSize'][i] * df_updated_stock['CurrentPrice'][i]

updated_account_value = inv.account_value + balance_after_selling + current_stock_value

################### Calculate Updated Stock size ##################
account_value = updated_account_value
risk_factor = 0.0025
list_stock_size =[]
for i in range(len(inv.df_rank)):
    stock_size = math.floor((account_value * risk_factor)/df_rank.ATR[i])
    list_stock_size.append(stock_size)
df_rank_stocksize = df_rank
df_rank_stocksize['StockSize'] = list_stock_size
print(df_rank_stocksize) 

# def rebalance():
#     ######## Check if the stocksize has increased or decreased from last week's stock size #########
#     for i in range(len(df_last_week_data['StocksPurchased'])):
#         for j in range(len(inv.df_eligible)):
#             if (df_last_week_data['Company'][i] == inv.df_eligible['Company'][j]) & (df_last_week_data['StocksPurchased'][i] > inv.df_eligible['StockSize'][j]):
#                 #SELL
#                 difference = df_last_week_data['StocksPurchased'][i] - inv.df_eligible['StockSize'][j]
#                 sell_amount = difference * inv.df_eligible['CurrentPrice'][j]
#                 sell_amount += sell_amount
#     return sell_amount

# balance_after_rebalancing = rebalance() + balance_after_selling
# print("balance_after_rebalancing ", balance_after_rebalancing)

# def buy_stock_weekly():
#     balance = balance_after_rebalancing
#     list_tot_stocks_bought =[]
#     for i in range(12):
#         for j in range(12):
#             if (inv.df_eligible['Company'][i] == df_last_week_data['Company'][j]) & (df_last_week_data['StocksPurchased'][j] < inv.df_eligible['StockSize'][i]):
#                 difference = inv.df_eligible['StockSize'][i] - df_last_week_data['StocksPurchased'][j]
#                 for l in range(difference):               



#                 balance -= buy_amount
#                 tot_stocks_bought = inv.df_eligible['StockSize'][i]
#                 list_tot_stocks_bought.append(tot_stocks_bought)
#             elif  (inv.df_eligible['Company'][i] in inv.df_eligible['Company'][0:11]) & (inv.df_eligible['Company'][i] != df_last_week_data['Company'][j]):
#                 for k in range(inv.df_eligible[0:11]):
#                     for l in range(inv.df_eligible['StockSize']):



#                 buy_amount = 

#     return buy_amount
                
    








