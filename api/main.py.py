import requests

API_URL="http://evolution.promentor.com.br/manager"
INSTANCE="exemplo_imob"
API_KEY="7BD01546CC1C-4E9D-A015-09F58B329717"

url = f"{API_URL}/message/sendText/{INSTANCE}"

headers={
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

body={
    "number":"5541996612239",
    "text":"Teste"
}


try:
    response = requests.post(url, headers=headers, json=body)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("Conexão bem-sucedida! Instância encontrada.")
        
        if response.text.strip() == "":
            print("Resposta vazia no corpo.")
        else:
            try:
                data = response.json()
                print("Resposta JSON:", data)
            except ValueError:
                print("A resposta não está em formato JSON.")
                print("Resposta bruta:", response.text)

    elif response.status_code == 401:
        print("Erro 401: API Key inválida ou não autorizada.")
    elif response.status_code == 404:
        print("Erro 404: Instância não encontrada.")
    else:
        print(f"Erro {response.status_code}: {response.text}")

except Exception as e:
    print(f"Erro na conexão: {str(e)}")