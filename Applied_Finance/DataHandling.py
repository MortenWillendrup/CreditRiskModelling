# Modules
import pandas as pd
import pandas_datareader as reader
from datetime import datetime
from linearmodels.asset_pricing import LinearFactorModel


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

SP_ESG['ESG-SP500'] = SP_ESG.SPXESUP - SP_ESG.SP500

SP_ESG['ESG-SP500_cum'] = (SP_ESG['ESG-SP500'] + 1).cumprod() - 1

ESG = pd.DataFrame()

ESG = (SP_ESG.SPXESUP - SP_ESG.SP500).to_frame()

# reading in the fama french factors
factors = reader.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench',start, datetime(2021, 1, 31))[0]/100
# factors.index= factors.index.to_timestamp(freq='M', how='s')

factors_merged = pd.merge(factors, ESG, left_index=True, right_index=True)

header = ['Mkt-RF' ,'SMB', 'HML', 'RMW', 'CMA', 'RF', 'ESG'] # added the ESG header name, we should come up with a new one

factors_merged.columns = header

# factors_merged.index.to_period('M')





# Reading the main xlsx file of portfolios
funds = pd.read_excel('USmutual.xlsx')





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


from datetime import datetime as dt
#Cleaning for performance data
for fund in fund_dict:
    fund_dict[fund] = fund_dict[fund].iloc[:, 26:280]
    fund_dict[fund] = fund_dict[fund].T
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

# Changing to PeriodIndex
for fund in fund_dict:
    fund_dict[fund] = fund_dict[fund].to_period('M')

# Changing input from object to float64
for fund in fund_dict:
    cols = fund_dict[fund].columns[fund_dict[fund].dtypes.eq(object)]
    fund_dict[fund][cols] = fund_dict[fund][cols].apply(pd.to_numeric, errors='coerce')

#Fama MacBeth implemention

risk_premia =[]
for fund in fund_dict:
    mod = LinearFactorModel(portfolios=fund_dict[fund],
                        factors=factors)
    res = mod.fit(cov_type='robust')

    print(res.risk_premia)
    risk_premia.append(res.risk_premia)


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


mod = LinearFactorModel(portfolios=Total,
                        factors=factors)
res = mod.fit(cov_type='robust')

print(res.risk_premia)
risk_premia.append(res.risk_premia)

fund_dict['Total'] = Total


risk_premia = pd.DataFrame(risk_premia,
                       index=fund_dict.keys(),
                       columns=factors.columns.tolist())
risk_premia.info()

print(risk_premia.to_latex())


#downback plot - Not in use at the moment

import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas_market_calendars as mcal
import numpy as np

fig, ax = plt.subplots()
ax = SP_ESG['ESG-SP500_cum'].plot(figsize=(10, 5), use_index=False, ylabel='Cummalative Return ESG index')
ax.set_xlim(0, SP_ESG.index.size-1)
ax.grid(axis='x', alpha=0.3)



peaks, _ = find_peaks(SP_ESG['ESG-SP500_cum'], width=7, prominence=4)
troughs, _ = find_peaks(-SP_ESG['ESG-SP500_cum'], width=7, prominence=4)
for peak, trough in zip(peaks, troughs):
    ax.axvspan(peak, trough, facecolor='red', alpha=.2)

ax.set_ylim(*ax.get_ylim())  # remove top and bottom gaps with plot frame
drawdowns = np.repeat(False, SP_ESG['ESG-SP500_cum'].size)
for peak, trough in zip(peaks, troughs):
    drawdowns[np.arange(peak, trough+1)] = True
ax.fill_between(np.arange(SP_ESG.index.size), *ax.get_ylim(), where=drawdowns,
                facecolor='red', alpha=1)
plt.show()