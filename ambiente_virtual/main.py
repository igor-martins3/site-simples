import re
from flask import Flask, render_template
from api_gemini import model

app = Flask(__name__)

size_dictionary = ["Casa Pequena", "Casa Média", "Casa Grande"]



@app.route('/')
def index():
    return render_template('form.html')


@app.route('/<size>')
def lights(size):
    return render_template('lights.html', size=size)

@app.route('/<size>/<lights>')
def electronics(size, lights):

    # Se não for o caso especial (lights != 4), segue o fluxo normal
    if (int(lights) != 4): 
        print(f"{lights} !={ int(lights)}")
        return render_template('electronics.html', size=size, lights=lights)


    # === Lógica do Gemini ===
    
    # 1. Monta o contexto
    # Nota: Como 'device' não existe nessa rota, pedi para o Gemini assumir 
    # que device é 3 (máximo) para o pior cenário, ou você pode pedir para ele inventar.
    prompt_text = (
        f"A minha casa é {size_dictionary[int(size)-1]}. "
        f"Considere 'lights'={lights} e assuma que 'device'=3 (muitos aparelhos). "
        "Calcule o consumo (size * lights * device). "
        "Me dê uma dica ecológica sarcástica."
    )

    # 2. Chama a IA
    ai_full_response = get_ai_tip(prompt_text)

    # 3. Extração com REGEX
    # Padrão para encontrar: [CONSUMO: numero]
    pattern = r"\[CONSUMO:\s*(\d+)\]"
    match = re.search(pattern, ai_full_response)

    if match:
        consumo_final = int(match.group(1)) # Pega apenas o número capturado
        
        # Remove a tag [CONSUMO: X] do texto para não aparecer para o usuário
        mensagem_limpa = re.sub(pattern, "", ai_full_response).strip()
    else:
        # Caso a IA falhe em seguir o padrão
        consumo_final = 0 
        mensagem_limpa = ai_full_response

    # 4. Envia para o site
    return render_template('end.html', 
                           result=consumo_final, 
                           gemini_tip=mensagem_limpa)

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

def get_ai_tip(consumption_context):
    try:    
        # Ajustamos a "persona" da IA para ser útil primeiro, engraçada depois.
        instructions = (
            "Você é um consultor de energia eficiente e prático, mas com um senso de humor leve. "
            "Sua missão tem duas partes obrigatórias:\n"
            "1. Dê uma solução real e útil para economizar energia nesse cenário (ex: sensores de presença, isolamento térmico, LEDs inteligentes).\n"
            "2. Faça um comentário final curto e levemente irônico sobre o tamanho da conta de luz, mas sem ofender.\n\n"
            "Formatação Obrigatória:\n"
            "Escreva a dica e a piada em um único parágrafo.\n"
            "No final, pule uma linha e coloque EXATAMENTE a tag: [CONSUMO: valor_calculado_aqui]"
        )
        
        # Passamos as instruções + o contexto (tamanho da casa, luzes, etc)
        prompt = f"Cenário do Usuário: {consumption_context}\n\nInstruções para a IA: {instructions}"
        
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        print(f"Erro na chamada da IA: {e}")
        # Retorno de segurança para não quebrar o site
        return "Dica: Use lâmpadas LED e sensores de presença! [CONSUMO: 0]"

if __name__ == "__main__":
    app.run(debug=True)