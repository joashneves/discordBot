import discord
from discord.ext import commands

prefix = "$"

info_bot = discord.Embed(title='O Bot',
                         description='O bot, ou a Skalart é um bot do discord sem foco aparente, ela tem como objetivo o aprendizado de um simples programador.')
info_bot.add_field(name='Sobre o criador', value='Meu nome é Joas, but muito conhecido como Yoyatsu, eu criei a Skalart pos sempre fui apaixonado pela ideia de ter um proprio bot', inline=False)
info_bot.add_field(name='Sobre a Skalart', value='Eu sirvo apenas para servi voces, auxiliar e conversar, e obvio deixar uns easter egg aqui e ali', inline=False)
info_bot.add_field(name='Github', value='https://github.com/joashneves/discordBot', inline=False)
info_bot.set_image(url='https://cdn.discordapp.com/attachments/1255938137499107490/1255938517800976384/Comission_Joas.png?ex=667ef364&is=667da1e4&hm=f1d461dc9dd574874a9b1e801d50151ab230d1db12f418c3863e27814a827783&')
info_bot.set_footer(text='Imagem por: https://x.com/Arty_Kafka')
info_avatar = discord.Embed(title='Avatar',
                           description='Lhe mostra um historico de todas as fotos de perfil que o usuario mencionado usou')
info_avatar.add_field(name='Comando: $avatar', value='paramentros: nenhum ou menção por @\nEx: $avatar @user', inline=False)
#Embed dos jogos
info_jogo = discord.Embed(title='Jogo',
                           description='Explicação de como funciona o jogo do bot\nVoce possui 5 tentativas a cada 10 minutos, seu objetivo é descobri o nome do personagem que aparece, ao conseguir voce adiciona ele a sua coleção e tem a possibilidade de editar suas informações')
info_jogo.add_field(name='Comando: $jogar', value='apos usar o comando $jogar, escreva o nome correto do personagem que aparece', inline=False)
info_jogo.add_field(name='Comando: $score', value='Mostra todos os personagens que voce encontrou e possibilita a muda as informações do mesmos.', inline=False)
info_jogo.add_field(name='Comando: $doar @user', value='Selecione o @ da pessoa que voce queria doar o personagem, e escolha o personagem.', inline=False)
info_jogo.set_image(url='https://cdn.discordapp.com/attachments/1255938137499107490/1256294540579704832/image.png?ex=66803ef7&is=667eed77&hm=059a36febce9cd6055290de5b6da708d2fbf9b934f0dda5314e9896116afc192&')
info_jogo.set_footer(text='Imagem de Exemplo')

class ViewInfo(discord.ui.View):
    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current = 0

    @discord.ui.button(label='<<<', style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @discord.ui.button(label='>>>', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

class AjudaComando():
    def __init__(self, client):
        self.client = client

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return

        if mensagem.content.startswith(prefix + "ajuda"):
            view_info = ViewInfo([info_bot, info_avatar, info_jogo])
            await mensagem.channel.send(embed=view_info.embeds[0], view=view_info)
