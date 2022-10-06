from flask import Flask, jsonify
import json
import pandas as pd

app = Flask(__name__)

# Cosntruir as funcionalidades
@app.route('/')
def pegardados():
  dadosAPI = pd.read_csv('2022/py/Simple-TF/Heatmap/dados/dados.csv')
  dadosAPI = (dadosAPI.to_string())
  

  resposta= {'dados': dadosAPI}

  return jsonify(resposta)

 

# Rodar API
app.run()

# tabela = pd.read_csv('2022/py/Simple-TF/Heatmap/dados/dados.csv')

