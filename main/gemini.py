# Arquivo: gemini.py

from google import genai
from dotenv import load_dotenv
import os

# ******* NOVO: CARREGAR O .ENV AQUI *******
# Garante que a chave seja lida antes de inicializar o cliente!
load_dotenv() 
# *****************************************

# Lê a chave da variável de ambiente
API_KEY = os.getenv('GEMINI_API_KEY') 

# Inicializa o cliente
if not API_KEY:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env!")

client = genai.Client(api_key=API_KEY)