import requests
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib as plt

API_KEY = 'MJLPMBB0U80SOFBK'

stock_name = 'IBM'

r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock_name + '&apikey=' + API_KEY)

print(r.status_code)

result = r.json()

dataForAllDays = result['Time Series (Daily)']
print(type(result))

#convert to dataframe

df = pd.DataFrame.from_dict(dataForAllDays, orient='index') 

df = df.reset_index()

#rename columns

df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})