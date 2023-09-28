import discord
import json
import random
import asyncio
import datetime
import re

from commands.mensagens import messagensBotRespostas

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.emojis = True
intents.members = True

client = MyClient(intents=intents)
users = {}
dados_users = {}


response_channel = 1058880199414005852 #canal de imagens
canal_dos_membros = 1058885030572732506

async def excluir_canal_apos_tempo(canal, tempo):
    await asyncio.sleep(tempo)  # Aguarda o intervalo de tempo especificado
    await canal.delete()        # Deleta o canal

# Carregar dados dos usuários a partir do arquivo
def carregar_dados():
    try:
        with open("dados_usuarios.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

# Salvar dados dos usuários no arquivo
def salvar_dados_users():
    with open("user_game.json", "w") as arquivo:
        json.dump(dados_users, arquivo)

def carregar_dados_users():
    try:
        with open("user_game.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

# Salvar dados dos usuários no arquivo
def salvar_dados():
    with open("dados_usuarios.json", "w") as arquivo:
        json.dump(users, arquivo)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    activity = discord.Activity(type=discord.ActivityType.playing, name='apenas em dias uteis')
    await client.change_presence(activity=activity)

    # Carregar os dados dos usuários do arquivo
    global users, dados_users
    users = carregar_dados()
    dados_users = carregar_dados_users()

bot_respostas = messagensBotRespostas(client)

@client.event
async def on_message(message):
    if message.author == client.user:  # Para evitar que o bot responda a suas próprias mensagens
        return
    else:
        await bot_respostas.processar_mensagem(message)

    jogadorID = str(message.author.id)
#region // reações

    palavrao = {"porra", "puta", "cu", "caralho", "fodase", "fuder", "foda", "fude","fuder","fds","puto","pqp","merda","vsf"}
    regex = re.compile(r'\b(?:' + '|'.join(palavrao) + r')\b', re.IGNORECASE)
    if regex.search(message.content):
        if jogadorID not in dados_users:
            dados_users[jogadorID] = [0,0,0,1,0]
        else:
            dados_users[jogadorID][3] += 1
        salvar_dados_users()
        numero_aleatorio = random.randint(0, 99)
        if numero_aleatorio > 50:
            await message.channel.send(" '-' ")
        elif numero_aleatorio < 5:
            await message.channel.send(" '-' ")
            await message.channel.send(f"voce xingou {str(dados_users[jogadorID][3])} vezes")
        else:
            return

#endregion

    prefix = "$"
    if message.content.startswith(prefix + "ajuda"):
        await message.channel.send(f'Comandos conhecidos são:\n$avatar\n$ping\n$jogar\n$score')
        registrar_comando(jogadorID)

    if message.content.lower().startswith(prefix + "teste"):
        if message.mentions:
            user = message.mentions[0]
            await message.channel.send(f'Voce mencionou o <@{user}>')
        else:
            await message.channel.send(message.author.avatar)
        registrar_comando(jogadorID)


#region // bom dia e sla
    if message.content.lower().startswith('bom dia'):
        user_id = str(message.author.id)

        # Obter a data atual
        data_atual = str(datetime.date.today())

        if user_id not in users or users[user_id][1] != str(data_atual):
            if user_id not in users:
                users[user_id] = [1, data_atual]
            else:
                users[user_id][0] += 1
                users[user_id][1] = str(data_atual)
            salvar_dados()
            await message.channel.send(f"Olá <@{message.author.id}>, você já deu {users[user_id][0]} bom dia(s).")
        else:
            await message.channel.send(f"<@{message.author.id}>, você já deu bom dia hoje e já deu {users[user_id][0]} bom dia(s) no totalz.")

    if message.content.startswith(prefix + 'avatar'):
        if message.mentions:
            user = message.mentions[0]
            await message.channel.\
                send(user.avatar)
        else:
            await message.channel.send(message.author.avatar)
        registrar_comando(jogadorID)

    if message.content.startswith(prefix + 'ping'):
        latency = client.latency
        await message.channel.send(f'A sua latência é de {latency:.2f} segundos.')
        registrar_comando(jogadorID)


    if message.channel.id == response_channel:
        if message.attachments:
            if message.attachments[0].url:
                last_message = await message.channel.fetch_message(message.channel.last_message_id)
                emoji_list = ['👍', '👎', '❤']
                for emoji in emoji_list:
                    await last_message.add_reaction(emoji)
#endregion

    global jogo_de_adivinhar, chute
    jogo_de_adivinhar= False

    if message.content.startswith(prefix + 'jogar') or jogo_de_adivinhar:
            jogo_de_adivinhar = True

            jogadorID = str(message.author.id)
            if jogadorID not in dados_users:
                dados_users[jogadorID] = [1,0,0,0,0]
            else:
                dados_users[jogadorID][0] += 1
            await message.channel.send(f"O jogo começou, <@{message.author.id}> jogou {str(dados_users[jogadorID][0])} vezes, digite qual é esse personagem?")
            with open("game.json", "r") as game:
                personagens = json.load(game)

            salvar_dados_users()
            # Obtém a quantidade de personagens presentes no arquivo JSON
            quantidade_personagens = len(personagens)

            # Gera um número aleatório entre 0 e a quantidade de personagens - 1
            numero_aleatorio = random.randint(0, quantidade_personagens - 1)

            # Encontra o nome e a imagem do primeiro personagem
            nome_personagem = personagens[numero_aleatorio]["nome"]
            imagem_personagem = personagens[numero_aleatorio]["imagem"]

            # Envia a imagem do personagem
            with open(imagem_personagem, "rb") as arquivo_imagem:
                await message.channel.send(file=discord.File(arquivo_imagem, "imagem.png"))

            chute = nome_personagem
            await esperar_resposta_do_jogador(message.author, message.channel, jogadorID)
            registrar_comando(jogadorID)

    if message.content.startswith(prefix + 'score'):
        if message.mentions:
            user = message.mentions[0]
            jogadorM = str(user.id)
            if jogadorM not in dados_users:
                    await message.channel.send(f"<@{user.id}> ainda não possui perfil!")
            else:
                    await message.channel.send(
                        f"<@{user.id}> jogou: {str(dados_users[jogadorM][0])} vezes\n acertou: {str(dados_users[jogadorM][1])} vezes\n"
                        f" errou: {str(dados_users[jogadorM][2])} vezes\n xingou: {str(dados_users[jogadorM][3])} vezes\n"
                        f" usou comandos: {dados_users[jogadorM][4]} vezes")
        else:
            if jogadorID not in dados_users:
                await message.channel.send("Você ainda não possui perfil!")
            else:
                await message.channel.send(f"voce jogou: {str(dados_users[jogadorID][0])} vezes\nvoce acertou: {str(dados_users[jogadorID][1])} vezes\n"
                                               f"voce errou: {str(dados_users[jogadorID][2])} vezes\nvoce xingou: {str(dados_users[jogadorID][3])} vezes\n"
                                               f"Voce usou comandos: {dados_users[jogadorID][4]} vezes")
        registrar_comando(jogadorID)



def check_resposta_jogador(message, autor_jogador):
    return message.author == autor_jogador

async def esperar_resposta_do_jogador(autor_jogador, canal_jogo,dados):
    try:
        resposta = await client.wait_for('message', check=lambda m: check_resposta_jogador(m, autor_jogador), timeout=12)
    except asyncio.TimeoutError:
        await canal_jogo.send('Tempo esgotado! O jogo acabou.')
    else:
        if resposta.content.lower().startswith(chute.lower()):
            dados_users[dados][1] += 1 #acertos
            await canal_jogo.send("Você acertou! e ganhou pontos")
            await canal_jogo.send(f"Você acertou: {dados_users[dados][1]} vezes")
        else:
            dados_users[dados][2] += 1  # erros
            await canal_jogo.send("Você ERROU!")
            await canal_jogo.send(f"Você ERROU: {dados_users[dados][2]} vezes")
        salvar_dados_users()

def registrar_comando(usuario_id):
    if usuario_id not in dados_users:
        dados_users[usuario_id] = [0,0,0,0,1]
    else:
        dados_users[usuario_id][4] += 1
    salvar_dados_users()

@client.event
async def on_member_join(member):
    print("alguem entrou")

client.run("TOKEN")
