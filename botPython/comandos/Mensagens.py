import discord
from discord import app_commands
from discord.ext import commands

class Mensagens(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        if msg.attachments:
                attachment = msg.attachments[0]
                if attachment.url:
                    try:
                        # Pega a última mensagem do canal para adicionar reações
                        last_message = await msg.channel.fetch_message(msg.channel.last_message_id)
                        emoji_list = ['👍', '👎', '❤', '😂', '😲']
                        for emoji in emoji_list:
                            await last_message.add_reaction(emoji)
                    except Exception as e:
                        print(f"Erro ao adicionar reações: {e}")


async def setup(bot):
    await bot.add_cog(Mensagens(bot))