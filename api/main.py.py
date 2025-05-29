import requests
import json
from pathlib import Path


#https://evolution.promentor.com.br/message/typebot/start/sendText/exemplo_imob

API_URL_BASE = "https://evolution.promentor.com.br/message"
API_URL_MANAGER = "http://evolution.promentor.com.br/manager"


INSTANCE = "exemplo_imob"
API_KEY = "7BD01546CC1C-4E9D-A015-09F58B329717"


HEADERS = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

# Função para consultar status da instância


def consultar_status_instancia():
    url = f"{API_URL_MANAGER}/sendText/{INSTANCE}"
    try:
        response = requests.get(url, headers=HEADERS)
        dados = response.json()
        print("Status da instância:", dados)

        salvar_json(dados, "status_instancia")
        return dados
    except Exception as e:
        erro = {"status_code": response.status_code, "response": response.text, "erro": str(e)}
        print("Erro na consulta:", erro)
        salvar_json(erro, "status_instancia_erro")
        return erro


#Função para obter informações gerais da instância ----------------------------------------------------------------obter instancia api
def obter_informacoes_instancia():
    url = f"{API_URL_MANAGER}/instanceStatus"
    try:
        response = requests.get(url, headers=HEADERS)
        dados = response.json()
        print("Informações da instância:", dados)

        salvar_json(dados, "informacoes_instancia")
        return dados
    except Exception as e:
        erro = {"status_code": response.status_code, "response": response.text, "erro": str(e)}
        print("Erro na consulta:", erro)
        salvar_json(erro, "informacoes_instancia_erro")
        return erro

# ----------------------------------------------------------------------------------------------------------------------def enviar mensagem
def enviar_mensagem(numero: str, mensagem: str):
    url = f"{API_URL_BASE}/typebot/start/sendText/{INSTANCE}"

    payload = {
        "number": numero, 
        "textMessage": mensagem
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        dados = response.json()
        print(" Mensagem enviada:", dados)

        salvar_json(dados, "envio_mensagem")
        return dados
    except Exception as e:
        erro = {
            "status_code": response.status_code,
            "response": response.text,
            "erro": str(e)
        }
        print("Erro no envio:", erro)
        salvar_json(erro, "envio_mensagem_erro")
        return erro



def enviar_mensagem(numero_destino: str, mensagem: str):
    url = f"{API_URL_BASE}/typebot/start/sendText/{INSTANCE}"

    payload = {
        "number": numero_destino,
        "text": mensagem
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        dados = response.json()
        print("✅ Mensagem enviada:", dados)

        salvar_json(dados, f"envio_mensagem_{numero_destino}")
        return dados
    except Exception as e:
        erro = {"status_code": response.status_code, "response": response.text, "erro": str(e)}
        print("Erro no envio da mensagem:", erro)
        salvar_json(erro, f"envio_mensagem_erro_{numero_destino}")
        return erro   


def salvar_json(dados: dict, nome_arquivo: str):
    Path("resultados_api").mkdir(exist_ok=True)
    caminho = f"resultados_api/{nome_arquivo}.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em: {caminho}")


if __name__ == "__main__":
    status = consultar_status_instancia()
    info = obter_informacoes_instancia()

     # 
    numero = "5541996612239"  
    mensagem = "Ola, mensagem de teste via entrada API Evolution!"

    enviar_mensagem(numero, mensagem)

    print("\nConsulta concluída!")


