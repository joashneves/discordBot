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
from commands.avatar import AvatarComandos
from commands.ajudaCommands import AjudaComando
from commands.gameWiki import GameWiki
from commands.wikilist import Wikilist
from commands.Coins import Coins
from commands.Perfil import Perfil
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
comandos_de_avatar = AvatarComandos(client)
ajuda_comando = AjudaComando(client)
game_wiki = GameWiki(client)
wiki_list = Wikilist(client)
coins = Coins(client)
perfil = Perfil(client)

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
        await ajuda_comando.processar_mensagem(message)
        await game_wiki.processar_mensagem(message)
        await wiki_list.processar_mensagem(message)
        await coins.processar_mensagem(message)
        await perfil.processar_mensagem(message)

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

    if message.content.lower().startswith(prefix + "teste"):
        if message.mentions:
            user = message.mentions[0]
            await message.channel.send(f'Voce mencionou o <@{user}>')
        else:
            await message.channel.send(message.author.avatar)



#region // bom dia e sla

    if message.content.startswith(prefix + 'ping'):
        latency = client.latency
        emberd = discord.Embed(title='ping', description=f'seu ping é {latency:.2f}')
        await message.channel.send(embed=emberd)


#endregion


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