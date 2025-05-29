import json
from datetime import datetime
from pathlib import Path
from typing import List
# from app.modelo import PerfilCliente, PerfilMultiploInteresse
from app.chatbot import chain

def verificar_clareza_mensagem(mensagem: str, limite_confianca: float = 0.7) -> bool:
    """
    Analisa se a mensagem do cliente está clara o suficiente
    Retorna True se a mensagem for clara, False se estiver confusa
    
    Parâmetros:
    mensagem (str): Texto digitado pelo cliente
    limite_confianca (float): Limite de confiança para considerar claro (0-1)
    
    Retorno:
    bool: True se mensagem for clara, False se confusa
    """
    # Verificações básicas de qualidade da mensagem
    if not mensagem or len(mensagem.strip()) < 3:
        return False
    
    # Análise de erros grosseiros (exemplo simplificado)
    palavras = mensagem.split()
    if len(palavras) < 2:  # Mensagens muito curtas
        return False
    
    # Verifica se contém palavras-chave essenciais
    palavras_chave = ['comprar', 'alugar', 'vender', 'casa', 'apartamento', 'terreno']
    contagem_palavras_chave = sum(1 for palavra in palavras if palavra.lower() in palavras_chave)
    
    if contagem_palavras_chave == 0:
        return False
    
    # Integração com o classificador existente (opcional)
    try:
        resultado = classificar_mensagem(mensagem)
        campos_preenchidos = sum(1 for v in resultado.values() if v.strip())
        
        # Se menos da metade dos campos foram preenchidos corretamente
        if campos_preenchidos / len(resultado) < limite_confianca:
            return False
            
    except Exception:
        # Em caso de erro na classificação, considera como mensagem confusa
        return False
    
    return True

def obter_resposta_clara(prompt: str, tentativas_max: int = 2) -> str:
    """
    Garante que a resposta do cliente seja clara, com múltiplas tentativas
    
    Parâmetros:
    prompt (str): Pergunta ou instrução para o cliente
    tentativas_max (int): Número máximo de tentativas permitidas
    
    Retorno:
    str: Mensagem validada do cliente
    """
    tentativas = 0
    
    while tentativas < tentativas_max:
        resposta = input(f"🤖 {prompt}\n👤 Você: ").strip()
        
        if verificar_clareza_mensagem(resposta):
            return resposta
        
        print("🤖 Ficou meio confuso o que você disse, poderia repetir por favor?")
        tentativas += 1
    
    raise ValueError("Número máximo de tentativas excedido")

# Exemplo de uso no fluxo existente:
def iniciar_atendimento():
    print("\n🤖 Olá, sou Mia, assistente virtual da Exemplo Imob!")
    
    try:
        nome = obter_resposta_clara("Antes de começarmos, qual é o seu nome completo?", tentativas_max=3)
        print(f"\nÉ um prazer te atender, {nome}!")
        
        while True:
            entrada = obter_resposta_clara(
                "Em que posso te ajudar hoje? "
                "Seja específico (ex: 'quero comprar uma casa e alugar um apartamento')",
                tentativas_max=2
            )
            
            interesses = identificar_interesses(entrada)
            if interesses:
                break
                
            print("⚠️ Não consegui entender. Vamos tentar novamente...")
            
        # ... restante do fluxo ...
        
    except ValueError as e:
        print(f"⚠️ {str(e)}. Vamos começar novamente mais tarde.")

def obter_nome_cliente():
    """Obtém e valida o nome do cliente"""
    while True:
        nome = input("🤖 Antes de começarmos, qual é o seu nome completo?\n👤 Você: ").strip()
        if nome:
            return nome
        print("⚠️ Por favor, informe seu nome para continuarmos.")

def identificar_interesses(mensagem: str) -> List[dict]:
    """Identifica interesses de forma robusta com validação"""
    mensagem = mensagem.lower()
    interesses = []
    
    # Mapeamentos melhorados
    operacoes = {
        'comprar': ['comprar', 'compra', 'adquirir', 'aquisição'],
        'alugar': ['alugar', 'aluguel', 'locação', 'arrendar'],
        'vender': ['vender', 'venda', 'colocar à venda']
    }
    
    tipos_imovel = {
        'casa': ['casa', 'residência', 'sobrado', 'vivenda'],
        'apartamento': ['apartamento', 'apto', 'flat', 'apê'],
        'terreno': ['terreno', 'lote', 'terreno baldio', 'área']
    }

    # Primeiro tenta entender a mensagem completa
    dados = classificar_mensagem(mensagem)
    if dados.get("operacao") and dados.get("tipo_imovel"):
        interesses.append({
            "operacao": dados["operacao"],
            "tipo_imovel": dados["tipo_imovel"]
        })

    # Verifica se há múltiplos interesses com conectores
    conectores = [" e ", " também ", ", além disso ", " e depois "]
    if any(conector in mensagem for conector in conectores):
        partes = []
        for conector in conectores:
            if conector in mensagem:
                partes = [p.strip() for p in mensagem.split(conector) if p.strip()]
                break
        
        if len(partes) >= 2:
            interesses = []
            for parte in partes:
                parte_dados = classificar_mensagem(parte)
                if parte_dados.get("operacao") and parte_dados.get("tipo_imovel"):
                    interesses.append({
                        "operacao": parte_dados["operacao"],
                        "tipo_imovel": parte_dados["tipo_imovel"]
                    })

    # Se não encontrou nada, tenta o método palavra por palavra
    if not interesses:
        ops_encontradas = []
        tipos_encontrados = []
        
        for op, palavras in operacoes.items():
            if any(palavra in mensagem for palavra in palavras):
                ops_encontradas.append(op)
        
        for tipo, palavras in tipos_imovel.items():
            if any(palavra in mensagem for palavra in palavras):
                tipos_encontrados.append(tipo)
        
        # Combina os resultados
        if ops_encontradas and tipos_encontrados:
            for i, op in enumerate(ops_encontradas):
                if i < len(tipos_encontrados):
                    interesses.append({
                        "operacao": op,
                        "tipo_imovel": tipos_encontrados[i]
                    })

    return interesses

