import matplotlib
import matplotlib.pyplot as plt
import io, base64, os, json, re 
import pandas as pd
import numpy as np
import datetime
import matplotlib as mpl
import matplotlib.dates as mdates
import mplfinance as mpf
import statistics
import warnings
warnings.filterwarnings('ignore')

# Read data from CSV file
manu_df = pd.read_csv("F:\\SRH Academics\\Data Engineering\\Project\Data\\daily_MANU.csv")
#print(manu_df.head())

# Aesthetics of the dataframe
manu_df['timestamp'] = pd.to_datetime(manu_df['timestamp'])
manu_df.set_index('timestamp', inplace = True)
manu_df.index.name = 'Date'
manu_df.sort_index(level = 'Date', ascending = True, inplace = True)
manu_df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
#print(manu_df.head())

# Selecting range of dataframe
df_100_days_data = manu_df[-50:]   #considering last 100 days trading data

# Calculating moving average
def simple_ma(no_of_days):
    df = manu_df.copy()
    #chunks = (df[i:i+no_of_days] for i in range(0,len(df),no_of_days))
    for r in no_of_days:
        sma = statistics.mean()

# Making candlestick plot
#mpf.plot(manu_df,type='candle', mav=(3,6,9), volume=True)
kwargs = dict(type='candle', mav=(20), volume=True, figratio=(11,8), figscale=1.00) #considered 20 days moving average
mc = mpf.make_marketcolors(up='g', down='r')
s  = mpf.make_mpf_style(marketcolors=mc, gridstyle = '-') 
mpf.plot(df_100_days_data, **kwargs, style=s)

