import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import asyncio
import datetime
import re
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

from commands.mensagens import messagensBotRespostas
from commands.user import User
from commands.bomdia import BomDia
from commands.dados import Dados
from commands.atribuicargo import AtribuiCargo
from commands.adicionarPersonagem import AdicionarPersonagem
from commands.avatar import avatarComandos
from commands.slashCommands import slashCommands

TOKEN = os.getenv('DISCORD_TOKEN')

permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.messages = True
bot = commands.Bot(command_prefix='$', intents=permissoes)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.emojis = True
intents.members = True

client = MyClient(intents=intents)

users = {}
dados_users = {}

async def excluir_canal_apos_tempo(canal, tempo):
    await asyncio.sleep(tempo)  # Aguarda o intervalo de tempo especificado
    await canal.delete()        # Deleta o canal

# Carregar dados dos usuários a partir do arquivo
def carregar_dados():
    try:
        with open("memoria/dados_usuarios.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

# Salvar dados dos usuários no arquivo
def salvar_dados():
    with open("memoria/dados_usuarios.json", "w") as arquivo:
        json.dump(users, arquivo)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    print('Connected to the following servers:')
    for guild in client.guilds:
        print(f'- {guild.name} (ID: {guild.id})')
    activity = discord.Activity(type=discord.ActivityType.playing, name='apenas em dias uteis')

    bot_atribuicargo = AtribuiCargo(client)
    await bot_atribuicargo.atribuiCargo()

    await client.change_presence(activity=activity)

# Classes
bot_respostas = messagensBotRespostas(client)
bot_bomDia = BomDia(client)
dados_rpg = Dados(client)
adicionar_personagem = AdicionarPersonagem(client)
comandos_de_avatar = avatarComandos(client)

@client.event
async def on_message(message):
    if message.author == client.user:  # Para evitar que o bot responda a suas próprias mensagens
        return
    else:
        await bot_bomDia.processar_mensagem(message)
        await bot_respostas.processar_mensagem(message)
        await dados_rpg.processar_mensagem(message)
        await adicionar_personagem.processar_mensagem(message)
        await comandos_de_avatar.avatar(message)

    jogadorID = str(message.author.id)
#region // reações

    palavrao = {"porra", "puta", "cu", "caralho", "fodase", "fuder", "foda", "fude","fuder","fds","puto","pqp","merda","vsf"}
    regex = re.compile(r'\b(?:' + '|'.join(palavrao) + r')\b', re.IGNORECASE)
    if regex.search(message.content):
        if jogadorID not in dados_users:
            dados_users[jogadorID] = [0,0,0,1,0]
        else:
            dados_users[jogadorID][3] += 1

        numero_aleatorio = random.randint(0, 99)
        if numero_aleatorio > 50:
            await message.channel.send(" '-' ")
        elif numero_aleatorio < 5:
            await message.channel.send(" '-' ")
            await message.channel.send(f"voce xingou {str(dados_users[jogadorID][3])} vezes")
        else:
            return

#endregion

    prefix = "$"
    if message.content.startswith(prefix + "ajuda"):
        await message.channel.send(f'Comandos conhecidos são:\n$avatar\n$ping\n$jogar\n$score\n caso queria que eu responda seus comando escreva: skalart o que é um bot?')
        registrar_comando(jogadorID)

    if message.content.lower().startswith(prefix + "teste"):
        if message.mentions:
            user = message.mentions[0]
            await message.channel.send(f'Voce mencionou o <@{user}>')
        else:
            await message.channel.send(message.author.avatar)
        registrar_comando(jogadorID)


#region // bom dia e sla

    if message.content.startswith(prefix + 'ping'):
        latency = client.latency
        emberd = discord.Embed(title='ping', description=f'seu ping é {latency:.2f}')
        await message.channel.send(embed=emberd)
        registrar_comando(jogadorID)

#endregion

    global jogo_de_adivinhar, chute
    jogo_de_adivinhar= False

    if message.content.startswith(prefix + 'jogar') or jogo_de_adivinhar:
            jogo_de_adivinhar = True

            jogadorID = str(message.author.id)
            if jogadorID not in dados_users:
                dados_users[jogadorID] = [1,0,0,0,0]
            else:
                dados_users[jogadorID][0] += 1
            await message.channel.send(f"O jogo começou, <@{message.author.id}> jogou {str(dados_users[jogadorID][0])} vezes, digite qual é esse personagem?")
            DATA_FILE = os.path.join('memoria', 'game.json')
            with open(DATA_FILE, "r") as game:
                personagens = json.load(game)

            # Obtém a quantidade de personagens presentes no arquivo JSON
            quantidade_personagens = len(personagens)

            # Gera um número aleatório entre 0 e a quantidade de personagens - 1
            numero_aleatorio = random.randint(0, quantidade_personagens - 1)

            # Encontra o nome e a imagem do primeiro personagem
            nome_personagem = personagens[numero_aleatorio]["nome"]
            imagem_personagem = personagens[numero_aleatorio]["imagem"]

            # Define o caminho do arquivo de imagem local
            imagem_local = os.path.join(imagem_personagem)

            if not os.path.exists(imagem_local):
                await message.channel.send(imagem_personagem)
            else:
                # Envia a imagem do personagem
                with open(imagem_personagem, "rb") as arquivo_imagem:
                    await message.channel.send(file=discord.File(arquivo_imagem, "imagem.png"))

            chute = nome_personagem
            await esperar_resposta_do_jogador(message.author, message.channel, jogadorID)
            registrar_comando(jogadorID)

    if message.content.startswith(prefix + 'score'):
        if message.mentions:
            user = message.mentions[0]
            jogadorM = str(user.id)
            if jogadorM not in dados_users:
                    await message.channel.send(f"<@{user.id}> ainda não possui perfil!")
            else:
                    await message.channel.send(
                        f"<@{user.id}> jogou: {str(dados_users[jogadorM][0])} vezes\n acertou: {str(dados_users[jogadorM][1])} vezes\n"
                        f" errou: {str(dados_users[jogadorM][2])} vezes\n xingou: {str(dados_users[jogadorM][3])} vezes\n"
                        f" usou comandos: {dados_users[jogadorM][4]} vezes")
        else:
            if jogadorID not in dados_users:
                await message.channel.send("Você ainda não possui perfil!")
            else:
                await message.channel.send(f"voce jogou: {str(dados_users[jogadorID][0])} vezes\nvoce acertou: {str(dados_users[jogadorID][1])} vezes\n"
                                               f"voce errou: {str(dados_users[jogadorID][2])} vezes\nvoce xingou: {str(dados_users[jogadorID][3])} vezes\n"
                                               f"Voce usou comandos: {dados_users[jogadorID][4]} vezes")
        registrar_comando(jogadorID)

def check_resposta_jogador(message, autor_jogador):
    return message.author == autor_jogador

async def esperar_resposta_do_jogador(autor_jogador, canal_jogo,dados):
    try:
        resposta = await client.wait_for('message', check=lambda m: check_resposta_jogador(m, autor_jogador), timeout=12)
    except asyncio.TimeoutError:
        await canal_jogo.send('Tempo esgotado! O jogo acabou.')
    else:
        if resposta.content.lower().startswith(chute.lower()):
            dados_users[dados][1] += 1 #acertos
            await canal_jogo.send("Você acertou! e ganhou pontos")
            await canal_jogo.send(f"Você acertou: {dados_users[dados][1]} vezes")
        else:
            dados_users[dados][2] += 1  # erros
            await canal_jogo.send("Você ERROU!")
            await canal_jogo.send(f"Você ERROU: {dados_users[dados][2]} vezes")


def registrar_comando(usuario_id):
    if usuario_id not in dados_users:
        dados_users[usuario_id] = [0,0,0,0,1]
    else:
        dados_users[usuario_id][4] += 1

# sincroniza os comandos slash
@bot.command()
async def sicronizar(ctx:commands.Context):
    print("Sicronizado...")
    if(ctx.author.id == 257566850081226752):
        sincs = await bot.tree.sync()
        await ctx.reply(f'{len(sincs)} comandos sicronizados')
    else:
        await ctx.reply(f'Voce é FRACO!')

@client.event
async def on_member_join(member):
    print(f"{member.name} entrou no servidor.")

    bot_atribuicargo = AtribuiCargo(client)
    await bot_atribuicargo.atribuiCargo()

@bot.tree.command(description='responde Ola')
async def ola(interact:discord.Interaction):
    await interact.response.send_message(f'Ola {interact.user.name}')

@bot.tree.command(description='responde (͡• ͜ʖ ͡•)')
async def safadenha(interact:discord.Interaction):
    await interact.response.send_message(f'(͡• ͜ʖ ͡•)', ephemeral=False)

@bot.tree.command(description="responde (ง︡'-'︠)ง ")
async def fight(interact:discord.Interaction):
    await interact.response.send_message("(ง︡'-'︠)ง ", ephemeral=False)

@bot.tree.command(description='responde (ㆆ_ㆆ) ')
async def impossivel(interact:discord.Interaction):
    await interact.response.send_message(f'(ㆆ_ㆆ) ', ephemeral=False)

@bot.tree.command(description='responde ʕ•́ᴥ•̀ʔっ ')
async def oifofo(interact:discord.Interaction):
    await interact.response.send_message(f'ʕ•́ᴥ•̀ʔっ ', ephemeral=False)

@bot.tree.command(description='responde (╥︣﹏᷅╥) ')
async def tisteza(interact:discord.Interaction):
    await interact.response.send_message(f'(╥︣﹏᷅╥) ', ephemeral=False)

client.run(TOKEN)
bot.run(TOKEN)