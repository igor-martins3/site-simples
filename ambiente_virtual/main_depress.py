from flask import Flask, render_template
import random

app = Flask(__name__)

# --- SEUS FATOS ANTIGOS ---
facts_list = [
    "A maioria das pessoas que sofrem de dependência tecnológica sente um forte estresse quando está fora da rede.",
    "Mais de 50% das pessoas entre 18 e 34 anos se consideram dependentes de seus smartphones.",
    "O estudo da dependência tecnológica é uma das áreas mais relevantes da pesquisa científica moderna.",
    "Mais de 60% das pessoas respondem a mensagens de trabalho em até 15 minutos após sair do serviço.",
    "Uma forma de combater a dependência é buscar atividades offline que tragam prazer.",
    "As redes sociais são projetadas para nos manter dentro da plataforma o máximo de tempo possível."
]

@app.route("/")
def home():
    # Menu principal atualizado
    return '''
    <div style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>🏠 Portal do Igor</h1>
        <p>Bem-vindo ao seu hub de ferramentas!</p>
        
        <div style="background-color: #d4edda; padding: 20px; margin: 10px; border-radius: 10px; display: inline-block;">
            <h3>🌱 Ecológico</h3>
            <p>Calcule a eficiência energética da sua casa.</p>
            <a href="/calculadora"><button style="padding: 10px; cursor: pointer;">Abrir Calculadora</button></a>
        </div>

        <div style="background-color: #fff3cd; padding: 20px; margin: 10px; border-radius: 10px; display: inline-block;">
            <h3>🎲 Diversão</h3>
            <p>Jogue ou aprenda algo novo.</p>
            <a href="/random_fact">Ver Fato Curioso</a> | 
            <a href="/moeda">Cara ou Coroa</a>
        </div>
    </div>
    '''

@app.route("/random_fact")
def fact():
    return f'<h1>{random.choice(facts_list)}</h1> <a href="/">Voltar</a>'

@app.route("/moeda")
def coin_flip():
    resultado = random.choice(["Cara", "Coroa"])
    return f'<h1>Resultado: {resultado}</h1> <a href="/">Voltar</a>'

# --- ROTA DA CALCULADORA (AULA DE HOJE) ---
@app.route("/calculadora")
def calculadora():
    return render_template('index.html')

# --- ROTA PARA A PRÓXIMA PÁGINA (LUZES) ---
@app.route('/<size>')
def lights(size):
    # O <size> pega o número 1, 2 ou 3 que veio do botão
    return render_template('lights.html', size=size)

@app.route('/<size>/<lights>')
def electronics(size, lights):
    # O <size> pega o número 1, 2 ou 3 que veio do botão
    return render_template('electronics.html', size=size, lights=lights)

app.route('/<size>/<lights>/<electronics>')
def end(size, lights, electronics):

    # ? Chamar a função de calculadora e passar size, lights, eletrocnics

    return render_template('end.html', result=140)

# --- COMANDO PARA LIGAR O SITE (SEMPRE NO FINAL) ---
if __name__ == "__main__":
    app.run(debug=True)