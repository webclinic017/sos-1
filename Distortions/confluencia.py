# Bibliotecas necessárias
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_datareader as web
from datetime import datetime
from datetime import timedelta
import xlwt
import matplotlib.pyplot as plt


# tickers
tickers = ['^BVSP']

end_date = '{}-{}-{}' .format(datetime.now().year,
                              datetime.now().month,  datetime.now().day)

end_d = datetime.now()

# daily
yahoo_data = yf.download(tickers=tickers,
                         start=end_d - timedelta(days=30),
                         end=end_date, interval='1d')

# intraday
intraday_data = yf.download(tickers=tickers, period="1d", interval="1h")


# daily data
close = yahoo_data['Close']
volume = yahoo_data['Volume']
high = yahoo_data['High']
low = yahoo_data['Low']

# intraday data
intraday_close = intraday_data['Close']
intraday_high = intraday_data['High']
intraday_low = intraday_data['Low']
intraday_volume = intraday_data['Volume']


# checar dados
'''print (intraday_volume.head())'''

dados = pd.DataFrame()
dados['Volume'] = volume.iloc[:-1]
dados['Close'] = close.iloc[:-1]
dados['Intraday Close'] = intraday_close.iloc[-1]
MME3 = close.ewm(span=9).mean()
MME7 = close.ewm(span=21).mean()
dados['MME3'] = MME3.iloc[:-1]
dados['MME7'] = MME7.iloc[:-1]
both_close = pd.concat([close, intraday_close.tail(1)])

'''print (MME3.head())'''


def Volume_Projetado(VolumeAtual):
    now = datetime.now()
    BrazilHour = now.hour - 3
    BrazilMinute = now.minute
    diffMinutes = 60 - BrazilMinute

    diffClose = (18 - BrazilHour) * 60 - BrazilMinute
    diffOpen = (BrazilHour - 10) * 60 + BrazilMinute

    VolumeFaltante = diffClose*(VolumeAtual/diffOpen)

    VolumeProjetado = VolumeAtual + VolumeFaltante
    return VolumeProjetado


# DELTA AVAT
# Volume Projetado
last_two = yf.download(tickers=tickers, period='7d',
                       interval='1d')['Volume'].iloc[:-1]
last_two.iloc[:-1] = Volume_Projetado(last_two.iloc[:-1])
last_two = (last_two)

'''print(last_two)'''

# RETORNO CLOSE ANTERIOR E ULTIMO PREÇO
dados['Retorno (Close[1]/Intra)'] = ((dados['Intraday Close'] /
                                      dados['Close']) - 1) * 100

'''print (dados['Retorno (Close[1]/Intra)'])'''

# DELTA AVAT 1D
# VOLUME PROJETADO / 1D AVAT
delta_avat_1d = (last_two.iloc[-1] / last_two.iloc[-2]) - 1
dados['Volume Projetado'] = last_two.iloc[-1]
dados['Delta AVAT 1D'] = (dados['Volume Projetado']/dados['Volume']) - 1
dados['Fast AVAT'] = np.where((dados['Delta AVAT 1D'] > 0.0) & (
    dados['Retorno (Close[1]/Intra)'] > -0.05), 1, 0)


dados['Fast AVAT'] = dados['Fast AVAT'].astype(int)

'''print (dados['Fast AVAT'])'''

dados['MME3_intraday'] = both_close.ewm(span=3).mean()
dados['MME7_intraday'] = both_close.ewm(span=7).mean()

dados['Fast EMA Cross'] = np.where(
    (dados['MME3'] < dados['MME3_intraday']), 1, 0)

dados['Fast EMA Cross Minus'] = np.where(
    (dados['MME3'] > dados['MME3_intraday']), 1, 0)

'''print(dados['Fast EMA Cross'])'''

'''MME10_intraday = both_close.ewm(span=10).mean()
MME28_intraday = both_close.ewm(span=28).mean()
MME10 = close.ewm(span=10).mean()
MME28 = close.ewm(span=28).mean()'''


dados['MME9'] = close.ewm(span=9).mean().iloc[:]
dados['MME21'] = close.ewm(span=21).mean().iloc[:]
dados['MME10_intraday'] = both_close.ewm(span=10).mean().iloc[:]
dados['MME28_intraday'] = both_close.ewm(span=28).mean().iloc[:]


dados['Slow EMA Cross'] = np.where(
    (dados['MME9'] < dados['MME10_intraday']), 1, 0)

dados['Slow EMA Cross Minus'] = np.where(
    (dados['MME9'] > dados['MME10_intraday']), -1, 0)

dados['Slow EMA Cross'] = dados['Slow EMA Cross'].astype(int)

dados['Slow EMA Cross Minus'] = dados['Slow EMA Cross Minus'].astype(int)*-1

