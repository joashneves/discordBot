import discord
from discord import app_commands
from discord.ext import commands
from models.db import _Sessao, Usuario

from asyncio import sleep
from random import randint
from models.Obter_dados import Obter_dados

class Saldo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command()
    async def saldo(self, ctx:commands.context):
        usuario_db = Obter_dados.obter_usuario(ctx.author.id)
        saldo = usuario_db.saldo
        await ctx.reply(f'ola, {ctx.author.name}! Seu saldo é : {saldo}')

    @commands.command()
    async def explorar(self, ctx:commands.context):
        usuario_db = Obter_dados.obter_usuario(ctx.author.id)
        tempo_exploracao = 5
        await ctx.reply(f'Exploração...')
        await sleep(tempo_exploracao)
        moedas_ganhas = randint(1,10)

        with _Sessao() as sessao:
            usuario_db = sessao.merge(usuario_db)
            usuario_db.saldo += moedas_ganhas
            sessao.commit()
        await ctx.reply(f'Voce ganhou {moedas_ganhas} pixels!')

async def setup(bot):
    await bot.add_cog(Saldo(bot))