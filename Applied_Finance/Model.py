

# Modules

import pandas as pd


# Reading the main xlsx file of portfolios

funds = pd.read_excel('USmutual.xlsx')

# Creating a loop to contain the different types of mutual funds cleaning of nan and integer values
funds_list = []
funds_list = funds['Morningstar Category'].unique()
funds_list = funds_list.tolist()
funds_list = [i for i in funds_list if type(i) is not int]
funds_list = [i for i in funds_list if str(i) != 'nan']
funds_list = [fund.replace(" ","_").replace("-","_") for fund in funds_list]

for fund in funds_list:
    print(fund)


# Creating DataFrames for each Category
for fund in funds_list:
    vars()[fund.replace(" ","_").replace("-","_")] = funds[(funds['Morningstar Category'] == fund) & (funds['2010-01-01'].notnull()) &
                         (funds['Ticker'].notnull())]






Large_cap_funds.to_csv('Large_cap_funds.csv', index=True)

Large_cap_funds = pd.read_csv('Large_cap_funds.csv',index_col=0)




Large_cap_funds.drop(Large_cap_funds.columns[2:147], inplace=True, axis =1)
Large_cap_funds.drop(Large_cap_funds.columns[136:540], inplace=True, axis =1)
Large_cap_funds.drop(Large_cap_funds.columns[0:1], inplace=True, axis =1)
Large_cap_funds_transposed = Large_cap_funds.T
Large_cap_funds_transposed.drop(Large_cap_funds.columns[134:160], inplace=True, axis =0)

new_header = Large_cap_funds_transposed.iloc[0]

df = Large_cap_funds_transposed[1:]

df.columns = new_header

df_good_data = df.dropna(axis=1)

df_good_data.to_csv('Large_funds_cleaned.csv', index=True)
from dateutil.relativedelta import *


import pandas as pd
df_good_data =pd.read_csv('Large_funds_cleaned.csv', index_col=0)
df_good_data.index = pd.to_datetime(df_good_data.index)
df_good_data.index = df_good_data.index + pd.DateOffset(months=1)
df_good_data.index = df_good_data.index - pd.tseries.offsets.MonthEnd()




df_good_data.info()

import pandas_datareader as reader
from datetime import datetime
factors = reader.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench',datetime(2010,1,1), datetime(2021,1,1))[0]/100
factors.index= factors.index.to_timestamp(freq='M', how='s')
factors.info()

df_good_data.name ='Date'
factors.index.name = 'Date'



merged_df = pd.merge(df_good_data, factors, left_index=True, right_index=True)

import pandas_datareader as reader
from datetime import datetime
indices_sp500 = reader.get_data_yahoo('^GSPC',datetime(2010,1,1), datetime(2021,1,1))['Adj Close']
indices_sp500_ESG = reader.get_data_yahoo('^SPXESUP',datetime(2010,1,1), datetime(2021,1,1))['Adj Close']

