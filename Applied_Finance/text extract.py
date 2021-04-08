

SP_ESG = pd.read_excel('SPXESUP.xlsx', index_col=0, header=0)


import pandas_datareader as reader
from datetime import datetime
factors = reader.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench',SP_ESG.index.min(), SP_ESG.index.max())[0]/100
factors.index= factors.index.to_timestamp(freq='M', how='s')

SP = reader.get_data_yahoo('^GSPC',datetime(SP_ESG.index.min().year, SP_ESG.index.min().month,1), SP_ESG.index.max())['Adj Close'].pct_change()
SP = SP.sample('M').agg(lambda x:(x+1).prod()-1)


print(datetime(SP_ESG.index.min().year, SP_ESG.index.min().month,1))
