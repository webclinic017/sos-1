from flask import Flask
import pandas as pd

app = Flask(__name__)

# Cosntruir as funcionalidades
@app.route('/')
def pegardados():
  dadosAPI = pd.read_json('C:/Codding Hub/2022/py/Simple-TF/Heatmap/sos/dados/dados.json')
  #dadosAPI = (dadosAPI.to_string())
  dadosAPI = dadosAPI.to_json()


  for dado in dadosAPI:
    resposta= {'dadosAPI':dadosAPI}

    return (resposta)

 

# Rodar API
app.run()

# tabela = pd.read_csv('2022/py/Simple-TF/Heatmap/dados/dados.csv')

