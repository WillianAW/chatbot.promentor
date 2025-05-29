from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
Você é um assistente de uma imobiliária.
Classifique os elementos da mensagem:

- tipo_imovel
- operacao
- valor
- caracteristicas
- localizacao

Mensagem:
{mensagem}

Responda em JSON com essas chaves.
""")

# 🔗 Monta o chain
chain = prompt | llm | parser