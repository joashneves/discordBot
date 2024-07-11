import asyncio

import discord
import os
import json

prefix = '$'
COINS_FILE = os.path.join('memoria', 'coins.json')
GAME_FILE = os.path.join('memoria', 'dados_personagem.json')
PROFILE_FILE = os.path.join('memoria', 'perfil.json')
CONQUISTAS_FILE = os.path.join('memoria', 'conquistas.json')

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

class PersonagemSelect(discord.ui.Select):
    def __init__(self, personagens, jogador_id, game_instance, page):
        self.personagens = personagens
        self.jogador_id = jogador_id
        self.game_instance = game_instance
        self.page = page

        options = []
        start = self.page * 25
        end = min((self.page + 1) * 25, len(self.personagens))
        for personagem in self.personagens[start:end]:
            options.append(discord.SelectOption(label=personagem['nome'], value=personagem['nome']))

        super().__init__(placeholder='Escolha um personagem...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        personagem_nome = self.values[0]
        for personagem in self.personagens:
            if personagem['nome'] == personagem_nome:
                self.game_instance.perfil_data[str(self.jogador_id)]['personagem_favorito'] = personagem_nome
                save_data(PROFILE_FILE, self.game_instance.perfil_data)
                await interaction.response.send_message(f'Personagem favorito atualizado para: {personagem_nome}', ephemeral=True)
                return

class EscolherFavoritoView(discord.ui.View):
    def __init__(self, personagens, jogador_id, game_instance):
        super().__init__()
        self.jogador_id = jogador_id
        self.personagens = personagens
        self.game_instance = game_instance
        self.page = 0
        self.update_select()

    def update_select(self):
        for item in self.children:
            if isinstance(item, discord.ui.Select):
                self.remove_item(item)
        select = PersonagemSelect(self.personagens, self.jogador_id, self.game_instance, self.page)
        self.add_item(select)

    @discord.ui.button(label='<<<', style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
            self.update_select()
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label='>>>', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (self.page + 1) * 25 < len(self.personagens):
            self.page += 1
            self.update_select()
            await interaction.response.edit_message(view=self)

class Perfil:
    def __init__(self, client):
        self.client = client
        self.coins_data = load_data(COINS_FILE)
        self.dados_personagem = load_data(GAME_FILE)
        self.perfil_data = load_data(PROFILE_FILE)
        self.conquista_data = load_data(CONQUISTAS_FILE )

    async def mostrar_perfil(self, message):
        if len(message.mentions) > 0:
            user_id = str(message.mentions[0].id)
            member = message.mentions[0]
        else:
            user_id = str(message.author.id)
            member = message.author

        coins_data = load_data(COINS_FILE)
        coins = coins_data.get(user_id, 0)
        personagens = self.dados_personagem.get(user_id, [])
        perfil = self.perfil_data.get(user_id, {"nivel": 1})
        descricao = perfil.get("descricao", "Sem descrição")
        personagem_favorito = perfil.get("personagem_favorito", "Nenhum")
        imagem_personalizada = perfil.get("imagem_personalizada", None)
        cor_embed = perfil.get("cor_embed", None)
        conquistas = perfil.get("conquistas", [])
        aprendiz = perfil.get("aprendiz", "Nenhum")

        nivel = perfil.get("nivel", 1)
        num_personagens = len(personagens)

        if nivel >= 2:
            embed = discord.Embed(title=f"Perfil de {member.name}", color=cor_embed or 0x00ff00)
            embed.add_field(name="Nível", value=nivel)
            embed.add_field(name="Personagens", value=num_personagens)
            embed.add_field(name="Pixel's", value=coins)
            embed.add_field(name="Descrição", value=descricao, inline=False)

            if nivel >= 3:
                embed.add_field(name="Casado: ", value=personagem_favorito, inline=False)
                embed.set_thumbnail(url=member.avatar.url)

            if nivel >= 4 and imagem_personalizada:
                embed.set_image(url=imagem_personalizada)

            if nivel >= 5:
                if conquistas:
                    conquistas_desc = "\n".join(
                        [f"{index + 1}. {conquista}" for index, conquista in enumerate(conquistas)])
                    embed.add_field(name="Conquistas", value=conquistas_desc, inline=False)
                else:
                    embed.add_field(name="Conquistas", value="Nenhuma conquista ainda.", inline=False)

                embed.add_field(name="Aprendiz", value=aprendiz, inline=False)

            await message.channel.send(embed=embed)
        else:
            response = (f"Perfil de {member.name}\n"
                        f"Nível: {nivel}\n"
                        f"Personagens: {num_personagens}\n"
                        f"Pixel's: {coins}")
            await message.channel.send(response)
    async def iniciar_aprendizado(self, message):
        user_id = str(message.author.id)
        perfil = self.perfil_data.get(user_id, {"nivel": 1})
        nivel = perfil.get("nivel", 1)

        if nivel < 5:
            await message.channel.send("Você precisa estar no nível 5 ou superior para usar este comando.")
            return

        if len(message.mentions) == 0:
            await message.channel.send("Você precisa mencionar alguém para aprender com essa pessoa.")
            return

        aprendiz_id = str(message.mentions[0].id)
        await message.channel.send(
            f"<@{aprendiz_id}>, você foi convidado(a) para ser aprendiz de <@{user_id}>. Você tem 30 segundos para aceitar.")

        def check(response_message):
            return response_message.author.id == int(aprendiz_id) and response_message.content.lower() in ['sim', 'não',
                                                                                                           'nao']

        try:
            response_message = await self.client.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send(f"O convite para aprendizagem com <@{aprendiz_id}> expirou.")
            return

        if response_message.content.lower() in ['sim']:
            self.perfil_data[user_id]["aprendiz"] = message.mentions[0].name
            save_data(PROFILE_FILE, self.perfil_data)
            await message.channel.send(f"<@{aprendiz_id}> agora é seu aprendiz!")
        else:
            await message.channel.send(f"<@{aprendiz_id}> recusou o convite para ser seu aprendiz.")

    async def remover_aprendiz(self, message):
        user_id = str(message.author.id)
        perfil = self.perfil_data.get(user_id, {"nivel": 1})

        if "aprendiz" in perfil:
            del perfil["aprendiz"]
            save_data(PROFILE_FILE, self.perfil_data)
            await message.channel.send("Aprendiz removido com sucesso!")
        else:
            await message.channel.send("Você não possui um aprendiz para remover.")

    async def editar_descricao(self, message, nova_descricao):
        user_id = str(message.author.id)
        if user_id not in self.perfil_data:
            self.perfil_data[user_id] = {"nivel": 1}

        self.perfil_data[user_id]["descricao"] = nova_descricao
        save_data(PROFILE_FILE, self.perfil_data)

        await message.channel.send("Descrição atualizada com sucesso!")

    async def upar_perfil(self, message):
        user_id = str(message.author.id)
        coins_data = load_data(COINS_FILE)
        coins = coins_data.get(user_id, 0)
        perfil = self.perfil_data.get(user_id, {"nivel": 1})
        nivel_atual = perfil.get("nivel", 1)
        custo_up = 1000 * nivel_atual

        if coins >= custo_up:
            self.coins_data[user_id] -= custo_up
            perfil["nivel"] = nivel_atual + 1
            self.perfil_data[user_id] = perfil
            save_data(COINS_FILE, self.coins_data)
            save_data(PROFILE_FILE, self.perfil_data)
            await message.channel.send(f"Parabéns! Você subiu para o nível {perfil['nivel']}!")
        else:
            await message.channel.send(f"Você precisa de {custo_up} moedas para upar para o próximo nível.")

    async def escolher_favorito(self, message):
        user_id = str(message.author.id)
        if str(user_id) not in self.dados_personagem or not self.dados_personagem[str(user_id)]:
            await message.channel.send(f"<@{message.author.id}> você não possui personagens para escolher como favorito.")
            return

        personagens = self.dados_personagem[str(user_id)]
        view = EscolherFavoritoView(personagens, user_id, self)
        await message.channel.send(f"<@{message.author.id}>, escolha um personagem para ser seu favorito:", view=view)

    async def enviar_imagem(self, message):
        user_id = str(message.author.id)
        perfil = self.perfil_data.get(user_id, {"nivel": 1})
        nivel = perfil.get("nivel", 1)

        if nivel >= 4:
            if len(message.attachments) > 0:
                attachment = message.attachments[0]
                if attachment.content_type.startswith('image/'):
                    self.perfil_data[user_id]["imagem_personalizada"] = attachment.url
                    save_data(PROFILE_FILE, self.perfil_data)
                    await message.channel.send("Imagem personalizada atualizada com sucesso!")
                else:
                    await message.channel.send("O anexo deve ser uma imagem.")
            else:
                await message.channel.send("Você precisa enviar uma imagem como anexo.")
        else:
            await message.channel.send(
                "Você precisa estar no nível 4 ou superior para enviar uma imagem personalizada.")
    async def editar_cor_embed(self, message, cor):
        user_id = str(message.author.id)
        if user_id not in self.perfil_data:
            self.perfil_data[user_id] = {"nivel": 1}

        # Verifica se a cor fornecida é um número inteiro
        try:
            cor_int = int(cor, 16)  # Converte a cor hexadecimal para um número inteiro
        except ValueError:
            await message.channel.send("Formato de cor inválido. Certifique-se de fornecer uma cor hexadecimal válida.")
            return

        self.perfil_data[user_id]["cor_embed"] = cor_int
        save_data(PROFILE_FILE, self.perfil_data)

        await message.channel.send("Cor do embed do perfil atualizada com sucesso!")

    async def processar_mensagem(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith(prefix + 'perfil') or message.content.startswith('/perfil'):
            await self.mostrar_perfil(message)
        elif message.content.startswith(prefix + 'editardescricao'):
            nova_descricao = message.content[len(prefix + 'editardescricao'):].strip()
            await self.editar_descricao(message, nova_descricao)
        elif message.content.startswith(prefix + 'upar_perfil'):
            await self.upar_perfil(message)
        elif message.content.startswith(prefix + 'escolher_favorito'):
            await self.escolher_favorito(message)
        elif message.content.startswith(prefix + 'enviar_imagem'):
            await self.enviar_imagem(message)
        elif message.content.startswith(prefix + 'aprendizar'):
            await self.iniciar_aprendizado(message)
        elif message.content.startswith(prefix + 'remover_aprendiz'):
            await self.remover_aprendiz(message)
        elif message.content.startswith(prefix + 'editarcorembed'):
            cor = message.content[len(prefix + 'editarcorembed'):].strip()
            await self.editar_cor_embed(message, cor)
