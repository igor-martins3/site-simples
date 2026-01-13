from flask import Flask, render_template
from api_gemini import model

app = Flask(__name__)

size_dictionary = ["Casa Pequena", "Casa Média", "Casa Grande"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<size>')
def lights(size):
    return render_template('lights.html', size=size)

@app.route('/<size>/<lights>')
def electronics(size, lights):

    if ( int(lights) != 4): 
        print(f"{lights} !={ int(lights)}")
        return render_template('electronics.html', size=size, lights=lights)

    # 2. Pergunta ao Gemini uma dica sobre esse consumo
    ai_message = get_ai_tip(f" A minha casa é {size_dictionary[int(size)-1]}, preciso de ajuda oara que ela fique bastante ecológica. Quantas lampadas eu tenho que ter para ter bastante iluminação, mas ainda sendo ecológico? E quantos aparelhos eletronicos? E Qual é o consumo total por mês simulado, usando a formula: size * lights * device, onde size é de 0 a 3 ( sendo 3 casa grande), lights de 0 a 3 ( sendo 3 muitas luzes ), e device de 0 a 3. ")

    # 3. Envia O CÁLCULO e a MENSAGEM DO GEMINI para o site
    return render_template('end.html', 
                           result=0, 
                           gemini_tip=ai_message)

@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    # 1. Faz o cálculo matemático
    
    total_consumption = calculate(int(size), int(lights), int(device))

    # 3. Envia O CÁLCULO e a MENSAGEM DO GEMINI para o site
    return render_template('end.html', 
                           result=total_consumption, 
                           gemini_tip="")

# Função matemática simples
def calculate(size, lights, device):
    return size * lights * device

def get_ai_tip(consumption):
    try:    
        prompt = (f"Question: {consumption} "
                  "Aja como um consultor de sustentabilidade ou um globalista abaixonado e dê uma dica curta (máximo 1 paragrafo), "
                  "criativa e prática de como economizar energia nesse cenário. "
                  "Fale de forma amigável, direta e um pouco sarcastica.")
        
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        # Se der erro na IA, retorna uma mensagem padrão para o site não quebrar
        print(f"Erro na chamada da IA: {e}")
        return "Dica: Use lâmpadas LED e aproveite a luz natural para economizar!"


if __name__ == "__main__":
    app.run(debug=True)