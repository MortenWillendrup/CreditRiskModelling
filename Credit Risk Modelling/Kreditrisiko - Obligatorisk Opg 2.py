from scipy.stats import binom, norm, norminvgauss
import pandas as pd
import numpy as np

def expected_payoff(N, p, a, d, L):
    runTotal = 0
    for k in range(N):
        if d-L*k > 0:
            max1 = d-L*k
        else:
            max1 = 0

        if a - L * k > 0:
            max2 = a - L * k
        else:
            max2 = 0
        runTotal = runTotal+binom.pmf(k, N, p)*(max1 - max2)

    return runTotal

def spread(N, p, a, d, L):
    tmp = ((d-a)/expected_payoff(N, p, a, d, L)-1)*100
    return tmp

tranch_dict = {
    1 : [0,3],
    2 : [3,6],
    3 : [6,9],
    4 : [9,12],
    5 : [12,22],
    6 : [22,100]
    }

expected_payoff_df = pd.DataFrame()

expected_payoff_list = []

spread_df = pd.DataFrame()

spread_list = []

for v,k in tranch_dict.items():
    print(f'E[P({k[0]},{k[1]})] = {expected_payoff(N=125, p=0.01, a=k[0], d=k[1], L=0.8):.5f}')
    # expected_payoff_list.append(round(expected_payoff(N=125, p=0.01, a=k[0], d=k[1], L=0.8),4))
    print(f's({k[0]},{k[1]}) = {spread(N=125, p=0.01, a=k[0], d=k[1], L=0.8)}')
    # spread_list.append(spread(N=125, p=0.01, a=k[0], d=k[1], L=0.8))


for v,k in tranch_dict.items():
    print(f'E[P({k[0]},{k[1]})] = {expected_payoff(N=125, p=0.05, a=k[0], d=k[1], L=0.8):.5f}')
    # expected_payoff_list.append(round(expected_payoff(N=125, p=0.01, a=k[0], d=k[1], L=0.8),4))
    print(f's({k[0]},{k[1]}) = {spread(N=125, p=0.05, a=k[0], d=k[1], L=0.8)}')
    # spread_list.append(spread(N=125, p=0.01, a=k[0], d=k[1], L=0.8))


# Exercise 3
g = lambda x, rho, p : (norm.pdf((np.sqrt(1-rho**2)*norm.ppf(x)-norm.ppf(p))/rho)*(-x)) * (np.sqrt(1-rho**2)/rho) * (1/(norm.pdf(norm.ppf(x))*(-x)))

# Time to maturity

plot_df = pd.DataFrame()

plot_df.insert(0, 'Loss fraction', np.linspace(0, 0.05, 10000))



plot_df['1'] = g(plot_df['Loss fraction'], 0.1, 0.01)
plot_df['2'] = g(plot_df['Loss fraction'], 0.3, 0.01)
plot_df['3'] = g(plot_df['Loss fraction'], 0.5, 0.01)

plot_df.set_index('Loss fraction', inplace=True)
import matplotlib.pyplot as plt
import seaborn as sns


ax = sns.lineplot(data=plot_df)

plt.clf()

plot_df2 = pd.DataFrame()

plot_df2.insert(0, 'Loss fraction', np.linspace(0, 0.05, 10000))



plot_df2['1'] = g(plot_df2['Loss fraction'], 0.1, 0.05)
plot_df2['2'] = g(plot_df2['Loss fraction'], 0.3, 0.05)
plot_df2['3'] = g(plot_df2['Loss fraction'], 0.5, 0.05)

plot_df2.set_index('Loss fraction', inplace=True)
import matplotlib.pyplot as plt
import seaborn as sns


ax = sns.lineplot(data=plot_df2)




plt.show()