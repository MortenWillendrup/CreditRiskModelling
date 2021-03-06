
# Importing the nessecary modules
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as si
import pandas as pd
df = pd.DataFrame
df1 = pd.DataFrame(data=np.linspace(0, 200, 200,  dtype=int), columns=['V'] )



# Parameters
V = 130
D = 50
r = 0.01
sigma = 0.25
T = 10
q = 0
λ = 0.1
k = -0.1
γ = np.log(0.8)
δ = np.sqrt(0.1)
Ds = 50
Dj = 50

# Time to maturity
dt = 1/1000
tau = np.arange(dt, T+dt, dt)

# Lambda functions

# Normal CDF
N = lambda x: stats.norm.cdf(x)

# Posisson PMF
P = lambda x, k: stats.poisson.pmf(x, k)

# Yield spreads (bps)
s = lambda Model: 10000 * (np.log(D/Model) / tau - r)




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
