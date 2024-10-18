import discord
from discord import app_commands
from discord.ext import commands

from models.Obter_chat import Obter_chat

class Mensagens(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        if not msg.guild or msg.author.bot:
            return

        server_id = str(msg.guild.id)
        channel_id = str(msg.channel.id)

        # Verificar se o servidor e canal estão no banco de dados
        if not Obter_chat.verificar_chat(server_id, channel_id):
            return  # Ignora mensagens fora dos canais cadastrados

        # Adicionar reações se houver anexos
        if msg.attachments:
            attachment = msg.attachments[0]
            if attachment.url:
                try:
                    last_message = await msg.channel.fetch_message(msg.channel.last_message_id)
                    emoji_list = ['👍', '👎', '❤', '😂', '😲']
                    for emoji in emoji_list:
                        await last_message.add_reaction(emoji)
                except Exception as e:
                    print(f"Erro ao adicionar reações: {e}")

    @commands.command()
    async def addchat(self, ctx:commands.context, channel:discord.TextChannel):
        server_id = str(ctx.guild.id)
        channel_id = str(channel.id)
        chat = Obter_chat.obter_chat(server_id, channel_id)
        if chat:
            await ctx.send(f"O canal {channel.mention} foi adicionado ao banco de dados!")
        else:
            await ctx.send("Ocorreu um erro ao adicionar o canal.")


async def setup(bot):
    await bot.add_cog(Mensagens(bot))