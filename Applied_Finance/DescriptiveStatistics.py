# Modules

import warnings
from datetime import datetime
import pandas as pd
from pandas.core.common import SettingWithCopyWarning
import os
import pandas_datareader as reader
import scipy.stats as stats
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

os.chdir(r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\Kreditrisiko\Python\Applied_Finance\SeminarData')

# Get the current working directory
cwd = os.getcwd()

# Print the current working directory
print("Current working directory: {0}".format(cwd))



portfolios = pd.read_excel('PF_returns.xlsx', index_col=0)
portfolios.index = portfolios.index.to_period('M')
ESG_factor = pd.read_excel('ESG_FACTOR.xlsx', index_col=0)


start = datetime(ESG_factor.index.min().year, ESG_factor.index.min().month, 1)
end = ESG_factor.index.max()



factors = reader.DataReader('Europe_5_Factors', 'famafrench',start, end)[0]/100


factors_merged = factors.copy()

factors_merged = factors_merged.drop('RF', axis=1)
ESG_factor.index = ESG_factor.index.to_period('M')
factors_merged['ESG'] =ESG_factor

# Creating descripte statics

NAME = []
N = []
mean = []
SD = []
skewness = []
Kurtosis = []
tvalue = []
pvalue = []

for name in factors_merged.columns:
    NAME.append(factors_merged[name].name)
    N.append(len(factors_merged[name].index))
    mean.append(round(factors_merged[name].mean()*100,3))
    SD.append(round(factors_merged[name].std() * 100, 3))
    skewness.append(round(factors_merged[name].skew(), 3))
    Kurtosis.append(round(factors_merged[name].kurtosis(), 3))
    tvalue.append(round(stats.ttest_1samp(factors_merged[name], 0)[0], 3))
    pvalue.append(round(stats.ttest_1samp(factors_merged[name], 0)[1], 3))
    print(stats.ttest_1samp(factors_merged[name], 0))

columns = [NAME, N, mean, SD, skewness, Kurtosis, tvalue, pvalue]

df = pd.DataFrame(columns)

new_header = df.iloc[0]
df = df[1:]
df.columns = new_header
df = df.dropna(axis=1)

df = df.T
df.columns = ['N', 'mean', 'SD', 'skewness', 'Kurtosis', 'tvalue', 'pvalue']


df.to_excel('DevStats.xlsx')
                                                                                                                                                                                                                                                                                                                                               ''''