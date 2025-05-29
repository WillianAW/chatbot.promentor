from app.config_llm import chain
from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter()


class Mensagem(BaseModel):
    mensagem: str

@router.post("/conversa/")
def conversar(msg: Mensagem):
    resultado = classificar_mensagem(msg.mensagem)

    resposta = f"✔️ Entendi que você quer {resultado.get('operacao', 'não informado')} um {resultado.get('tipo_imovel', 'não informado')} na região de {resultado.get('localizacao', 'não informado')} com características {resultado.get('caracteristicas', 'não informado')} e valor {resultado.get('valor', 'não informado')}."

    return {
        "resposta": resposta,
        "dados_classificados": resultado
    }

def classificar_mensagem(mensagem: str) -> dict:
    try:
        resultado = chain.invoke({"mensagem": mensagem})
        return {
            "tipo_imovel": resultado.get("tipo_imovel", ""),
            "operacao": resultado.get("operacao", ""),
            "valor": resultado.get("valor", ""),
            "caracteristicas": resultado.get("caracteristicas", ""),
            "localizacao": resultado.get("localizacao", "")
        }
    except Exception as e:
        print(f"Erro na classificação: {e}")
        return {}
