from flask import Flask
import random

app = Flask(__name__)

# Lista de fatos
facts_list = [
    "A maioria das pessoas que sofrem de dependência tecnológica sente um forte estresse quando está fora da rede.",
    "Mais de 50% das pessoas entre 18 e 34 anos se consideram dependentes de seus smartphones.",
    "O estudo da dependência tecnológica é uma das áreas mais relevantes da pesquisa científica moderna.",
    "Mais de 60% das pessoas respondem a mensagens de trabalho em até 15 minutos após sair do serviço.",
    "Uma forma de combater a dependência é buscar atividades offline que tragam prazer.",
    "As redes sociais são projetadas para nos manter dentro da plataforma o máximo de tempo possível.",
    "Elon Musk defende a regulamentação das redes sociais e proteção de dados.",
    "Devemos estar conscientes dos pontos positivos e negativos das redes sociais."
]

@app.route("/")
def home():
    # Adicionei links para TODAS as suas páginas aqui!
    return '''
    <h1>Bem-vindo ao meu Site!</h1>
    <p><a href="/random_fact">🎲 Ver um fato aleatório</a></p>
    <p><a href="/moeda">🪙 Jogar Cara ou Coroa</a></p>
    '''

@app.route("/random_fact")
def fact():
    return f'<h1>{random.choice(facts_list)}</h1> <a href="/">Voltar</a>'

# --- AQUI ESTÁ A SUA PÁGINA SECRETA ---
@app.route("/moeda")
def coin_flip():
    resultado = random.choice(["Cara", "Coroa"])
    return f'''
    <h1>O resultado foi: {resultado}</h1>
    <p><a href="/moeda">Jogar de novo</a></p>
    <p><a href="/">Voltar para o início</a></p>
    '''

app.run(debug=True)