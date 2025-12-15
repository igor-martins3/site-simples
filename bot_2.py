import discord
import random
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv
from gemini import client

# CARREGANDO .ENV
print(f"📂 Pasta atual: {os.getcwd()}")
carregou = load_dotenv()
print(f"📄 Arquivo .env encontrado? {'✅ SIM' if carregou else '❌ NÃO'}")
print("🗃️ Arquivos na pasta:", os.listdir())
token = os.getenv('DISCORD_SECRET')
print(f"🔑 Valor do token lido: {token}")
# ------------------------------------

# 1. Configurar as permissões (Intents)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessário para o boas-vindas e banir

# 2. Criar o bot com o prefixo '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# --- EVENTOS (Coisas automáticas) ---

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    print('Estou pronto para receber comandos!')

@bot.event
async def on_member_join(member):
    # Função de Boas-vindas
    canal = member.guild.system_channel
    if canal is not None:
        await canal.send(f'👋 Bem-vindo ao servidor, {member.mention}! Divirta-se!')

#comandos

@bot.command()
async def ecologia(ctx, *, text):  # Corrigido: Usando *, text para capturar a mensagem inteira
    
    # 1. Avisa que está pensando
    await ctx.send("🤖 Pensando em uma resposta irônica e ecológica...")

    try:
        # 2. Gera o conteúdo
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=f"Me ajude com: {text}. Responda de forma resumida porém ainda respondendo a pergunta, irônica e sarcástica, no máximo 3 frases." 
        )
        
        if response and response.text:
            await ctx.send(str(response.text)) # Usamos str() para garantir que é uma string
        else:
            # Caso a resposta não tenha texto (por bloqueio ou erro)
            await ctx.send("🚨 O Gemini não conseguiu gerar uma resposta para isso. Tente outra pergunta.")
        
    except Exception as e:
        # 4. Trata possíveis erros do Gemini (como a chave não estar funcionando)
        print(f"ERRO AO CHAMAR GEMINI: {e}")
        await ctx.send("🚨 Desculpe, tive um problema na conexão com a IA. O Gemini não está me respondendo (será que ele cansou de ser irônico?).")



# --- TOKEN (SEMPRE A ÚLTIMA LINHA) ---
bot.run(os.getenv('DISCORD_SECRET'))
