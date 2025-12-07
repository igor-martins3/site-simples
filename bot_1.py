import discord
import random
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv

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

# --- COMANDOS BÁSICOS ---

@bot.command()
async def oi(ctx):
    await ctx.send("Olá! Eu sou um bot da Kodland!")

@bot.command()
async def moeda(ctx):
    resultado = random.choice(["Cara", "Coroa"])
    await ctx.send(f'🪙 Saiu: **{resultado}**!')

# --- COMANDO COM INPUT (O novo!) ---

@bot.command()
async def conversa(ctx):
    await ctx.send("Ei! Qual é a sua cor favorita? (Responda em 30 segundos)")

    def check(msg):
        # Verifica se é VOCÊ falando no MESMO canal
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        # O bot espera você digitar
        mensagem = await bot.wait_for('message', check=check, timeout=30.0)
        cor_escolhida = mensagem.content
        await ctx.send(f"Uau! {cor_escolhida} é uma cor muito bonita! 🎨")

    except asyncio.TimeoutError:
        await ctx.send("Poxa, você demorou demais! Fiquei no vácuo. 😢")

# --- COMANDOS DE MODERAÇÃO ---

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f'🧹 {quantidade} mensagens foram limpas!', delete_after=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def expulsar(ctx, membro: discord.Member, *, motivo="Nenhum motivo"):
    await membro.kick(reason=motivo)
    await ctx.send(f'👢 {membro.mention} foi expulso! Motivo: {motivo}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def banir(ctx, membro: discord.Member, *, motivo="Nenhum motivo"):
    await membro.ban(reason=motivo)
    await ctx.send(f'🔨 {membro.mention} foi banido! Motivo: {motivo}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def eco(ctx, *, eco):
    await ctx.send(eco)

# --- TOKEN (SEMPRE A ÚLTIMA LINHA) ---
bot.run(os.getenv('DISCORD_SECRET'))

# Aqui está a "Cola" (Cheat Sheet)
#!oi

       # O que faz: O bot responde "Olá! Eu sou um bot da Kodland!".

#         Serve para: Ver se ele está lendo mensagens.

#     !moeda

#         O que faz: Joga uma moeda e diz se deu Cara ou Coroa.

#         Serve para: Testar a lógica de aleatoriedade (random).

# 🛡️ Comandos de Moderação (Testando o poder!)

#     !limpar 5

#         O que faz: Apaga as últimas 5 mensagens do chat.

#         Dica: Mande algumas mensagens aleatórias antes para ter o que apagar.

#     !expulsar @NomeDeAlguem

#         O que faz: Tira a pessoa do servidor (mas ela pode voltar se tiver o link).

#         Atenção: Você precisa marcar (@) a pessoa. Não teste no dono do servidor (você), teste em um amigo ou conta secundária!

#     !banir @NomeDeAlguem

#         O que faz: Bane a pessoa permanentemente (ela não consegue voltar).

# 👋 Teste Automático (Boas-vindas)

#     Como testar: Peça para um amigo entrar no servidor, ou saia você com uma conta secundária e entre de novo.

#     O que deve acontecer: O bot vai mandar sozinho uma mensagem: "👋 Bem-vindo ao servidor, @Fulano! Divirta-se!".