# Arquivo: gemini.py

# from google import genai
import google.generativeai as genai
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

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Erro ao configurar API: {e}")

# client = genai.Client(api_key=API_KEY)