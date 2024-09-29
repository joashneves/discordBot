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

    @commands.cooldown(1, 10, commands.BucketType.member)
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
    
    @explorar.error
    async def cooldown(self, ctx:commands.context, erro):
        if isinstance(erro, commands.CommandOnCooldown):
            await ctx.reply(f'Não, espera {erro.retry_after:.2f} s ai')
        else:
            raise erro

    @commands.command()
    async def pix(self, ctx:commands.Context, membro_alvo:discord.Member, valor:int):
        usuario_db = Obter_dados.obter_usuario(ctx.author.id)
        usuario_alvo_db = Obter_dados.obter_usuario(membro_alvo.id)
        with _Sessao() as sessao:
            usuario_db = sessao.merge(usuario_db)
            usuario_alvo_db = sessao.merge(usuario_alvo_db)
            if valor > usuario_db.saldo:
                await ctx.reply(f"Ow, voce não tem esse valor")
                return
            usuario_db.saldo -= valor
            usuario_alvo_db.saldo += valor
            sessao.commit()
            await ctx.reply(f'Voce transferiu {valor} pixels, para {membro_alvo.name}.')

async def setup(bot):
    await bot.add_cog(Saldo(bot))