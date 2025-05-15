from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from app.prompts import prompt
from dotenv import load_dotenv
import os

load_dotenv()
parser = JsonOutputParser()

# 🔑 Instancia o modelo da OpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 🔗 Cria o pipeline (prompt → modelo → parser)
chain = prompt | llm | parser

def classificar_mensagem(mensagem: str) -> dict:
    try:
        resultado = chain.invoke({"mensagem": mensagem})
        # Corrige campos que vieram como None
        resultado_corrigido = {k: (v if v is not None else "") for k, v in resultado.items()}
        return resultado_corrigido
    except Exception as e:
        print("⚠️ Erro ao classificar a mensagem:", e)
        return {
            "tipo_imovel": "",
            "operacao": "",
            "valor": "",
            "caracteristicas": "",
            "localizacao": ""
        }

