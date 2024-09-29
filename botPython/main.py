import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from models.db import _Sessao, Usuario

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
# Permissões e afins
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix='&', intents=permissoes)

async def carregar_comandos():
    for arquivo in os.listdir('comandos'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")

@bot.event
async def on_ready():
    await carregar_comandos()
    print(f"Bot {bot.user.name} está online!")

bot.run(TOKEN)
