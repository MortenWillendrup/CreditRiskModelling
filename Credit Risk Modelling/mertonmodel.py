import numpy as np
import scipy.stats as si
import sympy as sy
from sympy.stats import Normal, cdf
from sympy import init_printing
init_printing()
import pandas as pd


def bs_call(v, D, T, r, sigma):
    # S: spot price
    # K: strike price
    # T: time to maturity
    # r: interest rate
    # sigma: volatility of underlying asset

    d1 = (np.log(v / D) + (0.5 * sigma ** 2) * T + r*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call = (v * si.norm.cdf(d1, 0.0, 1.0) - D * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))

    return call

def merton_equity(v, d, sigma, r, t,T):
    """
    v - Value of firm
    d - ZCB value
    sigma - volatility
    r - riskfree interest rate
    T - Last period
    t - current period
    """
    period = T-t

    d1 = (np.log(v / d) + (0.5 * sigma ** 2) * period + r * period) / (sigma * np.sqrt(period))
    d2 = d1 - sigma * np.sqrt(period)

    equity = (v * si.norm.cdf(d1, 0.0, 1.0) - d * np.exp(-r * period) * si.norm.cdf(d2, 0.0, 1.0))

    return equity

def merton_debt(v, d, sigma, r, t, T):
    debt = v - merton_equity(v, d, sigma, r, t, T)

    return debt


print(merton_debt(180, 50, 0.025, 0.01, 0, 1))


import numpy as np
import pandas as pd

df = pd.DataFrame(data=np.linspace(0, 200, 200,  dtype=int), columns=['V'] )

param = {
            "v": 180,
            "Ds": 50,
            "Dj": 50,
            "r": 0.01,
            "sigma": 0.25,
            "T": 1
        }

df['B'] = merton_debt(df['V'], 50, 0.25, 0.01, 0, 1)

df['S'] = merton_equity(df['V'], 50, 0.25, 0.01, 0, 1)

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

sns.lineplot(data=[df['B'],df['S']])
plt.legend(['Debt','Equity'], ncol=2, loc='upper left')

plt.show()



import numpy as np
import scipy.stats as si
import pandas as pd
import sympy as sy
from sympy.stats import Normal, cdf
from sympy import init_printing
init_printing()
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def Senior_debt(v, ds, T, r, sigma):
    # S: spot price
    # K: strike price
    # T: time to maturity
    # r: interest rate
    # sigma: volatility of underlying asset

    d1 = (np.log(v / ds) + (0.5 * sigma ** 2) * T + r*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    Senior_debt = v - (v * si.norm.cdf(d1, 0.0, 1.0) - ds * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))

    return Senior_debt

print(Senior_debt(90, 50, 1, 0.01, 0.25))


def Junior_debt(v, ds, dj, T, r, sigma):
    # S     : value of firm
    # ds    : senior debt
    # dj    : junior debt
    # T     : time to maturity
    # r: interest rate
    # sigma: volatility of underlying asset

    d1 = (np.log(v / (ds+dj)) + (0.5 * sigma ** 2) * T + r*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    d1_senior = (np.log(v / ds) + (0.5 * sigma ** 2) * T + r*T) / (sigma * np.sqrt(T))
    d2_senior = d1_senior - sigma * np.sqrt(T)

    Junior_debt = (v * si.norm.cdf(d1_senior, 0.0, 1.0) - ds * np.exp(-r * T) * si.norm.cdf(d2_senior, 0.0, 1.0)) \
                  - (v * si.norm.cdf(d1, 0.0, 1.0) - (ds+dj) * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))


    return Junior_debt

print(Junior_debt(90, 50, 50, 1, 0.01, 0.25))


