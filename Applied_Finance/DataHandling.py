# Modules
import pandas as pd
import pandas_datareader as reader
from datetime import datetime
from linearmodels.asset_pricing import LinearFactorModel
# import sys
# file = open('FamaMacBeth.txt', 'a')
# sys.stdout = file

# Creating the ESG Factor
SP_ESG = pd.read_excel('SPXESUP.xlsx', index_col=0, header=0)

start = datetime(SP_ESG.index.min().year, SP_ESG.index.min().month, 1)
end = SP_ESG.index.max()

SP = reader.get_data_yahoo('^GSPC',start, end)['Adj Close'].pct_change()

SP = SP.resample('M').agg(lambda x:(x+1).prod()-1)

#Checking if the the last date is equal or later than today
if SP.index[-1] >= datetime.now():
    SP.drop(SP.tail(3).index, inplace=True)

if SP_ESG.index[-1] >= datetime.now():
    SP_ESG.drop(SP_ESG.tail(3).index,inplace=True)


SP_ESG['SP500'] = SP.to_frame()

SP_ESG['ESGF'] = SP_ESG.SPXESUP - SP_ESG.SP500

SP_ESG['ESG-SP500_cum'] = (SP_ESG['ESGF'] + 1).cumprod() - 1

ESG = pd.DataFrame()

ESG = (SP_ESG.SP500-SP_ESG.SPXESUP).to_frame()
SP_ESG.index = ESG.index.to_period('M')
# reading in the fama french factors
factors = reader.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench',start, datetime(2021, 1, 31))[0]/100
# factors.index= factors.index.to_timestamp(freq='M', how='s')

ESGF = SP_ESG['ESGF'].T
# print(ESGF.index)
factors_merged = factors.copy()
# print(factors_merged.index)
factors_merged = factors_merged.drop('RF', axis=1)
factors_merged['ESGF'] =ESGF

print(f'factors loaded')
#





# Reading the main xlsx file of portfolios
funds = pd.read_excel('USmutual.xlsx')
# funds = funds.astype(float)
print(f'funds loaded')






funds_ESG = funds[funds['Percent of AUM Covered - ESG']== 100]
print(funds_ESG['Historical Sustainability Score'].min())
print(funds_ESG['Historical Sustainability Score'].max())


funds_ESG['number'] =pd.qcut(funds_ESG['Historical Sustainability Score'], q = 5, labels = False)


funds_ESG['number'].value_counts()
esg_weight = funds_ESG['number'].unique()
esg_weight = esg_weight.tolist()
esg_weight.sort()

esg_dict = {elem : funds_ESG[funds_ESG['number'] == elem] for elem in esg_weight}



# Creating a loop to contain the different types of mutual funds cleaning for nan and integer values
funds_list = []
funds_list = funds['Morningstar Category'].unique()
funds_list = funds_list.tolist()
funds_list = [i for i in funds_list if type(i) is str]




# Creating a dict of DataFrames containing each Category

fund_dict = {}

for fund in funds_list:
    fund_dict[fund.replace(" ","_").replace("-","_")] = vars()[fund.replace(" ","_").replace("-","_")] = \
        fund_dict[fund.replace(" ", "_").replace("-", "_")] = vars()[fund.replace(" ", "_").replace("-", "_")] = \
        funds[(funds['Morningstar Category'] == fund) &
              (funds['Ticker'].notnull())]

funds_list = [fund.replace(" ","_").replace("-","_") for fund in funds_list]


#from datetime import datetime as dt
#Cleaning for performance data
for fund in fund_dict:
    fund_dict[fund] = fund_dict[fund].iloc[:, 26:280]
    fund_dict[fund] = fund_dict[fund].T
    # fund_dict[fund] = fund_dict[fund].astype(float)
    new_header = fund_dict[fund].iloc[0]
    fund_dict[fund] = fund_dict[fund][1:]
    fund_dict[fund].columns = new_header
    fund_dict[fund] = fund_dict[fund].dropna(axis=1)
    # fund_dict[fund].index.name = 'Date'

#converting the index for the DataFrames to datetime indexes
for fund in fund_dict:
    fund_dict[fund].index = pd.to_datetime(fund_dict[fund].index)

# printing the indices to control for DatetimeIndexing
# for fund in fund_dict:
#     print(fund_dict[fund].index)

#Adjust to end of month data
for fund in fund_dict:
    fund_dict[fund].index = fund_dict[fund].index + pd.DateOffset(months=1)
    fund_dict[fund].index =fund_dict[fund].index - pd.tseries.offsets.MonthEnd()

for fund in fund_dict:
    fund_dict[fund] = fund_dict[fund].loc[start:end]
    # fund_dict[fund].to_period('M')

