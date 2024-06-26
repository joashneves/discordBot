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
JOGOS_MAXIMOS = 10
INTERVALO_RESET_JOGOS = 20 * 60  # 20 minutos em segundos
TENTATIVAS_MAXIMAS = 5


def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}


def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


class ModelInfo(discord.ui.Modal):
    def __init__(self, personagem, dados_personagem, jogador_id):
        super().__init__(title='Editar informações do personagem')
        self.personagem = personagem
        self.dados_personagem = dados_personagem
        self.jogador_id = jogador_id

    descricao = discord.ui.TextInput(label='Descrição', default="", style=discord.TextStyle.paragraph)
    serie = discord.ui.TextInput(label='Universo/Série', default="")

    async def on_submit(self, interaction: discord.Interaction):
        descricao = self.descricao.value
        serie = self.serie.value

        for personagem in self.dados_personagem[str(self.jogador_id)]:
            if personagem['nome'] == self.personagem['nome']:
                personagem['descricao'] = descricao
                personagem['serie'] = serie
                break

        save_data(GAME_FILE, self.dados_personagem)
        await interaction.response.send_message("Informações atualizadas com sucesso!", ephemeral=True)


class ViewInfo(discord.ui.View):
    def __init__(self, embeds, jogador_id, dados_personagem):
        super().__init__()
        self.embeds = embeds
        self.current = 0
        self.jogador_id = jogador_id
        self.dados_personagem = dados_personagem

    @discord.ui.button(label='<<<', style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @discord.ui.button(label='>>>', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @discord.ui.button(label='libertar', style=discord.ButtonStyle.red, emoji='🔓')
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.jogador_id:
            personagem_nome = self.embeds[self.current].title.split(': ')[1]
            jogador_personagens = self.dados_personagem.get(str(self.jogador_id), [])
            self.dados_personagem[str(self.jogador_id)] = [
                personagem for personagem in jogador_personagens if personagem['nome'] != personagem_nome
            ]
            save_data(GAME_FILE, self.dados_personagem)

            del self.embeds[self.current]
            if self.current >= len(self.embeds):
                self.current = max(0, len(self.embeds) - 1)
            if self.embeds:
                await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
            else:
                await interaction.response.edit_message(content="Nenhum personagem restante.", view=None)
        else:
            await interaction.response.send_message("Você não tem permissão para liberar este personagem.",
                                                    ephemeral=True)

    @discord.ui.button(label='Editar', style=discord.ButtonStyle.green, emoji='✏️')
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.jogador_id:
            personagem_nome = self.embeds[self.current].title.split(': ')[1]
            jogador_personagens = self.dados_personagem.get(str(self.jogador_id), [])
            personagem = next((p for p in jogador_personagens if p['nome'] == personagem_nome), None)
            if personagem:
                modal = ModelInfo(personagem, self.dados_personagem, self.jogador_id)
                await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message("Você não tem permissão para editar este personagem.",
                                                    ephemeral=True)

class DoacaoView(discord.ui.View):
    def __init__(self, personagens, jogador_doador, jogador_destinatario, game_instance):
        super().__init__()
        self.jogador_doador = jogador_doador
        self.jogador_destinatario = jogador_destinatario
        self.add_item(PersonagemSelect(personagens, jogador_doador, jogador_destinatario, game_instance))

class PersonagemSelect(discord.ui.Select):
    def __init__(self, personagens, jogador_doador, jogador_destinatario, game_instance):
        self.jogador_doador = jogador_doador
        self.jogador_destinatario = jogador_destinatario
        self.game_instance = game_instance  # Passar a instância de GameWiki

        options = [
            discord.SelectOption(
                label=personagem['nome'],
                description=(personagem['descricao'][:97] + '...') if len(personagem['descricao']) > 100 else personagem['descricao']
            ) for personagem in personagens
        ]
        super().__init__(placeholder="Escolha um personagem para doar", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        personagem_selecionado = self.values[0]
        # Remover o personagem do jogador doador
        doador_personagens = self.game_instance.dados_personagem[str(self.jogador_doador)]
        personagem = next(p for p in doador_personagens if p['nome'] == personagem_selecionado)
        doador_personagens.remove(personagem)
        # Adicionar o personagem ao jogador destinatário
        if str(self.jogador_destinatario) not in self.game_instance.dados_personagem:
            self.game_instance.dados_personagem[str(self.jogador_destinatario)] = []
        self.game_instance.dados_personagem[str(self.jogador_destinatario)].append(personagem)
        save_data(GAME_FILE, self.game_instance.dados_personagem)
        await interaction.response.send_message(f"{personagem_selecionado} foi doado com sucesso!", ephemeral=True)

class GameWiki:
    def __init__(self, client):
        self.client = client
        self.jogo_de_adivinhar = False
        self.chute = ""
        self.dados_personagem = load_data(GAME_FILE)
        self.tentativas_restantes = {}  # Armazena o número de tentativas restantes para cada jogador
        self.ultima_tentativa = {}  # Armazena o timestamp da última tentativa para cada jogador
        self.jogos_restantes = {}  # Armazena o número de jogos restantes para cada jogador
        self.ultimo_jogo = {}  # Armazena o timestamp do último jogo para cada jogador

    async def processar_mensagem(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith(prefix + 'jogar'):
            if not self.jogo_de_adivinhar:
                await self.iniciar_jogo(message)
            else:
                await message.channel.send("Um jogo já está em andamento.")

        if message.content.startswith(prefix + 'score'):
            await self.mostrar_score(message)

        if message.content.startswith(prefix + 'doar'):
            await self.doar_personagem(message)

    async def iniciar_jogo(self, message):
        jogadorID = str(message.author.id)
        agora = datetime.datetime.now().timestamp()

        if jogadorID not in self.jogos_restantes:
            self.jogos_restantes[jogadorID] = JOGOS_MAXIMOS
            self.ultimo_jogo[jogadorID] = agora

        # Resetar jogos se passaram 20 minutos desde o último jogo
        if agora - self.ultimo_jogo[jogadorID] >= INTERVALO_RESET_JOGOS:
            self.jogos_restantes[jogadorID] = JOGOS_MAXIMOS
            self.ultimo_jogo[jogadorID] = agora

        if self.jogos_restantes[jogadorID] <= 0:
            tempo_restante = INTERVALO_RESET_JOGOS - (agora - self.ultimo_jogo[jogadorID])
            minutos_restantes = round(tempo_restante / 60)
            await message.channel.send(
                f"<@{message.author.id}>, você atingiu o limite de 10 jogos. Faltam {minutos_restantes} minutos para você poder jogar novamente.")
            return

        if jogadorID not in self.tentativas_restantes:
            self.tentativas_restantes[jogadorID] = TENTATIVAS_MAXIMAS
            self.ultima_tentativa[jogadorID] = agora

        # Resetar tentativas se passaram 10 minutos desde a última tentativa
        if agora - self.ultima_tentativa[jogadorID] >= INTERVALO_RESET_JOGOS:
            self.tentativas_restantes[jogadorID] = TENTATIVAS_MAXIMAS
            self.ultima_tentativa[jogadorID] = agora

        if self.tentativas_restantes[jogadorID] <= 0:
            tempo_restante = INTERVALO_RESET_JOGOS - (agora - self.ultima_tentativa[jogadorID])
            minutos_restantes = round(tempo_restante / 60)
            await message.channel.send(
                f"<@{message.author.id}>, você não tem mais tentativas restantes. Faltam {minutos_restantes} minutos.")
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
        await self.esperar_resposta_do_jogador(message.author, message.channel, jogadorID, nome_personagem,
                                               imagem_personagem)

    async def mostrar_score(self, message):
        jogadorID = str(message.author.id)
        user_mencionado = message.author
        if message.mentions:
            user = message.mentions[0]
            user_mencionado = message.mentions[0]
            jogadorID = str(user.id)

        if jogadorID not in self.dados_personagem:
            await message.channel.send(f"<@{message.author.id}> ainda não possui perfil!")
            return

        score = self.dados_personagem[jogadorID]
        embeds = self.criar_embeds_score(user_mencionado, score)
        view = ViewInfo(embeds, message.author.id, self.dados_personagem)
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

    async def esperar_resposta_do_jogador(self, autor_jogador, canal_jogo, jogadorID, nome_personagem,
                                          imagem_personagem):
        try:
            resposta = await self.client.wait_for('message',
                                                  check=lambda m: self.check_resposta_jogador(m, autor_jogador),
                                                  timeout=10)
        except asyncio.TimeoutError:
            await canal_jogo.send('Tempo esgotado! O jogo acabou.')
            self.jogo_de_adivinhar = False
        else:
            if resposta.content.lower().startswith(nome_personagem.lower()):
                if jogadorID not in self.dados_personagem:
                    self.dados_personagem[jogadorID] = []

                # Verifica se o personagem já pertence ao jogador ou a outro jogador
                for jogador, personagens in self.dados_personagem.items():
                    for personagem in personagens:
                        if personagem['nome'].lower() == nome_personagem.lower():
                            await canal_jogo.send(f"O(a) personagem {nome_personagem} já pertence a <@{jogador}>.")
                            self.jogo_de_adivinhar = False
                            return

                self.dados_personagem[jogadorID].append({
                    'nome': nome_personagem,
                    'data': datetime.datetime.now().strftime("%d/%m/%Y"),
                    'descricao': "Descrição padrão",
                    "serie": "Serie",
                    'imagem': imagem_personagem
                })
                save_data(GAME_FILE, self.dados_personagem)

                await canal_jogo.send(f"Você acertou! e agora {nome_personagem} é seu")
                self.jogo_de_adivinhar = False
            else:
                self.tentativas_restantes[jogadorID] -= 1
                await canal_jogo.send(
                    f"Você ERROU! Você tem {self.tentativas_restantes[jogadorID]} tentativas restantes.")
                if self.tentativas_restantes[jogadorID] > 0:
                    await self.esperar_resposta_do_jogador(autor_jogador, canal_jogo, jogadorID, nome_personagem,
                                                           imagem_personagem)
                else:
                    await canal_jogo.send('Você não tem mais tentativas restantes! O jogo acabou.')
                    self.jogo_de_adivinhar = False

    def check_resposta_jogador(self, message, autor_jogador):
        return message.author == autor_jogador

    async def doar_personagem(self, message):
        if len(message.mentions) != 1:
            await message.channel.send("Você deve mencionar um usuário para doar um personagem.")
            return

        jogador_doador = message.author.id
        jogador_destinatario = message.mentions[0].id

        if str(jogador_doador) not in self.dados_personagem or not self.dados_personagem[str(jogador_doador)]:
            await message.channel.send(f"<@{message.author.id}> você não possui personagens para doar.")
            return

        personagens = self.dados_personagem[str(jogador_doador)]
        view = DoacaoView(personagens, jogador_doador, jogador_destinatario, self)  # Passar a instância de GameWiki
        await message.channel.send(f"<@{message.author.id}>, escolha um personagem para doar:", view=view)
