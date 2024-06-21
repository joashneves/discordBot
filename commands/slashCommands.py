import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Habilitar a intenção de membros

# Classe para gerenciar comandos
class slashCommands:
    def __init__(self, bot):
        self.bot = bot

    def register_commands(self):
        pass