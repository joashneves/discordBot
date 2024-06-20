import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Habilitar a intenção de membros

client = commands.Bot(command_prefix='$', intents=intents)

# Classe para gerenciar comandos
class slashCommands:
    def __init__(self, bot):
        self.bot = bot

    def register_commands(self):
        @self.bot.tree.command(description='responde Ola')
        async def ola(interact:discord.Interaction):
            await interact.response.send_message(f'Ola {interact.user.name}')

        @self.bot.tree.command(description='responde (͡• ͜ʖ ͡•)')
        async def safadenha(interact:discord.Interaction):
            await interact.response.send_message(f'(͡• ͜ʖ ͡•)', ephemeral=False)

        @self.bot.tree.command(description="responde (ง︡'-'︠)ง ")
        async def fight(interact:discord.Interaction):
            await interact.response.send_message("(ง︡'-'︠)ง ", ephemeral=False)

        @self.bot.tree.command(description='responde (ㆆ_ㆆ) ')
        async def impossivel(interact:discord.Interaction):
            await interact.response.send_message(f'(ㆆ_ㆆ) ', ephemeral=False)

        @self.bot.tree.command(description='responde ʕ•́ᴥ•̀ʔっ ')
        async def oifofo(interact:discord.Interaction):
            await interact.response.send_message(f'ʕ•́ᴥ•̀ʔっ ', ephemeral=False)

        @self.bot.tree.command(description='responde (╥︣﹏᷅╥) ')
        async def tisteza(interact:discord.Interaction):
            await interact.response.send_message(f'(╥︣﹏᷅╥) ', ephemeral=False)