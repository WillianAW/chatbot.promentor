from fastapi import FastAPI, HTTPException
from pathlib import Path
import json
from api.routers import atendimento, chatbot

app = FastAPI(title="API Chatbot Imobiliário",
        description="API para atendimento inteligente de imóveis",
        version="1.0.0")

PASTA_CONSULTAS = Path("consultas")


@app.get("/")
def home():
    return {"mensagem": "API do Chatbot Imobiliário rodando! 🚀"}


@app.get("/consultas")
def listar_consultas():
    """Lista todos os arquivos de consultas salvos"""
    if not PASTA_CONSULTAS.exists():
        raise HTTPException(status_code=404, detail="Nenhuma consulta encontrada.")
    
    arquivos = list(PASTA_CONSULTAS.glob("*.json"))
    return {"consultas": [arquivo.name for arquivo in arquivos]}


@app.get("/consultas/{arquivo}")
def ler_consulta(arquivo: str):
    """Lê um arquivo específico de consulta"""
    caminho = PASTA_CONSULTAS / arquivo

    if not caminho.exists():
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return dados


@app.delete("/consultas/{arquivo}")
def deletar_consulta(arquivo: str):
    """Deleta um arquivo de consulta"""
    caminho = PASTA_CONSULTAS / arquivo

    if not caminho.exists():
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")

    caminho.unlink()

    return {"mensagem": f"Consulta {arquivo} deletada com sucesso."}

app.include_router(atendimento.router)
app.include_router(chatbot.router)