def sub_equity(v, ds, dj, T, r, sigma):
    # S     : value of firm
    # ds    : senior debt
    # dj    : junior debt
    # T     : time to maturity
    # r: interest rate
    # sigma: volatility of underlying asset

    d1 = (np.log(v / (ds+dj)) + (0.5 * sigma ** 2) * T + r*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    sub_equity = (v * si.norm.cdf(d1, 0.0, 1.0) - (ds+dj) * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    return sub_equity

param={
            "v" : 180,
            "Ds" : 50,
            "Dj" : 50,
            "r" : 0.01,
            "sigma" : 0.25,
            "T" : 1
            }
import numpy as np
import scipy.stats as si
def CreditSpreadMerton(V, D, T, t, sigma, r):
    tau = T-t

    d1 = (np.log(V / D) * (r + sigma ** 2 / 2) * tau) / (sigma * np.sqrt(tau))

    d2 = d1 - sigma*np.sqrt(tau)

    spread = (-1/tau) * si.norm.cdf(d2, 0.0, 1.0) + V * np.exp(r * tau) * si.norm.cdf(-d1 / D, 0.0, 1.0) #* 1e4 # in terms of bps

    return spread


# print(Junior_debt(param['v'],param['Ds'], param['Dj'], 15, param['r'], param['sigma']))

df2 = pd.DataFrame(data=np.linspace(1, 30, 30,  dtype=int), columns=['T'] )

df2['Senior debt'] = Senior_debt(param['v'],param['Ds'],df2['T'],param['r'],param['sigma'])

df2['Junior debt'] = Junior_debt(param['v'],param['Ds'], param['Dj'], df2['T'],param['r'], param['sigma'])

df2['Equity'] = sub_equity(param['v'],param['Ds'], param['Dj'], df2['T'],param['r'], param['sigma'])

df2['Senior spread'] = CreditSpreadMerton(param['v'],df2['Senior debt'],len(df2['T']),df2['T'],  param['sigma'],param['r'])

df2['Junior spread'] = CreditSpreadMerton(param['v'],df2['Junior debt'],len(df2['T']),df2['T'],  param['sigma'],param['r'])

sns.lineplot(data=[df2['Senior spread'], df2['Junior spread']])

#sns.lineplot(data=[df2['Senior debt'], df2['Junior debt'], df2['Equity']])


plt.show()

param={
            "v" : 90,
            "Ds" : 50,
            "Dj" : 50,
            "r" : 0.01,
            "sigma" : 0.25,
            "T" : 1
            }

df3 = pd.DataFrame(data=np.linspace(0, 11, 11,  dtype=int), columns=['T'] )

df3['Senior spread'] = CreditSpreadMerton(150,100,11,df2['T'],  0.20,0.05)

df3['Junior spread'] = CreditSpreadMerton(180,50,30,df2['T'],  0.25,0.01)

sns.lineplot(data=df2['Senior spread'])

plt.show()


def yield_bond(d,b,t,T):
    import numpy as np
    y = (1/(T-t))/np.log(d/b)

    return y

def credit_spread(d, b, t, T, r):
    spread = yield_bond(d, b, t, T) - r
    return spread


param={
            "v" : 150,
            "Ds" : 50,
            "Dj" : 50,
            "r" : 0.01,
            "sigma" : 0.25,
            "T" : 1
            }

df4 = pd.DataFrame(data=np.linspace(0, 10, 10,  dtype=int), columns=['T'] )

# df4['Senior debt'] = Senior_debt(param['v'],param['Ds'],df4['T'],param['r'],param['sigma'])

# df4['Junior debt'] = Junior_debt(param['v'],param['Ds'], param['Dj'], df4['T'],param['r'], param['sigma'])

df4['Senior spread'] = credit_spread(150,100, df4['T'], len(df4['T']),param['r'])*1e4

df4['Junior spread'] = credit_spread(50,90, df4['T'], len(df4['T']),param['r'])*1e4


sns.lineplot(data=[df4['Senior spread'], df4['Junior spread']])

plt.show()



df5 = pd.DataFrame(data=np.linspace(0, 100, 100,  dtype=int), columns=['T'] )
senior spread = np.log(Senior_debt(v,ds,T,r, sigma)/merton_debt(v,d,sigma,r,t,T))-r