from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chatbot import classificar_mensagem
from app.modelo import PerfilCliente

app = FastAPI(title="Chatbot Imobiliário")

# 📥 Modelo de entrada para a API
class MensagemRequest(BaseModel):

    mensagem: str

@app.get("/")
def home():
    return {"mensagem": "Chatbot Imobiliário online! Acesse /docs para testar a API."}

@app.get("/favicon.ico")
def favicon():
    return {}
   

# 🚪 Rota principal da API
@app.post("/atendimento", response_model=PerfilCliente)
def atendimento(req: MensagemRequest):
    try:
        resultado = classificar_mensagem(req.mensagem)
        perfil = PerfilCliente(**resultado)
        return perfil
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
