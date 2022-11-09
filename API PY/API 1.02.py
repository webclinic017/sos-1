from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Cosntruir as funcionalidades


@app.route('/sinais')
def pegardados_sinal():
    dadosAPI = pd.read_json(
        'C:/Codding Hub/2022/py/Simple-TF/Heatmap/sos/dados/dados.json')
    #dadosAPI = (dadosAPI.to_string())
    dadosAPI = dadosAPI.values.tolist()
    '''print (dadosAPI)'''

    for dado in dadosAPI:
        # cada indice representa uma ação da lista - quando for trocar a ação, troque o indice
        resposta = dadosAPI[1]

        return resposta


@app.route('/acao')
def pegardados_ticker():
    dadosAPI = pd.read_json(
        'C:/Codding Hub/2022/py/Simple-TF/Heatmap/sos/dados/dados.json')
    #dadosAPI = (dadosAPI.to_string())
    dadosAPI = pd.DataFrame(dadosAPI)
    dadosColuna = dadosAPI.iloc[-1]
    '''
    print (dadosColuna.first_valid_index())
    '''
    return dadosColuna.first_valid_index()  # cada indice representa uma ação da lista - quando for trocar a ação, troque o indice


# Rodar API
app.run()

# tabela = pd.read_csv('2022/py/Simple-TF/Heatmap/dados/dados.csv')
