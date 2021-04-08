# Modules

import pandas as pd
import datetime as dt

# Reading the main xlsx file of portfolios
funds = pd.read_excel('USmutual.xlsx')


# Creating a loop to contain the different types of mutual funds cleaning of nan and integer values
funds_list = []
funds_list = funds['Morningstar Category'].unique()
funds_list = funds_list.tolist()
funds_list = [i for i in funds_list if type(i) is str]




# Creating a dict of DataFrames containing each Category

fund_dict = {}

for fund in funds_list:
    fund_dict[fund.replace(" ","_").replace("-","_")] = vars()[fund.replace(" ","_").replace("-","_")] = \
        funds[(funds['Morningstar Category'] == fund) &
              # (funds['01-01-2010'].notnull()) &
              (funds['Ticker'].notnull())]

funds_list = [fund.replace(" ","_").replace("-","_") for fund in funds_list]


from datetime import datetime as dt
#Cleaning for performance data
for fund in fund_dict:
    fund_dict[fund] = fund_dict[fund].iloc[:, 26:280]
    fund_dict[fund] = fund_dict[fund].T
    new_header = fund_dict[fund].iloc[0]
    fund_dict[fund] = fund_dict[fund][1:]
    fund_dict[fund].columns = new_header
    fund_dict[fund] = fund_dict[fund].dropna(axis=1)
    fund_dict[fund].index.name = 'Date'

for fund in fund_dict:
    fund_dict[fund].index.to_datetime(format='&Y-%m')

for fund in fund_dict:
    print(fund_dict[fund].index)

#
for fund in fund_dict:
    fund_dict[fund].index = fund_dict[fund].index + pd.DateOffset(months=1)
    fund_dict[fund].index =fund_dict[fund].index - pd.tseries.offsets.MonthEnd()
    fund_dict[fund] = [fund_dict[fund].index.dt.year >= 2010]

# for fund in fund_dict:
#     fund_dict[fund].index.to_datetime()











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

