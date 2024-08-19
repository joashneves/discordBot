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

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline

nltk.download('vader_lexicon')

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

from commands.mensagens import messagensBotRespostas
from commands.user import User
from commands.bomdia import BomDia
from commands.dados import Dados
from commands.atribuicargo import AtribuiCargo
from commands.adicionarPersonagem import AdicionarPersonagem
from commands.avatar import AvatarComandos
from commands.ajudaCommands import AjudaComando
from commands.gameWiki import GameWiki
from commands.wikilist import Wikilist
from commands.Coins import Coins
from commands.Perfil import Perfil
from commands.Conquistas import Conquistas
from commands.slashCommands import slashCommands
from commands.ignoraCanal import colocarCanalDeImagens
from s3nha.atribuicargos3nha import AtribuiCargoS3nha

TOKEN = os.getenv('DISCORD_TOKEN')

permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.messages = True
permissoes.voice_states = True
permissoes.emojis = True
permissoes.members = True
bot = commands.Bot(command_prefix='$', intents=permissoes)


# Inicializar os pipelines de análise
sentiment_classifier = pipeline("sentiment-analysis", model="neuralmind/bert-base-portuguese-cased")
toxic_classifier = pipeline("text-classification", model="neuralmind/bert-base-portuguese-cased")  # Substitua se houver um modelo mais apropriado para toxicidade

dados_users = {}
SERVER_ID = 390309756918562823  # ID Do server
NOTIFICATION_CHANNEL_ID = 1274521956674174988  # canal de notificação


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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Connected to the following servers:')
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')
    activity = discord.Activity(type=discord.ActivityType.playing, name='apenas em dias uteis')

    bot_atribuicargo = AtribuiCargo(bot)
    bot_atribuicargoS3nha = AtribuiCargoS3nha(bot)
    await bot_atribuicargo.atribuiCargo()
    await bot_atribuicargoS3nha.atribuiCargo()

    await bot.change_presence(activity=activity)

# Instanciar classes
bot_respostas = messagensBotRespostas(bot)
bot_bomDia = BomDia(bot)
dados_rpg = Dados(bot)
adicionar_personagem = AdicionarPersonagem(bot)
comandos_de_avatar = AvatarComandos(bot)
ajuda_comando = AjudaComando(bot)
game_wiki = GameWiki(bot)
wiki_list = Wikilist(bot)
coins = Coins(bot)
perfil = Perfil(bot)
conquista = Conquistas(bot)
colocar_canal_imagem = colocarCanalDeImagens(bot)

# Lista para armazenar as mensagens recentes
recent_messages = []

