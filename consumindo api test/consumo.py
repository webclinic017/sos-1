import json, requests
resposta = {}
resposta = requests.get('http://127.0.0.1:5000/')


json_data = json.loads(resposta)



print(json.dumps(json_data, indent=4)[0])

