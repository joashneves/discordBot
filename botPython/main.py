import discord
from discord.ext import commands
import os

# Pegando o token do ambiente
TOKEN = os.getenv('DISCORD_TOKEN')

permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix='&', intents=permissoes)


async def carregar_comandos():
    print(os.listdir('comandos'))
    for arquivo in os.listdir('comandos'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")

@bot.event
async def on_ready():
    await carregar_comandos()
    print("On line")

bot.run(TOKEN)