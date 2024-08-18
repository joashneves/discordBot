import discord
from discord.ext import commands
import datetime
import json
import os
import random
import asyncio

from commands.Conquistas import Conquistas

prefix = '$'
data = datetime.date
DATA_FILE = os.path.join('memoria', 'game.json')
GAME_FILE = os.path.join('memoria', 'dados_personagem.json')
COINS_FILE = os.path.join('memoria', 'coins.json')
GAMEOFF_CHANNELS_FILE = os.path.join('memoria', 'canais_gameoff.json')

JOGOS_MAXIMOS = 10
INTERVALO_RESET_TENTATIVAS = 1 * 60  # 1 minutos em segundos
INTERVALO_RESET_JOGOS = 60 * 60  # 20 minutos em segundos
TENTATIVAS_MAXIMAS = 5

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}


def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

coins_data = load_data(COINS_FILE)

def ganhar_coin(id, coinMAX=10):
    try:
        _coins_data = load_data(COINS_FILE)
        id = str(id)  # Certifique-se de que o ID do usuário é uma string
        print(f'Pessoa {id}')
        print(f'Pessoa {coins_data}')
        # Recompensar o jogador com moedas
        moedas_ganhas = random.randint(10, coinMAX)
        print(f'moedas ganhas: {moedas_ganhas}')
        print(f'moedas atuais: {_coins_data.get(id, 0)}')
        if id in _coins_data:
            _coins_data[id] += moedas_ganhas
        else:
            _coins_data[id] = moedas_ganhas
        print(f'moedas atualizadas: {_coins_data[id]}')
        print(f'Pessoa {_coins_data}')
        save_data(COINS_FILE, _coins_data)

    except Exception as e:
        print(f"Ocorreu um erro ao salvar as moedas: {e}")

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
        ganhar_coin(self.jogador_id, 100)
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
                ganhar_coin(self.jogador_id, 300)
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


class PersonagemSelect(discord.ui.Select):
    def __init__(self, personagens, jogador_doador, jogador_destinatario, game_instance, page):
        self.jogador_doador = jogador_doador
        self.jogador_destinatario = jogador_destinatario
        self.game_instance = game_instance
        self.page = page
        self.total_pages = (len(personagens) - 1) // 25 + 1

        start_index = page * 25
        end_index = start_index + 25
        self.current_personagens = personagens[start_index:end_index]

        options = [
            discord.SelectOption(
                label=personagem['nome'],
                description=(personagem['descricao'][:97] + '...') if len(personagem['descricao']) > 100 else personagem['descricao']
            ) for personagem in self.current_personagens
        ]

        super().__init__(placeholder=f"Escolha um personagem para doar (Página {page + 1}/{self.total_pages})", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.jogador_doador:
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
            await interaction.response.send_message(f"{personagem_selecionado} foi doado com sucesso!", ephemeral=False)
            ganhar_coin(interaction.user.id, 250)
        else:
            await interaction.response.send_message("Você não tem permissão para trocar este personagem.", ephemeral=False)

class DoacaoView(discord.ui.View):
    def __init__(self, personagens, jogador_doador, jogador_destinatario, game_instance):
        super().__init__()
        self.jogador_doador = jogador_doador
        self.jogador_destinatario = jogador_destinatario
        self.personagens = personagens
        self.game_instance = game_instance
        self.page = 0
        self.update_select()

    def update_select(self):
        for item in self.children:
            if isinstance(item, discord.ui.Select):
                self.remove_item(item)
        select = PersonagemSelect(self.personagens, self.jogador_doador, self.jogador_destinatario, self.game_instance, self.page)
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

def load_image_channels():
    data = load_data(GAMEOFF_CHANNELS_FILE)
    return data.get('canais_gameoff', [])

canais_gameoof = load_image_channels()

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
        if message.channel.id not in canais_gameoof:
            if message.content.startswith(prefix + 'jogar'):
                if not self.jogo_de_adivinhar:
                    await self.iniciar_jogo(message)
                else:
                    await message.channel.send("Um jogo já está em andamento.")

            if message.content.startswith(prefix + 'score'):
                await self.mostrar_score(message)

            if message.content.startswith(prefix + 'doar'):
                await self.doar_personagem(message)
        elif message.content.startswith(prefix + 'jogar') and message.channel.id in canais_gameoof :
            await message.channel.send("Aqui não pode se inicar um jogo.")

    async def iniciar_jogo(self, message):
        jogadorID = str(message.author.id)
        agora = datetime.datetime.now().timestamp()

        if jogadorID not in self.jogos_restantes:
            self.jogos_restantes[jogadorID] = JOGOS_MAXIMOS
            self.ultimo_jogo[jogadorID] = agora
            print(self.jogos_restantes[jogadorID])
            print(self.ultimo_jogo[jogadorID] )
        print(self.jogos_restantes)
        self.jogos_restantes[jogadorID] -= 1;
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
        if agora - self.ultima_tentativa[jogadorID] >= INTERVALO_RESET_TENTATIVAS:
            self.tentativas_restantes[jogadorID] = TENTATIVAS_MAXIMAS
            self.ultima_tentativa[jogadorID] = agora

        if self.tentativas_restantes[jogadorID] <= 0:
            tempo_restante = INTERVALO_RESET_TENTATIVAS - (agora - self.ultima_tentativa[jogadorID])
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
                                                  timeout=50)
        except asyncio.TimeoutError:
            await canal_jogo.send('Tempo esgotado! O jogo acabou.')
            self.jogo_de_adivinhar = False
        else:
            if resposta.content.lower() == f'{prefix}ff':
                self.tentativas_restantes[jogadorID] = TENTATIVAS_MAXIMAS
                await canal_jogo.send(f"{autor_jogador.mention}, você desistiu do jogo atual.")
                self.jogo_de_adivinhar = False
                return

            if resposta.content.lower().startswith(nome_personagem.lower()):

                if jogadorID not in self.dados_personagem:
                    self.dados_personagem[jogadorID] = []

                # Verifica se o personagem já pertence ao jogador ou a outro jogador
                for jogador, personagens in self.dados_personagem.items():
                    for personagem in personagens:
                        if personagem['nome'].lower() == nome_personagem.lower():
                            await canal_jogo.send(f"O(a) personagem {nome_personagem} já pertence a <@{jogador}>.")
                            self.jogo_de_adivinhar = False
                            ganhar_coin(jogadorID, 20)
                            return
                # Recompensar o jogador com moedas
                ganhar_coin(jogadorID, 50)
                self.dados_personagem[jogadorID].append({
                    'nome': nome_personagem,
                    'data': datetime.datetime.now().strftime("%d/%m/%Y"),
                    'descricao': "Descrição padrão",
                    "serie": "Serie",
                    'imagem': imagem_personagem
                })
                save_data(GAME_FILE, self.dados_personagem)

                await canal_jogo.send(f"Você acertou! e agora {nome_personagem} é seu.")

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