# # Changing to PeriodIndex
# for fund in fund_dict:
#     fund_dict[fund] = fund_dict[fund].to_period('M')

# Changing input from object to float64 and subtract the risk free
for fund in fund_dict:
    cols = fund_dict[fund].columns[fund_dict[fund].dtypes.eq(object)]
    fund_dict[fund][cols] = fund_dict[fund][cols].apply(pd.to_numeric, errors='coerce')
    fund_dict[fund] = fund_dict[fund].sub(factors.RF, axis=0)



# OLS
#Fama MacBeth implemention

import sys
file = open('PM.txt', 'a')
sys.stdout = file

risk_premia =[]
risk_premia_tstats = []
rsquared = []
for fund in fund_dict:
    mod = LinearFactorModel(portfolios=fund_dict[fund],
                    factors=factors_merged)
    res = mod.fit(cov_type='robust')

    print(f'{fund} Riskpremia: {res.risk_premia} \n')
    print(f'\n')
    print(f'{fund} t stats: {res.risk_premia_tstats} \n')
    print(f'\n')
    print(f'{fund} R^2: {res.rsquared} \n')
    risk_premia_tstats.append(res.risk_premia_tstats)
    risk_premia.append(res.risk_premia)
    rsquared.append(res.rsquared)
    print(f'{fund} results added \n')

file.close()
print(f'Calculation the whole data series')
# Create total DataFrame
Total = pd.DataFrame()
Total = funds[funds['Ticker'].notnull()]
Total = Total.iloc[:, 26:280]
Total = Total.T
new_header = Total.iloc[0]
Total = Total[1:]
Total.columns = new_header
Total = Total.dropna(axis=1)

Total.index = Total.index + pd.DateOffset(months=1)
Total.index = Total.index - pd.tseries.offsets.MonthEnd()
Total = Total.loc[start:end]
Total = Total.to_period('M')

Total=Total.astype(float)

Total = Total.loc[:,~Total.columns.duplicated()]
#
#
mod = LinearFactorModel(portfolios=Total,
                        factors=factors_merged)
res = mod.fit(cov_type='robust')
print(f'Total DataFrame:\n {res.risk_premia}')

print(res.risk_premia)
# risk_premia.append(res.risk_premia)
#

# keys = [fund_dict.keys(), 'Total']
#
# Total ={
#     'Mkt-RF' : 0.010843 ,
#     'SMB' : 0.000136 ,
#     'HML' : -0.007313 ,
#     'RMW' : 0.001359 ,
#     'CMA' : -0.001465 ,
#     'ESFG' : 0.000394 }

# risk_premia.append(Total)
#
# fund_dict['Total'] = Total
# print(res.risk_premia)
# Mkt-RF    0.010843
# SMB       0.000136
# HML      -0.007313
# RMW       0.001359
# CMA      -0.001465
# ESFG      0.000394

risk_premia = pd.DataFrame(risk_premia,
                       index=fund_dict.keys(),
                       columns=factors_merged.columns.tolist())
risk_premia.info()

print(risk_premia.to_latex())


#downback plot - Not in use at the moment

# graph_df = SP_ESG.copy()
#
# graph_df.index = graph_df.index.to_timestamp()
#
# graph_df.index = graph_df.index.strftime('%d-%m-%Y')
#
#
# import matplotlib.pyplot as plt
# from scipy.signal import find_peaks
# import pandas_market_calendars as mcal
# import numpy as np
#
# fig, ax = plt.subplots()
# ax = SP_ESG['ESG-SP500_cum'].plot(figsize=(15, 10), use_index=False, ylabel='Cummalative Return ESG index')
# ax.set_xlim(0, SP_ESG.index.size-1)
# ax.grid(axis='x', alpha=0.3)
#
# peaks, _ = find_peaks(SP_ESG['ESG-SP500_cum'], width=8)#, prominence=1)
# troughs, _ = find_peaks(-SP_ESG['ESG-SP500_cum'], width=2)#, prominence=1)
# for peak, trough in zip(peaks, troughs):
#     ax.axvspan(peak, trough, facecolor='red', alpha=.2)
#
# ax.set_ylim(*ax.get_ylim())  # remove top and bottom gaps with plot frame
# drawdowns = np.repeat(False, SP_ESG['ESG-SP500_cum'].size)
# for peak, trough in zip(peaks, troughs):
#     drawdowns[np.arange(peak, trough+1)] = True
# ax.fill_between(np.arange(SP_ESG.index.size), *ax.get_ylim(), where=drawdowns,
#                 facecolor='red', alpha=0.2)
# plt.show()
#
# graph_df.to_excel('ESG_data.xlsx')
#
#
# factors_merged.describe(include=all).T.to_latex()




file.close()