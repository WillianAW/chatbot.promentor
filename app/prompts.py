from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
Você é um assistente de uma imobiliária.
Classifique a mensagem do cliente nas seguintes categorias:

- tipo_imovel
- operacao
- valor
- caracteristicas
- localizacao

Mensagem:
"{mensagem}"

Responda somente com JSON com essas 5 chaves.
""")
    