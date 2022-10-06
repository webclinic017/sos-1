<<<<<<< HEAD
import vectorbt as vbt
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import pandas as pd
import numpy as np

# Oganizando os dados (períodos mais curtos como intradiários - necessário mudar a API)
end_d = datetime.now() 
start_d = end_d - timedelta(days=3365)

carteira = ['VALE3.SA']

mdata = pd.DataFrame()
for t in carteira:
    mdata[t] = yf.download(t,start=start_d, end = end_d, interval='1d')['Adj Close']

'''volume = pd.DataFrame()
for t in carteira:
  volume[t]= yf.download(t,start=start_d, end = end_d, interval='1d')['Volume']
# checar os dados
# print(mdata,volume)'''

'''mdata = mdata.to_pandas()
volume = volume.to_pandas()'''

mdata['VALE3.SA'] = mdata
'''mdata['Volume'] = volume'''


#print(mdata)


def distortions(close, maf_window = 3, mas_window = 5, rsi_window= 14, media_close= 30, buy_force=30, sell_force=70):
  
  # 1 AVAT
  '''volume= mdata['Volume'].iloc[-1] # Volume do ultimo dia
  volume_ma = mdata['Volume'][media_vol:].mean() # Média de volume dos últimos 'N' dias'''
  
  # 2 Crossed MA (Supper Trend)
  ma_fast = vbt.MA.run(close, window=  maf_window) # Configurando MA
  ma_slow1 = vbt.MA.run(close, window=  mas_window) # Configurando MA

  # 3 RSI (Índice de Força Relativa)
  rsi = vbt.RSI.run(close, window= rsi_window).rsi.to_numpy() # Configurando RSI

  # 3 Breakout 
  high_p = close
  high_m = close[media_close:].mean()


  # Filtro
  trend = np.where((rsi < buy_force), 1, 0)
  trend = np.where((rsi > sell_force), -1, trend)
  return trend

ind = vbt.IndicatorFactory(
  class_name='distortions',
  short_name='distortions', # Apelido
  input_names=['close'], # Dados que vão passar pela função
  param_names=['maf_window', 'mas_window', 'rsi_window', 'media_close', 'buy_force', 'sell_force'], # Nome dos parâmetros passados
  output_names=['value']
  ).from_apply_func(
          distortions,
          maf_window = 3, 
          mas_window = 5, 
          rsi_window= 14, 
          media_close= 30, 
          buy_force=30, 
          sell_force=70 # Configure as janelas
          )

# print(pandasData)

res = ind.run(
    mdata,
    maf_window=3,
    mas_window=5,
    rsi_window=14,
    media_close=30,
    buy_force=30,
    sell_force=70
)

entries = res.value == 1.0
exits = res.value == -1.0

pf = vbt.Portfolio.from_signals(mdata, entries, exits)
returns = pf.total_return()
#(pf.stats())
print(returns.max())
=======
import vectorbt as vbt
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import pandas as pd
import numpy as np

# Oganizando os dados (períodos mais curtos como intradiários - necessário mudar a API)
end_d = datetime.now() 
start_d = end_d - timedelta(days=3365)

carteira = ['VALE3.SA']

mdata = pd.DataFrame()
for t in carteira:
    mdata[t] = yf.download(t,start=start_d, end = end_d, interval='1d')['Adj Close']

'''volume = pd.DataFrame()
for t in carteira:
  volume[t]= yf.download(t,start=start_d, end = end_d, interval='1d')['Volume']
# checar os dados
# print(mdata,volume)'''

'''mdata = mdata.to_pandas()
volume = volume.to_pandas()'''

mdata['VALE3.SA'] = mdata
'''mdata['Volume'] = volume'''


#print(mdata)


def distortions(close, maf_window = 3, mas_window = 5, rsi_window= 14, media_close= 30, buy_force=30, sell_force=70):
  
  # 1 AVAT
  '''volume= mdata['Volume'].iloc[-1] # Volume do ultimo dia
  volume_ma = mdata['Volume'][media_vol:].mean() # Média de volume dos últimos 'N' dias'''
  
  # 2 Crossed MA (Supper Trend)
  ma_fast = vbt.MA.run(close, window=  maf_window) # Configurando MA
  ma_slow1 = vbt.MA.run(close, window=  mas_window) # Configurando MA

  # 3 RSI (Índice de Força Relativa)
  rsi = vbt.RSI.run(close, window= rsi_window).rsi.to_numpy() # Configurando RSI

  # 3 Breakout 
  high_p = close
  high_m = close[media_close:].mean()


  # Filtro
  trend = np.where((rsi < buy_force), 1, 0)
  trend = np.where((rsi > sell_force), -1, trend)
  return trend

ind = vbt.IndicatorFactory(
  class_name='distortions',
  short_name='distortions', # Apelido
  input_names=['close'], # Dados que vão passar pela função
  param_names=['maf_window', 'mas_window', 'rsi_window', 'media_close', 'buy_force', 'sell_force'], # Nome dos parâmetros passados
  output_names=['value']
  ).from_apply_func(
          distortions,
          maf_window = 3, 
          mas_window = 5, 
          rsi_window= 14, 
          media_close= 30, 
          buy_force=30, 
          sell_force=70 # Configure as janelas
          )

# print(pandasData)

res = ind.run(
    mdata,
    maf_window=3,
    mas_window=5,
    rsi_window=14,
    media_close=30,
    buy_force=30,
    sell_force=70
)

entries = res.value == 1.0
exits = res.value == -1.0

pf = vbt.Portfolio.from_signals(mdata, entries, exits)
returns = pf.total_return()
#(pf.stats())
print(returns.max())
>>>>>>> d09eb31d531076f05d78ed8b89e0425bdd2e8e83
print(res.value.head()) 