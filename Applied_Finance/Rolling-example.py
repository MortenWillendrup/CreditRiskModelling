import pandas_datareader as pdr
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
from statsmodels.api import OLS, add_constant
import matplotlib.pyplot as plt
import seaborn
seaborn.set_style('darkgrid')
pd.plotting.register_matplotlib_converters()

#%%
factors = pdr.get_data_famafrench('F-F_Research_Data_Factors', start='1-1-2020')[0]
# print(factors.head())
industries = pdr.get_data_famafrench('17_Industry_Portfolios', start='1-1-2020')[0]
# print(industries.head())

#%%
exog_vars = ['Mkt-RF', 'SMB', 'HML','RF']
exog = sm.add_constant(factors[exog_vars])
returns = industries.sub(factors.RF, axis=0)


#%%
betas = []
rsquared = []
#%%
for industry in returns.columns:
    # print(returns.loc[returns.index, industry])
    endog = returns.loc[returns.index, industry]
    rols = RollingOLS(endog, exog, window=12)
    rres = rols.fit()
    params = rres.params.mean()
    betas.append(params.drop('const'))
    rsquared.append(rres.rsquared.mean())


betas = pd.DataFrame(betas,
                     columns=factors.columns,
                     index=industries.columns)
# betas = betas.drop(columns='RF')
# betas = betas.T
betas.info()


#%%
lambdas = []
#%%
# Second Stage regression


for period in industries.index:
    step2 = OLS(endog=industries.loc[period, betas.index],
                exog=betas).fit()
    lambdas.append(step2.params)


#%%
lambdas = pd.DataFrame(lambdas,
                       index=industries.index,
                       columns=betas.columns.tolist())

#%%
lambdas.mean()


#%%
ax1 = plt.subplot2grid((1, 3), (0, 0))
ax2 = plt.subplot2grid((1, 3), (0, 1), colspan=2)
ax2.margins(0.01)
lambdas.mean().plot.barh(ax=ax1)
lambdas0 = lambdas.rolling(6).mean().dropna()
lambdas0.plot(lw=2, figsize=(17,8), ax=ax2)
ax2.legend(bbox_to_anchor=(1.025, 1.05))
plt.show()

lambdas.rolling(12).mean().dropna().plot(lw=2, figsize=(14,20), subplots=True, sharey=True, sharex=True)
plt.show()