# Número máximo de mensagens a serem mantidas para análise
MAX_MESSAGES = 10

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Para evitar que o bot responda a suas próprias mensagens
        return

    await bot_bomDia.processar_mensagem(message)
    await bot_respostas.processar_mensagem(message)
    await dados_rpg.processar_mensagem(message)
    await adicionar_personagem.processar_mensagem(message)
    await comandos_de_avatar.avatar(message)
    await ajuda_comando.processar_mensagem(message)
    await game_wiki.processar_mensagem(message)
    await wiki_list.processar_mensagem(message)
    await coins.processar_mensagem(message)
    await perfil.processar_mensagem(message)
    await conquista.processar_mensagem(message)
    await colocar_canal_imagem.processar_mensagem(message)

    jogadorID = str(message.author.id)

    # Reações e filtros
    palavrao = {"porra", "puta", "cu", "caralho", "fodase", "fuder", "foda", "fude","fuder","fds","puto","pqp","merda","vsf"}
    regex = re.compile(r'\b(?:' + '|'.join(palavrao) + r')\b', re.IGNORECASE)
    if regex.search(message.content):
        if jogadorID not in dados_users:
            dados_users[jogadorID] = [0, 0, 0, 1, 0]
        else:
            dados_users[jogadorID][3] += 1

        numero_aleatorio = random.randint(0, 99)
        if numero_aleatorio > 50:
            await message.channel.send(" '-' ")
        elif numero_aleatorio < 5:
            await message.channel.send(" '-' ")
            await message.channel.send(f"Você xingou {str(dados_users[jogadorID][3])} vezes")
        else:
            return

    prefix = "$"

    if message.content.lower().startswith(prefix + "teste"):
        if message.mentions:
            user = message.mentions[0]
            await message.channel.send(f'Você mencionou o <@{user.id}>')
        else:
            await message.channel.send(message.author.avatar)

    if message.content.startswith(prefix + 'ping'):
        latency = bot.latency
        emberd = discord.Embed(title='ping', description=f'Seu ping é {latency:.2f}')
        await message.channel.send(embed=emberd)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # Adiciona a mensagem à lista de mensagens recentes
        recent_messages.append(message.content)

        # Mantém o número de mensagens no tamanho máximo
        if len(recent_messages) > MAX_MESSAGES:
            recent_messages.pop(0)

        # Adiciona a mensagem à lista de mensagens recentes
        recent_messages.append(message.content)

        # Mantém o número de mensagens no tamanho máximo
        if len(recent_messages) > MAX_MESSAGES:
            recent_messages.pop(0)

        guild = bot.get_guild(SERVER_ID)
        if guild:
            # Cria o texto da conversa a partir das mensagens recentes
            conversation_text = " ".join(recent_messages)

            # Análise de sentimento
            sentiment = sentiment_classifier(conversation_text)[0]
            sentiment_label = sentiment['label']
            sentiment_score = sentiment['score']

            # Detecção de toxicidade
            toxicity = toxic_classifier(conversation_text)[0]
            label = toxicity['label']
            score = toxicity['score']

            print(f'sentiments: {sentiment_score}  score : {score} {sentiment_score > 0.5}')

            # Notificações baseadas na análise de sentimentos e toxicidade
            if sentiment_label == "NEGATIVE" and sentiment_score > 0.5:
                notification_channel = guild.get_channel(NOTIFICATION_CHANNEL_ID)
                if notification_channel:
                    await notification_channel.send(
                        f"Mensagem negativa detectada de {message.author.mention}: {message.content}")

            if label == "TOXIC" and score > 0.5:
                await message.delete()  # Deleta a mensagem tóxica
                notification_channel = guild.get_channel(NOTIFICATION_CHANNEL_ID)
                if notification_channel:
                    await notification_channel.send(
                        f"Mensagem de {message.author.mention} foi removida por violar as regras do servidor.")

        await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    print(f"{member.name} entrou no servidor.")

    bot_atribuicargo = AtribuiCargo(bot)
    bot_atribuicargoS3nha = AtribuiCargoS3nha(bot)
    await bot_atribuicargo.atribuiCargo()
    await bot_atribuicargoS3nha.atribuiCargo()

# Sincroniza os comandos slash
@bot.command()
async def sincronizar(ctx: commands.Context):
    print("Sincronizando...")
    if ctx.author.id == 257566850081226752:
        try:
            # Sincroniza os comandos
            sincs = await bot.tree.sync()
            await ctx.reply(f'{len(sincs)} comandos sincronizados')
        except Exception as e:
            await ctx.reply(f'Erro ao sincronizar: {str(e)}')
            print(f'Erro ao sincronizar: {str(e)}')
    else:
        await ctx.reply(f'Você é FRACO!')

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

@bot.tree.command(name="deletarmensagem", description="Deleta um número específico de mensagens.")
async def deletar_mensagem(interaction: discord.Interaction, numero: int):
    if numero < 1 or numero > 100:
        await interaction.response.send_message("O número de mensagens deve estar entre 1 e 100.", ephemeral=True)
        return

    user = interaction.user
    # Verifica se o usuário tem permissões administrativas
    if any(role.permissions.administrator for role in user.roles):
        channel = interaction.channel

        if isinstance(channel, discord.TextChannel):
            await interaction.response.defer()  # Indica que a resposta será tardia
            messages = [message async for message in channel.history(limit=numero + 1)]
            await channel.delete_messages(messages)
            await interaction.response.send(f"{numero} mensagens deletadas com sucesso.", ephemeral=True)
        else:
            await interaction.response.send_message("Este comando só pode ser usado em canais de texto.", ephemeral=True)
    else:
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)

# Inicia o bot
bot.run(TOKEN)
