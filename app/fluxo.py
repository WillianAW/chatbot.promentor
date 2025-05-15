from app.chatbot import classificar_mensagem
from app.modelo import PerfilCliente

def iniciar_atendimento():
    print("\n🤖 Olá, sou Mia, assistente virtual da Exemplo Imob!")
    print("Em que posso te ajudar hoje?\n")

    entrada = input("👤 Você: ")
    dados = classificar_mensagem(entrada)
    perfil = PerfilCliente(**dados)

    perfil = preencher_faltantes(perfil)
    perfil = perguntar_email(perfil)
    confirmar_informacoes(perfil)

def preencher_faltantes(perfil: PerfilCliente) -> PerfilCliente:
    perguntas = {
        "tipo_imovel": "Qual o tipo de imóvel? (Ex: apartamento, casa, etc)",
        "operacao": "Você quer alugar, comprar ou vender?",
        "valor": "Qual é o valor estimado?",
        "caracteristicas": "Quais características do imóvel você busca?",
        "localizacao": "Qual bairro ou região tem preferência?"
    }

    for campo, pergunta in perguntas.items():
        if getattr(perfil, campo).strip() == "":
            resposta = input(f"🤖 {pergunta}\n👤 Você: ")
            novos = classificar_mensagem(resposta)
            setattr(perfil, campo, novos.get(campo, "").strip())

    return perfil

def perguntar_email(perfil: PerfilCliente) -> PerfilCliente:
    resp = input("\n🤖 Deseja informar seu e-mail para contato? (sim/não): ").lower()
    if resp in ["sim", "s"]:
        email = input("✉️ Por favor, digite seu e-mail:\n👤 Você: ")
        perfil.email = email
    return perfil

def confirmar_informacoes(perfil: PerfilCliente):
    print("\n📋 Aqui está o que eu entendi:")
    for campo, valor in perfil.dict().items():
        print(f"🔹 {campo.replace('_', ' ').capitalize()}: {valor or 'Não informado'}")

    alterar = input("\n🤖 Deseja alterar alguma informação? (sim/não): ").lower()
    if alterar in ["sim", "s"]:
        ajuste = input("📝 Escreva a nova informação:\n👤 Você: ")
        novos = classificar_mensagem(ajuste)

        # Atualiza campos detectáveis
        for campo in ["tipo_imovel", "operacao", "valor", "caracteristicas", "localizacao"]:
            if novos.get(campo):
                setattr(perfil, campo, novos[campo])

        # Reperguntar e atualizar e-mail se necessário
        if not perfil.email:
            perfil = perguntar_email(perfil)

        confirmar_informacoes(perfil)  # Chama recursivamente para nova verificação
    else:
        print("\n🤖 Obrigado! Vou encaminhar suas informações para um de nossos corretores.")
        print("📞 Em breve, entraremos em contato com as melhores opções.")
        print("👋 Tenha um ótimo dia!")
