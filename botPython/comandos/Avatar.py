import discord
from discord import app_commands
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command()
    async def avatar(self, ctx:commands.Context):
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.author
        await ctx.reply(user.avatar)

async def setup(bot):
    await bot.add_cog(Avatar(bot))