import pandas as pd
import numpy as np
import requests
import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io
from pandas_datareader import data as pdr
from yahoo_fin.stock_info import*
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
plt.style.use('fivethirtyeight')

company_1 = input("Enter the ticker symbol for the company: ")

ticker_list = [company_1]

yf.pdr_override()

data = pdr.get_data_yahoo([company_1], period='max')

data.drop(columns=['Volume','Close','Low','High','Open'], axis=1, inplace=True)

print(data)

df = data

df['Adj Close'].plot(figsize=(12.2, 6.4))
plt.title('Close Price for '+(company_1))
plt.ylabel('USD Price ($)')
plt.xlabel('Date')
plt.show()

def DEMA(data, time_period, column):
    EMA = data[column].ewm(span=time_period, adjust= False).mean()
    DEMA = 2 * EMA - EMA.ewm(span=time_period, adjust = False).mean()
    
    return DEMA
    
df['DEMA_short'] = DEMA(df, 20, 'Adj Close')
df['DEMA_long'] = DEMA(df, 50, 'Adj Close')

column_list = ['DEMA_short', 'DEMA_long', 'Adj Close']
df[column_list].plot(figsize=(12.2, 6.4))
plt.title('Close Price for '+(company_1))
plt.ylabel('USD Price ($)')
plt.xlabel('Date')
plt.show()

def DEMA_strategy(data):
    buy_list = []
    sell_list = []
    flag = False
    #Loop through the data
    for i in range(0, len(data)):
        if data['DEMA_short'][i] > data['DEMA_long'][i] and flag == False:
            buy_list.append(data['Adj Close'][i])
            sell_list.append(np.nan)
            flag = True
        elif data['DEMA_short'][i] < data['DEMA_long'][i] and flag == True:
            buy_list.append(np.nan)
            sell_list.append(data['Adj Close'][i])
            flag = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
            
    #Store the buy and sell signals/ list into the data set
    data['Buy'] = buy_list
    data['Sell']= sell_list
    
DEMA_strategy(df)

plt.figure(figsize=(12.2, 4.5))
plt.scatter(df.index, df['Buy'], color = 'green', label='Buy Signal', marker = '^', alpha = 1)
plt.scatter(df.index, df['Sell'], color = 'red', label='Sell Signal', marker = 'v', alpha = 1)
plt.plot(df['Adj Close'], label = 'Adj Close Price', alpha = 0.35)
plt.plot(df['DEMA_short'], label = 'DEMA_short', alpha = 0.35)
plt.plot(df['DEMA_long'], label = 'DEMA_long', alpha = 0.35)
plt.xticks(rotation=45)
plt.title('Close Price But and Sell Signals')
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Close Price ($)', fontsize = 18)
plt.legend(loc='upper left')
plt.show()
