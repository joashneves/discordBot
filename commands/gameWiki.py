import discord
from discord.ext import commands
import datetime
import json
import os
import random
import asyncio

prefix = '$'
data = datetime.date
DATA_FILE = os.path.join('memoria', 'game.json')
GAME_FILE = os.path.join('memoria', 'dados_personagem.json')

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

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

class GameWiki:
    def __init__(self, client):
        self.client = client
        self.jogo_de_adivinhar = False
        self.chute = ""
        self.dados_personagem = load_data(GAME_FILE)

    async def processar_mensagem(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith(prefix + 'jogar'):
            await self.iniciar_jogo(message)

        if message.content.startswith(prefix + 'score'):
            await self.mostrar_score(message)

    async def iniciar_jogo(self, message):
        self.jogo_de_adivinhar = True
        jogadorID = str(message.author.id)

        await message.channel.send(
            f"O jogo começou, <@{message.author.id}> jogou, digite qual é esse personagem?"
        )

        personagens = load_data(DATA_FILE)
        quantidade_personagens = len(personagens)
        numero_aleatorio = random.randint(0, quantidade_personagens - 1)

        nome_personagem = personagens[numero_aleatorio]["nome"]
        imagem_personagem = personagens[numero_aleatorio]["imagem"]
        self.chute = nome_personagem

        await message.channel.send(imagem_personagem)
        await self.esperar_resposta_do_jogador(message.author, message.channel, jogadorID, nome_personagem, imagem_personagem)

    async def mostrar_score(self, message):
        if message.mentions:
            user = message.mentions[0]
            jogadorM = str(user.id)
            if jogadorM not in self.dados_personagem:
                await message.channel.send(f"<@{user.id}> ainda não possui perfil!")
            else:
                score = self.dados_personagem[jogadorM]
                embeds = self.criar_embeds_score(user, score)
                view = ViewInfo(embeds)
                await message.channel.send(embed=embeds[0], view=view)
        else:
            jogadorID = str(message.author.id)
            if jogadorID not in self.dados_personagem:
                await message.channel.send("Você ainda não possui perfil!")
            else:
                score = self.dados_personagem[jogadorID]
                embeds = self.criar_embeds_score(message.author, score)
                view = ViewInfo(embeds)
                await message.channel.send(embed=embeds[0], view=view)

    def criar_embeds_score(self, user, score):
        embeds = []
        for item in score:
            embed = discord.Embed(
                title=f'Personagem: {item["nome"]}',
                description=f'Descrição: {item["descricao"]}'
            )
            embed.set_image(url=item['imagem'])
            embed.add_field(name='Data de acerto', value=item['data'], inline=False)
            embed.set_footer(text=f'Adivinhado por: {user.name}')
            embeds.append(embed)
        return embeds


    async def esperar_resposta_do_jogador(self, autor_jogador, canal_jogo, jogadorID, nome_personagem, imagem_personagem):
        try:
            resposta = await self.client.wait_for('message', check=lambda m: self.check_resposta_jogador(m, autor_jogador), timeout=12)
        except asyncio.TimeoutError:
            await canal_jogo.send('Tempo esgotado! O jogo acabou.')
        else:
            if resposta.content.lower().startswith(nome_personagem.lower()):
                if jogadorID not in self.dados_personagem:
                    self.dados_personagem[jogadorID] = []

                self.dados_personagem[jogadorID].append({
                    'nome': nome_personagem,
                    'data': datetime.datetime.now().strftime("%d/%m/%Y"),
                    'descricao': "Descrição padrão",
                    'imagem': imagem_personagem
                })
                save_data(GAME_FILE, self.dados_personagem)

                await canal_jogo.send(f"Você acertou! e agora {nome_personagem} é sua")
            else:
                await canal_jogo.send("Você ERROU!")

    def check_resposta_jogador(self, message, autor_jogador):
        return message.author == autor_jogador