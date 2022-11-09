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
    mdata[t] = yf.download(t, start=start_d, end=end_d,
                           interval='1d')['Volume']


def AVAT(mdata):

    # 1 AVAT
    volume= mdata['Volume'].iloc[-1] # Volume do ultimo dia
    volume_ma = mdata['Volume'].iloc[-1:-7].mean() # Média de volume dos últimos 'N' dias



    # Filtro
    trend = np.where((volume > (1.25 * volume_ma)), 1, 0)

    trend = np.where((volume < (0.5 * volume_ma)), -1, trend)
    return trend


ind = vbt.IndicatorFactory(
    class_name='AVAT',
    short_name='AVAT',  # Apelido
    input_names=['close'],  # Dados que vão passar pela função
    param_names=[mdata],  # Nome dos parâmetros passados
    output_names=['value']
).from_apply_func(
    AVAT,
  # Configure as janelas
)

# print(pandasData)

res = ind.run(
    mdata,

)

volume_acima = res.value == 1.0
volume_abaixo = res.value == -1.0

print(res.value)




# CSV
'''res.value.to_json('C:/Codding Hub/2022/py/Simple-TF/Heatmap/sos/dados/dados.json')'''
