# Modules

import warnings

import pandas as pd
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
import pandas_datareader as reader
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,6)

funds = pd.read_excel('ESG_FACTOR_DATA.xlsx')
funds.drop(funds.columns[0],axis=1,inplace=True)
print(f'Factor data loaded')
funds = funds[funds['Morningstar Sustainability Rating™'].notna()]
funds['Morningstar Sustainability Rating™'].unique()

mapping = {
    'low' : 1,
    'Below Average' :2,
    'Average' : 3 ,
    'Above Average' : 4,
    'High' : 5
}
funds = funds.replace({'Low': 1,
               'Below Average': 2,
               'Average': 3,
               'Above Average': 4,
               'High': 5})



funds['Morningstar Sustainability Rating™'].value_counts()
esg_weight = funds['Morningstar Sustainability Rating™'].unique()
esg_weight = esg_weight.tolist()
esg_weight.sort()

esg_dict = {elem : funds[funds['Morningstar Sustainability Rating™'] == elem] for elem in esg_weight}

for fund in esg_weight:
    weights= (esg_dict[fund]['Fund Size Base Currency']/esg_dict[fund]['Fund Size Base Currency'].sum())
    esg_dict[fund] = esg_dict[fund].iloc[:, 26:]

    esg_dict[fund] = esg_dict[fund].fillna(0)
    esg_dict[fund] = esg_dict[fund].mul(weights, axis=0)
    esg_dict[fund] = esg_dict[fund]/10

esg_dict_output = {}

for fund in esg_weight:
    esg_dict_output[fund] = esg_dict[fund].mean(axis=0)
    esg_dict_output[fund].to_frame()


ESG_factor = esg_dict_output[1] - esg_dict_output[5]

((ESG_factor + 1).cumprod()-1).plot()
plt.show()




all_df = pd.concat(esg_dict_output, axis=1).sum(axis=1, level=0).cumsum()
all_df.columns = ['Low','Below Average', 'Average','Above Average','High']
fig, ax = plt.subplots()


all_df.plot()
ax.legend()
plt.show()

# ESG_factor.to_excel('ESG_FACTOR.xlsx')


