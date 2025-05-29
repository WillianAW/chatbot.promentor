from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Evolution Webhook Receiver")

# Endpoint básico para receber webhooks
@app.post("/webhook/instance")
async def receive_webhook(request: Request):
    """
    Endpoint mais simples possível para receber webhooks da Evolution API
    """
    try:
        # 1. Obter os dados do webhook
        payload = await request.json()
        
        # 2. Log básico (apenas para demonstração)
        print(f"Webhook recebido: {payload}")
        
        # 3. Responder com sucesso
        return JSONResponse(
            content={"status": "success", "message": "Webhook received"},
            status_code=200
        )
        
    except Exception as e:
        # 4. Tratamento de erro básico
        print(f"Erro ao processar webhook: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid payload")

# Para rodar: uvicorn main:app --reload