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
TENTATIVAS_MAXIMAS = 5
INTERVALO_RESET_TENTATIVAS = 10 * 60  # 10 minutos em segundos

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
        self.tentativas_restantes = {}  # Armazena o número de tentativas restantes para cada jogador
        self.ultima_tentativa = {}  # Armazena o timestamp da última tentativa para cada jogador

    async def processar_mensagem(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith(prefix + 'jogar'):
            if self.jogo_de_adivinhar == False:
                await self.iniciar_jogo(message)
            else:
                await message.channel.send("um jogo ja esta em andamento")

        if message.content.startswith(prefix + 'score'):
            await self.mostrar_score(message)

    async def iniciar_jogo(self, message):
        jogadorID = str(message.author.id)
        agora = datetime.datetime.now().timestamp()

        if jogadorID not in self.tentativas_restantes:
            self.tentativas_restantes[jogadorID] = TENTATIVAS_MAXIMAS
            self.ultima_tentativa[jogadorID] = agora

        # Resetar tentativas se passaram 10 minutos desde a última tentativa
        if agora - self.ultima_tentativa[jogadorID] >= INTERVALO_RESET_TENTATIVAS:
            self.tentativas_restantes[jogadorID] = TENTATIVAS_MAXIMAS
            self.ultima_tentativa[jogadorID] = agora

        if self.tentativas_restantes[jogadorID] <= 0:
            await message.channel.send(f"<@{message.author.id}>, você não tem mais tentativas restantes. Aguarde até as tentativas serem resetadas.")
            return

        self.jogo_de_adivinhar = True

        await message.channel.send(
            f"O jogo começou, <@{message.author.id}> jogou, digite qual é esse personagem? Você tem {self.tentativas_restantes[jogadorID]} tentativas restantes."
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
            embed.add_field(name='De(Franquia):', value=item['serie'], inline=False)
            embed.add_field(name='Data de descoberta', value=item['data'], inline=False)
            embed.set_footer(text=f'Descoberto por: {user.name}')
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
                    "serie": "Serie",
                    'imagem': imagem_personagem
                })
                save_data(GAME_FILE, self.dados_personagem)

                await canal_jogo.send(f"Você acertou! e agora {nome_personagem} é sua")
            else:
                self.tentativas_restantes[jogadorID] -= 1
                await canal_jogo.send(f"Você ERROU! Você tem {self.tentativas_restantes[jogadorID]} tentativas restantes.")
                if self.tentativas_restantes[jogadorID] > 0:
                    await self.esperar_resposta_do_jogador(autor_jogador, canal_jogo, jogadorID, nome_personagem, imagem_personagem)
                else:
                    await canal_jogo.send('Você não tem mais tentativas restantes! O jogo acabou.')

    def check_resposta_jogador(self, message, autor_jogador):
        return message.author == autor_jogador