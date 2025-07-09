# Oil Shock Analysis with GARCH and Macro Data

import pandas as pd
import numpy as np
import yfinance as yf
from arch import arch_model
from statsmodels.api import OLS, add_constant
from pandas_datareader.data import DataReader
import os

# 1. Parameters
start_date = "2007-01-01"
end_date = "2024-12-31"
os.environ["FRED_API_KEY"] = "your_fred_api_key_here"  # Replace with your FRED API key

# 2. Daily Brent prices (Close only)
brent_df = yf.download("BZ=F", start=start_date, end=end_date, interval='1d')[['Close']].dropna()
brent_df.columns = ['Close']

# 3. Monthly Brent returns (log)
brent_mensal = brent_df.resample('ME').last()
brent_ret = np.log(brent_mensal / brent_mensal.shift(1)).dropna()
brent_ret.columns = ['brent_ret']

# 4. OVX - implied volatility of crude oil
ovx_df = yf.download("^OVX", start=start_date, end=end_date, interval='1d')[['Close']].dropna()
ovx_mensal = ovx_df.resample('ME').mean()
ovx_mensal.columns = ['OVX']

# 5. Global IPM (industrial production index as proxy)
ipm_raw = DataReader('INDPRO', 'fred', start=start_date, end=end_date)
ipm_mensal = ipm_raw.resample('ME').mean()
ipm_mensal.columns = ['ipm']

# 6. GARCH(1,1) conditional volatility of Brent returns
ret_diario = 100 * np.log(brent_df / brent_df.shift(1)).dropna()
modelo = arch_model(ret_diario, vol='Garch', p=1, q=1)
resultado = modelo.fit(disp='off')
vol_garch = resultado.conditional_volatility.to_frame(name='vol_garch')
vol_garch_mensal = vol_garch.resample('ME').mean()

# 7. Merge all data
brent_ret.columns = ['brent_ret']
df = pd.concat([brent_ret, ipm_mensal, vol_garch_mensal, ovx_mensal], axis=1).dropna()

# 8. Demand shock (ODS): part of oil return explained by IPM
X = add_constant(df['ipm'])
modelo_ods = OLS(df['brent_ret'], X).fit()
df['ODS'] = modelo_ods.fittedvalues

# 9. Supply shock (OSS): regression residual
df['OSS'] = modelo_ods.resid

# 10. Risk shock (ORS): proxied by GARCH volatility
df['ORS'] = df['vol_garch']

# 11. Print sample and available columns
print(df[['brent_ret', 'ipm', 'ODS', 'OSS', 'ORS']].head())
print("\nAvailable columns:", df.columns.tolist())
