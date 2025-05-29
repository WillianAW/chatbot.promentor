from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# 🎯 Estrutura dos dados que vamos coletar
class PerfilCliente(BaseModel):
    tipo_imovel: str = ""
    operacao: str = ""
    valor: str = ""
    caracteristicas: str = ""
    localizacao: str = ""
    email: str = ""

# class MensagemRequest(BaseModel):
#     mensagem: str

class PerfilMultiploInteresse(BaseModel):
    nome:str
    email:str
    interesses:List[PerfilCliente]
    data_consulta: str