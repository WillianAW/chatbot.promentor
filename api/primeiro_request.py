import requests 

url="https://httpbin.org/post"

resposta = requests.POST(url)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f'Impossível fazer o request! ERRO: {e}')
else:
    print('Resultado:')
    print(resposta.json())

# data={
#     "meus dados": [1, 2, 3],
#     "pessoa:":{
#         "nome": "Willian",
#         "professor": True
#      }
# }

# params={
#     'dataInicio':'2025-05-01',
#     'dataFim':'2025-09-08'    
# }
    # "pessoa1":{
    #     "nome":"Sofia",
    #     "professor": True
    # },
    # "pessoa2":{
    #     "nome":"Douglas",
    #     "professor": False
    # },
    # "pessoa3":{
    #     "nome":"Leo",
    #     "professor": True
    # },
    # "pessoa4":{
    #     "nome":"Leozera",
    #     "professor": True
    # }
