from pydantic import BaseModel

# 🎯 Estrutura dos dados que vamos coletar
class PerfilCliente(BaseModel):
    tipo_imovel: str = ""
    operacao: str = ""
    valor: str = ""
    caracteristicas: str = ""
    localizacao: str = ""
    email: str = ""

class MensagemRequest(BaseModel):
    mensagem: str
