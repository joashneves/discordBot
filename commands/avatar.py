import discord
import  datetime
prefix = '$';
data = datetime.date
class avatarComandos():

    def __init__(self, client):
        self.client = client

    async def avatar(self, mensagem):
        if mensagem.author == self.client.user:
            return
        if mensagem.content.startswith(prefix + 'avatar'):
            data_atual = data.today()
            data_formatada = data_atual.strftime("%d/%m/%Y")
            if mensagem.mentions:
                user = mensagem.mentions[0]
                user_avatar = user.avatar.url
                user_tag = user.display_name
                info_embed = discord.Embed(title=f'Nome: {user.name}', description=f'Informações da regeneração: {user.name}')
                info_embed.set_image(url=user_avatar)
                info_embed.add_field(name='ID', value=user.id, inline=False)
                info_embed.add_field(name='Apelido', value=user_tag, inline=False)
                info_embed.add_field(name='Data de regeneração', value=data_formatada, inline=False)
                info_embed.set_footer(text='1ª regeneração')
                await mensagem.channel.send(embed=info_embed)
            else:
                user = mensagem.author
                user_name = user.name
                user_id = user.id
                user_tag = user.display_name
                user_avatar = user.avatar.url
                info_embed = discord.Embed(title=f'Nome: {user_name}', description=f'Informações da regeneração: {user.name}')
                info_embed.set_image(url=user_avatar)
                info_embed.add_field(name='ID', value=user.id, inline=False)
                info_embed.add_field(name='Apelido', value=user_tag, inline=False)
                info_embed.add_field(name='Data de regeneração', value=data_formatada, inline=False)
                info_embed.set_footer(text='1ª regeneração')
                await mensagem.channel.send(embed=info_embed)


