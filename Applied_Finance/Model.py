
import pandas as pd


funds = pd.read_excel('USmutual.xlsx')

Large_cap_funds = funds[(funds['Morningstar Category'] == 'US Fund Large Blend') & (funds['2010-01-01'].notnull()) & (funds['Ticker'].notnull())]


Large_cap_funds.drop(Large_cap_funds.columns[2:147], inplace=True, axis =1)
Large_cap_funds.drop(Large_cap_funds.columns[136:540], inplace=True, axis =1)
Large_cap_funds.drop(Large_cap_funds.columns[0:1], inplace=True, axis =1)
Large_cap_funds_transposed = Large_cap_funds.T
Large_cap_funds_transposed.drop(Large_cap_funds.columns[134:160], inplace=True, axis =0)

new_header = Large_cap_funds_transposed.iloc[0]

df = Large_cap_funds_transposed[1:]

df.columns = new_header
df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

# df.reset_index(inplace=True)

# df.plot(x=df['index'])

df.isnull().sum()

df_good_data = df.dropna(axis=1)

df_good_data.info()