def coletar_detalhes_imovel(tipo: str, operacao: str) -> dict:
    """Coleta detalhes específicos para cada tipo de imóvel"""
    print(f"\n🤖 Vamos cadastrar os detalhes para {operacao} {tipo}:")
    detalhes = {}
    
    # Perguntas dinâmicas baseadas no tipo de imóvel
    perguntas = {
        "valor": f"Qual valor você pretende {operacao}? ",
        "localizacao": f"Em qual região quer {operacao} o {tipo}? ",
        "caracteristicas": f"Quais características importantes para o {tipo}? "
    }
    
    for campo, pergunta in perguntas.items():
        while True:
            resposta = input(f"🤖 {pergunta}\n👤 Você: ").strip()
            if resposta:
                detalhes[campo] = resposta
                break
            print(f"⚠️ Por favor, informe {campo.replace('_', ' ')}")
    
    return detalhes

def confirmar_alteracoes(perfil: dict) -> dict:
    """Permite ao cliente revisar e alterar cada campo"""
    while True:
        print("\n📋 Confira os detalhes:")
        for campo, valor in perfil.items():
            print(f"🔹 {campo.replace('_', ' ').title()}: {valor}")
        
        alterar = input("\n🤖 Deseja alterar algo? (sim/não): ").lower()
        if alterar not in ['sim', 's']:
            return perfil
        
        campo = input("📝 Qual informação deseja alterar? ").lower()
        if campo in perfil:
            novo_valor = input(f"✏️ Novo valor para {campo}: ").strip()
            if novo_valor:
                perfil[campo] = novo_valor
            else:
                print("⚠️ Valor inválido, mantendo o anterior")
        else:
            print("⚠️ Campo não encontrado")

def iniciar_atendimento():
    """Fluxo principal do atendimento"""
    print("\n🤖 Olá, sou Mia, assistente virtual da Exemplo Imob!")
    nome = obter_nome_cliente()
    print(f"\nÉ um prazer te atender, {nome}!")
    
    while True:
        entrada = input("🤖 Em que posso te ajudar hoje? Seja específico (ex: 'quero comprar uma casa e alugar um apartamento'):\n👤 Você: ")
        
        interesses = identificar_interesses(entrada)
        if not interesses:
            print("⚠️ Não entendi. Por favor, seja mais específico (ex: 'quero comprar uma casa' ou 'alugar um apartamento')")
            continue
        
        perfis = []
        for interesse in interesses:
            print(f"\n▶ Processando: {interesse['operacao']} {interesse['tipo_imovel']}")
            detalhes = coletar_detalhes_imovel(interesse['tipo_imovel'], interesse['operacao'])
            perfil = {
                "nome": nome,
                "tipo_imovel": interesse['tipo_imovel'],
                "operacao": interesse['operacao'],
                **detalhes
            }
            perfil = confirmar_alteracoes(perfil)
            perfis.append(perfil)
        
        # Coleta de e-mail apenas no final
        email = ""
        while True:
            resp = input("\n🤖 Deseja informar seu e-mail para contato? (sim/não): ").lower()
            if resp in ["sim", "s"]:
                email = input("✉️ Digite seu e-mail: ").strip()
                if "@" in email and "." in email.split("@")[1]:
                    break
                print("⚠️ E-mail inválido!")
            else:
                break
        
        # Cria o resumo final
        resumo = {
            "nome": nome,
            "email": email,
            "interesses": perfis,
            "data_consulta": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        # Confirmação final
        print("\n🔎 RESUMO FINAL:")
        print(f"👤 Cliente: {resumo['nome']}")
        print(f"✉️ E-mail: {resumo['email'] if resumo['email'] else 'Não informado'}")
        
        for i, interesse in enumerate(resumo['interesses'], 1):
            print(f"\n🏠 Interesse {i}: {interesse['operacao']} {interesse['tipo_imovel']}")
            print(f"   💰 Valor: {interesse['valor']}")
            print(f"   📍 Localização: {interesse['localizacao']}")
            print(f"   🏡 Características: {interesse['caracteristicas']}")
        
        confirmacao = input("\n🤖 Confirmar cadastro? (sim/não): ").lower()
        if confirmacao in ['sim', 's']:
            salvar_consulta(resumo)
            print("\n✅ Cadastro concluído com sucesso!")
            print("📞 Nossos corretores entrarão em contato em breve.")
            break
        else:
            print("\n🔄 Vamos recomeçar o processo...\n")

def salvar_consulta(resumo: dict):
    """Salva os dados apenas após todas as confirmações"""
    try:
        Path("consultas").mkdir(exist_ok=True)
        nome_arquivo = f"consultas/{resumo['nome'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(resumo, f, ensure_ascii=False, indent=2)
        
        print(f"📁 Dados salvos em: {nome_arquivo}")
    except Exception as e:
        print(f"⚠️ Erro ao salvar: {e}")

def classificar_mensagem(mensagem: str) -> dict:
    """Classificação robusta com tratamento de erros"""
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
        print("⚠️ Erro ao analisar sua mensagem")
        return {}