# Modules

import warnings
from datetime import datetime
import pandas as pd
from pandas.core.common import SettingWithCopyWarning
import os
import pandas_datareader as reader
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

os.chdir(r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\Kreditrisiko\Python\Applied_Finance\SeminarData')

# Get the current working directory
cwd = os.getcwd()

# Print the current working directory
print("Current working directory: {0}".format(cwd))
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
ax = plt.figure()

plt.rcParams["figure.figsize"] = (15,6)


ESG_factor = pd.read_excel('ESG_FACTOR.xlsx', index_col=0)
start = datetime(ESG_factor.index.min().year, ESG_factor.index.min().month, 1)
end = ESG_factor.index.max()
cum_df = pd.DataFrame()

cum_df['ESG'] =  ((ESG_factor['ESG'] + 1).cumprod() - 1)

C25 = reader.get_data_yahoo('OMXC20',start, end)['Adj Close'].pct_change()
C25_ret = C25.resample('M')
cum_df['C25'] = C25_ret.cumsum()


ax =((ESG_factor + 1).cumprod() - 1).plot()

ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
plt.tight_layout()
ax.get_legend().remove()
plt.savefig('ESG_cumulative.png', dpi=1200)

plt.show()