import json
from datetime import datetime
from pathlib import Path

def salvar_consulta(dados: dict):
    Path("consultas").mkdir(exist_ok=True)
    nome_arquivo = f"consultas/{dados['nome'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em {nome_arquivo}")