'''print(dados['Slow EMA Cross Minus'])'''

# 9.1 de Compra
# MME9 (ONTEM) > MME9_anterior (ANTEONTEM)
MME9_anterior_anterior = close.iloc[:-2].ewm(span=9).mean()
MME9_anterior = close.iloc[:-1].ewm(span=9).mean()
MME9 = close.ewm(span=9).mean()
# Close de ontem vs close de anteontem
close_anteontem = close.iloc[:-2]
close_ontem = close.iloc[:-1]
# máxima DE ONTEM
high_ontem = high.iloc[:-1]
# O VALOR INTRADAY MAX DE HOJE > max de ontem
high_agora = intraday_high.iloc[:]


'''print(high_agora)'''

dados['MME9 Anterior Anterior'] = MME9_anterior_anterior.iloc[:]
dados['MME9 Anterior'] = MME9_anterior.iloc[:]
dados['MME9'] = MME9.iloc[:]
dados['Close Anterior'] = close_anteontem
dados['Close'] = close_ontem
dados['High Ontem'] = high_ontem[-2]
dados['High Agora'] = high_agora.iloc[-1]


# MACD REVERSAL
# MACD1 = MME 26D - MME 12D
MME26 = both_close.ewm(span=26).mean()
MME12 = both_close.ewm(span=12).mean()
MACD1 = MME26 - MME12
# MACD1[1]
MME26_anterior = both_close.iloc[:-1].ewm(span=26).mean()
MME12_anterior = both_close.iloc[:-1].ewm(span=12).mean()
MACD1_anterior = MME26_anterior - MME12_anterior
# MACD SIGNAL = MME9D
MACD_SIGNAL = both_close.ewm(span=9).mean()
MACD_SIGNAL_anterior = both_close.iloc[:-1].ewm(span=9).mean()
# MACD2 = MACD1 - MACD SIGNAL
MACD2_anterior = MACD1_anterior - MACD_SIGNAL_anterior
MACD2 = MACD1 - MACD_SIGNAL
# Se MACD2 t-1 < 0 e MACD2 t > 0  ==>  sinal de reversão de tendência de baixa para alta
# Se MACD2 t-1 > 0 e MACD2t < 0   ==>  sinal de reversão de tendência de alta para baixa
dados['MACD[1]'] = MACD2_anterior.iloc[-1]
dados['MACD'] = MACD2.iloc[-1]

dados['MACD Reversal'] = np.where((dados['MACD[1]'] < 0), 1, 0)


dados['MACD Reversal Minus'] = np.where((dados['MACD[1]'] > 0), -1, 0)


# 90D
resistencia_90D = high.iloc[-90:-1].max()
suporte_90D = low.iloc[-90:-1].min()

dados['Breakout 90D'] = np.where((intraday_high.max() > resistencia_90D) & (
    high.iloc[-1] < resistencia_90D), 1, 0)
dados['Breakdown 90D'] = np.where(
    (intraday_low.min() < suporte_90D) & (low.iloc[-1] > suporte_90D), -1, 0)


# 180D
resistencia_180D = high.iloc[-180:-1].max()
suporte_180D = low.iloc[-180:-1].min()

dados['Breakout 180D'] = np.where((intraday_high.max() > resistencia_180D) & (
    high.iloc[-1] < resistencia_180D), 1, 0)
dados['Breakdown 180D'] = np.where(
    (intraday_low.min() < suporte_180D) & (low.iloc[-1] > suporte_180D), -1, 0)

# 260D

resistencia = high.iloc[-260:-1].max()
suporte = low.iloc[-260:-1].min()

dados['Breakout 260D'] = np.where((high.iloc[-1] < resistencia)
                          & (intraday_high.max() >= resistencia), 1, 0)
dados['Breakdown 260D'] = np.where((low.iloc[-1] > suporte) &
                           (intraday_low.min() <= suporte), -1, 0)

# BREAKOUT AND BREAKDOWN

dados['Breakout Signal'] = dados['Breakout 90D'] + dados['Breakdown 90D'] + \
    dados['Breakout 180D'] + dados['Breakdown 180D'] + \
    dados['Breakout 260D'] + dados['Breakdown 260D']

'''print(dados['Breakout Signal'])'''

pd.set_option("display.max_rows", None, "display.max_columns", None)

dados['SCORE'] = dados['Fast EMA Cross'] +  dados['Fast EMA Cross Minus'] +  dados['Slow EMA Cross'] +  dados['Slow EMA Cross Minus'] + dados['MACD Reversal'] +  dados['MACD Reversal Minus'] +  dados['Breakout Signal']

dados.sort_values( by=['SCORE'], ascending=False)

dados.to_excel('DestaquesMidLarge.xlsx')