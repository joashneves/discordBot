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
info_jogo = discord.Embed(title='Jogo(1/2)',
                           description='Explicação de como funciona o jogo do bot\nVoce possui 5 tentativas a cada 3 minutos, seu objetivo é descobri o nome do personagem que aparece, ao conseguir voce adiciona ele a sua coleção e tem a possibilidade de editar suas informações')
info_jogo.add_field(name='Comando: $jogar', value='apos usar o comando $jogar, escreva o nome correto do personagem que aparece', inline=False)
info_jogo.add_field(name='Comando: $score', value='Mostra todos os personagens que voce encontrou e possibilita a muda as informações do mesmos.', inline=False)
info_jogo.add_field(name='Comando: $doar @user', value='Selecione o @ da pessoa que voce queria doar o personagem, e escolha o personagem.', inline=False)
info_jogo.set_image(url='https://cdn.discordapp.com/attachments/1255938137499107490/1256294540579704832/image.png?ex=66803ef7&is=667eed77&hm=059a36febce9cd6055290de5b6da708d2fbf9b934f0dda5314e9896116afc192&')
info_jogo.set_footer(text='Imagem de Exemplo')
info_wiki = discord.Embed(title='Wiki do Jogo(2/2)',
                           description='Aqui estão alguns comandos para lhe ajudar na pesquisa do bot, apos pegar o personagem seria bom saber dessas coisas')
info_wiki.add_field(name='Comando: $wiki', value='Mostra todos os personagens descobertos', inline=False)
info_wiki.add_field(name='Comando: $wikilist', value='Mostra todos os personagens registrados.', inline=False)
info_wiki.add_field(name='Comando: $pesc [nome_personagem]', value='Mostra se o personagem existe ou não na lista', inline=False)
info_wiki.set_footer(text='Imagem de Exemplo')

tutorial_embed = discord.Embed(title="Tutorial dos Perfis", color=0x7289DA)
tutorial_embed.add_field(name=f"Explicação Geral!",
                         value=f'Os perfis começam de modo simples, mas podem acabar ficando um pouco complicado, porem aqui vai umas explicação bem rapida, para começar a configurar o perfil voce precisa de level, quanto mais level voce possui, mais modificações, sempre upe com $upar_perfil'
                               f'esse comando vai gastar seus pixel, e voce vai ter que juntar denovo pra upar, caso queira saber o custo é 1000 vezes seu nivel, boa compra :D',
                         inline=False)
tutorial_embed.add_field(name=f"{prefix}perfil [@usuário]",
                         value="Mostra o perfil do usuário mencionado ou do autor da mensagem se nenhum usuário for mencionado.")
tutorial_embed.add_field(name=f"{prefix}editardescricao <nova descrição>", value="Edita a descrição do seu perfil.")
tutorial_embed.add_field(name=f"{prefix}upar_perfil", value="Aumenta o nível do seu perfil, se possível.")
tutorial_embed.add_field(name=f"{prefix}escolher_favorito",
                         value="Permite escolher um personagem favorito para seu perfil.")
tutorial_embed.add_field(name=f"{prefix}enviar_imagem <URL>",
                         value="Envia uma imagem para ser usada como imagem personalizada no perfil (requer nível 4).")
tutorial_embed.add_field(name=f"{prefix}aprendizar @usuário",
                         value="Inicia um pedido para alguém se tornar seu aprendiz.")
tutorial_embed.add_field(name=f"{prefix}remover_aprendiz @usuário", value="Remove um usuário como seu aprendiz.")
tutorial_embed.add_field(name=f"{prefix}editarcorembed <cor hexadecimal>",
                         value="Edita a cor do embed do perfil (requer nível 5).")
tutorial_embed.add_field(name=f"{prefix}bank",
                         value="Mostra quanto de pixel voce tem individualmente.")

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
            view_info = ViewInfo([info_bot, info_avatar, info_jogo, info_wiki, tutorial_embed])
            await mensagem.channel.send(embed=view_info.embeds[0], view=view_info)
