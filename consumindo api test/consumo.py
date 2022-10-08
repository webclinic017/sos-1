import json, requests
resposta = {}
resposta = requests.get('http://127.0.0.1:5000/')


json_data = json.loads(resposta.text)



print(json.dumps(json_data, indent=4)[22:26])